<template>
  <v-sheet v-if="showForm" class="mt-4 mb-8">
    <v-form v-model="formIsValid" ref="jobForm" @submit.prevent>
      <fieldset class="pa-4" style="border-radius: 10px;">
        <legend class="d-flex pr-2">
          <v-badge dot inline class="px-1"></v-badge>
          <p class="body-2 mb-0">Veuillez compléter votre profil</p>
        </legend>
        <v-row v-if="askForRole">
          <v-col cols="12" sm="7">
            <v-select
              label="Choisir votre fonction"
              v-model="job"
              :items="jobOptions"
              :rules="[validators.required]"
              solo
              hide-details="auto"
            ></v-select>
          </v-col>
          <v-col cols="12" sm="7" v-if="showOtherField" class="my-0">
            <v-text-field
              label="Ma fonction"
              :rules="[validators.required]"
              solo
              v-model="otherJobDescription"
              hide-details="auto"
            ></v-text-field>
          </v-col>
          <v-col>
            <v-btn color="primary" height="3.5em" @click="updateProfile">Valider</v-btn>
          </v-col>
        </v-row>
        <v-row v-else-if="askForSource">
          <v-col cols="12" sm="7">
            <v-select
              label="Comment avez-vous connu ma-cantine ?"
              v-model="source"
              :items="sourceOptions"
              :rules="[validators.required]"
              solo
              hide-details="auto"
            ></v-select>
          </v-col>
          <v-col cols="12" sm="7" v-if="showOtherSourceField" class="my-0">
            <v-text-field
              label="Autre endroit"
              :rules="[validators.required]"
              solo
              v-model="otherSourceDescription"
              hide-details="auto"
            ></v-text-field>
          </v-col>
          <v-col>
            <v-btn color="primary" height="3.5em" @click="updateProfile">Valider</v-btn>
          </v-col>
        </v-row>
      </fieldset>
    </v-form>
  </v-sheet>
</template>

<script>
import Constants from "@/constants"
import validators from "@/validators"

export default {
  data() {
    return {
      validators,
      formIsValid: true,
      job: undefined,
      otherJobDescription: undefined,
      jobOptions: Constants.Jobs,
      source: undefined,
      otherSourceField: undefined,
      sourceOptions: Constants.UserSources,
      otherSourceDescription: undefined,
    }
  },
  computed: {
    loggedUser() {
      return this.$store.state.loggedUser
    },
    askForRole() {
      return !this.loggedUser.job && this.canteenCount === 0
    },
    showOtherField() {
      return this.job === "OTHER"
    },
    askForSource() {
      return !(
        this.loggedUser.mtm_source ||
        this.loggedUser.mtm_campaign ||
        this.loggedUser.mtm_medium ||
        this.loggedUser.source
      )
    },
    showOtherSourceField() {
      return this.source === "OTHER"
    },
    showForm() {
      return this.askForRole || this.askForSource
    },
  },
  methods: {
    updateProfile() {
      this.$refs.jobForm.validate()
      if (!this.formIsValid) {
        this.$store.dispatch("notifyRequiredFieldsError")
        return
      }
      const updateJob = !!this.job
      let payload = updateJob ? { job: this.job } : { source: this.source }
      if (this.showOtherField) {
        payload.otherJobDescription = this.otherJobDescription
      } else if (this.showOtherSourceField) {
        payload.otherSourceDescription = this.otherSourceDescription
      }
      this.$store
        .dispatch("updateProfile", { payload })
        .then(() => {
          this.bypassLeaveWarning = true
          this.$store.dispatch("notify", {
            title: "Merci, votre réponse a été sauvegardée",
            message: "Vous pourrez la modifier depuis votre profil",
            status: "success",
          })
          this.$router.push({ name: "ManagementPage" })
        })
        .catch((e) => {
          this.$store.dispatch("notifyServerError", e)
        })
    },
  },
}
</script>
