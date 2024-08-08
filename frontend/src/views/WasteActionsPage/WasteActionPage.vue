<template>
  <div id="wasteaction-page">
    <div v-if="wasteAction">
      <BreadcrumbsNav :title="wasteAction.title" :links="[{ to: backLink }]" />
      <v-row>
        <img
          :src="
            wasteAction.lead_image
              ? wasteAction.lead_image.meta.download_url
              : '/static/images/wasteaction-default-image.jpg'
          "
          class="lead-image"
          alt=""
        />
      </v-row>
      <v-row>
        <v-col cols="12" class="d-flex flex-column align-end mt-8" sm="2">
          <p class="mb-2">Type d'action</p>
          <DsfrTag :text="effortLabel" :closeable="false" :small="true" :clickable="false" />
          <p class="text-right">
            <i>{{ effortDescription }}</i>
          </p>
          <p class="mt-12 mb-2">Origine du gaspillage</p>
          <DsfrTagGroup
            v-if="wasteOrigins.length"
            :tags="wasteOrigins"
            :closeable="false"
            :small="true"
            :clickable="false"
            class="justify-end"
          />
        </v-col>
        <v-col cols="12" class="pa-12 text-left mt-sm-n12 body-wrapper" sm="8">
          <h1>{{ wasteAction.title }}</h1>
          <p class="mt-12">{{ wasteAction.subtitle }}</p>
          <p v-html="wasteAction.description" class="mt-9"></p>
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
      wasteAction: null,
      backLink: { name: "WasteActionsHome" },
    }
  },
  props: {
    id: {
      required: true,
    },
  },
  methods: {
    setWasteAction(wasteAction) {
      this.wasteAction = wasteAction
      if (wasteAction) document.title = `${this.wasteAction.title} - ${this.$store.state.pageTitleSuffix}`
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
    effort() {
      return Constants.WasteActionEffortLevels.find((item) => item.value === this.wasteAction.effort)
    },
    effortLabel() {
      return this.effort?.text || "Inconnu"
    },
    effortDescription() {
      return this.effort?.description || ""
    },
    wasteOrigins() {
      return this.wasteAction.waste_origin.map((wasteOriginId) => {
        const wasteOriginLabel = Constants.WasteActionOrigins.find((item) => item.value === wasteOriginId)?.text
        return {
          id: wasteOriginId,
          text: wasteOriginLabel ? wasteOriginLabel : "Inconnu",
        }
      })
    },
  },
  mounted() {
    this.fetchWasteAction()
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
