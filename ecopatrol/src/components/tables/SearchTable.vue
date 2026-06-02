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
              <button class="button is-small is-info" @click="startCall(350, rowIndex)" style="margin-left: 0.5rem;">📞</button>
              <button
                v-if="callStarted && activeRowIndex === rowIndex"
                class="button is-small is-danger"
                @click="handleHangup"
                style="margin-left: 0.5rem;"
              >
                Ընդատել
              </button>
            </template>

            <template v-else>
              {{ cell }}
            </template>
          </td>
        </tr>
      </tbody>
    </table>

    <audio id="remoteAudio" autoplay playsinline></audio>

  </div>
</template>

<script>
import axios from "axios";
import { initSip, callNumber, endCall } from "@/services/sip";

export default {
  data() {
    return {
      callStarted: false,
      activeRowIndex: null,
    };
  },

  props: {
    header: Array,
    invoice: Array,
    isPerson: Boolean,
  },

  mounted() {
    window.addEventListener("sip-call-ended", this.onSipCallEnded);
  },

  beforeUnmount() {
    window.removeEventListener("sip-call-ended", this.onSipCallEnded);
  },

  methods: {
    onSipCallEnded() {
      this.callStarted = false;
      this.activeRowIndex = null;
    },
    async startCall(number, rowIndex) {
      this.callStarted = true;
      this.activeRowIndex = rowIndex;

      try {
        await initSip();

        const shiftIdParam = this.$route.params.id;

        const response = await axios.post(
          "http://192.168.88.111:8000/api/phone/call/",
          {
            phone_number: number,
          }
        );

        if (response.data.status === "call_sent") {
          await callNumber(number, shiftIdParam);
        } else {
          console.warn("Unexpected call response:", response.data);
          this.callStarted = false;
          this.activeRowIndex = null;
        }
      } catch (error) {
        console.error("CALL ERROR:", error);
        this.callStarted = false;
        this.activeRowIndex = null;
      }
    },

    async handleHangup() {
      try {
        await endCall();
      } catch (error) {
        console.error("Hangup failed:", error);
      } finally {
        this.callStarted = false;
        this.activeRowIndex = null;
      }
    },
  },
};
</script>