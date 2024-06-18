<template>
  <div>
    <h2 class="grey--text text--darken-4 mb-6">Contactez « {{ canteen.name }} »</h2>
    <div v-if="canteen.canBeClaimed">
      <p>Nous n'avons pas de coordonnées de contact pour cette cantine.</p>
    </div>
    <div v-else>
      <div class="text-left grey--text text--darken-4 mt-n1 mb-6 text-body-2">
        <ul class="no-bullets">
          <li class="mb-1 d-flex align-center">
            <v-icon small color="green" class="mr-1">$check-line</v-icon>
            <span>Demandez des informations supplémentaires sur la cantine « {{ canteen.name }} »</span>
          </li>
          <li class="mb-1 d-flex align-center">
            <v-icon small color="green" class="mr-1">$check-line</v-icon>
            <span>
              Demandez aux gestionnaires leur retour d'expérience sur une action mise en place
            </span>
          </li>
        </ul>
        <ul class="mt-4 no-bullets">
          <li class="mb-1 d-flex align-center">
            <v-icon small color="amber darken-3" class="mr-1">$error-warning-line</v-icon>
            <span>
              Pour postuler à une offre d'emploi privilégiez les contacts directs de l'établissement
            </span>
          </li>
          <li class="mb-1 d-flex align-center">
            <v-icon small color="amber darken-3" class="mr-1">$error-warning-line</v-icon>
            <span class="mb-0">
              Pour informer l'établissement de l'absence de votre enfant à la pension du midi, utilisez votre site de «
              vie scolaire »
            </span>
          </li>
          <li class="mb-1 d-flex align-center">
            <v-icon small color="amber darken-3" class="mr-1">$error-warning-line</v-icon>
            <span class="mb-0">
              Proposez vos services parmi les
              <router-link :to="{ name: 'PartnersHome' }">
                acteurs de l'éco-système
              </router-link>
              en remplissant le
              <a
                href="https://startupdetat.typeform.com/to/JhhsMCYC"
                target="_blank"
                rel="noopener external"
                title="formulaire de référencement - ouvre une nouvelle fenêtre"
              >
                formulaire de référencement
                <v-icon color="primary" small>mdi-open-in-new</v-icon>
              </a>
            </span>
          </li>
        </ul>
      </div>
      <v-form v-model="formIsValid" ref="form" @submit.prevent>
        <DsfrEmail v-model="fromEmail" />
        <DsfrFullName v-model="name" />
        <DsfrTextarea v-model="message" label="Message" :rules="[validators.required]" />
        <p class="caption text-left grey--text text--darken-1 mt-n1 mb-6">
          Ne partagez pas d'informations sensibles (par ex. mot de passe, numéro de carte bleue, etc).
          <br />
          L'équipe de « ma cantine » se réserve un droit de modération et décide ou non de valider votre message dans
          les 3 jours ouvrables.
        </p>
      </v-form>
      <v-btn x-large color="primary" class="mt-0 mb-6" @click="sendEmail">
        <v-icon class="mr-2">mdi-send</v-icon>
        Envoyer
      </v-btn>
    </div>
  </div>
</template>

<script>
import validators from "@/validators"
import DsfrFullName from "@/components/DsfrFullName"
import DsfrEmail from "@/components/DsfrEmail"
import DsfrTextarea from "@/components/DsfrTextarea"

export default {
  name: "ContactForm",
  components: { DsfrFullName, DsfrTextarea, DsfrEmail },
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
