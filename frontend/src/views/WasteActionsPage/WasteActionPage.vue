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
          <!-- Implement action buttons -->
          <p class="mb-2">Mis en place</p>
          <DsfrTagGroup
            v-if="canteensDoneAction && canteensDoneAction.length"
            :tags="canteensDoneAction"
            :closeable="false"
            :small="true"
            :clickable="false"
          />
          <p v-else>
            <i>Aucune cantine</i>
          </p>
          <br />
          <v-btn small color="primary" @click="showActionModal">
            <span class="mx-2">
              Modifier
            </span>
          </v-btn>
        </v-col>
      </v-row>
      <v-row class="mt-9">
        <BackLink :to="backLink" text="Retour" :primary="true" />
      </v-row>

      <v-dialog v-model="showModal">
        <v-card class="pa-6">
          <div class="mt-n6 mx-n6 mb-4 pa-4 d-flex" style="background-color: #F5F5F5">
            <v-spacer></v-spacer>
            <v-btn outlined color="primary" @click="showModal = false">
              Fermer
            </v-btn>
          </div>

          <h2 id="modal-title" class="mb-3" tabindex="-1">Mis en place ?</h2>

          <v-form ref="form" v-model="actionFormIsValid" @submit.prevent>
            <DsfrAutocomplete
              v-model="chosenCanteenIds"
              :items="userCanteens"
              clearable
              multiple
              hide-details
              id="select-canteen"
              placeholder="Toutes mes cantines"
              class="mt-1"
              no-data-text="Pas de résultats"
              item-text="name"
              item-value="id"
            />
            <v-row class="mt-2 pa-4">
              <v-spacer></v-spacer>
              <v-btn x-large color="primary" @click="saveActionChanges">Valider</v-btn>
            </v-row>
          </v-form>
        </v-card>
      </v-dialog>
    </div>
  </div>
</template>
<script>
import DsfrAutocomplete from "@/components/DsfrAutocomplete"
import BreadcrumbsNav from "@/components/BreadcrumbsNav.vue"
import BackLink from "@/components/BackLink"
import DsfrTagGroup from "@/components/DsfrTagGroup"
import DsfrTag from "@/components/DsfrTag"
import Constants from "@/constants"

export default {
  components: { DsfrAutocomplete, BreadcrumbsNav, BackLink, DsfrTagGroup, DsfrTag },
  data() {
    return {
      wasteAction: null,
      actionModal: false,
      actionFormIsValid: true,
      chosenCanteenIds: [],
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
    createOrUpdateResourceAction(canteenId, is_done = true) {
      return this.$store
        .dispatch("createOrUpdateResourceAction", {
          resourceId: this.id,
          payload: { canteenId, is_done },
        })
        .catch((e) => this.$store.dispatch("notifyServerError", e))
    },
    showActionModal() {
      // Get the canteens that have already done the action
      this.chosenCanteenIds = this.userCanteens
        .filter((canteen) => this.actionsDone.find((actionCanteen) => actionCanteen.id === canteen.id))
        .map((canteen) => canteen.id)
      this.actionModal = true
    },
    saveActionChanges() {
      const actionChanges = []
      // Compare the chosen canteens with the actions done (new & removed)
      this.chosenCanteenIds.forEach((canteenId) => {
        if (!this.actionsDone.find((actionCanteen) => actionCanteen.id === canteenId)) {
          actionChanges.push(this.createOrUpdateResourceAction(canteenId, true))
        }
      })
      this.actionsDone.forEach((actionCanteen) => {
        if (!this.chosenCanteenIds.includes(actionCanteen.id)) {
          actionChanges.push(this.createOrUpdateResourceAction(actionCanteen.id, false))
        }
      })
      // close modal and refresh the wasteAction if needed
      if (actionChanges.length) {
        Promise.all(actionChanges).then(() => {
          this.fetchWasteAction()
          this.actionModal = false
        })
      } else {
        this.actionModal = false
      }
    },
  },
  computed: {
    loggedUser() {
      return this.$store.state.loggedUser
    },
    userCanteens() {
      if (!this.loggedUser) return []
      return this.$store.state.userCanteenPreviews
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
    canteensDoneAction() {
      return this.wasteAction?.canteenActions
        ?.filter((canteenAction) => canteenAction.isDone)
        .map((canteenAction) => ({ id: canteenAction.canteen.id, text: canteenAction.canteen.name }))
    },
    showModal: {
      get() {
        return !!this.actionModal
      },
      set(newValue) {
        if (!newValue) this.actionModal = null
      },
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
