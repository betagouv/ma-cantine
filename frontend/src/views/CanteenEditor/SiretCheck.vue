<template>
  <div>
    <v-dialog v-if="showProgressIndicator" persistent fullscreen :value="true" :transition="false">
      <v-sheet color="rgba(0, 0, 0, .36)" class="fill-height d-flex justify-center align-center">
        <v-progress-circular indeterminate></v-progress-circular>
      </v-sheet>
    </v-dialog>
    <v-form ref="siretForm" @submit.prevent>
      <div class="mb-6" v-if="!allowDuplicates">
        <v-alert v-if="duplicateSiretCanteen" outlined type="info" color="primary">
          <div v-if="duplicateSiretCanteen.isManagedByUser" class="black--text">
            <h2 class="mb-4 body-1 font-weight-bold black--text" style="line-height: 1.25rem;">
              La cantine « {{ duplicateSiretCanteen.name }} » avec le SIRET {{ duplicateSiretCanteen.siret }} fait déjà
              partie de vos cantines.
            </h2>
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
            <h2 class="mb-4 body-1 font-weight-bold black--text" style="line-height: 1.25rem;">
              Il existe déjà une cantine avec le SIRET {{ duplicateSiretCanteen.siret }}
            </h2>
            <div v-if="!requestSent">
              <p>
                La cantine « {{ duplicateSiretCanteen.name }} » est déjà référencée sur notre site mais n'a pas encore
                de gestionnaire enregistré.
              </p>
              <v-btn color="primary" @click="claimCanteen">
                <v-icon class="mr-2">mdi-key</v-icon>
                Revendiquer cette cantine
              </v-btn>
            </div>
            <v-alert v-else type="success" class="mb-0">
              <p class="mb-0">
                Votre demande a bien été prise en compte. Nous reviendrons vers vous au plus vite.
                <router-link class="white--text" :to="{ name: 'ManagementPage' }">
                  Revenir à mes cantines
                </router-link>
              </p>
            </v-alert>
          </div>
          <div v-else class="black--text">
            <h2 class="mb-4 body-1 font-weight-bold black--text" style="line-height: 1.25rem;">
              Il existe déjà une cantine avec le SIRET {{ duplicateSiretCanteen.siret }}
            </h2>
            <div v-if="!requestSent">
              <p>
                Ceci peut arriver lors qu'un autre membre de votre équipe a déjà ajouté votre cantine sur notre site.
                Vous pouvez cependant demander l'accès aux gestionnaires de « {{ duplicateSiretCanteen.name }} »
              </p>
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
            <v-alert v-else type="success" class="mb-0">
              <p class="mb-0">
                Message envoyé,
                <router-link class="white--text" :to="{ name: 'ManagementPage' }">
                  revenir à mes cantines
                </router-link>
              </p>
            </v-alert>
          </div>
        </v-alert>
      </div>

      <v-row class="pa-4">
        <DsfrTextField
          validate-on-blur
          label="SIRET"
          v-model="siret"
          :rules="[validators.length(14), validators.luhn, siretSatelliteValidator()]"
          labelClasses="body-2 mb-2"
          style="max-width: 30rem;"
        />
        <v-btn
          large
          color="primary"
          class="ml-4 align-self-center"
          @click="validateSiret"
          :disabled="!siret && !!duplicateSiretCanteen"
        >
          Valider
        </v-btn>
        <v-btn
          large
          outlined
          color="primary"
          v-if="backTo && (!canteen || !canteen.siret)"
          class="ml-4 align-self-center"
          :to="backTo"
        >
          Annuler
        </v-btn>
      </v-row>
    </v-form>
  </div>
</template>

<script>
import validators from "@/validators"
import DsfrTextField from "@/components/DsfrTextField"
import DsfrTextarea from "@/components/DsfrTextarea"

export default {
  name: "SiretCheck",
  components: { DsfrTextField, DsfrTextarea },
  props: ["canteen", "backTo", "allowDuplicates"],
  data() {
    const user = this.$store.state.loggedUser
    return {
      siret: this.canteen?.siret,
      duplicateSiretCanteen: undefined,
      user,
      fromName: `${user.firstName} ${user.lastName}`,
      messageJoinCanteen: null,
      requestSent: false,
      showProgressIndicator: false,
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

      if (this.canteen?.siret && this.siret === this.canteen?.siret) {
        this.$emit("siretIsValid", this.siret)
        return
      }

      this.showProgressIndicator = true
      return fetch("/api/v1/canteenStatus/siret/" + this.siret)
        .then((response) => response.json())
        .then((response) => {
          const isDuplicateSiret = !!response.id

          if (!isDuplicateSiret) return this.saveSiretIfNeeded().then(() => this.$emit("siretIsValid", response))

          if (this.allowDuplicates) return this.$emit("duplicateCanteenFound", response)

          this.siret = null
          this.requestSent = false
          this.duplicateSiretCanteen = response
        })
        .finally(() => (this.showProgressIndicator = false))
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
          this.requestSent = true
          this.$store.dispatch("notify", {
            status: "success",
            message: `Votre message a bien été envoyé.`,
          })
          window.scrollTo(0, 0)
        })
        .catch((e) => this.$store.dispatch("notifyServerError", e))
    },
    claimCanteen() {
      const canteenId = this.duplicateSiretCanteen.id
      return this.$store
        .dispatch("claimCanteen", { canteenId })
        .then(() => (this.requestSent = true))
        .catch((e) => this.$store.dispatch("notifyServerError", e))
    },
    saveSiretIfNeeded() {
      if (!this.canteen?.id) return Promise.resolve()
      const payload = { siret: this.siret }
      return this.$store.dispatch("updateCanteen", { id: this.canteen?.id, payload }).then((canteen) => {
        this.$store.dispatch("notify", {
          status: "success",
          message: "Votre SIRET a bien été mis à jour",
        })
        this.$emit("updateCanteen", canteen)
      })
    },
    siretSatelliteValidator() {
      if (!this.canteen?.centralProducerSiret) return true
      const message =
        "Le numéro SIRET de la cuisine centrale ne peut pas être le même que celui de la cantine satellite."
      return validators.isDifferent(this.canteen?.centralProducerSiret, message)
    },
  },
}
</script>
