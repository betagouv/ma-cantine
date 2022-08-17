<template>
  <div>
    <v-list-item>
      <v-list-item-icon>
        <v-icon :color="isInvitation ? 'secondary' : 'primary'">
          {{ isInvitation ? "mdi-account-clock" : "mdi-account-check" }}
        </v-icon>
      </v-list-item-icon>
      <v-list-item-content>
        <v-list-item-title
          v-text="isInvitation ? manager.email : `${manager.firstName} ${manager.lastName}`"
        ></v-list-item-title>
        <v-list-item-subtitle>
          <span v-if="isInvitation">Invitation envoyée</span>
          <span v-else-if="$store.state.loggedUser.email === manager.email">
            Vous êtes gestionnaire de cette cantine
          </span>
          <span v-else>{{ manager.email }}</span>
        </v-list-item-subtitle>
      </v-list-item-content>
      <AdminRemovalDialog v-if="showDeleteButton" :manager="manager" v-model="dialog" @delete="deleteManager" />
    </v-list-item>
    <v-divider class="my-1"></v-divider>
  </div>
</template>

<script>
import AdminRemovalDialog from "./AdminRemovalDialog"

export default {
  components: { AdminRemovalDialog },
  data() {
    return {
      dialog: false,
    }
  },
  props: {
    manager: {
      type: Object,
      required: true,
    },
  },
  computed: {
    isInvitation() {
      return !this.manager.lastName
    },
    showDeleteButton() {
      return this.$store.state.loggedUser.email !== this.manager.email
    },
  },
  methods: {
    deleteManager() {
      this.$emit("delete", this.manager)
      this.dialog = false
    },
  },
}
</script>
