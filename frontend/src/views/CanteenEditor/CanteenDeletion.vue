<template>
  <div class="text-left pb-10" v-if="originalCanteen">
    <h1 class="font-weight-black text-h4 my-4">
      Supprimer ma cantine
    </h1>
    <p class="body-1 mb-10">
      La suppression d'une cantine entraîne aussi celle des diagnostics associés. Aucun gestionnaire ne sera en mesure
      d'accéder aux données après la suppression.
    </p>
    <DeletionDialog v-model="deletionDialog" @delete="deleteCanteen" :canteen="originalCanteen" />
  </div>
</template>

<script>
import DeletionDialog from "./DeletionDialog"

export default {
  name: "CanteenDeletion",
  components: { DeletionDialog },
  props: {
    originalCanteen: {
      type: Object,
    },
  },
  created() {
    document.title = `Supprimer - ${this.originalCanteen?.name || ""} - ${this.$store.state.pageTitleSuffix}`
  },
  data() {
    return {
      deletionDialog: false,
    }
  },
  methods: {
    deleteCanteen() {
      this.$store
        .dispatch("deleteCanteen", { id: this.originalCanteen.id })
        .then(() => {
          this.$store.dispatch("notify", {
            message:
              "Votre cantine a bien été supprimée. En cas d'erreur vous pouvez nous contacter à l'adresse contact@egalim.beta.gouv.fr",
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
