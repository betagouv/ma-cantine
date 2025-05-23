<template>
  <div id="wasteaction-page">
    <div v-if="wasteAction">
      <BreadcrumbsNav :title="wasteAction.title" :links="[{ to: backLink }]" />
      <v-row>
        <img
          :src="wasteAction.leadImage ? wasteAction.leadImage.image : '/static/images/wasteaction-default-image.jpg'"
          class="lead-image"
          alt=""
        />
      </v-row>
      <v-row>
        <v-col cols="12" class="d-flex flex-column align-end mt-8" sm="2">
          <p class="mb-2">Type d'action</p>
          <DsfrTag :text="effort.text" :icon="effort.icon" :closeable="false" :small="true" :clickable="false" />
          <p class="text-right">
            <i>{{ effort.description }}</i>
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
        <v-col v-if="loggedUser" cols="12" class="d-flex flex-column align-start mt-8" sm="2">
          <p class="mb-2">Mis en place</p>
          <DsfrTagGroup
            v-if="canteensActionDone.length"
            class="mb-2"
            :tags="canteensActionDone"
            :closeable="false"
            :small="true"
            :clickable="false"
          />
          <p v-else class="mb-2">
            <i>Aucune cantine</i>
          </p>
          <v-btn small color="primary" @click="showActionDialog">
            <span class="mx-2">
              <span v-if="!canteensActionDone.length">J'ai mis en place cette action</span>
              <span v-else-if="userCanteens.length > 1">Modifier</span>
              <span v-else>Retirer</span>
            </span>
          </v-btn>
        </v-col>
      </v-row>
      <v-row class="mt-9">
        <BackLink :to="backLink" text="Retour" :primary="true" />
      </v-row>
      <ResourceActionDialog
        v-model="actionDialog"
        :resourceId="id"
        :userCanteens="userCanteens"
        :canteensActionDone="canteensActionDone"
        @close="closeActionDialog($event)"
      />
    </div>
  </div>
</template>

<script>
import BreadcrumbsNav from "@/components/BreadcrumbsNav.vue"
import BackLink from "@/components/BackLink"
import DsfrTagGroup from "@/components/DsfrTagGroup"
import DsfrTag from "@/components/DsfrTag"
import ResourceActionDialog from "./ResourceActionDialog"
import Constants from "@/constants"
import { normaliseText } from "@/utils"

export default {
  components: { BreadcrumbsNav, BackLink, DsfrTagGroup, DsfrTag, ResourceActionDialog },
  data() {
    return {
      wasteAction: null,
      actionDialog: false,
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
      const headers = {
        "X-CSRFToken": window.CSRF_TOKEN || "",
        "Content-Type": "application/json",
      }
      return fetch(`/api/v1/wasteActions/${this.id}`, { headers })
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
    showActionDialog() {
      this.actionDialog = true
    },
    closeActionDialog(refresh) {
      if (refresh) this.fetchWasteAction()
      this.actionDialog = false
    },
  },
  computed: {
    loggedUser() {
      return this.$store.state.loggedUser
    },
    userCanteens() {
      if (!this.loggedUser) return []
      const canteens = this.$store.state.userCanteenPreviews
      return canteens.sort((a, b) => {
        return normaliseText(a.name) > normaliseText(b.name) ? 1 : 0
      })
    },
    effort() {
      return (
        Constants.WasteActionEffortLevels.find((item) => item.value === this.wasteAction.effort) || {
          text: "Inconnu",
          icon: "",
          description: "",
        }
      )
    },
    wasteOrigins() {
      return this.wasteAction.wasteOrigins.map((wasteOriginId) => {
        const wasteOrigin = Constants.WasteActionOrigins.find((item) => item.value === wasteOriginId)
        return {
          id: wasteOriginId,
          text: wasteOrigin?.text || "Inconnu",
          icon: wasteOrigin?.icon,
        }
      })
    },
    canteensActionDone() {
      if (!this.wasteAction?.canteenActions) return []
      return this.wasteAction?.canteenActions
        ?.filter((canteenAction) => canteenAction.isDone)
        .map((canteenAction) => ({ id: canteenAction.canteen.id, text: canteenAction.canteen.name }))
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
