<template>
  <v-form ref="siretForm">
    <v-alert v-if="duplicateSiretCanteen" outlined type="info">
      <h2 class="mb-4 text-h6 black--text" style="line-height: 1.25rem;">
        Il existe déjà une cantine avec le SIRET {{ duplicateSiretCanteen.siret }}
      </h2>
      <div v-if="duplicateSiretCanteen.isManagedByUser" class="black--text">
        <p>« {{ duplicateSiretCanteen.name }} » a le même SIRET et fait déjà partie de vos cantines.</p>
        <!-- TODO: more guidance for the user in the case where they think they want to add multiple canteens with the same SIRET -->
        <v-btn
          color="primary"
          :to="{
            name: 'CanteenModification',
            params: { canteenUrlComponent: $store.getters.getCanteenUrlComponent(duplicateSiretCanteen) },
          }"
        >
          Accéder à « {{ duplicateSiretCanteen.name }} »
        </v-btn>
      </div>
      <div v-else-if="duplicateSiretCanteen.canBeClaimed" class="black--text">
        <p>
          <!-- TODO: more of an explanation of how this might have happened? -->
          <!-- e.g. your canteen was created from publicly available data? -->
          La cantine « {{ duplicateSiretCanteen.name }} » est déjà référencée sur notre site mais n'est pas encore
          gérée.
        </p>
        <v-btn color="primary" @click="claimCanteen">
          <v-icon class="mr-2">mdi-key</v-icon>
          Demander accès à cette cantine
        </v-btn>
      </div>
      <div v-else class="black--text">
        <p>Probablement, un autre membre de votre équipe à déjà ajouté votre cantine sur notre site.</p>
        <p>Demandez accès aux gestionnaires de « {{ duplicateSiretCanteen.name }} »</p>
        <DsfrTextarea
          v-model="messageJoinCanteen"
          label="Message (optionnel)"
          hide-details="auto"
          rows="2"
          class="mt-2 body-2"
        />
        <v-btn color="primary" class="mt-4" @click="sendMgmtRequest">
          <v-icon class="mr-2">mdi-key</v-icon>
          Demander l'accès
        </v-btn>
      </div>
    </v-alert>

    <DsfrTextField
      hide-details="auto"
      validate-on-blur
      label="SIRET"
      v-model="siret"
      :rules="[validators.length(14), validators.luhn]"
      labelClasses="body-2 mb-2"
      style="max-width: 20rem;"
    />

    <v-sheet rounded color="grey lighten-4 pa-3 mt-4" class="d-flex">
      <v-spacer></v-spacer>
      <v-btn x-large outlined color="primary" class="mr-4 align-self-center" :to="{ name: 'ManagementPage' }">
        Annuler
      </v-btn>
      <v-btn x-large color="primary" @click="validateSiret">
        Valider
      </v-btn>
    </v-sheet>
  </v-form>
</template>

<script>
import validators from "@/validators"
import DsfrTextField from "@/components/DsfrTextField"
import DsfrTextarea from "@/components/DsfrTextarea"

export default {
  name: "SiretCheck",
  components: { DsfrTextField, DsfrTextarea },
  data() {
    const user = this.$store.state.loggedUser
    return {
      siret: undefined,
      duplicateSiretCanteen: undefined,
      user,
      fromName: `${user.firstName} ${user.lastName}`,
      messageJoinCanteen: null,
      messageTroubleshooting: null,
      siretFormIsValid: true,
      siretDialog: false,
      claimSucceeded: undefined,
    }
  },
  computed: {
    validators() {
      return validators
    },
  },
  methods: {
    validateSiret() {
      if (!this.$refs.siretForm.validate()) {
        this.$store.dispatch("notifyRequiredFieldsError")
        window.scrollTo(0, 0)
        return
      }
      return fetch("/api/v1/siret/" + this.siret)
        .then((response) => response.json())
        .then((response) => {
          const isDuplicateSiret = !!response.id
          if (isDuplicateSiret) {
            this.siret = null
            this.duplicateSiretCanteen = response
            this.messageTroubleshooting = `Je veux ajouter une deuxième cantine avec le même SIRET : ${this.siret}...`
          } else {
            this.$emit("siretIsValid", this.siret)
          }
        })
    },
    // TODO: after request sent, change front end to clear message and discourage duplicate sending
    // maybe clear siret and red box, adding a green alert at the top which includes the SIRET in the message
    // or something...
    sendMgmtRequest() {
      const payload = {
        email: this.user.email,
        name: this.fromName,
        message: this.messageJoinCanteen,
      }

      this.$store
        .dispatch("sendCanteenTeamRequest", { canteenId: this.duplicateSiretCanteen.id, payload })
        .then(() => {
          this.message = null
          this.$store.dispatch("notify", {
            status: "success",
            message: `Votre message a bien été envoyé.`,
          })
          window.scrollTo(0, 0)
        })
        .catch((e) => this.$store.dispatch("notifyServerError", e))
    },
    sendSiretHelp() {
      this.$refs.siretHelp.validate()
      if (!this.siretFormIsValid) {
        this.$store.dispatch("notifyRequiredFieldsError")
        return
      }

      let meta = this.meta || {}
      meta.userId = this.$store.state.loggedUser?.id
      meta.userAgent = navigator.userAgent

      const payload = {
        from: this.fromEmail,
        message: this.messageTroubleshooting,
        // TODO: put misc inquiry types in the title of trello card directly
        inquiryType: "cantine SIRET",
        meta,
      }

      this.$store
        .dispatch("sendInquiryEmail", payload)
        .then(() => {
          this.message = null
          this.$store.dispatch("notify", {
            status: "success",
            message: `Votre message a bien été envoyé. Nous reviendrons vers vous dans les plus brefs délais.`,
          })
          this.siretDialog = false

          window.scrollTo(0, 0)
        })
        .catch((e) => this.$store.dispatch("notifyServerError", e))
    },
    claimCanteen() {
      const canteenId = this.duplicateSiretCanteen.id
      return this.$store
        .dispatch("claimCanteen", { canteenId })
        .then(() => (this.claimSucceeded = true))
        .catch((e) => this.$store.dispatch("notifyServerError", e))
    },
  },
}
</script>

<style></style>
