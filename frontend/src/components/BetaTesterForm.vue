<template>
  <div>
    <v-form v-model="formIsValid" ref="form" @submit.prevent>
      <h2 class="text-h4 font-weight-black mb-8">Devenir béta-testeur</h2>
      <p class="text-body-2 text-left">
        Nous sommes en version de test et cherchons continuellement à améliorer la plateforme. Pour cela nous cherchons
        des cantines prêtes à nous accompagner en devenant béta-testeur. Si vous souhaitez y participer merci de nous
        communiquer vos informations ci-dessous.
      </p>

      <p class="body-2 mb-1 mt-2 text-left">Nom de votre cantine</p>
      <v-text-field
        validate-on-blur
        hide-details="auto"
        :rules="[validators.notEmpty]"
        solo
        v-model="formData.school"
      ></v-text-field>

      <p class="body-2 mb-1 mt-2 text-left">Ville / commune</p>
      <v-text-field
        validate-on-blur
        hide-details="auto"
        :rules="[validators.notEmpty]"
        solo
        v-model="formData.city"
      ></v-text-field>

      <p class="body-2 mb-1 mt-2 text-left">Votre email</p>
      <v-text-field
        validate-on-blur
        hide-details="auto"
        :rules="[validators.isEmail]"
        solo
        v-model="formData.email"
      ></v-text-field>

      <p class="body-2 mb-1 mt-2 text-left">Numéro de téléphone (optionnel)</p>
      <v-text-field hide-details="auto" solo v-model="formData.phone"></v-text-field>

      <p class="body-2 mb-1 mt-2 text-left">Message (optionnel)</p>
      <v-textarea hide-details="auto" rows="3" solo v-model="formData.message"></v-textarea>
    </v-form>
    <v-btn x-large color="primary" class="mt-8" @click="subscribeBetaTester">Je participe</v-btn>
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
    measures() {
      const userCanteen = this.$store.state.loggedUser ? this.$store.state.userCanteens[0] : null
      const diagnostics = userCanteen ? userCanteen.diagnostics : this.$store.getters.getLocalDiagnostics()
      return diagnostics.find((x) => x.year === 2020) || {}
    },
  },
  methods: {
    subscribeBetaTester() {
      this.$refs.form.validate()
      if (!this.formIsValid) return

      this.$store
        .dispatch("subscribeBetaTester", { ...this.formData, ...{ measures: this.measures } })
        .then(() => {
          this.formData = {}
          alert("Merci de vôtre intérêt pour ma cantine, nous reviendrons vers vous dans les plus brefs délais.")
        })
        .catch((error) => {
          console.log(error.message)
          alert("Une erreur est survenue, vous pouvez nous contacter directement à contact@egalim.beta.gouv.fr")
        })
    },
  },
}
</script>
