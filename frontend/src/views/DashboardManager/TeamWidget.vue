<template>
  <v-card outlined class="fill-height d-flex flex-column pa-4">
    <v-card-title class="fr-h4">
      Mon équipe
    </v-card-title>
    <v-card-text class="fill-height">
      <div v-if="managers.length > 1" class="fill-height d-flex flex-column">
        <p class="fr-text mb-0 grey--text text--darken-3">
          {{ managers.length }} personnes (dont vous) peuvent actuellement modifier cet établissement et ajouter des
          données.
        </p>
        <v-spacer></v-spacer>
        <ul class="pl-0 fr-text-xs grey--text text--darken-2 mb-n2">
          <li v-for="manager in managers" :key="manager.email" class="mb-4">
            <v-row class="align-center mx-0">
              <v-icon small class="mr-2">
                {{ manager.isInvite ? "$user-add-line" : "$user-line" }}
              </v-icon>
              {{ manager.isInvite ? manager.email : `${manager.firstName} ${manager.lastName}` }}
              <span v-if="manager.email === loggedUser.email" class="ml-1">(vous)</span>
            </v-row>
          </li>
        </ul>
        <v-spacer></v-spacer>
      </div>
      <p class="fr-text grey--text text--darken-3" v-else>
        Actuellement, vous êtes la seule personne qui peut modifier cet établissement et ajouter des données.
      </p>
    </v-card-text>
    <v-spacer></v-spacer>
    <v-card-actions>
      <v-btn
        :to="{
          name: 'CanteenManagers',
          params: { canteenUrlComponent: this.$store.getters.getCanteenUrlComponent(canteen) },
        }"
        outlined
        color="primary"
        class="mx-2 mb-2"
      >
        Modifier
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
export default {
  name: "TeamWidget",
  props: {
    canteen: {
      type: Object,
      required: true,
    },
  },
  computed: {
    loggedUser() {
      return this.$store.state.loggedUser
    },
    managers() {
      if (!this.canteen) []
      const managersCopy = [...this.canteen.managers]
      const loggedUserIndex = managersCopy.findIndex((x) => x.email === this.loggedUser.email)
      managersCopy.splice(0, 0, managersCopy.splice(loggedUserIndex, 1)[0])
      return managersCopy.concat(this.managerInvitations)
    },
    managerInvitations() {
      return (
        this.canteen?.managerInvitations.map((i) => {
          i.isInvite = true
          return i
        }) || []
      )
    },
  },
}
</script>

<style scoped>
ul {
  list-style: none;
}
/* https://developer.mozilla.org/en-US/docs/Web/CSS/list-style-type#accessibility_concerns */
ul li::before {
  content: "\200B";
}
</style>
