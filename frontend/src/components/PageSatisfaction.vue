<template>
  <v-card class="py-6 px-16 mx-auto my-6 box text-center" elevation="0" color="secondary lighten-4" v-if="!hasRating">
    <label class="body-2 grey--text text--darken-4" for="page-rating">
      Êtes-vous satisfait de cette page ?
    </label>
    <v-rating
      v-model.number="rating"
      color="primary"
      empty-icon="mdi-star-outline"
      full-icon="mdi-star"
      class="mt-2 body-2"
      id="page-rating"
      background-color="grey"
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
              Êtes-vous satisfait de cette page ?
            </label>
            <v-rating
              v-model.number="rating"
              color="primary"
              empty-icon="mdi-star-outline"
              full-icon="mdi-star"
              class="mt-2 mb-4 body-2"
              id="dialog-rating"
              background-color="grey"
              length="5"
              hover
            ></v-rating>
            <label class="body-2 grey--text text--darken-3" for="suggestion">
              Que pouvons-nous améliorer afin de mieux répondre à vos attentes ?
            </label>
            <v-textarea
              v-model="suggestion"
              solo
              id="suggestion"
              :rules="[validators.required]"
              validate-on-blur
              hide-details="auto"
              class="mt-2 mb-4 body-2"
              rows="5"
            ></v-textarea>
            <p class="caption mb-0">
              On pourrait vous contacter si on aurait besoin de plus des informations ou si on pense qu'on pourrait vous
              aider en vos démarches.
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

export default {
  name: "PageSatisfaction",
  data() {
    return {
      dialog: false,
      validators,
      formIsValid: true,
      rating: null,
      suggestion: null,
      email: null,
      hasRating: true, // default to not showing it to avoid it appearing and disappearing on load
      page: this.$route.name,
    }
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
          this.hasRating = true
        })
        .catch((e) => {
          this.$store.dispatch("notifyServerError", e)
        })
    },
    cancel() {
      this.$refs.form.reset()
      this.dialog = false
    },
    getRating() {
      return fetch(`/api/v1/reviews/${this.page}`).then((response) => {
        if (response.status === 404) {
          this.hasRating = false
        }
      })
    },
  },
  mounted() {
    this.getRating()
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
