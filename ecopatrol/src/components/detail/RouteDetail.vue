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
          <div>{{ map_info?.region }}</div>
        </div>
      </div>
      <div class="column">
        <div class="field">
          <div>{{ map_info?.precinct }}</div>
        </div>
      </div>
      <div class="column">
        <div class="field">
          <div>Երթուղի {{ map_info?.route_number }}</div>
        </div>
      </div>
      <div class="column">
        <div class="field">
          <div>Երթուղու երկարություն {{ map_info?.route_length }} կմ</div>
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

delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: markerIcon2x,
  iconUrl: markerIcon,
  shadowUrl: markerShadow,
});

export default {
  name: "RouteDetail",
  data() {
    return {
      map_info: null
    }
  },

  async mounted() {
    this.$nextTick(async () => {
      try {
        const id = this.$route.params.id;

        const res = await axios.get(
          `/api/ekopatrol/routes/${id}/`
        );

        this.map_info = res.data;

        const kmlUrl = `http://${window.location.hostname}:8000/media/kml/${id}/doc.kml`;
        // const kmlUrl = `http://127.0.0.1:8000/media/kml/${id}/doc.kml`;

        const map = L.map("map").setView([40.1792, 44.4991], 10);

        L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
          maxZoom: 30,
          attribution: "© OpenStreetMap contributors"
        }).addTo(map);

        omnivore
          .kml(kmlUrl)
          .on("ready", function () {
            map.fitBounds(this.getBounds());
          })
          .on("error", function (e) {
            console.error("KML LOAD ERROR:", e);
          })
          .addTo(map);

        setTimeout(() => {
          map.invalidateSize();
        }, 500);

      } catch (err) {
        console.error("ERROR:", err);
      }
    });
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