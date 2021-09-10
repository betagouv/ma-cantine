<template>
  <div class="text-left">
    <v-form v-model="formIsValid" ref="form" @submit.prevent>
      <h2 class="text-h4 font-weight-black mb-8">Devenir béta-testeur</h2>
      <p class="text-body-2">
        Nous sommes en version de test et cherchons continuellement à améliorer la plateforme. Pour cela nous cherchons
        des cantines prêtes à nous accompagner en devenant béta-testeur. Si vous souhaitez y participer merci de nous
        communiquer vos informations ci-dessous.
      </p>

      <label for="school" class="body-2">Nom de votre cantine</label>
      <v-text-field
        id="school"
        validate-on-blur
        hide-details="auto"
        :rules="[validators.required]"
        solo
        v-model="formData.school"
        class="mt-2 mb-4"
      ></v-text-field>

      <label for="city" class="body-2">Ville / commune</label>
      <v-text-field
        id="city"
        validate-on-blur
        hide-details="auto"
        :rules="[validators.required]"
        solo
        v-model="formData.city"
        class="mt-2 mb-4"
      ></v-text-field>

      <label for="email" class="body-2">Votre email</label>
      <v-text-field
        id="email"
        validate-on-blur
        hide-details="auto"
        :rules="[validators.email]"
        solo
        v-model="formData.email"
        class="mt-2 mb-4"
      ></v-text-field>

      <label for="phone" class="body-2">Numéro de téléphone (optionnel)</label>
      <v-text-field id="phone" hide-details="auto" v-model="formData.phone" solo class="mt-2 mb-4"></v-text-field>

      <label for="message" class="body-2">Message (optionnel)</label>
      <v-textarea
        id="message"
        hide-details="auto"
        rows="3"
        v-model="formData.message"
        solo
        class="mt-2 mb-4"
      ></v-textarea>
    </v-form>
    <v-row class="my-8">
      <v-spacer></v-spacer>
      <v-btn x-large color="primary" class="mr-2" @click="subscribeBetaTester">Je participe</v-btn>
    </v-row>
  </div>
</template>

<script>
import validators from "@/validators"

export default {
  data() {
    return {
      formData: {},
      formIsValid: true,
    }
  },
  computed: {
    validators() {
      return validators
    },
    latestDiagnostic() {
      const diagnostics =
        this.$store.state.loggedUser && this.$store.state.userCanteens.length
          ? this.$store.state.userCanteens[0].diagnostics
          : this.$store.getters.getLocalDiagnostics()
      return diagnostics.find((x) => x.year === 2020)
    },
  },
  methods: {
    subscribeBetaTester() {
      this.$refs.form.validate()
      if (!this.formIsValid) {
        this.$store.dispatch("notifyRequiredFieldsError")
        return
      }

      const payload = Object.assign({ measures: this.latestDiagnostic }, this.formData)

      this.$store
        .dispatch("subscribeBetaTester", payload)
        .then(() => {
          this.formData = {}
          this.$store.dispatch("notify", {
            message: "Merci de vôtre intérêt pour ma cantine, nous reviendrons vers vous dans les plus brefs délais.",
          })
        })
        .catch((error) => {
          console.log(error.message)
          this.$store.dispatch("notifyServerError")
        })
    },
  },
}
</script>
