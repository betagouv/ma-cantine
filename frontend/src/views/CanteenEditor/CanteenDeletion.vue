<template>
  <DeletionDialog v-model="deletionDialog" @delete="deleteCanteen" :canteen="originalCanteen" />
</template>

<script>
import DeletionDialog from "./DeletionDialog"

export default {
  name: "CanteenDeletion",
  components: { DeletionDialog },
  props: {
    originalCanteen: {
      type: Object,
      required: true,
    },
  },
  created() {
    document.title = `Supprimer - ${this.originalCanteen.name} - ma-cantine.beta.gouv.fr`
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
        .catch(() => {
          this.$store.dispatch("notifyServerError")
        })
    },
  },
}
</script>
