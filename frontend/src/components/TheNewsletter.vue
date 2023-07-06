<template>
  <div class="text-left">
    <v-row>
      <v-col class="pa-4 pa-md-0" cols="12" sm="8" md="7">
        <v-card elevation="0" class="pa-0">
          <v-card-title class="text-h4">
            Suivre les actualités du site ma cantine
          </v-card-title>

          <v-card-subtitle class="text-body-1">
            Inscrivez-vous à la newsletter et recevez environ 1 email par mois.
          </v-card-subtitle>

          <v-card-text>
            <v-form ref="form" class="d-flex align-center" v-model="formIsValid" @submit.prevent>
              <DsfrTextField
                v-model="email"
                class="flex-grow-1"
                ref="email"
                label="Votre adresse email"
                validate-on-blur
                :rules="[validators.email]"
                labelClasses="text-body-1 mb-2"
              />
              <v-btn @click="subscribe" outlined color="primary" class="text-button ml-4 mt-1" large>Valider</v-btn>
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
import DsfrTextField from "@/components/DsfrTextField"

export default {
  components: { DsfrTextField },
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
