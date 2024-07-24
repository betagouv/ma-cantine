<script setup>
import { onMounted, reactive, watch } from "vue"
import { useVuelidate } from "@vuelidate/core"
import { required, decimal } from "@vuelidate/validators"
import { formatError } from "@/utils.js"
import HelpText from "./HelpText.vue"
import DsfrBooleanRadio from "@/components/DsfrBooleanRadio.vue"

const emit = defineEmits(["provide-vuelidate", "update-payload"])

const payload = reactive({
  preparationExcess: undefined,
  sortedEdible: undefined,
})

const rules = {
  preparationExcess: { decimal },
  sortedEdible: { required },
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
  <div>
    <div class="fr-grid-row">
      <div class="fr-col-12 fr-col-sm-6">
        <DsfrInputGroup
          v-model.number="payload.preparationExcess"
          type="number"
          label="Masse de gaspillage pour les excédents de préparation"
          hint="En kg (optionnel)"
          label-visible
          class="fr-mb-2w"
          :error-message="formatError(v$.preparationExcess)"
        />
      </div>
      <div class="fr-col-sm-6">
        <HelpText question="À quoi correspondent les excédents de préparation ?">
          <p>
            Par exemple, si vous avez jeté des épluchures, des parures ou si vous avez des ingrédients excédentaires que
            vous ne réutiliserez pas, il s’agit d’excédents de préparation. Dans le cas où vous avez mesuré les denrées
            en stock que vous avez jetées durant la période de mesure (du type yaourts à DLC dépassée, salades pourries,
            ...), les excédents de préparation incluent ces déchets issus de stocks.
          </p>
        </HelpText>
      </div>
    </div>
    <div class="fr-grid-row">
      <div class="fr-col-12 fr-col-sm-6">
        <DsfrBooleanRadio
          v-model.number="payload.sortedEdible"
          legend="Avez-vous trié entre comestible et non-comestible ?"
          name="sortedEdible"
          class="fr-mb-2w"
          :error-message="formatError(v$.sortedEdible)"
        />
      </div>
      <div class="fr-col-sm-6">
        <HelpText>
          <p>
            Les parties des denrées alimentaires considérées comme non comestibles incluent les os, les arrêtes, les
            noyaux, les trognons de pommes, les épluchures... Les parties considérées comme comestibles incluent les
            morceaux de viande restants, les pâtes restant dans les assiettes, le pain restant au niveau des plateaux...
          </p>
        </HelpText>
      </div>
    </div>
  </div>
</template>
