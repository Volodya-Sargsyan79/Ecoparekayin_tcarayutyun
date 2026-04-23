// services/sip.js
import { UserAgent, Inviter } from "sip.js";

let ua = null;

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
        console.log("🎧 Remote audio received");

        const audio = document.getElementById("remoteAudio");

        if (audio) {
          audio.srcObject = event.streams[0];
          audio.muted = false;
          audio.volume = 1;

          audio.play().catch((e) => {
            console.error("Play error:", e);
          });
        }
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