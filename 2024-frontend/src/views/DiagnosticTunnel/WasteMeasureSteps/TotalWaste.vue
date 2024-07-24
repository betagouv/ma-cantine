<script setup>
import { onMounted, reactive, watch, inject } from "vue"
import { useVuelidate } from "@vuelidate/core"
import { required, decimal, minValue } from "@vuelidate/validators"
import { formatError } from "@/utils.js"
import HelpText from "./HelpText.vue"

const emit = defineEmits(["provide-vuelidate", "update-payload"])

const originalPayload = inject("originalPayload")

const payload = reactive({
  total: originalPayload.total,
})

const rules = {
  total: { required, decimal, minValue: minValue(1) },
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
      <DsfrInputGroup
        v-model.number="payload.total"
        type="number"
        label="Masse totale de gaspillage relevée sur la période de mesure"
        hint="en kg"
        label-visible
        class="fr-mb-2w"
        :error-message="formatError(v$.total)"
      />
    </div>
    <div class="fr-col-sm-6">
      <HelpText question="Dois-je compter les os et les épluchures ?">
        <p>
          Inutile à ce stade de différencier les denrées comestibles et non comestibles. Si vous l’avez fait, vous
          pourrez saisir les données détaillées aux étapes suivantes.
        </p>
      </HelpText>
    </div>
  </div>
</template>
