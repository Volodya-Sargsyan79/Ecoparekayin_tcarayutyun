<template>
  <div class="box">
    <div class="columns">
      <div class="column">
        <div class="map-container">
          <div id="map"></div>
        </div>
      </div>
    </div>

    <div class="columns">
      <div class="column">
        <div class="field">
          <div>{{ shift_info?.region }}</div>
        </div>
      </div>
      <div class="column">
        <div class="field">
          <div>{{ shift_info?.precinct }}</div>
        </div>
      </div>
      <div class="column">
        <div class="field">
          <div>Երթուղի {{ shift_info?.route_number }}</div>
        </div>
      </div>
      <div class="column">
        <div class="field">
          <div>Երթուղու երկարություն {{ shift_info?.route_length }} կմ</div>
        </div>
      </div>
    </div>
    <div class="columns">
        <div class="column">
            <div class="field">
                <SearchTable 
                    :header="header.carHeader"
                    :invoice="invoice.carInfo"
                />
            </div>
        </div>
    </div>
    
    <h3 class="title is-5 has-text-centered mb-4">
        Հերթափոխ անձնակազմ
    </h3>

    <div class="columns">
      <div class="column">
            <div class="field">
                <SearchTable 
                  :header="header.personHeader"
                  :invoice="invoice.personInfo"
                  :isPerson="true"
                />
            </div>
        </div>
    </div>

🎨 Թարմացված UI (սկզբնական վիճակով)
<h3 class="title is-5 has-text-centered mb-5">
  ☕ Հանգստի գրանցումներ
</h3>

<!-- ACTION BUTTONS -->
<div class="columns mb-4">
  
  <div class="column">
    <button
      class="button is-warning is-fullwidth"
      @click="startLunch"
      :disabled="isOnBreak"
    >
      ☕ Գնում եմ հանգստի
    </button>
  </div>

  <div class="column">
    <button
      class="button is-success is-fullwidth"
      @click="endLunch"
      :disabled="!isOnBreak"
    >
      🟢 Վերադարձա
    </button>
  </div>

</div>

<!-- STATS -->
<div class="columns mb-4">

  <div class="column">
    <div class="box has-text-centered">
      <p class="heading">Օգտագործված</p>
      <p class="title is-4 has-text-info">
        {{ formatMinutes(stats.used) }}
      </p>
    </div>
  </div>

  <div class="column">
    <div class="box has-text-centered">
      <p class="heading">Մնացած</p>
      <p 
        class="title is-4"
        :class="stats.remaining >= 0 ? 'has-text-success' : 'has-text-danger'"
      >
        {{ formatMinutes(Math.abs(stats.remaining)) }}
      </p>
    </div>
  </div>

</div>

<!-- INITIAL MESSAGE -->
<div v-if="!lunches.length" class="notification is-info is-light has-text-centered">
  ⏱ Դուք ունեք <strong>2 ժամ (02:00)</strong> հանգստի ժամանակ
</div>

<!-- TABLE -->
<div v-else class="box">
  <table class="table is-fullwidth is-striped">

    <thead>
      <tr>
        <th>#</th>
        <th>Սկիզբ</th>
        <th>Ավարտ</th>
        <th>Տևողություն</th>
      </tr>
    </thead>

    <tbody>
      <tr v-for="(l, index) in lunches" :key="index">
        <td>{{ index + 1 }}</td>

        <td>{{ l.start }}</td>

        <td>
          <span v-if="l.end && l.end !== 'None'">
            {{ l.end }}
          </span>
          <span v-else class="has-text-warning">
            ընթացքի մեջ...
          </span>
        </td>

        <td>
          <span v-if="l.duration">
            {{ formatMinutes(l.duration) }}
          </span>
          <span v-else>—</span>
        </td>
      </tr>
    </tbody>

  </table>
