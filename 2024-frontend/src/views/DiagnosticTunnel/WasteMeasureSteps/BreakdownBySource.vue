<script setup>
import { onMounted, reactive, watch, computed, ref, inject, nextTick, defineProps } from "vue"
import { useVuelidate } from "@vuelidate/core"
import { required, decimal, minValue, maxValue } from "@vuelidate/validators"
import { formatError } from "@/utils.js"
import HelpText from "./HelpText.vue"
import DsfrBooleanRadio from "@/components/DsfrBooleanRadio.vue"

const props = defineProps(["data"])
const sources = {
  preparation: {
    totalKey: "preparationTotal",
    sortedKey: "preparationSorted",
    edibleKey: "preparationEdible",
    inedibleKey: "preparationInedible",
    title: "Excédents de préparation",
    primaryLabel: "Masse de gaspillage pour les excédents de préparation",
    description:
      "Par exemple, si vous avez jeté des épluchures, des parures ou si vous avez des ingrédients excédentaires que vous ne réutiliserez pas, il s’agit d’excédents de préparation",
    edibleHelp:
      "Les parties des denrées alimentaires considérées comme non comestibles incluent les os, les morceaux de gras retirés du reste des pièces de viande, les épluchures, les yaourts jetés ayant une DLC dépassée, les fonds de pots de crèmes ou de sauces non valorisés et jetés, les fruits et légumes non présentés et non valorisés du fait de leur mauvaise apparence, ...",
  },
  unserved: {
    totalKey: "unservedTotal",
    sortedKey: "unservedSorted",
    edibleKey: "unservedEdible",
    inedibleKey: "unservedInedible",
    title: "Denrées présentées aux convives mais non servies",
    primaryLabel: "Masse de gaspillage pour les denrées présentées aux convives mais non servies",
    description:
      "Par exemple, si vous présentez en vitrine un nombre excédentaire de salades, de parts de tarte aux pommes et que ces denrées supplémentaires ne sont ni consommées ni valorisées, il s’agit d’excédents présentés aux convives et non servis",
    edibleHelp:
      "Les parties des denrées alimentaires considérées comme non comestibles incluent les os, les arrêtes, les noyaux, les trognons de pommes, les épluchures... Les parties considérées comme comestibles incluent les morceaux de viande restants, les pâtes restant dans les assiettes, le pain restant au niveau des plateaux...",
  },
  leftovers: {
    totalKey: "leftoversTotal",
    sortedKey: "leftoversSorted",
    edibleKey: "leftoversEdible",
    inedibleKey: "leftoversInedible",
    title: "Reste assiette",
    primaryLabel: "Masse de gaspillage pour le reste assiette",
    description:
      "Il s’agit de l’ensemble des restes alimentaires des plateaux repas /assiettes incluant les os, noyaux et épluchures",
    edibleHelp:
      "Les parties des denrées alimentaires considérées comme non comestibles incluent les os, les arrêtes, les noyaux, les trognons de pommes, les épluchures... Les parties considérées comme comestibles incluent les morceaux de viande restants, les pâtes restant dans les assiettes, le pain restant au niveau des plateaux...",
  },
}
const source = computed(() => sources[props.data.source])
if (!source.value) console.error("Invalid source :", props.data.source)

const emit = defineEmits(["provide-vuelidate", "update-payload"])

const originalPayload = inject("originalPayload")

const payload = reactive({
  totalKey: originalPayload[source.value.totalKey],
  sortedKey: originalPayload[source.value.sortedKey],
  edibleKey: originalPayload[source.value.edibleKey],
  inedibleKey: originalPayload[source.value.inedibleKey],
})

const genericPayloadKeys = Object.keys(payload)

const rules = {
  totalKey: { decimal, minValue: minValue(0) },
  sortedKey: { required },
  edibleKey: { decimal, maxValue: maxValue(computed(() => payload.totalKey)) },
  inedibleKey: { decimal, maxValue: maxValue(computed(() => payload.totalKey)) },
}

const v$ = useVuelidate(rules, payload)

const updatePayload = () => {
  const payloadForStep = {}
  genericPayloadKeys.forEach((k) => (payloadForStep[source.value[k]] = payload[k]))
  emit("update-payload", payloadForStep)
}

