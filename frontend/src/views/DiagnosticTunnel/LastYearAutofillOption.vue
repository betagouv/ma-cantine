<template>
  <DsfrCallout v-if="lastYearDiagnostic">
    <div>
      <p>
        Voulez-vous completer votre bilan avec les réponses de l'année {{ lastYearDiagnostic.year }} ? Vous pouvez
        modifier les réponses après.
      </p>
      <v-btn outlined color="primary" @click="fillFromLastYear">Compléter les réponses</v-btn>
    </div>
  </DsfrCallout>
</template>

<script>
import DsfrCallout from "@/components/DsfrCallout"

export default {
  name: "LastYearAutofillOption",
  props: {
    canteen: {
      type: Object,
      required: true,
    },
    diagnostic: {
      type: Object,
      required: true,
    },
    fields: {
      type: Array,
      required: true,
    },
  },
  components: {
    DsfrCallout,
  },
  computed: {
    lastYearDiagnostic() {
      return this.canteen.diagnostics?.find((d) => d.year === this.diagnostic.year - 1)
    },
  },
  methods: {
    fillFromLastYear() {
      const payload = {}
      this.fields.forEach((f) => (payload[f] = this.lastYearDiagnostic[f]))
      this.$emit("tunnel-autofill", {
        payload,
        message: {
          status: "success",
          message: "Vos réponses on été rapportés dans votre bilan.",
        },
      })
    },
  },
}
</script>
