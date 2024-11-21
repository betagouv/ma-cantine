<script setup>
import { onMounted, reactive, watch, inject } from "vue"
import { useVuelidate } from "@vuelidate/core"
import { formatError } from "@/utils.js"
import HelpText from "./HelpText.vue"
import { useValidators } from "@/validators.js"
const { required, decimal, minValue } = useValidators()

const emit = defineEmits(["provide-vuelidate", "update-payload"])

const originalPayload = inject("originalPayload")

const payload = reactive({})

const rules = {
  totalMass: { required, decimal, minValue: minValue(1) },
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

  payload.totalMass = originalPayload.totalMass
})
</script>

<template>
  <div class="fr-grid-row justify-space-between">
    <div class="fr-col-12 fr-col-sm-5">
      <DsfrInputGroup
        v-model.number="payload.totalMass"
        type="number"
        label="Masse totale des déchets alimentaires relevée sur la période de mesure"
        hint="en kg"
        label-visible
        class="fr-mb-2w"
        :error-message="formatError(v$.totalMass)"
      />
    </div>
    <div class="fr-col-sm-6">
      <HelpText>
        <p class="fr-mb-0">
          Les déchets alimentaires incluent une fraction comestible (assimilable à du gaspillage alimentaire) et une
          fraction non comestible (os, épluchures, arêtes).
        </p>
      </HelpText>
    </div>
  </div>
</template>
