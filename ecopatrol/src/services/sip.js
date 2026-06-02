import { UserAgent, Inviter, Registerer } from "sip.js";

let ua = null;
let registerer = null;
let currentSession = null;
let mediaRecorder = null;
let recordedChunks = [];
let localStreamRef = null;
let audioContextRef = null;
let eventSocket = null;  // WebSocket for Asterisk events

// metadata placeholders — դրանք պետք է լրացվեն ձեր լոգիկայով երբ սկսվում է զանգը
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
let heartbeatInterval = null;


// Connect to WebSocket for Asterisk events
function connectToEventSocket() {
  // Force ws:// for development (backend is running on HTTP)
  const protocol = 'ws:';
  const backendHost = '192.168.88.111:8000';
  const eventSocketUrl = `${protocol}//${backendHost}/ws/asterisk-events/`;

  console.log("🔌 Connecting to event socket:", eventSocketUrl);
  
  eventSocket = new WebSocket(eventSocketUrl);
  
  eventSocket.onopen = () => {
    console.log("✅ Event socket connected");
  };
  
  eventSocket.onmessage = (event) => {
    try {
      const data = JSON.parse(event.data);
      console.log("📨 Event received:", data);
      
      // Handle incoming call notifications from Asterisk
      if (data.type === 'incoming_call') {
        console.log(`📞 Incoming call from ${data.caller_id}`);
        window.dispatchEvent(new CustomEvent('asterisk-incoming-call', { detail: data }));
      }
    } catch (err) {
      console.error("Error parsing event:", err);
    }
  };
  
  eventSocket.onerror = (err) => {
    console.error("❌ Event socket error:", err);
  };
  
  eventSocket.onclose = () => {
    console.warn("⚠️ Event socket disconnected, reconnecting in 3s...");
    setTimeout(() => connectToEventSocket(), 1000);
  };
}

// Sanitize incoming/outgoing SDP to remove unsupported or conflicting codecs (e.g. G726)
function sanitizeSdp(sdp) {
  if (!sdp || typeof sdp !== 'string') return sdp;

  const lines = sdp.split(/\r?\n/);
  const toRemove = new Set();

  // find payload numbers referenced by G726 rtpmap lines
  for (const line of lines) {
    const m = line.match(/^a=rtpmap:(\d+)\s+G726(?:-32)?\/[0-9]+/i);
    if (m) toRemove.add(m[1]);
  }

  if (toRemove.size === 0) return sdp;

  // remove only the a=rtpmap:, a=fmtp:, a=rtcp-fb: lines for those payloads
  const filtered = lines.filter((line) => {
    let m = line.match(/^a=rtpmap:(\d+)\s+/i);
    if (m && toRemove.has(m[1])) return false;
    m = line.match(/^a=fmtp:(\d+)\s+/i);
    if (m && toRemove.has(m[1])) return false;
    m = line.match(/^a=rtcp-fb:(\d+)\s+/i);
    if (m && toRemove.has(m[1])) return false;
    return true;
  });

  return filtered.join('\r\n');
}

