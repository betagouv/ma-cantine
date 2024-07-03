<template>
  <div>
    <v-row>
      <v-col class="pa-4 pa-md-0" cols="12" sm="8" md="7">
        <v-card elevation="0" class="pa-0">
          <v-card-title>
            <h2 class="fr-h5 mb-2">
              Suivre les actualités du site ma cantine
            </h2>
          </v-card-title>

          <v-card-subtitle class="text-left">
            <p class="mb-0">
              Inscrivez-vous à la newsletter et recevez environ 1 email par mois.
            </p>
          </v-card-subtitle>

          <v-card-text>
            <v-form ref="form" class="d-sm-flex align-sm-center text-left" v-model="formIsValid" @submit.prevent>
              <DsfrEmail v-model="email" class="flex-grow-1 mb-sm-6" />
              <v-btn @click="subscribe" outlined color="primary" class="ml-sm-4" large>Valider</v-btn>
            </v-form>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col v-if="$vuetify.breakpoint.smAndUp" class="d-flex align-center" cols="4" md="2">
        <v-img src="/static/images/doodles-dsfr/primary/LayingDoodle.png" contain max-height="100px"></v-img>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import validators from "@/validators"
import DsfrEmail from "@/components/DsfrEmail"

export default {
  components: { DsfrEmail },
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
    subscribe() {
      this.$refs.form.validate()
      if (!this.formIsValid) return

      return this.$store
        .dispatch("subscribeNewsletter", this.email)
        .then(() => {
          this.email = null
          this.$store.dispatch("notify", {
            message: "Vous êtes bien inscrit.e à la newsletter de ma cantine.",
            status: "success",
          })
        })
        .catch((e) => this.$store.dispatch("notifyServerError", e))
    },
  },
}
</script>
