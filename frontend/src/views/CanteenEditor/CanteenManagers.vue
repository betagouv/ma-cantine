<template>
  <div class="text-left pb-10">
    <h1 class="font-weight-black text-h4 my-4">
      Gestionnaires
    </h1>
    <p class="body-1">
      Tous les gestionnaires peuvent modifier et supprimer une cantine, ainsi qu'ajouter et enlever autres
      gestionnaires.
    </p>
    <v-list>
      <ManagerItem @delete="deleteManager" v-for="manager in managers" :key="manager.email" :manager="manager" />
    </v-list>
    <v-list>
      <p class="text-body-1 font-weight-black" v-if="managerInvitations && managerInvitations.length > 0">
        Invitations en cours
      </p>
      <ManagerItem
        @delete="deleteManager"
        v-for="manager in managerInvitations"
        :key="manager.email"
        :manager="manager"
      />
    </v-list>
    <v-row>
      <v-col cols="12" sm="10" md="8">
        <v-form ref="managerForm" class="mt-3 px-2" v-model="managerFormIsValid" v-on:submit.prevent="addManager">
          <p class="body-2 mb-2 text-left grey--text text--darken-1">Ajouter un gestionnaire</p>
          <div class="d-flex align-center">
            <DsfrTextField
              v-model="newManagerEmail"
              label="Adresse email"
              :rules="[validators.emailOrEmpty]"
              class="flex-grow-1"
              validate-on-blur
            />
            <v-btn
              @click="addManager"
              outlined
              color="primary darken-1"
              class="ml-4 mt-1"
              large
              :disabled="!newManagerEmail"
            >
              Ajouter
            </v-btn>
          </div>
        </v-form>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import ManagerItem from "./ManagerItem"
import validators from "@/validators"
import DsfrTextField from "@/components/DsfrTextField"

export default {
  name: "CanteenManagers",
  components: { ManagerItem, DsfrTextField },
  props: {
    originalCanteen: {
      type: Object,
      required: true,
    },
  },
  created() {
    document.title = `Gestionnaires - ${this.originalCanteen.name} - ${this.$store.state.pageTitleSuffix}`
  },
  data() {
    return {
      managerFormIsValid: true,
      newManagerEmail: this.$route.query.email,
    }
  },
  computed: {
    validators() {
      return validators
    },
    managers() {
      const managersCopy = [...this.originalCanteen.managers]
      const loggedUserIndex = managersCopy.findIndex((x) => x.email === this.$store.state.loggedUser.email)
      managersCopy.splice(0, 0, managersCopy.splice(loggedUserIndex, 1)[0])
      return managersCopy
    },
    managerInvitations() {
      return this.originalCanteen.managerInvitations
    },
  },
  methods: {
    addManager() {
      this.$refs.managerForm.validate()

      if (!this.managerFormIsValid) {
        this.$store.dispatch("notifyRequiredFieldsError")
        return
      }

      this.$store
        .dispatch("addManager", {
          canteenId: this.originalCanteen.id,
          email: this.newManagerEmail.trim(),
        })
        .then((managementTeam) => {
          this.$store.dispatch("notify", {
            title: "Mise à jour prise en compte",
            message: `${this.newManagerEmail} a bien été ajouté`,
            status: "success",
          })
          this.newManagerEmail = undefined
          this.originalCanteen.managers = managementTeam["managers"]
          this.originalCanteen.managerInvitations = managementTeam["managerInvitations"]
        })
        .catch((e) => {
          this.$store.dispatch("notifyServerError", e)
          this.newManagerEmail = undefined
        })
    },
    deleteManager(manager) {
      this.$store
        .dispatch("removeManager", {
          canteenId: this.originalCanteen.id,
          email: manager.email.trim(),
        })
        .then((managementTeam) => {
          this.$store.dispatch("notify", {
            title: "Mise à jour prise en compte",
            message: `${manager.email} n'est plus gestionnaire de cette cantine`,
            status: "success",
          })
          this.originalCanteen.managers = managementTeam["managers"]
          this.originalCanteen.managerInvitations = managementTeam["managerInvitations"]
        })
        .catch((e) => {
          this.$store.dispatch("notifyServerError", e)
        })
    },
  },
}
</script>
