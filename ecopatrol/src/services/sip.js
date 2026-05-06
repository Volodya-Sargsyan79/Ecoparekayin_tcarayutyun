import { UserAgent, Inviter } from "sip.js";

let ua = null;
let currentSession = null;
let mediaRecorder = null;
let recordedChunks = [];
let localStreamRef = null;
let audioContextRef = null;

// metadata placeholders — դրանք պետք է լրացվեն ձեր լոգիկայով երբ սկսվում է զանգը
let shiftId = null;
let callId = null;
let callerNumber = null;
let calledNumber = null;
let callStartISOString = null;
let callEndISOString = null;
let callDurationSeconds = 0;

// initialize SIP UA
export async function initSip() {
  if (ua) return;

  ua = new UserAgent({
    uri: UserAgent.makeURI("sip:809@192.168.1.5"),
    transportOptions: { server: "wss://192.168.1.5:8089/ws" },
    authorizationUsername: "809",
    authorizationPassword: "K*EsGdQ^c9",
    sessionDescriptionHandlerFactoryOptions: {
      constraints: { audio: true, video: false },
      peerConnectionConfiguration: {
        iceServers: [{ urls: "stun:stun.l.google.com:19302" }],
      },
    },
  });

  await ua.start();
  console.log("✅ SIP started");
}

// call a number
export async function callNumber(number, shiftIdParam) {
  if (!ua) throw new Error("UA not initialized. Call initSip() first.");

  // set metadata for this call
  shiftId = shiftIdParam;
  callId = crypto.randomUUID ? crypto.randomUUID() : String(Date.now()) + Math.random().toString(36).slice(2);
  callerNumber = "809"; // փոխարինեք ճիշտ caller-ի արժեքով եթե պետք է
  calledNumber = String(number);
  callStartISOString = new Date().toISOString();
  callEndISOString = null;
  callDurationSeconds = 0;

  const target = UserAgent.makeURI(`sip:${number}@192.168.1.5`);
  const inviter = new Inviter(ua, target);
  currentSession = inviter;

  inviter.delegate = {
    onSessionDescriptionHandler: async (sdh) => {
      const pc = sdh.peerConnection;

      // track remote audio
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

      // connection / ice state guards to stop recording on abrupt disconnects
      pc.onconnectionstatechange = () => {
        console.log("PC connectionState:", pc.connectionState);
        if (["disconnected", "failed", "closed"].includes(pc.connectionState)) stopAndCleanup();
      };
      pc.oniceconnectionstatechange = () => {
        console.log("PC iceConnectionState:", pc.iceConnectionState);
        if (["disconnected", "failed", "closed"].includes(pc.iceConnectionState)) stopAndCleanup();
      };
    },

    onConnected: () => {
      console.log("📞 Call connected");
    },

    // when remote hangs up (BYE)
    onBye: () => {
      console.log("👋 Call ended by remote");
      // mark end time and duration
      callEndISOString = new Date().toISOString();
      callDurationSeconds = calcCallDuration(callStartISOString, callEndISOString);
      stopAndCleanup();
    },

    // when session terminated for any reason
    onTerminated: () => {
      console.log("🔚 Session terminated");
      callEndISOString = callEndISOString || new Date().toISOString();
      callDurationSeconds = calcCallDuration(callStartISOString, callEndISOString);
      stopAndCleanup();
    },
  };

  await inviter.invite();
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
    // fallback: if mixing fails, prefer remote stream
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
    console.log("🎙 Recording stopped");
    saveRecording();
  };

  try {
    mediaRecorder.start(1000);
    console.log("🎙 Recording started");
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
    // 🔥 ԱՅՍ Է ԿԱՐԵՎՈՐԸ
    const response = await uploadWebm(blob, meta);

    console.log("✅ Uploaded in server");

    // 🔥 dispatch event
    window.dispatchEvent(
      new CustomEvent("new-call", {
        detail: {
          call_start: meta.call_start,
          caller_number: meta.caller_number,
          called_number: meta.called_number,
          recording_url: response.recording_url, // ✅ հիմա կա
        },
      })
    );
  } catch (err) {
    console.error("❌ Upload failed:", err);
  }
}

// Cleanup on call end / hangup
function stopAndCleanup() {
  console.log("🧹 Cleaning up call...");

  if (mediaRecorder && mediaRecorder.state === "recording") {
    try {
      mediaRecorder.requestData();
    } catch (_) {}
    setTimeout(() => {
      try { mediaRecorder.stop(); } catch (_) {}
    }, 200);
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

  // reset call metadata (optional)
  currentSession = null;
  // note: do not clear callId/callerNumber immediately if you need them for upload; they are used in saveRecording
}

// Manual hangup
export function endCall() {
  if (currentSession) {
    try {
      currentSession.bye();
      // cleanup will run from onBye/onTerminated handlers
    } catch (err) {
      console.error("endCall error:", err);
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
