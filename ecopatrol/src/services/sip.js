// services/sip.js
import { UserAgent, Inviter } from "sip.js";

let ua = null;
let mediaRecorder = null;
let recordedChunks = [];

export async function initSip() {
  if (ua) return;

  ua = new UserAgent({
    uri: UserAgent.makeURI("sip:809@192.168.1.5"),
    transportOptions: {
      server: "wss://192.168.1.5:8089/ws",
    },
    authorizationUsername: "809",
    authorizationPassword: "K*EsGdQ^c9",

    sessionDescriptionHandlerFactoryOptions: {
      constraints: {
        audio: true,
        video: false,
      },
      peerConnectionConfiguration: {
        iceServers: [
          { urls: "stun:stun.l.google.com:19302" }
        ],
      },
    },
  });

  await ua.start();
  console.log("✅ SIP started");
}

export async function callNumber(number) {
  const target = UserAgent.makeURI(`sip:${number}@192.168.1.5`);

  const inviter = new Inviter(ua, target);

  inviter.delegate = {
    onSessionDescriptionHandler: (sdh) => {
      const pc = sdh.peerConnection;

      // 🔥 ԱՀԱ ՍԱ Է քո audio-ի լուծումը
      pc.ontrack = (event) => {
        const stream = event.streams[0];

        // 🔊 PLAY
        const audio = document.getElementById("remoteAudio");
        if (audio) {
          audio.srcObject = stream;
          audio.play();
        }

        // 🎙 RECORD START
        startRecording(stream);
      };
    },

    onConnected: () => {
      console.log("📞 Call connected");
    },

    onDisconnected: () => {
      console.log("❌ Call ended");
    },
  };

  await inviter.invite();
}

function startRecording(stream) {
  recordedChunks = [];

  mediaRecorder = new MediaRecorder(stream);

  mediaRecorder.ondataavailable = (e) => {
    if (e.data.size > 0) {
      recordedChunks.push(e.data);
    }
  };

  mediaRecorder.onstop = () => {
    const blob = new Blob(recordedChunks, { type: "audio/webm" });
    console.log("🎧 Recorded file:", blob);
  };

  mediaRecorder.start();
  console.log("🎙 Recording started");
}