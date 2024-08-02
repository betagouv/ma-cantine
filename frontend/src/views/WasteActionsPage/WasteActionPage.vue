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
      <v-row justify="center">
        <v-col cols="12" class="mt-7" sm="2">
          <v-row justify="end">Type d'action</v-row>
          <v-row justify="end">
            <DsfrTag :text="effort" class="mt-2 ml-2" :closeable="false" color="rgb(238, 238, 238)" :small="true" />
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
      effortItems: [
        {
          value: "SMALL",
          text: "Petit pas",
        },
        {
          value: "MEDIUM",
          text: "Moyen",
        },
        {
          value: "LARGE",
          text: "Grand projet",
        },
      ],
      wasteOriginItems: [
        {
          value: "PREP",
          text: "Préparation",
        },
        {
          value: "UNSERVED",
          text: "Non servi",
        },
        {
          value: "PLATE",
          text: "Retour assiette",
        },
      ],
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
    effort() {
      const effortLabel = this.effortItems.find((item) => item.value === this.wasteaction.effort).text
      return effortLabel ? effortLabel : "default"
    },
    wasteOrigins() {
      return this.wasteaction.waste_origin.map((wasteOriginId) => {
        const wasteOriginLabel = this.wasteOriginItems.find((item) => item.value === wasteOriginId).text
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
