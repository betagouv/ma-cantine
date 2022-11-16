<template>
  <div>
    <h1 class="font-weight-black text-h4 my-4">Publier mes satellites</h1>
    <p>
      « {{ originalCanteen.name }} » est une cuisine centrale sans lieu de consommation. La publication concerne
      <b>uniquement les lieux de restauration recevant des convives.</b>
    </p>
    <p>
      Vous pouvez
      <router-link :to="{ name: 'NewCanteen' }">ajouter une cantine satellite</router-link>
      ou indiquer que
      <router-link
        :to="{
          name: 'CanteenModification',
          params: { canteenUrlComponent: $store.getters.getCanteenUrlComponent(originalCanteen) },
        }"
      >
        votre cantine reçoit des convives sur place.
      </router-link>
    </p>
    <p v-if="publicationRequested">
      Précédemment vous aviez choisi de publier cette cantine. En tant que cuisine centrale, vous pouvez désormais
      retirer cette publication.
    </p>
    <v-sheet v-if="publicationRequested" rounded color="grey lighten-4 pa-3 my-6" class="d-flex">
      <v-spacer></v-spacer>
      <v-btn x-large color="primary" @click="removeCanteenPublication">
        Retirer la publication
      </v-btn>
    </v-sheet>
  </div>
</template>

<script>
export default {
  name: "CentralKitchenPublication",
  props: {
    originalCanteen: {
      type: Object,
    },
  },
  data() {
    return {
      publicationRequested: true,
    }
  },
  methods: {
    removeCanteenPublication() {
      console.log("TODO: refactor to be an emit")
    },
  },
}
</script>
