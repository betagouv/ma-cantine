<script setup>
import { ref, computed } from 'vue'
import { computedAsync } from "@vueuse/core"
import { formatSiretOrSiren } from '@/utils'
import AppFieldDisplay from '@/components/AppFieldDisplay.vue'
import AppLinkRouter from '@/components/AppLinkRouter.vue'
import cantines from '@/data/cantines.json'
import sectorsService from '@/services/sectors'
import cantineService from '@/services/canteens'

const props = defineProps(["canteenIsGroupe", "canteenInformation"])

/* Dynamic fields */
const showCentralProducerSiret = computed(() => {
  const isFilled = props.canteenInformation.centralProducerSiret
  const isGroupe = props.canteenIsGroupe
  const isSatellite = props.canteenInformation.productionType === "siteCookedElsewhere"
  return isFilled || isGroupe || isSatellite
})
const showGroupeInformations = computed(() => props.canteenInformation.groupe !== null)

/* Tooltips */
const tooltips = computed(() => {
  return {
    economicModel: cantines.economicModel.find(option => option.value === props.canteenInformation?.economicModel)?.hint,
    dailyMealCount: props.canteenIsGroupe ? "Estimation du nombre de couverts / jour sur l’ensemble des cantines du groupe." : "Estimation du nombre de couverts / jour moyen. Permet d’informer sur la taille de la cantine."
  }
})

/* Value */
const getPrettyValue = (name, field) => {
  if (!name) return null
  return cantines[field].find(model => model.value === name).label
}

/* Errors */
const canteenCheck = computedAsync(async () => await cantineService.checkCanteen(props.canteenInformation.id), [])
const canteenErrors = computed(() => canteenCheck.value.isFilled ? [] : canteenCheck.value.errors)

/* Sectors and line ministries */
const sectorsList = computedAsync(async () => await sectorsService.getSectors(), [])
const lineMinistriesList = computedAsync(async () => await sectorsService.getMinistries(), [])
const showLineMinistry = ref(false)
const getPrettySectors = (canteenSectors) => {
  if (sectorsList.value.length === 0 || !canteenSectors || canteenSectors.length === 0) return []
  const filteredSectors = sectorsList.value.filter((sector) => canteenSectors.includes(sector.value))
  showLineMinistry.value = filteredSectors.some((sector) => sector.hasLineMinistry)
  const filteredSectorsNames = filteredSectors.map((filter) => filter.name)
  return filteredSectorsNames
}
const getPrettyLineMinistry = (canteenLineMinistry) => {
  if (lineMinistriesList.value.length === 0 || !canteenLineMinistry ) return null
  const filteredLineMinistries = lineMinistriesList.value.filter((ministry) => ministry.value === canteenLineMinistry)
  return filteredLineMinistries.length > 0 ? filteredLineMinistries[0].name : null
}
</script>

