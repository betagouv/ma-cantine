<script setup>
import { onMounted, reactive, watch, inject } from "vue"
import { useVuelidate } from "@vuelidate/core"
import { formatError } from "@/utils.js"
import HelpText from "./HelpText.vue"
import DsfrBooleanRadio from "@/components/DsfrBooleanRadio.vue"
import { useValidators } from "@/validators.js"
const { required } = useValidators()

const emit = defineEmits(["provide-vuelidate", "update-payload"])

const originalPayload = inject("originalPayload")
const payload = reactive({})

const rules = {
  isSortedBySource: { required },
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

  payload.isSortedBySource = originalPayload.isSortedBySource
})
</script>

<template>
  <div class="fr-grid-row">
    <div class="fr-col-12 fr-col-sm-6">
      <DsfrBooleanRadio
        v-model="payload.isSortedBySource"
        legend="Avez-vous trié vos déchets en fonction de leur source ?"
        name="isSortedBySource"
        class="fr-mb-2w"
        :error-message="formatError(v$.isSortedBySource)"
      />
    </div>
    <div class="fr-col-sm-6">
      <HelpText>
        <p class="fr-mb-0">
          Cela signifie procéder à des pesées séparées en fonction de la source des déchets : restes assiettes,
          excédents présentés aux convives et non servis ou non valorisés, et excédents de préparation.
        </p>
      </HelpText>
    </div>
  </div>
</template>
