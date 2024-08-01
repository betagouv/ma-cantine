<template>
  <div id="wasteaction-page">
    <div v-if="wasteaction">
      <BreadcrumbsNav :title="wasteaction.title" :links="[{ to: { name: 'WasteActionsHome' } }]" />
      <v-row>
        <img
          :src="wasteaction.lead_image ? wasteaction.lead_image.url : '/static/images/wasteaction-default-image.png'"
          class="lead-image"
          alt=""
        />
      </v-row>
      <v-row justify="center">
        <v-col cols="12" class="mt-7" sm="2">
          <v-row justify="end">Type d'action</v-row>
          <v-row justify="end">
            <DsfrTag
              :text="wasteaction.effort"
              class="mt-2 ml-2"
              :closeable="false"
              color="rgb(238, 238, 238)"
              :small="true"
            />
          </v-row>
          <v-row justify="end">Origine du gaspillage</v-row>
          <v-row justify="end">
            <DsfrTagGroup
              v-if="wasteaction.waste_origin.length"
              :tags="wasteOrigins"
              :closeable="false"
              :small="true"
            />
          </v-row>
        </v-col>
        <v-col cols="12" class="pa-12 text-left mt-sm-n12 body-wrapper" sm="7">
          <h1>{{ wasteaction.title }}</h1>
          <p>{{ wasteaction.subtitle }}</p>
          <p v-html="wasteaction.description"></p>
        </v-col>
        <v-col cols="12" v-bind:class="{ 'mt-7': $vuetify.breakpoint.smAndUp }" sm="2">
          <!-- Implement action buttons -->
        </v-col>
      </v-row>
    </div>
    <BackLink :to="backLink" text="Retour à la liste des actions" :primary="true" class="my-10 d-block" />
  </div>
</template>
<script>
import BreadcrumbsNav from "@/components/BreadcrumbsNav.vue"
import BackLink from "@/components/BackLink"
import DsfrTagGroup from "@/components/DsfrTagGroup"
import DsfrTag from "@/components/DsfrTag"

export default {
  components: { BreadcrumbsNav, BackLink, DsfrTagGroup, DsfrTag },
  data() {
    return {
      wasteaction: null,
      backLink: { name: "WasteActionsHome" },
    }
  },
  props: {
    id: {
      required: true,
    },
  },
  methods: {
    fetchWasteAction() {
      return fetch(`/apicms/v1/wasteactions/${this.id}/?fields=*`)
        .then((response) => {
          if (response.status !== 200) throw new Error()
          response.json().then((x) => (this.wasteaction = x))
        })
        .catch(() => {
          this.$router.push({ name: "WasteActionsHome" }).then(() => {
            this.$store.dispatch("notify", {
              message: "Nous n'avons pas trouvé cet article",
              status: "error",
            })
          })
        })
    },
  },
  computed: {
    wasteOrigins() {
      return this.wasteaction.waste_origin.map((tag) => {
        return {
          id: tag,
          text: tag,
          color: "rgb(238, 238, 238)",
        }
      })
    },
  },
  mounted() {
    this.fetchWasteAction()
  },
  beforeRouteEnter(to, from, next) {
    next((vm) => {
      if (from.name == "WasteActionsHome") {
        vm.backLink = from
      }
    })
  },
}
</script>
<style scoped>
.lead-image {
  width: 100%;
  height: 425px;
  object-fit: cover;
}
.body-wrapper {
  background-color: white;
  z-index: 1;
}
</style>