<template>
  <ol class="ma-cantine--ordered-list ma-cantine--unstyled-list">
    <li class="fr-my-3w">
      <h3 class="fr-h5">Caractéristiques</h3>
      <AppFieldDisplay v-if="!canteenIsGroupe" :label="cantines.economicModelName" :value="getPrettyValue(canteenInformation.economicModel, 'economicModel')" :error="canteenErrors?.economicModel" :tooltip="tooltips.economicModel"/>
      <AppFieldDisplay :label="cantines.managementTypeName" :value="getPrettyValue(canteenInformation.managementType, 'managementType')" :error="canteenErrors?.managementType" />
      <AppFieldDisplay :label="cantines.productionTypeName" :value="getPrettyValue(canteenInformation.productionType, 'productionType')" :error="canteenErrors?.productionType" />
      <AppFieldDisplay v-if="showCentralProducerSiret" :label="cantines.centralProducerSiret" :value="formatSiretOrSiren(canteenInformation.centralProducerSiret)" :error="canteenErrors?.centralProducerSiret" />
    </li>
    <li class="fr-my-3w">
      <h3 class="fr-h5">Identification {{ canteenIsGroupe ? 'du groupe' : 'de la cantine' }}</h3>
      <AppFieldDisplay :label="cantines.id" :value="canteenInformation.id" tooltip="Identifiant unique de l'établissement, ce champ ne peut pas être modifié."/>
      <AppFieldDisplay v-if="!canteenIsGroupe && canteenInformation.siret" :label="cantines.siretName" :value="formatSiretOrSiren(canteenInformation.siret)" :error="canteenErrors?.siret" />
      <AppFieldDisplay v-else-if="canteenInformation.sirenUniteLegale" :label="cantines.sirenUniteLegaleName" :value="formatSiretOrSiren(canteenInformation.sirenUniteLegale)" :error="canteenErrors?.sirenUniteLegale" />
      <AppFieldDisplay v-else-if="!canteenIsGroupe && !canteenInformation.sirenUniteLegale && !canteenInformation.siret" :label="`${cantines.siretName} ou ${cantines.sirenUniteLegaleName}`" :value="null" :error="canteenErrors?.siret" />
      <AppFieldDisplay v-else-if="canteenIsGroupe && !canteenInformation.sirenUniteLegale" :label="cantines.sirenUniteLegaleName" :value="null" :error="canteenErrors?.sirenUniteLegale" />
      <AppFieldDisplay :label="canteenIsGroupe ? cantines.nameGroupe : cantines.nameCantine" :value="canteenInformation.name" :error="canteenErrors?.name" />
      <AppFieldDisplay :label="cantines.dailyMealCountName" :value="canteenInformation.dailyMealCount" :error="canteenErrors?.dailyMealCount" :tooltip="tooltips.dailyMealCount" />
      <AppFieldDisplay v-if="!canteenIsGroupe && canteenInformation.sirenUniteLegale" :label="cantines.city" :value="canteenInformation.city" />
      <AppFieldDisplay v-if="!canteenIsGroupe && canteenInformation.sirenUniteLegale" :label="cantines.postalCode" :value="canteenInformation.postalCode" />
    </li>
    <li v-if="!canteenIsGroupe" class="fr-my-3w">
      <h3 class="fr-h5">Informations générées</h3>
      <DsfrAlert title="Ces informations ne sont pas modifiables" type="info" class="fr-mb-2w" titleTag="h4">
        Informations générées à partir à partir du SIRET ou du SIREN de la cantine, via les référentiels
        <a href="https://annuaire-entreprises.data.gouv.fr" target="_blank">l'annuaire des entreprises</a>
        et
        <a href="https://france-pat.fr" target="_blank">France PAT</a>.
        Si vous remarquez une erreur sur les données géographiques, rendez-vous sur <a href="https://www.insee.fr/fr/information/1401387" target="_blank">Immatriculation, cessation ou modification des données au répertoire Sirene | Insee</a>.<br/>
        Concernant les Projets alimentaires territoriaux, la base est actualisée deux fois par ans, à partir des données actualisées sur France PAT.
      </DsfrAlert>
      <AppFieldDisplay v-if="!canteenInformation.sirenUniteLegale" :label="cantines.city" :value="canteenInformation.city" />
      <AppFieldDisplay v-if="!canteenInformation.sirenUniteLegale" :label="cantines.postalCode" :value="canteenInformation.postalCode" />
      <AppFieldDisplay :label="cantines.cityInseeCode" :value="canteenInformation.cityInseeCode" />
      <AppFieldDisplay :label="cantines.departmentLib" :value="canteenInformation.departmentLib" />
      <AppFieldDisplay :label="cantines.regionLib" :value="canteenInformation.regionLib" />
      <AppFieldDisplay :label="cantines.patLibList" :value="canteenInformation.patLibList" />
      <AppFieldDisplay :label="cantines.epciLib" :value="canteenInformation.epciLib" />
    </li>
    <li v-if="!canteenIsGroupe" class="fr-my-3w">
      <h3 class="fr-h5">Secteurs</h3>
      <AppFieldDisplay :label="cantines.sectorList" :value="getPrettySectors(canteenInformation.sectorList)" :error="canteenErrors?.sectorList" />
      <AppFieldDisplay v-if="showLineMinistry" :label="cantines.lineMinistry" :value="getPrettyLineMinistry(canteenInformation.lineMinistry)" :error="canteenErrors?.lineMinistry" />
    </li>
    <li v-if="!canteenIsGroupe" class="fr-my-3w">
      <h3 class="fr-h5">Description</h3>
      <p>{{ canteenInformation.publicationComments || 'Aucune description enregistrée'}}</p>
    </li>
    <li v-if="showGroupeInformations" class="fr-my-3w">
      <h3 class="fr-h5">Informations de mon groupe</h3>
      <DsfrAlert title="Le gestionnaire du groupe de restaurants satellites a ajouté votre établissement" type="info" class="fr-mb-2w" titleTag="h4">
        Cela lui permet de réaliser une déclaration unique pour laquelle le montant total des achats du groupe est ensuite réparti automatiquement entre chaque restaurant satellite, au prorata de son nombre de couverts annuels.
        Si vous remarquez une erreur ou souhaitez ne plus être associer au groupe, merci de <AppLinkRouter title="nous contacter" :to="{name: 'Contact'}" />.
      </DsfrAlert>
      <AppFieldDisplay :label="cantines.nameGroupe" :value="canteenInformation.groupe?.name" />
      <AppFieldDisplay :label="cantines.id" :value="canteenInformation.groupe?.id" />
      <AppFieldDisplay :label="`${cantines.sirenUniteLegaleName} du groupe`" :value="formatSiretOrSiren(canteenInformation.groupe?.sirenUniteLegale)" />
    </li>
  </ol>
</template>
