<template>
  <div>
    <v-row class="my-8 align-center">
      <v-spacer></v-spacer>
      <h1>Envoyer un message - {{ canteen.name }}</h1>
      <v-spacer></v-spacer>
      <v-col v-if="$vuetify.breakpoint.mdAndUp" cols="3">
        <v-img src="/static/images/LayingDoodle.png" contain max-height="80px"></v-img>
      </v-col>
      <v-spacer></v-spacer>
    </v-row>
    <v-form v-model="formIsValid" ref="form" @submit.prevent>
      <v-text-field
        v-model="fromEmail"
        label="Votre email"
        :rules="[validators.isEmail]"
        validate-on-blur
        outlined
      ></v-text-field>
      <v-textarea v-model="message" label="Message" outlined required></v-textarea>
    </v-form>
    <v-btn x-large color="primary" class="mt-6" @click="sendEmail">Envoyer message</v-btn>
  </div>
</template>

<script>
import validators from "@/validators"

export default {
  name: "ContactPage",
  props: {
    canteenUrlComponent: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      formIsValid: true,
      fromEmail: "",
      message: "",
    }
  },
  created() {
    document.title = `Contacter ${this.canteen.name} - ma-cantine.beta.gouv.fr`
  },
  computed: {
    canteen() {
      return this.$store.getters.getCanteenFromUrlComponent(this.canteenUrlComponent)
    },
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
        message: this.message,
      }

      this.$store
        .dispatch("sendCanteenEmail", payload)
        .then(() => {
          this.formData = {}
          this.$store.dispatch("notify", {
            status: "success",
            message: `Votre message a bien été envoyé à ${this.canteen.name}. Merci de vôtre intérêt.`,
          })
          this.$router.push({ name: "CanteenPage", params: { canteenUrlComponent: this.canteenUrlComponent } })
        })
        .catch((error) => {
          console.log(error.message)
          this.$store.dispatch("notifyServerError")
        })
    },
  },
}
</script>