// initialize SIP UA
export async function initSip() {
  if (ua) return;

  // Connect to event socket first
  connectToEventSocket();

  ua = new UserAgent({
    uri: UserAgent.makeURI("sip:809@192.168.1.5"),
    transportOptions: { server: "wss://192.168.1.5:8089/ws" },
    // Workaround: prefer advertising page hostname in Contact/Via when PBX rewrites to 127.0.0.1
    hackIpInContact: true,
    viaHost: window.location.hostname || undefined,
    contactParams: { host: window.location.hostname || undefined, transport: 'ws' },
    authorizationUsername: "809",
    authorizationPassword: "K*EsGdQ^c9",
    sessionDescriptionHandlerFactoryOptions: {
      constraints: { audio: true, video: false },
      peerConnectionConfiguration: {
        iceServers: [
          { urls: "stun:stun.l.google.com:19302" },
          // TODO: replace with your TURN server details
          { urls: "turn:turn.example.com:3478", username: "TURN_USER", credential: "TURN_PASS" }
        ],
        // Prefer gathering public candidates for NAT traversal
        iceTransportPolicy: "all",
      },
      // sanitize SDP to strip unsupported/conflicting codecs (G726) before applying
      modifiers: [async (description) => {
        try {
          return { type: description.type, sdp: sanitizeSdp(description.sdp) };
        } catch (e) {
          return description;
        }
      }],
    },
  });

  await ua.start();
  console.log("✅ SIP started");
  startHeartbeat();

  ua.transport.onDisconnect = () => {
    console.warn("❌ SIP transport disconnected → reconnecting...");

    setTimeout(async () => {
      try {
        await ua.start();
        console.log("♻️ SIP reconnected");

        if (registerer) {
          await registerer.register();
          console.log("✅ re-REGISTERED");
        }
      } catch (e) {
        console.error("Reconnect failed:", e);
      }
    }, 3000);
  };

  // perform SIP REGISTER so PBX knows this UA is available
  try {
    registerer = new Registerer(ua);
    await registerer.register();
    console.log("✅ REGISTERED");
  } catch (err) {
    console.warn("⚠️ Register failed:", err);
  }

  // Handle incoming calls
  ua.delegate = {
    onInvite: async (inviter) => {
      // Safely extract caller number from inviter (avoid reading .uri of undefined)
      function extractCallerId(inv) {
        try {
          if (inv && inv.remoteIdentity && inv.remoteIdentity.uri && inv.remoteIdentity.uri.user) return inv.remoteIdentity.uri.user;
          if (inv && inv.request && inv.request.from && inv.request.from.uri && inv.request.from.uri.user) return inv.request.from.uri.user;
          if (inv && inv.nameAddrHeader && inv.nameAddrHeader.uri && inv.nameAddrHeader.uri.user) return inv.nameAddrHeader.uri.user;
        } catch (e) {
          // ignore
        }
        return null;
      }

      const incomingCaller = extractCallerId(inviter) || 'unknown';
      console.log("📞 Incoming call from:", incomingCaller);

      // Debug: log raw INVITE body if present to inspect SDP issues
      try {
        const reqBody = inviter && inviter.request && inviter.request.body ? inviter.request.body : null;
        if (reqBody) {
          console.log("🔍 INVITE body (may include SDP):", reqBody);
          window.dispatchEvent(new CustomEvent('sip-debug-invite', { detail: { body: reqBody } }));
        }
      } catch (e) {
        console.warn("Could not log INVITE body", e);
      }

      // Reset variables for incoming call
      alreadySaved = false;
      callId = crypto.randomUUID ? crypto.randomUUID() : String(Date.now()) + Math.random().toString(36).slice(2);
      callerNumber = incomingCaller;
      calledNumber = "809";
      callStartISOString = new Date().toISOString();
      callEndISOString = null;
      callDurationSeconds = 0;
      
      currentSession = inviter;

      // Auto-answer the call
      inviter.delegate = {
        onSessionDescriptionHandler: async (sdh) => {
          const pc = sdh.peerConnection;

          // Debug: log peerConnection configuration and ICE candidates for incoming calls
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
          console.log("📞 Incoming call connected");
        },

        onBye: () => {
          console.log("👋 Incoming call ended by remote");
          callEndISOString = new Date().toISOString();
          callDurationSeconds = calcCallDuration(callStartISOString, callEndISOString);
          stopAndCleanup();
        },

        onTerminated: () => {
          console.log("🔚 Incoming session terminated");
          callEndISOString = callEndISOString || new Date().toISOString();
          callDurationSeconds = calcCallDuration(callStartISOString, callEndISOString);
          stopAndCleanup();
        },
      };

      inviter.stateChange.addListener((state) => {
        console.log("INCOMING CALL STATE:", state);
      });

      // DO NOT auto-answer here to avoid duplicate call legs when a physical phone picks up.
      // Emit an event so the UI can decide to accept the call (e.g., when user clicks answer).
      window.dispatchEvent(new CustomEvent('sip-invite-received', {
        detail: {
          callId,
          caller: callerNumber,
          inviterId: callId // lightweight identifier; inviter object kept in closure via currentSession
        }
      }));

      console.log('ℹ️ Incoming INVITE dispatched to UI (no auto-answer)');
    },
  };
  function startHeartbeat() {
    stopHeartbeat();

    heartbeatInterval = setInterval(() => {
      try {
        if (!ua || ua.isConnected === false) {
          console.warn("💔 UA not connected, skipping heartbeat");
          return;
        }

        ua.transport.send({
          method: "OPTIONS",
          uri: ua.configuration.uri
        });

        console.log("💓 SIP OPTIONS heartbeat sent");
      } catch (e) {
        console.warn("Heartbeat failed:", e);
      }
    }, 25000);
  }

  function stopHeartbeat() {
    if (heartbeatInterval) {
      clearInterval(heartbeatInterval);
      heartbeatInterval = null;
    }
  }
}

