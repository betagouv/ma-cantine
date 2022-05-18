<template>
  <div style="background-color: #ffddd8;" class="py-6 px-16 mx-auto">
    <label class="body-2 grey--text text--darken-4" for="page-satisfaction">
      Êtes-vous satisfait de cette page ?
    </label>
    <v-rating
      v-model.number="satisfaction"
      color="primary"
      empty-icon="mdi-star-outline"
      full-icon="mdi-star"
      class="mt-2 mb-4 body-2"
      id="page-satisfaction"
      background-color="grey"
      length="5"
      hover
    ></v-rating>

    <v-dialog v-model="dialog" width="500">
      <template v-slot:activator="{ on, attrs }">
        <v-btn color="primary" v-bind="attrs" v-on="on">Faire une suggestion</v-btn>
      </template>

      <v-card class="text-left pa-4">
        <v-card-title class="font-weight-black">
          Faire une suggestion
        </v-card-title>

        <v-card-text>
          <v-form ref="form" v-model="formIsValid">
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
            <div v-if="!hasLoggedUser">
              <label class="body-2 grey--text text--darken-3" for="email">
                Votre adresse mail
              </label>
              <v-text-field
                v-model="email"
                solo
                id="email"
                :rules="[validators.emailOrEmpty]"
                validate-on-blur
                hide-details="auto"
                class="mt-2 mb-4 body-2"
              ></v-text-field>
            </div>
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
  </div>
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
  computed: {
    hasLoggedUser() {
      return this.$store.state.loggedUser
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
        satisfaction: this.satisfaction,
        suggestion: this.suggestion,
      }
      this.sendPayload(payload)
      this.dialog = false
    },
    sendPayload(payload) {
      payload.page = this.$route.name
      if (this.hasLoggedUser) {
        payload.userId = this.$store.state.loggedUser.id
      } else {
        payload.email = this.email
      }
      // TODO: success message
    },
    cancel() {
      this.$refs.form.reset()
      this.dialog = false
    },
  },
  watch: {
    // TODO: is there a way of associating the rating (submitted the moment it changes)
    // with the suggestion (optionally submitted later) ?
    // and to allow user to change their mind on the rating.
    // for logged in users this is easy (userId + page - is it though?)
    satisfaction(newValue) {
      if (newValue && newValue < 3) {
        this.dialog = true
      }
      this.sendPayload({ satisfaction: newValue })
    },
  },
}
</script>
