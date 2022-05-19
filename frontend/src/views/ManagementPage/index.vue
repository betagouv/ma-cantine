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
    <CompleteProfileField />
    <div class="mt-4">
      <h1 class="my-4 text-h5 font-weight-black">Mes cantines</h1>
      <CanteensPagination v-on:canteen-count="canteenCount = $event" />
    </div>
    <PageSatisfaction />
    <div class="mt-12 mb-8">
      <h2 class="text-h5 font-weight-black mb-4">Mes outils</h2>
      <UserTools />
    </div>
  </div>
</template>

<script>
import CanteensPagination from "./CanteensPagination.vue"
import PageSatisfaction from "@/components/PageSatisfaction.vue"
import UserTools from "./UserTools"
import CompleteProfileField from "./CompleteProfileField"
import validators from "@/validators"

export default {
  components: { CanteensPagination, UserTools, CompleteProfileField, PageSatisfaction },
  data() {
    return {
      validators,
      canteenCount: undefined,
    }
  },
  computed: {
    loggedUser() {
      return this.$store.state.loggedUser
    },
  },
}
</script>
