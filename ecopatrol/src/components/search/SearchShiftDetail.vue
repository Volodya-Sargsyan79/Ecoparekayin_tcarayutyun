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
                />
            </div>
        </div>
    </div>
    <h3 class="title is-5 has-text-centered mb-4">
      Սարքի հաշվետվություն
    </h3>
    <div class="columns">
      <div class="column">
        <div class="field">
          <SearchTable
            :header="header.summaryHeader"
            :invoice="summaryInfo"
          />
        </div>
      </div>
    </div>
     <!-- Information Section -->
    <div class="columns" v-if="shift_pdf?.length > 0">
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
      lat: null,       // latitude input
      lng: null,       // longitude input
      map: null,       // store map instance
      marker: null,
      polyline: null,    // store marker instance
      summary: null,
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
      }
  },
  async mounted() {
    this.$nextTick(async () => {
      try {
        const id = this.$route.params.id;

        const res = await axios.get(`/api/ekopatrol/getstationshift/${id}/`);
        
        this.shift_info = res.data[0];

        const route_id = this.shift_info.route_id

        // const kmlUrl = `http://${window.location.hostname}:8000/media/kml/${route_id}/doc.kml`;
        const kmlUrl = `http://127.0.0.1:8000/media/kml/${route_id}/doc.kml`;


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

        const TOKEN = "RjBEAiBU_uoM5J7R6xs7LDCwCQxvDRsBpBAUwk3UwbNbXn3pjAIgOumaesKHD7DSuRnakhKuie3TTun4tI5vkAKMxDX66c17InUiOjIsImUiOiIyMDI2LTA0LTE5VDIwOjAwOjAwLjAwMCswMDowMCJ9";

        // ✅ ժամանակների ֆորմատավորում
        const from = new Date(
          this.shift_info.start_shift.replace(" ", "T")
        ).toISOString();

        const to = new Date(
          this.shift_info.end_shift.replace(" ", "T")
        ).toISOString();

        // console.log("FROM:", from);
        // console.log("TO:", to);

        // 🔥 2 API call միաժամանակ (ավելի արագ)
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

        // =========================
        // 📍 POSITIONS (քարտեզ)
        // =========================
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

        // 🧹 հին route մաքրում
        if (this.polyline) {
          this.map.removeLayer(this.polyline);
        }

        // 🔴 route
        this.polyline = L.polyline(points, {
          color: "red",
          weight: 2,
        }).addTo(this.map);

        // 📍 վերջին կետ
        const last = points[points.length - 1];

        if (this.marker) {
          this.map.removeLayer(this.marker);
        }

        this.marker = L.marker(last)
          .addTo(this.map)
          .bindPopup(`📍 Վերջին դիրք<br>${last[0]}, ${last[1]}`)
          .openPopup();

        this.map.fitBounds(this.polyline.getBounds());

        // =========================
        // 📊 SUMMARY (տվյալներ)
        // =========================
        // console.log("SUMMARY RAW:", summaryRes.data);

        // եթե array է
        this.summary = Array.isArray(summaryRes.data)
          ? summaryRes.data[0]
          : summaryRes.data;

        // console.log("SUMMARY:", this.summary);

      } catch (err) {
        console.error("GPS API ERROR:", err);
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

    });
  },

  methods: {
    formatHours(ms) {
      if (!ms) return "-";

        const totalSeconds = Math.floor(ms / 1000); // 🔥 սա է կարևոր

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