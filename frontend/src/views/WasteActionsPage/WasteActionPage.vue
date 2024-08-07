<template>
  <div id="wasteaction-page">
    <div v-if="wasteaction">
      <BreadcrumbsNav :title="wasteaction.title" :links="[{ to: { name: 'WasteActionsHome' } }]" />
      <v-row>
        <img
          :src="
            wasteaction.lead_image
              ? wasteaction.lead_image.meta.download_url
              : '/static/images/wasteaction-default-image.jpg'
          "
          class="lead-image"
          alt=""
        />
      </v-row>
      <v-row>
        <v-col cols="12" class="mt-8" sm="2">
          <v-row justify="end">Type d'action</v-row>
          <v-row justify="end">
            <DsfrTag :text="effortLabel" :closeable="false" color="rgb(238, 238, 238)" :small="true" />
          </v-row>
          <v-row justify="end">
            <p class="text-right">
              <i>{{ effortDescription }}</i>
            </p>
          </v-row>
          <v-row justify="end" class="mt-12">Origine du gaspillage</v-row>
          <v-row justify="end">
            <DsfrTagGroup
              v-if="wasteaction.waste_origin.length"
              :tags="wasteOrigins"
              :closeable="false"
              :small="true"
              class="flex-row-reverse"
            />
          </v-row>
        </v-col>
        <v-col cols="12" class="pa-12 text-left mt-sm-n12 body-wrapper" sm="7">
          <h1>{{ wasteaction.title }}</h1>
          <p class="mt-12">{{ wasteaction.subtitle }}</p>
          <p v-html="wasteaction.description" class="mt-9"></p>
        </v-col>
        <v-col cols="12" v-bind:class="{ 'mt-7': $vuetify.breakpoint.smAndUp }" sm="2">
          <!-- Implement action buttons -->
        </v-col>
      </v-row>
      <v-row class="mt-9">
        <BackLink :to="backLink" text="Retour" :primary="true" />
      </v-row>
    </div>
  </div>
</template>
<script>
import BreadcrumbsNav from "@/components/BreadcrumbsNav.vue"
import BackLink from "@/components/BackLink"
import DsfrTagGroup from "@/components/DsfrTagGroup"
import DsfrTag from "@/components/DsfrTag"
import Constants from "@/constants"

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
    setWasteAction(wasteaction) {
      this.wasteaction = wasteaction
      if (wasteaction) document.title = `${this.wasteaction.title} - ${this.$store.state.pageTitleSuffix}`
    },
    fetchWasteAction() {
      return fetch(`/apicms/v1/wasteactions/${this.id}/?fields=*`)
        .then((response) => {
          if (response.status !== 200) throw new Error()
          response.json().then((x) => this.setWasteAction(x))
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
    effortLabel() {
      const effortLabel = Constants.WasteActionEffortLevels.find((item) => item.value === this.wasteaction.effort).text
      return effortLabel ? effortLabel : "default"
    },
    effortDescription() {
      const effortDescription = Constants.WasteActionEffortLevels.find((item) => item.value === this.wasteaction.effort)
        .description
      return effortDescription ? effortDescription : ""
    },
    wasteOrigins() {
      return this.wasteaction.waste_origin.map((wasteOriginId) => {
        const wasteOriginLabel = Constants.WasteActionOrigins.find((item) => item.value === wasteOriginId).text
        return {
          id: wasteOriginId,
          text: wasteOriginLabel ? wasteOriginLabel : "default",
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
