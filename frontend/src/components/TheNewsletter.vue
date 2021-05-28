<template>
  <div>
    <v-row>
      <v-col class="pa-0" cols="12" sm="8" md="7">
        <v-card elevation="0" class="pa-0">
          <v-card-title class="font-weight-bold">
            Suivre les actualités du site ma cantine
          </v-card-title>

          <v-card-subtitle class="text-left">
            Inscrivez-vous à la newsletter et recevez environ 1 email par mois.
          </v-card-subtitle>

          <v-card-text>
            <v-form ref="form" class="d-flex" v-model="formIsValid">
              <v-text-field
                solo
                v-model="email"
                ref="email"
                label="Votre adresse email"
                validate-on-blur
                :rules="[validators.isEmail]"
              ></v-text-field>
              <v-btn @click="subscribe" outlined color="primary darken-1" class="ml-4 mt-1" large>Valider</v-btn>
            </v-form>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col v-if="$vuetify.breakpoint.smAndUp" class="d-flex align-center">
        <v-img src="/static/images/appli-food.svg" contain max-height="100px"></v-img>
      </v-col>
      <v-spacer></v-spacer>
    </v-row>
  </div>
</template>

<script>
import { subscribeNewsletter } from "@/data/submit-actions.js"
import validators from "@/validators"

export default {
  data() {
    return {
      email: "",
      formIsValid: true,
    }
  },
  computed: {
    validators() {
      return validators
    },
  },
  methods: {
    async subscribe() {
      this.$refs.form.validate()
      if (!this.formIsValid) return

      const response = await subscribeNewsletter(this.email)

      if (response.status === 201 || response.status === 204) {
        this.email = null
        alert("Vous êtes bien inscrit.e à la newsletter de ma cantine.")
      } else {
        const error = await response.json()
        console.log(error)
      }
    },
  },
}
</script>
