import { UserAgent, Inviter, Registerer } from "sip.js";

let ua = null;
let registerer = null;
let currentSession = null;
let mediaRecorder = null;
let recordedChunks = [];
let localStreamRef = null;
let audioContextRef = null;
let shiftId = null;
let callId = null;
let callerNumber = null;
let calledNumber = null;
let callStartISOString = null;
let callEndISOString = null;
let callDurationSeconds = 0;
let alreadySaved = false;
let callAnswered = false;
let ringbackAudio = null;
let dialToneAudio = null;

// initialize SIP UA
export async function initSip() {
  ua = new UserAgent({
    uri: UserAgent.makeURI("sip:809@192.168.1.5"),
    transportOptions: { server: "wss://192.168.1.5:8089/ws" },
    authorizationUsername: "809",
    authorizationPassword: "K*EsGdQ^c9",
    sessionDescriptionHandlerFactoryOptions: {
      constraints: { audio: true, video: false },
    },
  });
}

// call a number
export async function callNumber(number, shiftIdParam) {
  if (!ua || !ua.transport || !ua.transport.isConnected()) {
    try {
      await ua.start();
      if (!registerer) {
        registerer = new Registerer(ua);
      }
      await registerer.register();
    } catch (e) {
      throw new Error("SIP is not available even after reconnect");
    }
  }
  
  alreadySaved = false;

  shiftId = shiftIdParam;
  callId = crypto.randomUUID ? crypto.randomUUID() : String(Date.now()) + Math.random().toString(36).slice(2);
  callerNumber = "809";
  calledNumber = String(number);
  callStartISOString = new Date().toISOString();
  callEndISOString = null;
  callDurationSeconds = 0;
  callAnswered = false;

  const target = UserAgent.makeURI(`sip:${number}@192.168.1.5`);
  const inviter = new Inviter(ua, target);
  
  currentSession = inviter;
  dialToneAudio = new Audio("/sounds/dialtone.mp3");
  dialToneAudio.loop = true;
  dialToneAudio.play().catch(() => {});
  ringbackAudio = new Audio("/sounds/ringback.mp3");
  ringbackAudio.loop = true;

  inviter.stateChange.addListener((state) => {
    if (state === "Initial" || state === "Progressing" || state === "Early") {
      if (dialToneAudio) {
        dialToneAudio.pause();
        dialToneAudio.currentTime = 0;
      }
      if (ringbackAudio) {
        ringbackAudio.play().catch(() => {});
      }
    }
    if (state === "Established") {
      callAnswered = true;
      dialToneAudio?.pause();
      ringbackAudio?.pause();
      dialToneAudio.currentTime = 0;
      ringbackAudio.currentTime = 0;
    }
    if (state === "Terminated") {
      dialToneAudio?.pause();
      ringbackAudio?.pause();
      dialToneAudio.currentTime = 0;
      ringbackAudio.currentTime = 0;
    }
  });

  inviter.delegate = {
    onSessionDescriptionHandler: async (sdh) => {
      const pc = sdh.peerConnection;

      pc.ontrack = async (event) => {
        const remoteStream = event.streams[0];
        const remoteAudio = document.getElementById("remoteAudio");
        if (remoteAudio) {
          remoteAudio.srcObject = remoteStream;
          remoteAudio.play().catch(() => {});
        }
        try {
          const localStream = await navigator.mediaDevices.getUserMedia({ audio: true, video: false });
          localStreamRef = localStream;
          const mixedStream = await mixAudioStreams(localStream, remoteStream);
          startRecording(mixedStream);
        } catch (err) {
          console.error("Could not get local microphone:", err);
        }
      };
    },

    onConnected: () => {
      callAnswered = true;
      if (ringbackAudio) {
        ringbackAudio.pause();
        ringbackAudio.currentTime = 0;
      }
    },

    // when remote hangs up (BYE)
    onBye: () => {
      callEndISOString = new Date().toISOString();
      callDurationSeconds = calcCallDuration(callStartISOString, callEndISOString);
      stopAndCleanup();
    },

    // when session terminated for any reason
    onTerminated: () => {
      callEndISOString = callEndISOString || new Date().toISOString();
      callDurationSeconds = calcCallDuration(callStartISOString, callEndISOString);
      stopAndCleanup();
    },
  };

  try {
    await inviter.invite({});
  } catch (err) {
    console.error("CALL ERROR:", err);
    // stop any playing tones
    try { if (ringbackAudio) { ringbackAudio.pause(); ringbackAudio.currentTime = 0; } } catch (_) {}
    try { if (dialToneAudio) { dialToneAudio.pause(); dialToneAudio.currentTime = 0; } } catch (_) {}
    // cleanup local resources
    stopAndCleanup();
    // rethrow so callers can handle if needed
    throw err;
  }
}

function calcCallDuration(startISO, endISO) {
  if (!startISO || !endISO) return 0;
  const s = new Date(startISO).getTime();
  const e = new Date(endISO).getTime();
  if (isNaN(s) || isNaN(e) || e < s) return 0;
  return Math.round((e - s) / 1000);
}

// Mix local + remote into one MediaStream via AudioContext
async function mixAudioStreams(localStream, remoteStream) {
  audioContextRef = new (window.AudioContext || window.webkitAudioContext)();
  const destination = audioContextRef.createMediaStreamDestination();

  try {
    const localSource = audioContextRef.createMediaStreamSource(localStream);
    const remoteSource = audioContextRef.createMediaStreamSource(remoteStream);

    localSource.connect(destination);
    remoteSource.connect(destination);
  } catch (err) {
    console.error("mixAudioStreams error:", err);
    return remoteStream;
  }

  return destination.stream;
}

