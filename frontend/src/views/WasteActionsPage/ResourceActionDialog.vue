<template>
  <v-dialog v-model="isOpen" max-width="500px">
    <v-card class="pa-6">
      <div class="mt-n6 mx-n6 mb-4 pa-4 d-flex" style="background-color: #F5F5F5">
        <v-spacer></v-spacer>
        <v-btn outlined color="primary" @click="$emit('close')">
          Annuler
        </v-btn>
      </div>

      <h2 class="mb-3">Mis en place ?</h2>

      <v-form ref="form" @submit.prevent>
        <DsfrAutocomplete
          v-model="chosenCanteenIds"
          :items="userCanteens"
          clearable
          multiple
          hide-details
          id="select-canteen"
          placeholder="Choisissez les établissements"
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
</template>

<script>
import DsfrAutocomplete from "@/components/DsfrAutocomplete"

export default {
  name: "ResourceActionDialog",
  components: { DsfrAutocomplete },
  props: {
    value: {
      type: Boolean,
      required: true,
    },
    resourceId: {
      required: true,
    },
    userCanteens: {
      type: Array,
      required: true,
    },
    canteensActionDone: {
      type: Array,
      required: true,
      // example: [{ id: 1, name: "Cantine 1" }],
    },
  },
  data() {
    return {
      chosenCanteenIds: [],
    }
  },
  mounted() {
    // Pre-select the canteens that have already done the action
    this.chosenCanteenIds = this.userCanteens
      .filter((canteen) => this.canteensActionDone.find((canteenActionDone) => canteenActionDone.id === canteen.id))
      .map((canteen) => canteen.id)
  },
  computed: {
    isOpen: {
      get() {
        return this.value
      },
      set(newValue) {
        this.$emit("input", newValue)
      },
    },
  },
  methods: {
    createOrUpdateResourceAction(canteenId, isDone) {
      return this.$store
        .dispatch("createOrUpdateResourceAction", {
          resourceId: this.resourceId,
          payload: { canteenId, isDone },
        })
        .catch((e) => this.$store.dispatch("notifyServerError", e))
    },
    saveActionChanges() {
      const actionChanges = []
      // Compare the chosen canteens with the actions done (new & removed)
      this.chosenCanteenIds.forEach((canteenId) => {
        if (!this.canteensActionDone.find((canteenActionDone) => canteenActionDone.id === canteenId)) {
          actionChanges.push(this.createOrUpdateResourceAction(canteenId, true))
        }
      })
      this.canteensActionDone.forEach((canteenActionDone) => {
        if (!this.chosenCanteenIds.includes(canteenActionDone.id)) {
          actionChanges.push(this.createOrUpdateResourceAction(canteenActionDone.id, false))
        }
      })
      // close dialog and refresh the wasteAction if needed
      if (actionChanges.length) {
        Promise.all(actionChanges).then(() => {
          this.$emit("close", true)
        })
      } else {
        this.$emit("close")
      }
    },
  },
}
</script>