</div>
    
    <h3 class="title is-5 has-text-centered mb-4">
        Զանգեր հերթափոխի հետ
    </h3>

    <div class="columns">
      <div class="column">
        <div class="field">
          <table class="table is-fullwidth">
            <thead>
              <tr>
                <th>#</th>
                <th>Ժամ</th>
                <th>Ումից</th>
                <th>Ում</th>
                <th>Լսել</th>
              </tr>
            </thead>

            <tbody>
              <tr v-for="(call, index) in callList" :key="index">
                <td>{{ index + 1 }}</td>
                <td>{{ call.call_start }}</td>
                <td>{{ call.caller_number }}</td>
                <td>{{ call.called_number }}</td>

                <td>
                  <button @click="playAudio(call.recording_url)">
                    ▶️ Play
                  </button>
                </td>
              </tr>
            </tbody>
          </table>

          <!-- Player -->
          <audio id="recordedAudio" controls style="width:100%; margin-top:20px;"></audio>
        </div>
      </div>
    </div>           

    <!-- Information Section -->
    <div class="columns" >
      <div class="column">
        <h3 class="title is-5 has-text-centered mb-4">
          Զեկուցագիր / Տեղեկություն
        </h3>

        <div 
          class="box mb-3" 
          v-for="(value, index) in shift_pdf" 
          :key="index"
        >
          <!-- Text -->
          <p class="mb-3" v-if="value.text_info">
            {{ value.text_info }}
          </p>

          <!-- PDF -->
          <a 
            v-if="value.pdf_file"
            :href="`http://127.0.0.1:8000/media/${value.pdf_file}`" 
            target="_blank" 
            class="button is-link is-small"
          >
            📄 Բացել PDF
          </a>
        </div>

      </div>
    </div>
      
    <div class="columns">
      <div class="column" style="display: flex; align-items: flex-end;">
        <button class="button is-primary" @click="handleClick">Ավելացնել զեկուցագիր կամ տեղեկատվություն</button>
      </div>
    </div>
  </div>
</template>

<script>
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import omnivore from "leaflet-omnivore";
import axios from "axios";
import SearchTable from "../tables/SearchTable.vue";

import markerIcon2x from "leaflet/dist/images/marker-icon-2x.png";
import markerIcon from "leaflet/dist/images/marker-icon.png";
import markerShadow from "leaflet/dist/images/marker-shadow.png";

delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: markerIcon2x,
  iconUrl: markerIcon,
  shadowUrl: markerShadow,
});

