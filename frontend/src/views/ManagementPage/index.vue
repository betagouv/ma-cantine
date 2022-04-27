<template>
  <div class="text-left">
    <div class="mt-4">
      <p class="my-2 text-body-1 font-weight-bold">
        Bienvenue {{ loggedUser.firstName }}
        <v-btn text class="text-decoration-underline text-caption mb-1" :to="{ name: 'AccountEditor' }">
          <v-icon class="mr-1" small>mdi-pencil</v-icon>
          Modifier mon profil
        </v-btn>
      </p>
    </div>
    <v-sheet v-if="askForRole" class="mt-4 mb-8">
      <v-form v-model="roleFormIsValid" ref="roleForm" @submit.prevent>
        <fieldset class="pa-4" style="border-radius: 10px;">
          <legend class="d-flex pr-2">
            <v-badge dot inline></v-badge>
            <p class="text--body-2 primary--text mb-0">Veuillez completer votre profil :</p>
          </legend>
          <v-row>
            <v-col cols="7">
              <v-select
                label="Choisir votre fonction"
                v-model="role"
                :items="roleOptions"
                :rules="[validators.required]"
                solo
                hide-details="auto"
              ></v-select>
            </v-col>
            <v-col cols="7" v-if="showOtherField" class="my-0">
              <v-text-field
                label="Ma fonction"
                :rules="[validators.required]"
                solo
                v-model="otherRoleDetail"
                hide-details="auto"
              ></v-text-field>
            </v-col>
            <v-col>
              <v-btn color="primary" height="3.5em" @click="updateRole">Valider</v-btn>
            </v-col>
          </v-row>
        </fieldset>
      </v-form>
    </v-sheet>
    <div class="mt-4">
      <h1 class="my-4 text-h5 font-weight-black">Mes cantines</h1>
      <CanteensPagination />
    </div>
    <div class="mt-12 mb-8">
      <h2 class="text-h5 font-weight-black mb-4">Mes outils</h2>
      <UserTools />
    </div>
  </div>
</template>

<script>
import CanteensPagination from "./CanteensPagination.vue"
import UserTools from "./UserTools"
import validators from "@/validators"

export default {
  components: { CanteensPagination, UserTools },
  data() {
    return {
      validators,
      role: undefined,
      otherRoleDetail: undefined,
      roleOptions: [
        {
          text: "Gestionnaire d'établissement",
          value: "managerEstablishment",
        },
        {
          text: "Direction Achat Société de restauration",
          value: "purchasesManager",
        },
        {
          text: "Responsable d'achats en gestion directe",
          value: "purchasesManager",
        },
        {
          text: "Responsable de plusieurs établissements (type cuisine centrale)",
          value: "managerCentral",
        },
        {
          text: "Responsable de plusieurs établissements (SRC)",
          value: "managerSociety",
        },
        {
          text: "Autre (spécifiez)",
          value: "other",
        },
      ],
      roleFormIsValid: true,
    }
  },
  computed: {
    loggedUser() {
      return this.$store.state.loggedUser
    },
    askForRole() {
      // TODO: check if user has any canteens as well
      return !this.loggedUser.role
    },
    showOtherField() {
      return this.role === "other"
    },
  },
  methods: {
    updateRole() {
      this.$refs.roleForm.validate()
      if (!this.roleFormIsValid) {
        this.$store.dispatch("notifyRequiredFieldsError")
        return
      }
      let payload = { role: this.role }
      if (this.showOtherField) {
        payload.otherRoleDetail = this.otherRoleDetail
      }
      this.$store
        .dispatch("updateProfile", { payload })
        .then(() => {
          this.bypassLeaveWarning = true
          this.$store.dispatch("notify", {
            title: "Merci, votre poste a été sauvegardé",
            message: "Vous pourrez le modifier depuis votre profil",
            status: "success",
          })
          this.$router.push({ name: "ManagementPage" })
        })
        .catch((e) => {
          this.$store.dispatch("notifyServerError", e)
        })
    },
  },
}
</script>