const specifySortedExcess = computed(() => {
  return !!payload.totalKey && payload.sortedKey
})
const leftHandQuestionsClass = computed(() => {
  return !specifySortedExcess.value ? "fr-col-sm-5" : "fr-col-10"
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
  if (payload.edibleKey === "" || payload.inedibleKey === "") {
    userChoice.value = undefined
    payload.edibleKey = undefined
    payload.inedibleKey = undefined
  }
}

const calculateOtherWeight = () => {
  // TODO: handle floating point errors
  if (userChoice.value === userChoices.edible) {
    payload.inedibleKey = payload.totalKey - payload.edibleKey
  } else if (userChoice.value === userChoices.inedible) {
    payload.edibleKey = payload.totalKey - payload.inedibleKey
  }
}

watch(props, () => {
  nextTick().then(() => {
    payload._freezeWatcher = true
    genericPayloadKeys.forEach((k) => (payload[k] = originalPayload[source.value[k]]))
    delete payload._freezeWatcher
  })
})

watch(payload, () => {
  if (!payload._freezeWatcher) {
    resetCalculationMaybe()
    calculateOtherWeight()
    updatePayload()
  }
})

onMounted(() => {
  emit("provide-vuelidate", v$)
})
</script>

<template>
  <div class="fr-grid-row fr-grid-row--middle">
    <div :class="specifySortedExcess ? 'fr-col-sm-6' : ''">
      <div class="fr-grid-row justify-space-between">
        <div :class="leftHandQuestionsClass">
          <DsfrInputGroup
            v-model.number="payload.totalKey"
            type="number"
            :label="source.primaryLabel"
            hint="En kg (optionnel)"
            label-visible
            class="fr-mb-2w"
            :error-message="formatError(v$.totalKey)"
          />
        </div>
        <div v-if="!specifySortedExcess" class="fr-col-sm-6">
          <HelpText question="À quoi cela correspond-il ?">
            <p class="fr-mb-0">
              {{ source.description }}
            </p>
          </HelpText>
        </div>
      </div>
      <div class="fr-grid-row justify-space-between fr-mt-4w">
        <div :class="leftHandQuestionsClass">
          <!-- TODO: maybe reset validation if go from yes to no? -->
          <DsfrBooleanRadio
            v-model.number="payload.sortedKey"
            legend="Avez-vous trié entre comestible et non-comestible&nbsp;?"
            name="sortedKey"
            class="fr-mb-2w"
            :error-message="formatError(v$.sortedKey)"
          />
        </div>
        <div v-if="!specifySortedExcess" class="fr-col-sm-6">
          <HelpText>
            <p class="fr-mb-0">
              {{ source.edibleHelp }}
            </p>
          </HelpText>
        </div>
      </div>
    </div>
    <!-- TODO: indication which field is calculated -->
    <div v-if="specifySortedExcess" class="sorted-inputs fr-col-sm-6">
      <div class="fr-grid-row fr-grid-row--middle fr-mb-4w">
        <p class="source-title-tooltip fr-mb-0">
          {{ source.title }}
        </p>
        <DsfrTooltip :content="source.edibleHelp" />
      </div>
      <DsfrInputGroup
        v-model.number="payload.edibleKey"
        type="number"
        label="Total du gaspillage de denrées comestibles"
        hint="En kg (optionnel)"
        label-visible
        class="fr-mb-2w"
        :error-message="formatError(v$.edibleKey)"
        @keydown="userChose(userChoices.edible)"
        :disabled="userChoice === userChoices.inedible"
      />
      <!-- TODO: not sure keydown is best - can scroll -->
      <DsfrInputGroup
        v-model.number="payload.inedibleKey"
        type="number"
        label="Total du gaspillage de denrées non comestibles"
        hint="En kg (optionnel)"
        label-visible
        class="fr-mb-2w"
        :error-message="formatError(v$.inedibleKey)"
        @keydown="userChose(userChoices.inedible)"
        :disabled="userChoice === userChoices.edible"
      />
      <p class="calculation-info fr-text--sm fr-mb-0 fr-mt-4w">
        <span class="fr-icon-info-fill fr-icon--sm fr-mr-1v"></span>
        Remplissez un des deux champs pour calculer l’autre automatiquement
      </p>
    </div>
  </div>
</template>

<style scoped>
.sorted-inputs {
  border-left: 2px solid var(--grey-900-175);
  padding: 1rem 2rem;
  padding-right: 0;
}
p.source-title-tooltip {
  font-weight: bold;
}
.calculation-info {
  color: var(--info-425-625);
}
</style>
