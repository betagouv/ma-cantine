<script setup>
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { computedAsync } from "@vueuse/core"
import { formatSiretOrSiren } from '@/utils'
import LayoutSidebarCanteen from '@/layouts/LayoutSidebarCanteen.vue'
import AppFieldDisplay from '@/components/AppFieldDisplay.vue'
import AppLinkRouter from '@/components/AppLinkRouter.vue'
import cantines from '@/data/cantines.json'
import sectorsService from '@/services/sectors'

const route = useRoute()
const router = useRouter()
const canteenUrlComponent = route.params.canteenUrlComponent

/* Edit redirect */
const goToEdit = (canteenIsGroupe) => {
  const pageName = canteenIsGroupe ? 'GestionnaireCantineGroupeModifier' : 'GestionnaireCantineRestaurantModifier'
  router.push({ name: pageName })
}

/* Value */
const getPrettyValue = (name, field) => {
  if (!name) return null
  return cantines[field].find(model => model.value === name).label
}

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
  <LayoutSidebarCanteen v-slot="{ canteenIsGroupe, canteenInformation }">
    <div class="ma-cantine--flex-between ma-cantine--flex-gap-1">
      <h2 class="fr-mb-0">{{ canteenIsGroupe ? 'Informations du groupe' : 'Mes informations' }}</h2>
      <DsfrButton @click="goToEdit(canteenIsGroupe)" :label="canteenIsGroupe ? 'Modifier les informations du groupe' : 'Modifier mes informations'" icon="ri-pencil-line" />
    </div>
    <ol class="ma-cantine--ordered-list ma-cantine--unstyled-list">
      <li class="fr-my-3w">
        <h3>Caractéristiques</h3>
        <AppFieldDisplay v-if="!canteenIsGroupe" :label="cantines.economicModelName" :value="getPrettyValue(canteenInformation.economicModel, 'economicModel')" />
        <AppFieldDisplay :label="cantines.managementTypeName" :value="getPrettyValue(canteenInformation.managementType, 'managementType')" />
        <AppFieldDisplay :label="cantines.productionTypeName" :value="getPrettyValue(canteenInformation.productionType, 'productionType')" />
        <AppFieldDisplay v-if="canteenInformation.centralProducerSiret" :label="cantines.centralProducerSiret" :value="canteenInformation.centralProducerSiret" />
      </li>
      <li class="fr-my-3w">
        <h3>Identification de l'établissement</h3>
        <AppFieldDisplay :label="cantines.id" :value="canteenInformation.id" tooltip="Identifiant unique de l'établissement, ce champ ne peut pas être modifié."/>
        <AppFieldDisplay v-if="!canteenIsGroupe && canteenInformation.siret" :label="cantines.siretName" :value="formatSiretOrSiren(canteenInformation.siret)" />
        <AppFieldDisplay v-if="canteenInformation.sirenUniteLegale" :label="cantines.sirenUniteLegaleName" :value="formatSiretOrSiren(canteenInformation.sirenUniteLegale)" />
        <AppFieldDisplay :label="canteenIsGroupe ? cantines.nameGroupe : cantines.nameCantine" :value="canteenInformation.name" />
        <AppFieldDisplay :label="cantines.dailyMealCountName" :value="canteenInformation.dailyMealCount"
          tooltip="Donnez une moyenne globale sur les jours ouverts de vos établissements (pour évaluer la taille de votre établissement)"
        />
        <AppFieldDisplay v-if="!canteenIsGroupe && canteenInformation.sirenUniteLegale" :label="cantines.city" :value="canteenInformation.city" />
        <AppFieldDisplay v-if="!canteenIsGroupe && canteenInformation.sirenUniteLegale" :label="cantines.postalCode" :value="canteenInformation.postalCode" />
      </li>
      <li v-if="!canteenIsGroupe" class="fr-my-3w">
        <h3>Informations générées</h3>
        <DsfrAlert title="Ces informations ne sont pas modifiables" type="info" class="fr-mb-2w">
          À partir des informations renseignées, nous avons généré des données avec d'autres référentiels :
          <a href="https://france-pat.fr" target="_blank">France PAT</a>
          et
          <a href="https://annuaire-entreprises.data.gouv.fr" target="_blank">l'annuaire des entreprises</a>.
          Si vous remarquez une erreur, merci de <AppLinkRouter title="nous contacter" :to="{name: 'Contact'}" />.
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
        <h3>Secteurs</h3>
        <AppFieldDisplay :label="cantines.sectorList" :value="getPrettySectors(canteenInformation.sectorList)" />
        <AppFieldDisplay v-if="showLineMinistry" :label="cantines.lineMinistry" :value="getPrettyLineMinistry(canteenInformation.lineMinistry)" />
      </li>
      <li v-if="canteenInformation.groupe !== null" class="fr-my-3w">
        <h3>Informations de mon groupe</h3>
        <DsfrAlert title="Le gestionnaire du groupe de restaurants satellites a ajouté votre établissement" type="info" class="fr-mb-2w">
          Cela lui permet de réaliser une déclaration unique pour laquelle le montant total des achats du groupe est ensuite réparti automatiquement entre chaque restaurant satellite, au prorata de son nombre de couverts annuels.
          Si vous remarquez une erreur ou souhaitez ne plus être associer au groupe, merci de <AppLinkRouter title="nous contacter" :to="{name: 'Contact'}" />.
        </DsfrAlert>
        <AppFieldDisplay :label="cantines.nameGroupe" :value="canteenInformation.groupe?.name" />
        <AppFieldDisplay :label="cantines.id" :value="canteenInformation.groupe?.id" />
        <AppFieldDisplay :label="`${cantines.sirenUniteLegaleName} du groupe`" :value="formatSiretOrSiren(canteenInformation.groupe?.sirenUniteLegale)" />
      </li>
      <li v-if="!canteenIsGroupe" class="fr-my-3w">
        <h3>Description</h3>
        <p>{{ canteenInformation.publicationComments || 'Aucune description renseignée' }}</p>
      </li>
    </ol>
    <div v-if="canteenUrlComponent" class="fr-container fr-background-alt--red-marianne fr-p-4w fr-mt-3w">
      <h2 class="fr-h6 fr-text-default--error fr-mb-2w">
        <span class="mdi mdi-archive"></span>
        Archiver cet établissement
      </h2>
      <p class="fr-mb-0">
        Vous ne souhaitez plus faire apparaître cet établissement sur la plateforme <em>ma cantine</em> ? <br />
        Vous pouvez l’archiver <AppLinkRouter :to="{ name: 'GestionnaireCantineArchiver', params: { canteenUrlComponent: canteenUrlComponent } }" title="en cliquant ici" />
      </p>
    </div>
  </LayoutSidebarCanteen>
</template>