export default {
  name: "ShiftDetail",
  data() {
    return {
      shift_info: null,
      shift_pdf: null,
      lat: null,       // latitude input
      lng: null,       // longitude input
      map: null,       // store map instance
      marker: null,    // store marker instance
      file: null,
      previewUrl: null,
      previewType: null,
      lunches: [],
      stats: {
        used: 0,
        remaining: 120,
        overused: 0
      },
      currentLunch: null,
      isOnBreak: false
    };
  },
    components: {
    SearchTable
  },
  computed: {
      // hasActiveLunch() {
      //   return this.lunches.some(l => !l.end || l.end === 'None');
      // },
      header() {
        return {
          carHeader: [
            "Հերթափոխի սկիզբ",
            "Հերթափոխի ավարտ",
            "Մեքենայի պետհամարանիշ",
            "Մեքենայի կողային համարանիշ"
          ],
          personHeader: [
            "#",
            "Անուն",
            "Ազգանուն",
            "Պաշտոն",
            "Հեռախոս",
            "Տեսախցիկ"
          ],
          summaryHeader: [
            "Միջին արագություն",
            "Առավելագույն արագություն", 
            "Վազք",
            "Արագացուցիչի վազքը <br> հետթափոխի սկզբին",
            "Արագացուցիչի վազքը <br> հետթափոխի ավարտին",
            "Շարժիչի աշխատանք",
            
           
          ]
        } 
      },
      invoice() {
        const routes = this.$store.state.user.stationshif || []

        return {
          carInfo: [
            [
              this.shift_info?.start_shift,
              this.shift_info?.end_shift,
              this.shift_info?.car_number,
              this.shift_info?.board_number,
            ]
          ],
          personInfo: [ 
            [
              this.shift_info?.employee_01_name,
              this.shift_info?.employee_01_surname,
              this.shift_info?.employee_01_position_held,
              this.shift_info?.employee_01_phone,
              this.shift_info?.employee_01_camera,
            ],
            [
              this.shift_info?.employee_02_name,
              this.shift_info?.employee_02_surname,
              this.shift_info?.employee_02_position_held,
              this.shift_info?.employee_02_phone,
              this.shift_info?.employee_02_camera,
            ],
            [
              this.shift_info?.employee_03_name,
              this.shift_info?.employee_03_surname,
              this.shift_info?.employee_03_position_held,
              this.shift_info?.employee_03_phone,
              this.shift_info?.employee_03_camera,
            ],
            [
              this.shift_info?.employee_04_name,
              this.shift_info?.employee_04_surname,
              this.shift_info?.employee_04_position_held,
              this.shift_info?.employee_04_phone,
              this.shift_info?.employee_04_camera,
            ]
          ].filter(row => row.some(cell => cell))
        }
      },
      summaryInfo() {
        if (!this.summary) return [];

        return [
          [
            this.formatSpeed(this.summary.averageSpeed),
            this.formatSpeed(this.summary.maxSpeed),
            `${this.summary.distance?.toFixed(2)/1000} կմ`,
            `${this.summary.startOdometer?.toFixed(2)/1000} կմ`,
            `${this.summary.endOdometer?.toFixed(2)/1000} կմ`,
            this.formatHours(this.summary.engineHours),
          ]
        ];
      },
      callList() {
        return this.$store.state.user.call_list || [];
      }
  },
  async mounted() {
    const shiftId = this.$route.params.id;
    axios
      .get('/api/phone/call_list/', {
          params: { shift_id: shiftId},
      }) 
      .then((res) => {
          this.$store.state.user.call_list = res.data;
      })
      .catch(err => { console.error(err) })
    
    window.addEventListener("new-call", this.onNewCall);

    // ⬇️ GET lunches from backend
    axios.get("/api/ekopatrol/lunches/", {
      params: { shift_id: shiftId }
    })
    .then(res => {
      this.lunches = res.data;

      // 🔥 ստուգում ենք՝ կա՞ open lunch
      const active = this.lunches.find(l => !l.end || l.end === "None");

      if (active) {
        this.isOnBreak = true;
        this.currentLunch = {
          start: active.start,
          end: null,
          duration: null
        };
      } else {
        this.isOnBreak = false;
        this.currentLunch = null;
      }

      this.recalculateStats?.();
    });

    this.recalculateStats();

    this.$nextTick(async () => {
      try {
        const id = this.$route.params.id;

        const res = await axios.get(`/api/ekopatrol/getstationshift/${id}/`);
        
        this.shift_info = res.data[0];

        const route_id = this.shift_info.route_id

        const kmlUrl = `http://${window.location.hostname}:8000/media/kml/${route_id}/doc.kml`;
        // const kmlUrl = `http://127.0.0.1:8000/media/kml/${route_id}/doc.kml`;


        this.map = L.map("map").setView([40.1792, 44.4991], 10);

        L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
          maxZoom: 30,
          attribution: "© OpenStreetMap contributors",
        }).addTo(this.map);

        omnivore
          .kml(kmlUrl)
          .on("ready", (e) => {
            this.map.fitBounds(e.target.getBounds()); // ✅ fixed
          })
          .on("error", (e) => {
            console.error("KML LOAD ERROR:", e);
          })
          .addTo(this.map);

        setTimeout(() => {
          this.map.invalidateSize();
        }, 500);

      } catch (err) {
        console.error("ERROR:", err);
      }

      try {
        const id = this.$route.params.id;

        console.log("id:", id)

        const res = await axios
                .get("/api/ekopatrol/getinformationforshift/", {
                    params: { id: id },
                })
                
        this.shift_pdf = res.data;

      } catch (err) {
        console.error("ERROR:", err);
      }

      try {
        const TOKEN = "RjBEAiBCuH_SKGfbJ43SjUmiZ6ya-hMZDHFeKGCExUNpuuUL1AIgU5yrqPiiA1sWcjnTFfxkyzEglQKNxxoSkkzrGKt8lAt7InUiOjIsImUiOiIyMDI2LTA1LTEyVDIwOjAwOjAwLjAwMCswMDowMCJ9";

        const res = await axios.get(
          "https://gps.eps.am/api/positions",
          {
            params: {
              deviceId: this.shift_info.deviceId,
              to: new Date().toISOString()
            },
            headers: {
              Authorization: `Bearer ${TOKEN}`
            }
          }
        );

        // console.log("GPS DATA:", res.data);

        if (res.data.length > 0) {
          const last = res.data[0];

          const lat = last.latitude;
          const lng = last.longitude;
          const speed = this.formatSpeed(last.speed)

          // console.log("COORD:", lat, lng);

          if (!lat || !lng) {
            alert("Մեքենայի տեղորոշման կոորդինատները հասանելի չեն:");
            return;
          }

          const latLng = [parseFloat(lat), parseFloat(lng)];

          if (this.marker) {
            this.map.removeLayer(this.marker);
          }

          this.marker = L.marker(latLng)
            .addTo(this.map)
            .bindPopup(
              `<b>📍 Կոորդինատներ</b><br>
              ${lat}, ${lng} <br><br>
              <b> 📍 Ներկա արագություն</b><br>
              ${speed}`
            )
            .openPopup();

          this.map.flyTo(latLng, 14); 
        }

      } catch (err) {
        console.error("GPS API ERROR:", err);
      }
    });
  },
  beforeUnmount() {
    window.removeEventListener("new-call", this.onNewCall);
  },
  methods: {
    formatSpeed(value, type = "knots") {
      if (!value) return "0 կմ/ժ";

        let kmh;

        if (type === "knots") kmh = value * 1.852;
        else if (type === "ms") kmh = value * 3.6;
        else kmh = value;

        return `${kmh.toFixed(2)} կմ/ժ`;
    },

    startLunch() {
      const now = this.getTime();
      const shiftId = this.$route.params.id;

      const fd = new FormData();

      fd.append("shift_id", shiftId);
      fd.append("start_lanch", now);

      const lunch = {
        start: now,
        end: null,
        duration: null
      };
      console.log(now, shiftId, lunch)
      
      this.currentLunch = lunch;
      this.lunches.push(lunch);
      this.isOnBreak = true;



    axios.post("/api/ekopatrol/lunch_start/", fd)
      .then(() => {
        console.log("ok");
      })
      .catch(err => {
        console.error(err.response?.data || err);
      });

    },

    endLunch() {
      const now = this.getTime();
      const shiftId = this.$route.params.id;

      const fd = new FormData();

      fd.append("shift_id", shiftId);
      fd.append("end_lanch", now);

      if (!this.currentLunch) return;

      const index = this.lunches.findIndex(
        l => !l.end || l.end === "None"
      );

      if (index !== -1) {
        const updated = {
          ...this.lunches[index],
          end: now,
          duration: this.diffMinutes(this.lunches[index].start, now)
        };

        // 🔥 Vue 3 correct reactive update
        this.lunches.splice(index, 1, updated);
      }

      const duration = this.diffMinutes(this.currentLunch.start, now);

      this.updateStats(duration);

      this.currentLunch = null;
      this.isOnBreak = false;

      this.recalculateStats();

      // optional API
      axios.post("/api/ekopatrol/lunch_end/", fd)
      .then(() => {
        console.log("ok");
      })
      .catch(err => {
        console.error(err.response?.data || err);
      });
    },
    
    recalculateStats() {
      let used = 0;

      this.lunches.forEach(l => {
        if (l.start && l.end && l.end !== "None") {
          const [sh, sm] = l.start.split(":").map(Number);
          const [eh, em] = l.end.split(":").map(Number);

          used += (eh * 60 + em) - (sh * 60 + sm);
        }
      });

      this.stats.used = used;
      this.stats.remaining = 120 - used;
    },
    getTime() {
      return new Date().toTimeString().slice(0, 8); // HH:MM:SS
    },

    diffMinutes(start, end) {
      const [sh, sm] = start.split(":").map(Number);
      const [eh, em] = end.split(":").map(Number);

      return (eh * 60 + em) - (sh * 60 + sm);
    },

    updateStats(mins) {
      this.stats.used += mins;
      this.stats.remaining = 120 - this.stats.used;
    },

    formatMinutes(mins) {
      if (!mins && mins !== 0) return "00:00";

      const h = Math.floor(mins / 60);
      const m = mins % 60;

      return `${String(h).padStart(2, "0")}:${String(m).padStart(2, "0")}`;
    },

    handleFileUpload(event) {
      const selectedFile = event.target.files[0];
      if (!selectedFile) return;

      this.file = selectedFile;

      // Ստուգել ֆայլի type
      if (selectedFile.type.startsWith('image/')) {
        this.previewType = 'image';
        this.previewUrl = URL.createObjectURL(selectedFile);
      } else if (selectedFile.type === 'application/pdf') {
        this.previewType = 'pdf';
        this.previewUrl = URL.createObjectURL(selectedFile);
      } else {
        alert("Խնդրում ենք ընտրել նկար կամ PDF ֆայլ");
        this.file = null;
        this.previewUrl = null;
        this.previewType = null;
      }
    },

    handleClick() {
      this.$router.push({
        name: "shift-edit",
        params: { id: this.shift_info.id }
      })
    },

    playAudio(url) {
      const audio = document.getElementById("recordedAudio");

      if (audio) {
        audio.src = url;
        audio.load();
        audio.play();
      }
    },
    onNewCall(event) {
      const newCall = event.detail;

      this.$store.state.user.call_list.unshift(newCall);
    }
  }
};
</script>

<style>
.map-container {
  width: 100%;
  height: 600px;
}

#map {
  width: 100%;
  height: 100%;
}
</style>