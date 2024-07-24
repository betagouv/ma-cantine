<script setup>
import { onMounted, reactive, watch, computed, ref } from "vue"
import { useVuelidate } from "@vuelidate/core"
import { required, decimal, maxValue } from "@vuelidate/validators"
import { formatError } from "@/utils.js"
import HelpText from "./HelpText.vue"
import DsfrBooleanRadio from "@/components/DsfrBooleanRadio.vue"

const emit = defineEmits(["provide-vuelidate", "update-payload"])

const payload = reactive({
  preparationExcess: undefined,
  sortedEdible: undefined,
  ediblePreparationExcess: undefined,
  inediblePreparationExcess: undefined,
})

const rules = {
  preparationExcess: { decimal },
  sortedEdible: { required },
  ediblePreparationExcess: { decimal, maxValue: maxValue(computed(() => payload.preparationExcess)) },
  inediblePreparationExcess: { decimal, maxValue: maxValue(computed(() => payload.preparationExcess)) },
}

const v$ = useVuelidate(rules, payload)

const updatePayload = () => {
  emit("update-payload", payload)
}

const specifySortedExcess = computed(() => {
  return !!payload.preparationExcess && payload.sortedEdible
})

const userChoices = {
  edible: "edible",
  inedible: "inedible",
}
const userChoice = ref()

const userChose = (type) => {
  userChoice.value = type
}

const resetCalculationMaybe = () => {
  if (payload.ediblePreparationExcess === "" || payload.inediblePreparationExcess === "") {
    userChoice.value = undefined
    payload.ediblePreparationExcess = undefined
    payload.inediblePreparationExcess = undefined
  }
}

const calculateOtherWeight = () => {
  // TODO: handle floating point errors
  if (userChoice.value === userChoices.edible) {
    payload.inediblePreparationExcess = payload.preparationExcess - payload.ediblePreparationExcess
  } else if (userChoice.value === userChoices.inedible) {
    payload.ediblePreparationExcess = payload.preparationExcess - payload.inediblePreparationExcess
  }
}

watch(payload, () => {
  resetCalculationMaybe()
  calculateOtherWeight()
  updatePayload()
})

onMounted(() => {
  emit("provide-vuelidate", v$)
})
</script>

<template>
  <div class="fr-grid-row">
    <div class="fr-col-sm-6">
      <DsfrInputGroup
        v-model.number="payload.preparationExcess"
        type="number"
        label="Masse de gaspillage pour les excédents de préparation"
        hint="En kg (optionnel)"
        label-visible
        class="fr-mb-2w"
        :error-message="formatError(v$.preparationExcess)"
      />
      <DsfrBooleanRadio
        v-model.number="payload.sortedEdible"
        legend="Avez-vous trié entre comestible et non-comestible&nbsp;?"
        name="sortedEdible"
        class="fr-mb-2w"
        :error-message="formatError(v$.sortedEdible)"
      />
    </div>
    <div v-if="!specifySortedExcess" class="fr-col-sm-6">
      <HelpText question="À quoi correspondent les excédents de préparation ?">
        <p>
          Par exemple, si vous avez jeté des épluchures, des parures ou si vous avez des ingrédients excédentaires que
          vous ne réutiliserez pas, il s’agit d’excédents de préparation. Dans le cas où vous avez mesuré les denrées en
          stock que vous avez jetées durant la période de mesure (du type yaourts à DLC dépassée, salades pourries,
          ...), les excédents de préparation incluent ces déchets issus de stocks.
        </p>
        <p>
          Les parties des denrées alimentaires considérées comme non comestibles incluent les os, les arrêtes, les
          noyaux, les trognons de pommes, les épluchures... Les parties considérées comme comestibles incluent les
          morceaux de viande restants, les pâtes restant dans les assiettes, le pain restant au niveau des plateaux...
        </p>
      </HelpText>
    </div>
    <!-- TODO: styling with border and padding -->
    <div v-else class="fr-col-sm-6">
      <DsfrInputGroup
        v-model.number="payload.ediblePreparationExcess"
        type="number"
        label="Total du gaspillage de denrées comestibles"
        hint="En kg (optionnel)"
        label-visible
        class="fr-mb-2w"
        :error-message="formatError(v$.ediblePreparationExcess)"
        @keydown="userChose(userChoices.edible)"
        :disabled="userChoice === userChoices.inedible"
      />
      <DsfrInputGroup
        v-model.number="payload.inediblePreparationExcess"
        type="number"
        label="Total du gaspillage de denrées comestibles"
        hint="En kg (optionnel)"
        label-visible
        class="fr-mb-2w"
        :error-message="formatError(v$.inediblePreparationExcess)"
        @keydown="userChose(userChoices.inedible)"
        :disabled="userChoice === userChoices.edible"
      />
    </div>
  </div>
</template>
