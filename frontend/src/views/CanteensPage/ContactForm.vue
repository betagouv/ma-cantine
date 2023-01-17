<template>
  <div>
    <h2 class="font-weight-black text-h6 grey--text text--darken-4 mb-6">Contactez « {{ canteen.name }} »</h2>
    <div class="text-left grey--text text--darken-2 mt-n1 mb-6">
      <p>Vous pouvez par exemple :</p>
      <div class="ml-2">
        <p class="mb-1">
          <v-icon small color="green">$check-line</v-icon>
          demander des informations supplémentaires sur la cantine que vous fréquentez;
        </p>
        <p class="mb-1">
          <v-icon small color="green">$check-line</v-icon>
          contacter un collègue gestionnaire afin de lui demander un retour d'expérience sur une action mise en place...
        </p>
      </div>
      <p class="mt-4">Il ne s'agit cependant pas de :</p>
      <div class="ml-2">
        <p class="mb-1">
          <v-icon small color="red">$close-line</v-icon>
          postuler à une offre d'emploi pour une cantine => privilégier des contacts de l'établissements hors de ma
          cantine
        </p>
        <p class="mb-1">
          <v-icon small color="red">$close-line</v-icon>
          informer l'établissement de l'absence/présence de soi ou d'un tiers au repas du jour => privilégier un contact
          avec la "vie scolaire"
        </p>
        <p class="mb-1">
          <v-icon small color="red">$close-line</v-icon>
          en tant que fournisseur de proposer ses services => privilégier votre référencement parmis les
          <router-link :to="{ name: 'PartnersHome' }">
            acteurs de l'éco-système
          </router-link>
          en
          <a href="https://startupdetat.typeform.com/to/JhhsMCYC" target="_blank" rel="noopener">
            demandant votre référencement
            <v-icon color="primary" small>mdi-open-in-new</v-icon>
          </a>
        </p>
      </div>
      <p class="mt-4">
        Nota bene : l'équipe de « ma cantine » se réserve un droit de modération et décide ou non de valider votre
        message dans
        <b>les 3 jours ouvrables.</b>
      </p>
    </div>
    <v-form v-model="formIsValid" ref="form" @submit.prevent>
      <DsfrTextField v-model="fromEmail" label="Votre email" :rules="[validators.email]" validate-on-blur />
      <DsfrTextField v-model="name" label="Prénom et nom (facultatif)" />
      <DsfrTextarea v-model="message" label="Message" :rules="[validators.required]" />
      <p class="caption text-left grey--text text--darken-1 mt-n1 mb-6">
        Ne partagez pas d'informations sensibles (par ex. mot de passe, numéro de carte bleue, etc).
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
import DsfrTextField from "@/components/DsfrTextField"
import DsfrTextarea from "@/components/DsfrTextarea"

export default {
  name: "ContactForm",
  components: { DsfrTextField, DsfrTextarea },
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
        destinationCanteen: this.canteen.id,
        senderEmail: this.fromEmail,
        senderName: this.name,
        body: this.message,
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
        .catch((e) => this.$store.dispatch("notifyServerError", e))
    },
  },
}
</script>
