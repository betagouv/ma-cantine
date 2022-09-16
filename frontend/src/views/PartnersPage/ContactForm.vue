<template>
  <div>
    <h2 class="font-weight-black text-h6 grey--text text--darken-4 mb-6">Contactez « {{ partner.name }} »</h2>
    <v-form v-model="formIsValid" ref="form" @submit.prevent>
      <DsfrTextField v-model="fromEmail" label="Votre email" :rules="[validators.email]" validate-on-blur />
      <DsfrTextField v-model="name" label="Prénom et nom (facultatif)" />
      <DsfrTextarea v-model="message" label="Message" :rules="[validators.required]" />
      <p class="caption text-left grey--text text--darken-1 mt-n1 mb-6">
        Ne partagez pas d'informations sensibles (par ex. mot de passe, numéro de carte bleue, etc). Ces messages
        peuvent être lus pour des fins de modération.
      </p>
    </v-form>
    <v-btn x-large color="primary" class="mt-0 mb-6" @click="sendEmail">
      <v-icon class="mr-2">$send-plane-fill</v-icon>
      Envoyer
    </v-btn>
  </div>
</template>

<script>
import validators from "@/validators"
import DsfrTextField from "@/components/DsfrTextField"
import DsfrTextarea from "@/components/DsfrTextarea"

export default {
  name: "ContactForm",
  components: { DsfrTextField, DsfrTextarea },
  props: ["partner"],
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
        destinationCanteen: this.partner.id,
        senderEmail: this.fromEmail,
        senderName: this.name,
        body: this.message,
      }

      this.$store
        .dispatch("sendPartnerEmail", payload)
        .then(() => {
          this.$refs.form.reset()
          this.$store.dispatch("notify", {
            status: "success",
            message: `Votre message a bien été envoyé à ${this.partner.name}. Merci de vôtre intérêt.`,
          })

          if (this.$matomo) {
            this.$matomo.trackEvent("message", "send", "partner-email-contact")
          }
          window.scrollTo(0, 0)
        })
        .catch((e) => this.$store.dispatch("notifyServerError", e))
    },
  },
}
</script>
