<template>
  <DsfrCallout icon=" ">
    <div class="ml-n4">
      <p class="text-body-1 font-weight-bold">
        Ajoutez un aperçu sur votre site
      </p>
      <div class="text-body-2" style="font-family: monospace;">
        <DsfrTextField class="widget-text-field" :value="iframeCodeSnippet" readonly hide-details />
        <div class="d-flex mt-6 mb-2">
          <v-btn small color="primary" outlined @click="onWidgetCopy">
            <v-icon small class="mr-2">$clipboard-fill</v-icon>
            Copier
          </v-btn>
          <div class="green--text text--darken-3 ml-4 mt-1" v-if="showCopySuccessMessage">
            <v-icon small color="success">$checkbox-circle-fill</v-icon>
            Copié
          </div>
        </div>
      </div>
    </div>
  </DsfrCallout>
</template>

<script>
import DsfrCallout from "@/components/DsfrCallout"
import DsfrTextField from "@/components/DsfrTextField"

export default {
  name: "AddPublishedCanteenWidget",
  props: {
    canteen: {
      type: Object,
      required: true,
    },
  },
  components: { DsfrCallout, DsfrTextField },
  data() {
    return {
      showCopySuccessMessage: false,
    }
  },
  computed: {
    iframeCodeSnippet() {
      const pathname = this.$router.resolve({
        name: "CanteenPage",
        params: { canteenUrlComponent: this.$store.getters.getCanteenUrlComponent(this.canteen) },
      }).href
      const url = `${window.location.origin}/widgets${pathname}`
      return `<iframe src='${url}' style='width: 480px; height: 420px;' scrolling='no'></iframe>`
    },
  },
  methods: {
    onWidgetCopy() {
      navigator.clipboard.writeText(this.iframeCodeSnippet)
      this.showCopySuccessMessage = true
      setTimeout(() => (this.showCopySuccessMessage = false), 3000)
    },
  },
}
</script>

<style scoped>
.widget-text-field >>> .v-input .v-input__slot {
  background: white !important;
}
</style>
