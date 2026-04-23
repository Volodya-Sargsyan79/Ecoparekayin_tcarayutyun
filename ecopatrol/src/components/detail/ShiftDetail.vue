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
      previewType: null
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
        const TOKEN = "RjBEAiBNqznm3YuIuUodgC_Ur-hJ-hwKUbCxYA_WUYaUPjUZRAIgMVHw66rraqKVJ0mhB3EEKToZrZr_4Hm5GsUt2KhZZix7InUiOjIsImUiOiIyMDI2LTA0LTI3VDIwOjAwOjAwLjAwMCswMDowMCJ9";

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
  methods: {
    formatSpeed(value, type = "knots") {
      if (!value) return "0 կմ/ժ";

        let kmh;

        if (type === "knots") kmh = value * 1.852;
        else if (type === "ms") kmh = value * 3.6;
        else kmh = value;

        return `${kmh.toFixed(2)} կմ/ժ`;
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