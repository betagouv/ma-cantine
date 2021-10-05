<template>
  <div>
    <h2 class="font-weight-black text-h6 grey--text text--darken-4 mb-6">Contactez « {{ canteen.name }} »</h2>
    <v-form v-model="formIsValid" ref="form" @submit.prevent>
      <v-text-field
        v-model="fromEmail"
        label="Votre email"
        :rules="[validators.email]"
        validate-on-blur
        outlined
        class="my-2"
      ></v-text-field>
      <v-text-field v-model="name" label="Prénom et nom (facultatif)" outlined class="my-2"></v-text-field>
      <v-textarea v-model="message" label="Message" outlined :rules="[validators.required]" class="mt-2"></v-textarea>
      <p class="caption text-left grey--text text--darken-1 mt-n3 mb-6">
        Ne partagez pas d'informations sensibles (par ex. mot de passe, numéro de carte bleue, etc). Ces messages
        peuvent être lus pour des fins de modération.
      </p>
    </v-form>
    <v-btn x-large color="primary" class="mt-0 mb-6" @click="sendEmail">
      <v-icon class="mr-2">mdi-send</v-icon>
      Envoyer
    </v-btn>
  </div>
</template>

<script>
import validators from "@/validators"

export default {
  name: "ContactForm",
  props: ["canteen"],
  data() {
    const user = this.$store.state.loggedUser
    return {
      formIsValid: true,
      fromEmail: user ? user.email : "",
      name: user ? `${user.firstName} ${user.lastName}` : "",
      message: "",
    }
  },
  computed: {
    validators() {
      return validators
    },
  },
  methods: {
    sendEmail() {
      this.$refs.form.validate()
      if (!this.formIsValid) {
        this.$store.dispatch("notifyRequiredFieldsError")
        return
      }

      const payload = {
        canteenId: this.canteen.id,
        from: this.fromEmail,
        name: this.name,
        message: this.message,
      }

      this.$store
        .dispatch("sendCanteenEmail", payload)
        .then(() => {
          this.$refs.form.reset()
          this.$store.dispatch("notify", {
            status: "success",
            message: `Votre message a bien été envoyé à ${this.canteen.name}. Merci de vôtre intérêt.`,
          })

          if (this.$matomo) {
            this.$matomo.trackEvent("message", "send", "canteen-email-contact")
          }
          window.scrollTo(0, 0)
        })
        .catch((error) => {
          console.log(error.message)
          this.$store.dispatch("notifyServerError")
        })
    },
  },
}
</script>
