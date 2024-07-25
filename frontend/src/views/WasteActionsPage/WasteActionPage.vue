<template>
  <div id="wasteaction-page">
    <div v-if="wasteaction">
      <BreadcrumbsNav :title="wasteaction.title" :links="[{ to: { name: 'WasteActionsHome' } }]" />
      <v-row v-if="wasteaction.lead_image">
        <v-img
          :src="wasteaction.lead_image.meta.download_url"
          class="lead-image"
          alt="wasteaction.lead_image.title"
          cover
          max-height="200"
        ></v-img>
      </v-row>
      <v-row>
        <v-col cols="12" class="mt-7" sm="3">
          <v-row>Origine du gaspillage</v-row>
          <v-row>
            <DsfrTagGroup
              v-if="wasteaction.waste_origin.length"
              :tags="wasteOrigins"
              :closeable="false"
              :small="true"
            />
          </v-row>
          <v-row>Type d'action</v-row>
          <v-row>
            <DsfrBadge :mode="wasteaction.effort == 'SMALL' ? 'SUCCESS' : 'ERROR'" class="mt-2 ml-2">
              {{ wasteaction.effort }}
            </DsfrBadge>
          </v-row>
          <v-row>
            <i>Description du type d'action à ajouter</i>
          </v-row>
        </v-col>
        <v-col
          cols="12"
          v-bind:class="{ 'text-left': true, 'negative-margin': $vuetify.breakpoint.smAndUp && wasteaction.lead_image }"
          sm="6"
        >
          <h1>{{ wasteaction.title }}</h1>
          <p>{{ wasteaction.subtitle }}</p>
          <p v-html="wasteaction.description"></p>
        </v-col>
        <v-col cols="12" class="text-left mt-7" sm="3">
          <v-row class="mb-1">
            <v-btn color="primary" outlined>
              <v-icon small class="mr-2">$bookmark-line</v-icon>
              Ajouter aux favoris
            </v-btn>
          </v-row>
          <v-row>
            <v-btn color="primary">
              J'ai mis en place cette action
            </v-btn>
          </v-row>
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
import DsfrBadge from "@/components/DsfrBadge"

export default {
  components: { BreadcrumbsNav, BackLink, DsfrTagGroup, DsfrBadge },
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
<style>
.lead-image {
  opacity: 1;
  max-height: 100%;
  max-width: 100%;
  height: 100%;
  width: 100%;
  object-fit: cover;
  filter: brightness(90%);
}
.negative-margin {
  margin-top: -50px;
  background-color: white;
  z-index: 1;
}
</style>
