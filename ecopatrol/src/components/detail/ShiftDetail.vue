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
          <div>Սկիզբ: {{ shift_info?.start_shift }}</div>
        </div>
      </div>
      <div class="column">
        <div class="field">
          <div>Ավարտ: {{ shift_info?.end_shift }}</div>
        </div>
      </div>
      <div class="column">
        <div class="field">
          <div>Մեքենայի պետհամարանիշ: {{ shift_info?.car_number }}</div>
        </div>
      </div>
      <div class="column">
        <div class="field">
          <div>Մեքենայի կողային համարանիշ {{ shift_info?.board_number }}</div>
        </div>
      </div>
    </div>

    <div class="columns">
      <div class="column">
        <div class="field">
          <div>Անուն: {{ shift_info?.employee_01_name }}</div>
        </div>
      </div>
      <div class="column">
        <div class="field">
          <div>Ազգանուն: {{ shift_info?.employee_01_surname }}</div>
        </div>
      </div>
      <div class="column">
        <div class="field">
          <div>Պաշտոն: {{ shift_info?.employee_01_position_held }}</div>
        </div>
      </div>
      <div class="column">
        <div class="field">
          <div>Հեռ.: {{ shift_info?.employee_01_phone }}</div>
        </div>
      </div>
      <div class="column">
        <div class="field">
          <div>Տեսախցիկ: {{ shift_info?.employee_01_camera }}</div>
        </div>
      </div>
    </div>
    <div class="columns">
      <div class="column">
        <div class="field">
          <div>Անուն: {{ shift_info?.employee_02_name }}</div>
        </div>
      </div>
      <div class="column">
        <div class="field">
          <div>Ազգանուն: {{ shift_info?.employee_02_surname }}</div>
        </div>
      </div>
      <div class="column">
        <div class="field">
          <div>Պաշտոն: {{ shift_info?.employee_02_position_held }}</div>
        </div>
      </div>
      <div class="column">
        <div class="field">
          <div>Հեռ.: {{ shift_info?.employee_02_phone }}</div>
        </div>
      </div>
      <div class="column">
        <div class="field">
          <div>Տեսախցիկ: {{ shift_info?.employee_02_camera }}</div>
        </div>
      </div>
    </div>
    <div class="columns" v-if="shift_info?.employee_03_name !== null">
      <div class="column">
        <div class="field">
          <div>Անուն: {{ shift_info?.employee_03_name }}</div>
        </div>
      </div>
      <div class="column">
        <div class="field">
          <div>Ազգանուն: {{ shift_info?.employee_03_surname }}</div>
        </div>
      </div>
      <div class="column">
        <div class="field">
          <div>Պաշտոն: {{ shift_info?.employee_03_position_held }}</div>
        </div>
      </div>
      <div class="column">
        <div class="field">
          <div>Հեռ.: {{ shift_info?.employee_03_phone }}</div>
        </div>
      </div>
      <div class="column">
        <div class="field">
          <div>Տեսախցիկ: {{ shift_info?.employee_03_camera }}</div>
        </div>
      </div>
    </div>
    <div class="columns" v-if="shift_info?.employee_04_name !== null">
      <div class="column">
        <div class="field">
          <div>Անուն: {{ shift_info?.employee_04_name }}</div>
        </div>
      </div>
      <div class="column">
        <div class="field">
          <div>Ազգանուն: {{ shift_info?.employee_04_surname }}</div>
        </div>
      </div>
      <div class="column">
        <div class="field">
          <div>Պաշտոն: {{ shift_info?.employee_04_position_held }}</div>
        </div>
      </div>
      <div class="column">
        <div class="field">
          <div>Հեռ.: {{ shift_info?.employee_04_phone }}</div>
        </div>
      </div>
      <div class="column">
        <div class="field">
          <div>Տեսախցիկ: {{ shift_info?.employee_04_camera }}</div>
        </div>
      </div>
    </div>
    <div class="columns">
      <div class="column" style="display: flex; align-items: flex-end;">
        <button class="button is-primary" @click="goToCoordinate">Հերթափոխի գտնվելու վայրը</button>
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
      lat: null,       // latitude input
      lng: null,       // longitude input
      map: null,       // store map instance
      marker: null,    // store marker instance
    };
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
    });
  },
  methods: {
    async goToCoordinate() {
      try {
        const TOKEN = "RzBFAiA5UB9KYvQkmg9kRf1crNeXR7kmTsKY9KFBN03to_0K_gIhALBskv28tPHdwY47wVWS-M_9LkdIFsETEuzAP1JrmSS1eyJ1IjoyLCJlIjoiMjAyNi0wNC0wNVQyMDowMDowMC4wMDArMDA6MDAifQ";

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

        console.log("GPS DATA:", res.data);

        if (res.data.length > 0) {
          const last = res.data[0];

          const lat = last.latitude;
          const lng = last.longitude;

          console.log("COORD:", lat, lng);

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
            .bindPopup(`📍 ${lat}, ${lng}`)
            .openPopup();

          this.map.flyTo(latLng, 14); 
        }

      } catch (err) {
        console.error("GPS API ERROR:", err);
      }
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