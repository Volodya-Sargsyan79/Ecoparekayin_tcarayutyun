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
        <h3 class="title is-5 has-text-centered mb-4">Ծառայողական մեքենայի տվյալներ</h3>
        <div class="box mb-3">
          <div class="field">
              <SearchTable :header="header.carHeader" :invoice="invoice.carInfo"/>
          </div>
        </div>
      </div>
    </div>
    <div class="columns" >
      <div class="column">
        <h3 class="title is-5 has-text-centered mb-4">Կարգախմբի տվյալներ</h3>
        <div class="box mb-3">
          <div class="field">
              <SearchTable :header="header.personHeader" :invoice="invoice.personInfo"/>
          </div>
        </div>
      </div>
    </div>
    <div v-if="lunches.length > 0" class="columns">
      <div class="column">
        <h3 class="title is-5 has-text-centered mb-5">☕ Հանգստի ժամանակներ և տևողություն</h3>
        <div class="box mb-3">
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
                  <span v-if="l.end && l.end !== 'None'">{{ l.end }}</span>
                  <span v-else class="has-text-warning">ընթացքի մեջ...</span>
                </td>
                <td>
                  <span v-if="l.duration">{{ formatMinutes(l.duration) }}</span>
                  <span v-else>—</span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
    <div v-if="summary" class="columns">
      <div class="column">
        <h3 class="title is-5 has-text-centered mb-4">Հերթափոխի ամփոփ տվյալներ</h3>
        <div class="box mb-3">
          <div class="field">
            <SearchTable :header="header.summaryHeader" :invoice="summaryInfo"/>
          </div>
        </div>
      </div>
    </div>
    <div class="columns" v-if="callList?.length > 0">
      <div class="column">
        <h3 class="title is-5 has-text-centered mb-4">Զանգերի պատմություն</h3>
        <div class="box mb-3">
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
                    <button @click="playAudio(call.recording_url)"> ▶️ Play</button>
                  </td>
                </tr>
              </tbody>
            </table>
            <audio id="recordedAudio" controls style="width:100%; margin-top:20px;"></audio>
          </div>
        </div>
      </div>
    </div>           
    <div class="columns" v-if="shift_pdf?.length > 0">
      <div class="column">
        <h3 class="title is-5 has-text-centered mb-4">Զանգվածային և տեքստային տեղեկություններ հերթափոխի մասին</h3>
        <div class="box mb-3" v-for="(value, index) in shift_pdf" :key="index">
          <p class="mb-3" v-if="value.text_info">{{ value.text_info }}</p>
          <a v-if="value.pdf_file" :href="`http://${$hostname}:8000/media/${value.pdf_file}`" target="_blank" class="button is-link is-small">📄 Բացել PDF</a>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import L from "leaflet";
  import "leaflet/dist/leaflet.css";
  import omnivore from "leaflet-omnivore";
  import axios from "axios";
  import markerIcon2x from "leaflet/dist/images/marker-icon-2x.png";
  import markerIcon from "leaflet/dist/images/marker-icon.png";
  import markerShadow from "leaflet/dist/images/marker-shadow.png";
  import SearchTable from "../tables/SearchTable.vue";

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
        shift_pdf: null,
        shift_info: null,
        lat: null,
        lng: null,
        map: null,
        marker: null,
        polyline: null,
        summary: null,
        lunches: [],
      };
    },
    components: {
      SearchTable
    },
    computed: {
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
              "Արագացուցիչի վազքը <br> հերթափոխի սկզբին",
              "Արագացուցիչի վազքը <br> հերթափոխի ավարտին",
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
      try {
        const callsRes = await axios.get('/api/phone/call_list/', {
          params: { shift_id: shiftId }
        });
        this.$store.commit('setCallList', callsRes.data);
      } catch (err) {
        console.error('CALL LIST ERROR:', err);
      }
      try {
        const lunchesRes = await axios.get("/api/ecopatrol/lunches/", {
          params: { shift_id: shiftId }
        });
        this.lunches = lunchesRes.data;
      } catch (err) {
        console.error('LUNCHES ERROR:', err);
      }
      try {
        const id = this.$route.params.id;
        const res = await axios.get("/api/ecopatrol/getinformationforshift/", {
              params: { id: id },
          })
        this.shift_pdf = res.data;
      } catch (err) {
        console.error("ERROR:", err);
      }
      this.$nextTick(async () => {
        try {
          const id = this.$route.params.id;
          const res = await axios.get(`/api/ecopatrol/getstationshift/${id}/`);
          this.shift_info = res.data[0];
          const route_id = this.shift_info.route_id
          const kmlUrl = `http://${window.location.hostname}:8000/media/kml/${route_id}/doc.kml`;
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
          if (!this.map) {
            console.error("MAP NOT READY");
            return;
          }
          if (!this.shift_info?.start_shift || !this.shift_info?.end_shift) {
            console.error("SHIFT TIME NOT FOUND");
            return;
          }
          const TOKEN = "SDBGAiEAv5Rc5L7LmxRjHReMqaM5LKptTGGGjT1WezwAlyVXDAQCIQCh0lLO_xlVrefOGUUCNTFsBFGU_cdtaqsv4sN0-yRxAnsidSI6MiwiZSI6IjIwMjYtMDYtMDRUMjA6MDA6MDAuMDAwKzAwOjAwIn0";
          const from = new Date(
            this.shift_info.start_shift.replace(" ", "T")
          ).toISOString();
          const to = new Date(
            this.shift_info.end_shift.replace(" ", "T")
          ).toISOString();
          const [positionsRes, summaryRes] = await Promise.all([
            axios.get("https://gps.eps.am/api/positions", {
              params: {
                deviceId: this.shift_info.deviceId,
                from,
                to,
              },
              headers: {
                Authorization: `Bearer ${TOKEN}`,
              },
            }),
            axios.get("https://gps.eps.am/api/reports/summary", {
              params: {
                deviceId: this.shift_info.deviceId,
                from,
                to,
                daily: true,
              },
              headers: {
                Authorization: `Bearer ${TOKEN}`,
              },
            }),
          ]);
          const gpsData = positionsRes.data;
          if (!gpsData || gpsData.length === 0) {
            alert("Տվյալներ չկան");
            return;
          }
          const points = gpsData
            .filter(
              (p) =>
                p.latitude &&
                p.longitude &&
                p.latitude != 0 &&
                p.longitude != 0
            )
            .map((p) => [
              parseFloat(p.latitude),
              parseFloat(p.longitude),
            ]);
          if (points.length === 0) {
            alert("Վավեր կոորդինատներ չկան");
            return;
          }
          if (this.polyline) {
            this.map.removeLayer(this.polyline);
          }
          this.polyline = L.polyline(points, {
            color: "red",
            weight: 2,
          }).addTo(this.map);
          const last = points[points.length - 1];
          if (this.marker) {
            this.map.removeLayer(this.marker);
          }
          this.marker = L.marker(last)
            .addTo(this.map)
            .bindPopup(`📍 Վերջին դիրք<br>${last[0]}, ${last[1]}`)
            .openPopup();
          this.map.fitBounds(this.polyline.getBounds());
          this.summary = Array.isArray(summaryRes.data)
            ? summaryRes.data[0]
            : summaryRes.data;
        } catch (err) {
          console.error("GPS API ERROR:", err);
        }
      });
    },
    methods: {
      formatHours(ms) {
        if (!ms) return "-";
          const totalSeconds = Math.floor(ms / 1000);
          const h = Math.floor(totalSeconds / 3600);
          const m = Math.floor((totalSeconds % 3600) / 60);
          return `${h} ժ ${m} ր`;
      },
      formatSpeed(value, type = "knots") {
        if (!value) return "0";
        let kmh;
        if (type === "knots") kmh = value * 1.852;
        else if (type === "ms") kmh = value * 3.6;
        else kmh = value;
        return `${kmh.toFixed(2)} կմ/ժ`;
      },
      playAudio(url) {
        const audio = document.getElementById("recordedAudio");
        if (!audio) return;
        audio.src = url;
        audio.load();
        audio.play();
      },
      formatMinutes(mins) {
        if (!mins && mins !== 0) return "00:00";
        const h = Math.floor(mins / 60);
        const m = mins % 60;
        return `${String(h).padStart(2, "0")}:${String(m).padStart(2, "0")}`;
      }
    },
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