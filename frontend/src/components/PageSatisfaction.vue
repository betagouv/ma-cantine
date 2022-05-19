<template>
  <v-card class="py-6 px-16 mx-auto my-6 box text-center" elevation="0" color="secondary lighten-4">
    <label class="body-2 grey--text text--darken-4" for="page-satisfaction">
      Êtes-vous satisfait de cette page ?
    </label>
    <v-rating
      v-model.number="satisfaction"
      color="primary"
      empty-icon="mdi-star-outline"
      full-icon="mdi-star"
      class="mt-2 body-2"
      id="page-satisfaction"
      background-color="grey"
      length="5"
      hover
    ></v-rating>

    <v-dialog v-model="dialog" width="500">
      <!-- <template v-slot:activator="{ on, attrs }">
        <v-btn color="primary" v-bind="attrs" v-on="on">Faire une suggestion</v-btn>
      </template> -->

      <v-card class="text-left pa-4">
        <v-card-title class="font-weight-black">
          Faire une suggestion
        </v-card-title>

        <v-card-text>
          <v-form ref="form" v-model="formIsValid">
            <label class="body-2 grey--text text--darken-4" for="dialog-satisfaction">
              Êtes-vous satisfait de cette page ?
            </label>
            <v-rating
              v-model.number="satisfaction"
              color="primary"
              empty-icon="mdi-star-outline"
              full-icon="mdi-star"
              class="mt-2 mb-4 body-2"
              id="dialog-satisfaction"
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
      satisfaction: null,
      suggestion: null,
      email: null,
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
        satisfaction: this.satisfaction,
        suggestion: this.suggestion,
        page: this.$route.name,
        userId: this.$store.state.loggedUser.id,
      }
      console.log("payload", payload)
      // TODO: POST payload
      // TODO: success message
      this.dialog = false
    },
    cancel() {
      this.$refs.form.reset()
      this.dialog = false
    },
  },
  watch: {
    satisfaction(newValue) {
      if (newValue) {
        this.dialog = true
      }
    },
    dialog(newValue) {
      if (newValue === false) {
        this.satisfaction = null
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
