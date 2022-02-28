<template>
  <div class="text-left">
    <v-form v-model="formIsValid" ref="form" @submit.prevent>
      <div class="spinner" v-if="loading">
        <v-progress-circular indeterminate style="position: absolute; left: 50%; top: 50%"></v-progress-circular>
      </div>
      <h2 class="text-h4 font-weight-black mb-8">Devenir béta-testeur</h2>
      <p class="text-body-2">
        Nous sommes en version de test et cherchons continuellement à améliorer la plateforme. Pour cela nous cherchons
        des cantines prêtes à nous accompagner en devenant béta-testeur. Si vous souhaitez y participer merci de nous
        communiquer vos informations ci-dessous.
      </p>

      <label for="name" class="body-2">Votre nom et prénom</label>
      <v-text-field
        id="name"
        validate-on-blur
        hide-details="auto"
        :rules="[validators.required]"
        solo
        v-model="formData.name"
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
      <v-btn x-large color="primary" :disabled="loading" class="mr-2" @click="subscribeBetaTester">Je participe</v-btn>
    </v-row>
  </div>
</template>

<script>
import validators from "@/validators"
import { lastYear } from "@/utils"

export default {
  data() {
    return {
      formData: {},
      formIsValid: true,
      loading: false,
    }
  },
  computed: {
    validators() {
      return validators
    },
    latestDiagnostic() {
      const diagnostics = this.$store.getters.getLocalDiagnostics()
      return diagnostics.find((x) => x.year === lastYear())
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
      this.loading = true
      this.$store
        .dispatch("subscribeBetaTester", payload)
        .then(() => {
          this.formData = {}
          this.$store.dispatch("notify", {
            message: "Merci de vôtre intérêt pour ma cantine, nous reviendrons vers vous dans les plus brefs délais.",
          })
        })
        .catch((e) => this.$store.dispatch("notifyServerError", e))
        .finally(() => {
          this.loading = false
        })
    },
  },
}
</script>

<style scoped>
.spinner {
  background: #d5d5d53b none repeat scroll 0% 0%;
  position: absolute;
  inset: 0px;
  z-index: 1;
}
</style>
