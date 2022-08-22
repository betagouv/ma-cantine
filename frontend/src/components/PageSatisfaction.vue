<template>
  <v-card class="py-6 px-8 mx-auto box text-center" elevation="0" color="primary lighten-5" v-if="askForRating">
    <label class="body-2 grey--text text--darken-4" for="page-rating">
      Êtes-vous satisfait de la plateforme « ma cantine » ?
    </label>
    <v-rating
      v-model.number="rating"
      color="primary"
      empty-icon="$star-line"
      full-icon="$star-fill"
      class="mt-2 body-2"
      id="page-rating"
      background-color="grey darken-1"
      length="5"
      hover
    ></v-rating>

    <v-dialog v-model="dialog" width="500">
      <v-card class="text-left pa-4">
        <v-card-title class="font-weight-black">
          Faire une suggestion
        </v-card-title>

        <v-card-text>
          <v-form ref="form" v-model="formIsValid">
            <label class="body-2 grey--text text--darken-4" for="dialog-rating">
              Êtes-vous satisfait de la plateforme « ma cantine » ?
            </label>
            <v-rating
              v-model.number="rating"
              color="primary"
              empty-icon="$star-line"
              full-icon="$star-fill"
              class="mt-2 mb-4 body-2"
              id="dialog-rating"
              background-color="grey"
              length="5"
              hover
            ></v-rating>
            <label class="body-2 grey--text text--darken-3" for="suggestion">
              Que pouvons-nous améliorer afin de mieux répondre à vos attentes ?
            </label>
            <DsfrTextarea v-model="suggestion" id="suggestion" hide-details="auto" class="mt-2 mb-4 body-2" rows="5" />
            <p class="caption mb-0">
              Notre équipe pourrait être amenée à prendre contact avec vous afin d'échanger sur vos besoins.
            </p>
          </v-form>
        </v-card-text>

        <v-divider></v-divider>

        <v-card-actions class="mt-2 mb-n2">
          <v-spacer></v-spacer>
          <v-btn @click="cancel" x-large outlined color="primary" class="mr-4">
            Annuler
          </v-btn>
          <v-btn color="primary" @click="submitSuggestion" x-large>
            Valider
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-card>
</template>

<script>
import validators from "@/validators"
import DsfrTextarea from "@/components/DsfrTextarea"

export default {
  name: "PageSatisfaction",
  components: { DsfrTextarea },
  data() {
    return {
      dialog: false,
      validators,
      formIsValid: true,
      rating: null,
      suggestion: null,
      email: null,
      page: this.$route.name,
    }
  },
  computed: {
    askForRating() {
      const user = this.$store.state.loggedUser
      const hasCanteen = user.reviews.some((review) => review.hasCanteen)
      const hasDiagnostic = user.reviews.some((review) => review.hasDiagnostic)
      return this.page === "DiagnosticList" ? !hasDiagnostic : !hasCanteen || !hasDiagnostic
    },
  },
  methods: {
    submitSuggestion() {
      this.$refs.form.validate()
      if (!this.formIsValid) {
        this.$store.dispatch("notifyRequiredFieldsError")
        return
      }

      const payload = {
        rating: this.rating,
        suggestion: this.suggestion,
        page: this.page,
      }
      this.$store
        .dispatch("createReview", { payload })
        .then(() => {
          this.$store.dispatch("notify", {
            title: "Merci, votre évaluation a bien été prise en compte",
            status: "success",
          })
          this.dialog = false
        })
        .catch((e) => {
          this.$store.dispatch("notifyServerError", e)
        })
    },
    cancel() {
      this.$refs.form.reset()
      this.dialog = false
    },
  },
  watch: {
    rating(newValue) {
      if (newValue) {
        this.dialog = true
      }
    },
    dialog(newValue) {
      if (newValue === false) {
        this.rating = null
      }
    },
  },
}
</script>

<style lang="scss" scoped>
.box {
  width: fit-content;
}
</style>
