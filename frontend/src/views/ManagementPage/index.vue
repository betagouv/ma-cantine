<template>
  <div class="text-left">
    <div class="mt-4">
      <p class="my-2 text-body-1 font-weight-bold">
        Bienvenue {{ loggedUser.firstName }}
        <v-btn text class="text-decoration-underline text-caption mb-1" :to="{ name: 'AccountEditor' }">
          <v-icon class="mr-1" small>mdi-pencil</v-icon>
          Modifier mon profil
        </v-btn>
      </p>
    </div>
    <v-sheet v-if="askForRole" class="mt-4 mb-8">
      <v-form v-model="jobFormIsValid" ref="jobForm" @submit.prevent>
        <fieldset class="pa-4" style="border-radius: 10px;">
          <legend class="d-flex pr-2">
            <v-badge dot inline class="px-1"></v-badge>
            <p class="body-2 mb-0">Veuillez compléter votre profil</p>
          </legend>
          <v-row>
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
              <v-btn color="primary" height="3.5em" @click="updateRole">Valider</v-btn>
            </v-col>
          </v-row>
        </fieldset>
      </v-form>
    </v-sheet>
    <div class="mt-4">
      <h1 class="my-4 text-h5 font-weight-black">Mes cantines</h1>
      <CanteensPagination v-on:canteen-count="canteenCount = $event" />
    </div>
    <div class="mt-12 mb-8">
      <h2 class="text-h5 font-weight-black mb-4">Mes outils</h2>
      <UserTools />
    </div>
  </div>
</template>

<script>
import CanteensPagination from "./CanteensPagination.vue"
import UserTools from "./UserTools"
import validators from "@/validators"
import Constants from "@/constants"

export default {
  components: { CanteensPagination, UserTools },
  data() {
    return {
      validators,
      job: undefined,
      otherJobDescription: undefined,
      jobOptions: Constants.Jobs,
      jobFormIsValid: true,
      canteenCount: undefined,
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
  },
  methods: {
    updateRole() {
      this.$refs.jobForm.validate()
      if (!this.jobFormIsValid) {
        this.$store.dispatch("notifyRequiredFieldsError")
        return
      }
      let payload = { job: this.job }
      if (this.showOtherField) {
        payload.otherJobDescription = this.otherJobDescription
      }
      this.$store
        .dispatch("updateProfile", { payload })
        .then(() => {
          this.bypassLeaveWarning = true
          this.$store.dispatch("notify", {
            title: "Merci, votre fonction a été sauvegardé",
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
