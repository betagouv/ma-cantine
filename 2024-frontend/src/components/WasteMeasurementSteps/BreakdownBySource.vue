<script setup>
import { onMounted, reactive, watch, computed, inject, nextTick } from "vue"
import Constants from "@/constants.js"
import { useVuelidate } from "@vuelidate/core"
import { formatError } from "@/utils.js"
import HelpText from "./HelpText.vue"
import DsfrBooleanRadio from "@/components/DsfrBooleanRadio.vue"
import { helpers } from "@vuelidate/validators"
import { useValidators } from "@/validators.js"
const { decimal, minValue, maxValue } = useValidators()

const props = defineProps(["data"])
const sources = {
  preparation: {
    totalKey: "preparationTotalMass",
    sortedKey: "preparationIsSorted",
    edibleKey: "preparationEdibleMass",
    inedibleKey: "preparationInedibleMass",
    title: Constants.WasteMeasurement.preparation.title,
    primaryLabel: "Masse de déchets alimentaires pour les excédents de préparation (en kg)",
    description:
      "Par exemple, si vous avez jeté des épluchures, des parures ou si vous avez des ingrédients excédentaires que vous ne réutiliserez pas, il s’agit d’excédents de préparation",
    edibleHelp:
      "Les parties des denrées alimentaires considérées comme non comestibles incluent les os, les morceaux de gras retirés du reste des pièces de viande, les épluchures, les yaourts jetés ayant une DLC dépassée, les fonds de pots de crèmes ou de sauces non valorisés et jetés, les fruits et légumes non présentés et non valorisés du fait de leur mauvaise apparence, ...",
  },
  unserved: {
    totalKey: "unservedTotalMass",
    sortedKey: "unservedIsSorted",
    edibleKey: "unservedEdibleMass",
    inedibleKey: "unservedInedibleMass",
    title: Constants.WasteMeasurement.unserved.title,
    primaryLabel: "Masse de déchets alimentaires pour les denrées présentées aux convives mais non servies (en kg)",
    description:
      "Par exemple, si vous présentez en vitrine un nombre excédentaire de salades, de parts de tarte aux pommes et que ces denrées supplémentaires ne sont ni consommées ni valorisées, il s’agit d’excédents présentés aux convives et non servis ou non valorisés",
    edibleHelp:
      "Les parties des denrées alimentaires considérées comme non comestibles incluent les os, les arrêtes, les noyaux, les trognons de pommes, les épluchures... Les parties considérées comme comestibles incluent les morceaux de viande restants, les pâtes restant dans les assiettes, le pain restant au niveau des plateaux...",
  },
  leftovers: {
    totalKey: "leftoversTotalMass",
    sortedKey: "leftoversIsSorted",
    edibleKey: "leftoversEdibleMass",
    inedibleKey: "leftoversInedibleMass",
    title: Constants.WasteMeasurement.leftovers.title,
    primaryLabel: "Masse de déchets alimentaires pour le reste assiette (en kg)",
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

const payload = reactive({})

const genericPayloadKeys = ["totalKey", "sortedKey", "edibleKey", "inedibleKey"]

const sumCheck = () => {
  if (!payload.totalKey) return true
  if (!(payload.edibleKey > 0) || !(payload.inedibleKey > 0)) return true
  return payload.edibleKey + payload.inedibleKey === payload.totalKey
}
const combination = helpers.withMessage(
  "La somme de denrées comestibles et non comestibles devrait être égale au total",
  sumCheck
)

const rules = {
  totalKey: { decimal, minValue: minValue(0) },
  sortedKey: {},
  edibleKey: { decimal, maxValue: maxValue(computed(() => payload.totalKey)), minValue: minValue(0) },
  inedibleKey: { decimal, maxValue: maxValue(computed(() => payload.totalKey)), minValue: minValue(0) },
  combined: { combination },
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

watch(props, () => {
  nextTick().then(() => {
    payload._freezeWatcher = true
    genericPayloadKeys.forEach((k) => (payload[k] = originalPayload[source.value[k]]))
    delete payload._freezeWatcher
  })
})

watch(payload, () => {
  if (!payload._freezeWatcher) {
    updatePayload()
  }
})

onMounted(() => {
  emit("provide-vuelidate", v$)
  genericPayloadKeys.forEach((k) => (payload[k] = originalPayload[source.value[k]]))
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
            hint="Optionnel"
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
          <DsfrBooleanRadio
            v-model="payload.sortedKey"
            legend="Avez-vous trié entre comestible et non comestible&nbsp;?"
            hint="Optionnel"
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
    <div v-if="specifySortedExcess" class="sorted-inputs fr-col-sm-6">
      <div class="fr-grid-row fr-grid-row--middle fr-mb-4w">
        <p class="source-title-tooltip fr-mb-0">
          {{ source.title }}
        </p>
        <DsfrTooltip :content="source.edibleHelp" />
      </div>
      <DsfrInputGroup :error-message="formatError(v$.combined)">
        <DsfrInputGroup
          v-model.number="payload.edibleKey"
          type="number"
          label="Masse des déchets alimentaires comestibles (assimilable à du gaspillage alimentaire) (en kg)"
          hint="Optionnel"
          label-visible
          class="fr-mb-2w"
          :error-message="formatError(v$.edibleKey)"
        />
        <DsfrInputGroup
          v-model.number="payload.inedibleKey"
          type="number"
          label="Masse des déchets alimentaires non comestibles (en kg)"
          hint="Optionnel"
          label-visible
          class="fr-mb-2w"
          :error-message="formatError(v$.inedibleKey)"
        />
      </DsfrInputGroup>
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
