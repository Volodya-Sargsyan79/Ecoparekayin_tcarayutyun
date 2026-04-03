<template>
  <div class="box">
    <div class="columns">
      <div class="column is-3">
        <div class="field">
            <!-- <img 
              :src="`http://${$hostname}:8000/media/${person.image}`" 
            /> -->
            <img 
              :src="`http://127.0.0.1:8000/media/${person.image}`" 
            />
        </div>
      </div>
      <div class="column is-9">
        <div class="field">
          <div>
           <h1 class="title is-4">{{ person?.name }} {{ person?.surname }}</h1>
          </div>
        </div>  
        <div class="field">
          <p><samp class="title is-6">Հեռ.:</samp> {{ person?.phone }}</p>
          <p><samp class="title is-6">Ծնդ.:</samp> {{ person?.birth_day }}</p>
          <p><samp class="title is-6">Անձնագիր:</samp> {{ person?.passport }}</p>
          <p><samp class="title is-6">Բնակության վայր:</samp> {{ person?.residential_address }}</p>
        </div>
        <div class="field">
          <p><samp class="title is-6">Մարզային վարչություն:</samp> {{ person?.region }}</p>
          <p><samp class="title is-6">Տեղամաս:</samp> {{ person?.precinct }}</p>
          <p><samp class="title is-6">Պաշտոն:</samp> {{ person?.position_held }}</p>
          <p><samp class="title is-6">Ընդուման հրամանի ամսաթիվ:</samp> {{ person?.order_day }}</p>
          <p><samp class="title is-6">Վկայականի համար:</samp> {{ person?.service_number }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "PersonDetail",
  data() {
    return {
      person: {}
    }
  },

  async mounted() {
    this.$nextTick(async () => {
      try {
        const id = this.$route.params.id;

        const res = await axios.get(
          `/api/ekopatrol/getemployee/${id}/`
        );

        this.person = res.data[0];

      } catch (err) {
        console.error("ERROR:", err);
      }
    });
  },
};
</script>

<style>

</style>