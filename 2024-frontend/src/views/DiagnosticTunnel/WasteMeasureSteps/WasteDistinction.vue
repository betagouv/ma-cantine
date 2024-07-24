<script setup>
import { onMounted, reactive, watch, inject } from "vue"
import { useVuelidate } from "@vuelidate/core"
import { required } from "@vuelidate/validators"
import { formatError } from "@/utils.js"
import HelpText from "./HelpText.vue"
import DsfrBooleanRadio from "@/components/DsfrBooleanRadio.vue"

const emit = defineEmits(["provide-vuelidate", "update-payload"])

const originalPayload = inject("originalPayload")
// TODO: show remaining steps only if this is true ?
const payload = reactive({
  sortedSource: originalPayload.sortedSource,
})

const rules = {
  sortedSource: { required },
}

const v$ = useVuelidate(rules, payload)

const updatePayload = () => {
  emit("update-payload", payload)
}

watch(payload, () => {
  updatePayload()
})

onMounted(() => {
  emit("provide-vuelidate", v$)
})
</script>

<template>
  <div class="fr-grid-row">
    <div class="fr-col-12 fr-col-sm-6">
      <DsfrBooleanRadio
        v-model.number="payload.sortedSource"
        legend="Avez-vous trié votre gaspillage en fonction de sa source ?"
        name="sortedSource"
        class="fr-mb-2w"
        :error-message="formatError(v$.sortedSource)"
      />
    </div>
    <div class="fr-col-sm-6">
      <HelpText>
        <p>
          Cela signifie procéder à des pesées séparées en fonction de la source de gaspillage : restes assiettes,
          excédents présentés aux convives et non servis, et excédents de préparation.
        </p>
      </HelpText>
    </div>
  </div>
</template>
