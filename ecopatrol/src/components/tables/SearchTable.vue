<template>
  <div>
    <table class="table is-fullwidth">
      <thead>
        <tr>
          <th
            v-for="(value, index) in header"
            :key="index"
            style="text-align: center;"
          >
            <span v-html="value"></span>
          </th>
        </tr>
      </thead>

      <tbody>
        <tr v-for="(row, rowIndex) in invoice" :key="rowIndex">
          <td v-if="invoice.length > 1">
            {{ rowIndex + 1 }}
          </td>

          <td
            v-for="(cell, cellIndex) in row"
            :key="cellIndex"
            style="text-align: center;"
          >
            <template v-if="isPerson && cellIndex === 3 && cell">
              {{ cell }}

              <!-- 🔥 Զանգ -->
              <button @click="startCall(350)">📞</button>
            </template>

            <template v-else>
              {{ cell }}
            </template>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- 🔥 ԱՀԱ ՍԱ ՊԱՐՏԱԴԻՐ Է -->
    <audio id="remoteAudio" autoplay playsinline></audio>

    <!-- 🔥 Chrome unlock -->
    <button @click="unlockAudio">🔊 Enable Sound</button>
  </div>
</template>

<script>
import axios from "axios";
import { initSip, callNumber } from "@/services/sip";

export default {
  props: {
    header: Array,
    invoice: Array,
    isPerson: Boolean,
  },

  methods: {
    async startCall(number) {
      try {
        // 🔥 unlock audio (շատ կարևոր)
        this.unlockAudio();

        await initSip();

        // backend call (եթե պետք է)
        const response = await axios.post(
          "http://192.168.88.111:8000/api/phone/call/",
          {
            phone_number: number,
          }
        );

        if (response.data.status === "call_sent") {
          await callNumber(number);
        }
      } catch (error) {
        console.error("CALL ERROR:", error);
      }
    },

    unlockAudio() {
      const audio = document.getElementById("remoteAudio");

      if (audio) {
        audio.muted = false;
        audio.volume = 1;

        audio.play().catch(() => {});
      }
    },
  },
};
</script>