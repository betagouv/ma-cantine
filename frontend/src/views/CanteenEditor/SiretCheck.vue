<template>
  <v-form ref="siretForm">
    <DsfrTextField
      hide-details="auto"
      validate-on-blur
      label="SIRET"
      v-model="siret"
      :rules="[validators.length(14), validators.luhn]"
      labelClasses="body-2 mb-2"
    />
    <p class="caption mt-1 ml-2">
      Vous ne le connaissez pas ? Utilisez cet
      <a href="https://annuaire-entreprises.data.gouv.fr/" target="_blank" rel="noopener">
        outil de recherche pour trouver le SIRET
        <v-icon color="primary" small>mdi-open-in-new</v-icon>
      </a>
      de votre cantine.
    </p>

    <v-card outlined class="my-4" v-if="duplicateSiretCanteen" color="red lighten-5">
      <v-card-title class="pt-2 pb-1 font-weight-medium">
        Une cantine avec ce SIRET existe déjà
      </v-card-title>
      <v-card-text v-if="duplicateSiretCanteen.isManagedByUser">
        <p>« {{ duplicateSiretCanteen.name }} » a le même SIRET et fait déjà partie de vos cantines.</p>
        <v-btn
          color="primary"
          :to="{
            name: 'CanteenModification',
            params: { canteenUrlComponent: $store.getters.getCanteenUrlComponent(duplicateSiretCanteen) },
          }"
          target="_blank"
          rel="noopener"
        >
          Voir les informations de « {{ duplicateSiretCanteen.name }} »
        </v-btn>
      </v-card-text>
      <v-card-text v-else>
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
      </v-card-text>

      <v-card-text class="py-2">
        <v-divider class="mt-2"></v-divider>

        <p class="mb-0 mt-2">
          <span style="vertical-align: sub;" class="mr-4">Il s'agit d'une erreur ?</span>
          <v-dialog v-model="siretDialog" width="500">
            <template v-slot:activator="{ on, attrs }">
              <v-btn text v-bind="attrs" v-on="on" color="primary darken-1" class="pl-0">
                Contactez l'équipe ma cantine
              </v-btn>
            </template>

            <v-card class="text-left">
              <v-card-title class="font-weight-bold">Contactez l'équipe ma cantine</v-card-title>
              <v-card-text class="pb-0">
                <p>
                  Vous recontrez des problèmes concernant le SIRET de votre cantine ? Envoyez nous un message et notre
                  équipe reviendra vers vous dans les plus brefs délais
                </p>
                <v-form v-model="siretFormIsValid" ref="siretHelp" @submit.prevent>
                  <DsfrTextarea
                    v-model="messageTroubleshooting"
                    label="Message"
                    labelClasses="body-2 text-left mb-2"
                    rows="3"
                    :rules="[validators.required]"
                    class="body-2"
                  />
                </v-form>
              </v-card-text>

              <v-divider></v-divider>

              <v-card-actions class="pa-4 pr-6">
                <v-spacer></v-spacer>
                <v-btn x-large outlined color="primary" @click="siretDialog = false" class="mr-2">
                  Annuler
                </v-btn>
                <v-btn x-large color="primary" @click="sendSiretHelp">
                  <v-icon class="mr-2">mdi-send</v-icon>
                  Envoyer
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>
        </p>
      </v-card-text>
    </v-card>
    <v-sheet rounded color="grey lighten-4 pa-3" class="d-flex">
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
      duplicateSiretCanteen: null,
      user,
      fromName: `${user.firstName} ${user.lastName}`,
      messageJoinCanteen: null,
      messageTroubleshooting: null,
      siretFormIsValid: true,
      siretDialog: false,
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
      // if (e.jsonPromise) {
      //   e.jsonPromise.then((json) => {
      //     const isDuplicateSiret = json.detail === "La resource que vous souhaitez créer existe déjà"
      //     if (isDuplicateSiret) {
      //       this.duplicateSiretCanteen = json
      //       this.messageTroubleshooting = `Je veux ajouter une deuxième cantine avec le même SIRET : ${payload.siret}...`
      //     }
      //   })
      //   this.$store.dispatch("notifyRequiredFieldsError")
      // } else {
      //   this.$store.dispatch("notifyServerError", e)
      // }
      // window.scrollTo(0, 0)
      this.$emit("siretIsValid", this.siret)
    },
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
  },
}
</script>

<style></style>
