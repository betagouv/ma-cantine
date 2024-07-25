<template>
  <div id="wasteactions-home">
    <div v-if="loading" class="mt-8">
      <v-progress-circular inderterminate></v-progress-circular>
    </div>
    <div v-if="!loading && wasteactions.length > 0">
      <h1>Explorez et mettez en avant vos actions de lutte contre le gaspillage</h1>
      <v-row class="cta-group pa-2 mt-2">
        <v-col vols="12" sm="6" md="4" v-for="wasteaction in wasteactions" :key="wasteaction.id">
          <WasteActionCard :wasteaction="wasteaction" />
        </v-col>
      </v-row>
    </div>
  </div>
</template>
<script>
import WasteActionCard from "./WasteActionCard.vue"
export default {
  name: "WasteActionsHome",
  components: { WasteActionCard },
  data() {
    return {
      offset: 0,
      tag: null,
      searchTerm: null,
      wasteactions: [],
    }
  },
  computed: {
    loading() {
      return this.wasteactions === null
    },
  },
  methods: {
    fetchCurrentPage() {
      this.$store
        .dispatch("fetchWasteActions", { offset: this.offset, tag: this.tag, search: this.searchTerm })
        .then((response) => {
          this.wasteactions = response.items
        })
        .catch(() => {
          this.$store.dispatch("notifyServerError")
        })
    },
  },
  mounted() {
    this.fetchCurrentPage()
  },
}
</script>
