<template>
  <div>
    <v-row>
      <v-col>
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
          <v-select
            v-model="inquiryType"
            :items="inquiryOptions"
            label="Type de demande"
            outlined
            class="my-2"
            :rules="[validators.required]"
          ></v-select>
          <v-textarea
            v-model="message"
            label="Message"
            outlined
            :rules="[validators.required]"
            class="mt-2"
          ></v-textarea>
          <p class="caption grey--text text--darken-1 mt-n1 mb-6">
            Ne partagez pas d'informations sensibles (par ex. mot de passe, numéro de carte bleue, etc).
          </p>
        </v-form>
        <v-btn x-large color="primary" class="mt-0 mb-6" @click="sendEmail">
          <v-icon class="mr-2">mdi-send</v-icon>
          Envoyer
        </v-btn>
        <p class="grey--text text--darken-1">
          Si vous n'arrivez pas à utiliser le formulaire ci-dessus, vous pouvez nous contacter directement par email à
          l'adresse suivante:
          <a href="mailto:contact@egalim.beta.gouv.fr">contact@egalim.beta.gouv.fr</a>
        </p>
      </v-col>
      <v-col cols="4" v-if="$vuetify.breakpoint.smAndUp">
        <div class="fill-height d-flex flex-column align-center">
          <v-spacer></v-spacer>
          <v-img src="/static/images/doodles/primary/SittingDoodle.png" contain style="transform: scaleX(-1);"></v-img>
          <v-spacer></v-spacer>
        </div>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import validators from "@/validators"

export default {
  name: "GeneralContactForm",
  props: {
    initialInquiryType: {
      type: String,
      required: false,
    },
    // meta is a JSON serialisable object containing data that could help the team help the user
    // such as the page the user was on when they sent the message
    meta: {
      type: Object,
      required: false,
    },
  },
  data() {
    const user = this.$store.state.loggedUser
    return {
      formIsValid: true,
      fromEmail: user ? user.email : "",
      name: user ? `${user.firstName} ${user.lastName}` : "",
      message: "",
      inquiryType: "",
      inquiryOptions: [
        { text: "Poser une question sur une fonctionnalité de ma cantine ?", value: "functionalityQuestion" },
        { text: "Demander une démo", value: "demo" },
        { text: "Signaler un bug", value: "bug" },
        { text: "Question sur la loi EGAlim", value: "egalim" },
        { text: "Autre", value: "other" },
      ],
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

      let meta = this.meta || {}
      meta.userId = this.$store.state.loggedUser?.id
      meta.userAgent = navigator.userAgent

      // this text is visible to the team when the inquiry is sent
      const inquiryTypeDisplay = {
        functionalityQuestion: "fonctionnalité",
        bug: "bug",
        egalim: "loi",
        demo: "requête de démo",
        other: "autre",
      }

      const payload = {
        from: this.fromEmail,
        name: this.name,
        message: this.message,
        inquiryType: inquiryTypeDisplay[this.inquiryType],
        meta,
      }

      this.$store
        .dispatch("sendInquiryEmail", payload)
        .then(() => {
          this.$store.dispatch("notify", {
            status: "success",
            message: `Votre message a bien été envoyé. Nous reviendrons vers vous dans les plus brefs délais.`,
          })

          if (this.$matomo) {
            this.$matomo.trackEvent("inquiry", "send", this.inquiryType)
          }
          this.$refs.form.reset()
          window.scrollTo(0, 0)
        })
        .catch((e) => this.$store.dispatch("notifyServerError", e))
    },
  },
}
</script>