// Start recording given MediaStream
function startRecording(stream) {
  recordedChunks = [];
  try {
    mediaRecorder = new MediaRecorder(stream, { mimeType: "audio/webm;codecs=opus" });
  } catch (err) {
    console.error("MediaRecorder not supported or init failed:", err);
    return;
  }

  mediaRecorder.ondataavailable = (e) => {
    if (e.data && e.data.size > 0) recordedChunks.push(e.data);
  };

  mediaRecorder.onstop = () => {
    saveRecording();
  };

  try {
    mediaRecorder.start(1000);
  } catch (err) {
    console.error("mediaRecorder.start failed:", err);
  }
}

// Stop recording public function
export function stopRecording() {
  if (mediaRecorder && mediaRecorder.state === "recording") {
    mediaRecorder.stop();
  }
}

async function saveRecording() {
  if (alreadySaved) return; // 🔥 ԱՅՍՏԵՂ է կարևորը
  alreadySaved = true;

  if (!callAnswered) {
    return;
  }

  if (recordedChunks.length === 0) return;

  const blob = new Blob(recordedChunks, { type: "audio/webm" });

  const meta = {
    call_id: callId,
    caller_number: callerNumber,
    called_number: calledNumber,
    call_start: callStartISOString,
    call_end: callEndISOString,
    call_duration: callDurationSeconds,
  };

  try {
    const response = await uploadWebm(blob, meta);
    window.dispatchEvent(
      new CustomEvent("new-call", {
        detail: {
          call_start: meta.call_start,
          caller_number: meta.caller_number,
          called_number: meta.called_number,
          recording_url: response.recording_url,
        },
      })
    );
  } catch (err) {
    console.error("❌ Upload failed:", err);
  }
}

// Cleanup on call end / hangup
function stopAndCleanup() {
  if (mediaRecorder) {
    if (mediaRecorder.state === "recording") {
      try {
        mediaRecorder.requestData();
      } catch (_) {}
      setTimeout(() => {
        try { mediaRecorder.stop(); } catch (_) {}
      }, 200);
    } else if (mediaRecorder.state === "inactive" && recordedChunks.length > 0 && !alreadySaved) {
      saveRecording();
    }
  }

  if (localStreamRef) {
    localStreamRef.getTracks().forEach((t) => {
      try { t.stop(); } catch (_) {}
    });
    localStreamRef = null;
  }

  if (audioContextRef) {
    audioContextRef.close().catch(() => {});
    audioContextRef = null;
  }

  const remoteAudio = document.getElementById("remoteAudio");
  if (remoteAudio) remoteAudio.srcObject = null;

  if (ringbackAudio) {
    ringbackAudio.pause();
    ringbackAudio.currentTime = 0;
  }

  window.dispatchEvent(new CustomEvent("sip-call-ended", {
    detail: {
      call_id: callId,
      caller_number: callerNumber,
      called_number: calledNumber,
    },
  }));

  currentSession = null;
}

// Manual hangup
export async function endCall() {
  if (currentSession) {
    try {
      const sessionState = currentSession.state || "";
      const canCancel = typeof currentSession.cancel === "function";
      const canReject = typeof currentSession.reject === "function";
      const canBye = typeof currentSession.bye === "function";

      // If this is an incoming Invitation that hasn't been accepted, prefer reject()
      if (canReject && sessionState !== "Established" && sessionState !== "established") {
        try {
          const callLabel = (currentSession.request && currentSession.request.callId) ? currentSession.request.callId : callId;
          await currentSession.reject({ statusCode: 486, reasonPhrase: "Busy Here" });
          window.dispatchEvent(new CustomEvent('sip-call-rejected', { detail: { call_id: callLabel } }));
        } catch (err) {
          console.warn("Reject failed, falling back to cancel/bye if available:", err);
          if (canCancel) {
            await currentSession.cancel();
            console.log("Outgoing call canceled (fallback)");
          } else if (canBye) {
            await currentSession.bye();
            console.log("Call ended with BYE (fallback)");
          }
        }
      } else if (canCancel && sessionState !== "Established" && sessionState !== "established") {
        await currentSession.cancel();
      } else if (canBye) {
        await currentSession.bye();
      } else {
        console.warn("No hangup/cancel/reject method available on current session");
      }
    } catch (err) {
      console.error("endCall error:", err);
    } finally {
      stopAndCleanup();
    }
  } else {
    stopAndCleanup();
  }
}

/* ---------- Upload helper ---------- */

// get CSRF token from cookie (if using Django CSRF)
function getCsrfToken() {
  const match = document.cookie.split(';').map(c => c.trim()).find(c => c.startsWith('csrftoken='));
  return match ? match.split('=')[1] : null;
}

// upload WebM Blob to Django endpoint
async function uploadWebm(blob, meta) {
  const fd = new FormData();
  fd.append('file', blob, 'call.webm');
  if (meta.call_id) fd.append('call_id', meta.call_id);
  if (meta.caller_number) fd.append('caller_number', meta.caller_number);
  if (meta.called_number) fd.append('called_number', meta.called_number);
  if (meta.call_start) fd.append('call_start', meta.call_start);
  if (meta.call_end) fd.append('call_end', meta.call_end);
  if (meta.call_duration != null) fd.append('call_duration', String(meta.call_duration));
  if (shiftId) {
    fd.append("shift_id", shiftId);
  }

  const headers = {};
  const csrftoken = getCsrfToken();
  if (csrftoken) headers['X-CSRFToken'] = csrftoken;

  const resp = await fetch('http://192.168.88.111:8000/api/phone/upload_call_record/', {
    method: 'POST',
    headers,
    body: fd,
    credentials: 'include' // include cookies if needed
  });

  if (!resp.ok) {
    const text = await resp.text();
    throw new Error(`Upload failed: ${resp.status} ${text}`);
  }
  return await resp.json();
}
