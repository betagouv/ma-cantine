<script setup>
import { onMounted, reactive, watch } from "vue"
import { useVuelidate } from "@vuelidate/core"
import { required } from "@vuelidate/validators"
import { formatError } from "@/utils.js"
import HelpText from "./HelpText.vue"

const emit = defineEmits(["provide-vuelidate", "update-payload"])

const questionName = "distinction"
const yesNoOptions = [
  {
    label: "Oui",
    id: `${questionName}-yes`,
    value: true,
  },
  {
    label: "Non",
    id: `${questionName}-no`,
    value: false,
  },
]

const payload = reactive({
  sorted: undefined,
})

const rules = {
  sorted: { required },
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
      <DsfrRadioButtonSet
        v-model.number="payload.sorted"
        legend="Avez-vous trié votre gaspillage en fonction de sa source ?"
        :name="questionName"
        :options="yesNoOptions"
        class="fr-mb-2w"
        :error-message="formatError(v$.sorted)"
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