// call a number
export async function callNumber(number, shiftIdParam) {
  if (!ua || !ua.transport || !ua.transport.isConnected()) {
    console.error("🚫 SIP is disconnected → trying to recover before call");

    try {
      await ua.start();

      if (!registerer) {
        registerer = new Registerer(ua);
      }

      await registerer.register();
      console.log("♻️ recovered SIP before call");
    } catch (e) {
      throw new Error("SIP is not available even after reconnect");
    }
  }
  // Ensure UA is running and registered. If not, try to initialize and register automatically.
  if (!ua) {
    console.warn("UA not initialized. Initializing UA before calling...");
    try {
      await initSip();
    } catch (err) {
      console.error("Failed to initialize UA:", err);
      throw new Error("UA not initialized. Call initSip() first.");
    }
  }

  // If we don't have a registerer (or registerer was cleared), attempt a best-effort register.
  if (!registerer) {
    try {
      registerer = new Registerer(ua);
      await registerer.register();
      console.log("✅ REGISTERED (auto)");
    } catch (err) {
      console.warn("Auto-register failed:", err);
      // continue — user can still attempt call; PBX may reject if not registered
    }
  }
  
  alreadySaved = false;
  
  // set metadata for this call

  shiftId = shiftIdParam;
  callId = crypto.randomUUID ? crypto.randomUUID() : String(Date.now()) + Math.random().toString(36).slice(2);
  callerNumber = "809"; // փոխարինեք ճիշտ caller-ի արժեքով եթե պետք է
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
  console.log("CALL STATE:", state);

  // 📡 anything except established → ringing state
  if (state === "Initial" || state === "Progressing" || state === "Early") {
    if (dialToneAudio) {
      dialToneAudio.pause();
      dialToneAudio.currentTime = 0;
    }

    if (ringbackAudio) {
      ringbackAudio.play().catch(() => {});
    }
  }

  // ☎️ answered
  if (state === "Established") {
    callAnswered = true;
    dialToneAudio?.pause();
    ringbackAudio?.pause();

    dialToneAudio.currentTime = 0;
    ringbackAudio.currentTime = 0;
  }

  // 🔚 end
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

      // Debug: log peerConnection configuration and ICE candidates for outgoing calls

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
      callAnswered = true;
      if (ringbackAudio) {
        ringbackAudio.pause();
        ringbackAudio.currentTime = 0;
      }
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
  if (alreadySaved) return; // 🔥 ԱՅՍՏԵՂ է կարևորը
  alreadySaved = true;

  if (!callAnswered) {
    console.log("🛑 Call was not answered; skipping recording upload.");
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

    console.log("✅ Uploaded in server");

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
  console.log("🧹 Cleaning up call...");

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

  // reset call metadata (optional)
  currentSession = null;
  // note: do not clear callId/callerNumber immediately if you need them for upload; they are used in saveRecording
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
          console.log("→ Sending explicit REJECT 486 Busy Here for session:", callLabel, "state:", sessionState);
          // Send an explicit 486 Busy Here to request the PBX stop ringing immediately
          await currentSession.reject({ statusCode: 486, reasonPhrase: "Busy Here" });
          console.log("❌ Incoming call rejected (486 Busy Here)");
          window.dispatchEvent(new CustomEvent('sip-call-rejected', { detail: { call_id: callLabel } }));
        } catch (err) {
          console.warn("Reject failed, falling back to cancel/bye if available:", err);
          if (canCancel) {
            await currentSession.cancel();
            console.log("❌ Outgoing call canceled (fallback)");
          } else if (canBye) {
            await currentSession.bye();
            console.log("❌ Call ended with BYE (fallback)");
          }
        }
      } else if (canCancel && sessionState !== "Established" && sessionState !== "established") {
        await currentSession.cancel();
        console.log("❌ Outgoing call canceled");
      } else if (canBye) {
        await currentSession.bye();
        console.log("❌ Call ended with BYE");
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

// Shutdown SIP and close WebSocket
export async function shutdownSip() {
  if (currentSession) {
    endCall();
  }
  
  if (registerer) {
    try {
      await registerer.unregister();
      console.log("✅ UNREGISTERED");
    } catch (err) {
      console.warn("⚠️ Unregister failed:", err);
    }
    registerer = null;
  }

  if (ua) {
    await ua.stop();
    ua = null;
  }
  
  if (eventSocket) {
    eventSocket.close();
    eventSocket = null;
  }
  
  console.log("✅ SIP shutdown complete");
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
