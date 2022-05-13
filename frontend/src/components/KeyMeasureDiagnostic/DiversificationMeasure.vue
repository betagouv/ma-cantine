<template>
  <div>
    <v-checkbox
      hide-details="auto"
      class="mb-4"
      v-model="diagnostic.hasDiversificationPlan"
      label="J'ai mis en place un plan pluriannuel de diversification des protéines incluant des alternatives à base de protéines végétales"
      :readonly="readonly"
      :disabled="readonly"
      v-if="applicableRules.hasDiversificationPlan"
    />

    <fieldset class="my-3" v-if="applicableRules.hasDiversificationPlan">
      <legend class="text-left mb-2 mt-3" :class="{ 'grey--text': !diagnostic.hasDiversificationPlan }">
        Ce plan comporte, par exemple, les actions suivantes (voir guide du CNRC) :
      </legend>
      <v-checkbox
        hide-details="auto"
        class="ml-8 mt-2"
        v-model="diagnostic.diversificationPlanActions"
        :multiple="true"
        v-for="item in diversificationPlanActions"
        :key="item.value"
        :value="item.value"
        :label="item.label"
        :readonly="readonly || !diagnostic.hasDiversificationPlan"
        :disabled="readonly || !diagnostic.hasDiversificationPlan"
      />
    </fieldset>

    <fieldset>
      <legend class="text-left my-3">J'ai mis en place un menu végétarien dans ma cantine :</legend>
      <v-radio-group class="my-0" v-model="diagnostic.vegetarianWeeklyRecurrence" hide-details>
        <v-radio
          class="ml-8"
          v-for="item in frequency"
          :key="item.value"
          :label="item.label"
          :value="item.value"
          :readonly="readonly"
          :disabled="readonly"
        ></v-radio>
      </v-radio-group>
    </fieldset>

    <fieldset class="mt-3">
      <legend class="text-left my-3">Le menu végétarien proposé est :</legend>
      <v-radio-group class="my-0" v-model="diagnostic.vegetarianMenuType" hide-details>
        <v-radio
          class="ml-8"
          v-for="item in menuTypes"
          :key="item.value"
          :label="item.label"
          :value="item.value"
          :readonly="readonly"
          :disabled="readonly"
        ></v-radio>
      </v-radio-group>
    </fieldset>

    <fieldset class="mt-3">
      <legend class="text-left mb-2 mt-3">
        Le plat principal de mon menu végétarien est majoritairement à base de :
      </legend>
      <v-checkbox
        hide-details="auto"
        class="ml-8 mt-2"
        v-model="diagnostic.vegetarianMenuBases"
        :multiple="true"
        v-for="item in menuBases"
        :key="item.value"
        :value="item.value"
        :label="item.label"
        :readonly="readonly"
        :disabled="readonly"
      />
    </fieldset>

    <v-divider v-if="showExpeSegment" class="my-4"></v-divider>
    <div v-if="showExpeSegment">
      <p class="text-h6 font-weight-bold">
        Expérimentation de l'option végétarienne quotidienne pour les collectivités volontaires
      </p>
      <p class="body-2">
        Pour participer à l'expérimentation d'une option végétarienne quotidienne, telle que prévue par la loi Climat et
        résilience, nous vous proposons de répondre à quelques questions sur la mise en œuvre de l'option végétarienne
        quotidienne dans votre établissement.
      </p>
      <p class="body-2">
        En particulier, les questions portent sur les catégories de plats végétariens servis, l'impact sur les pesées de
        gaspillage alimentaire, la fréquentation, la satisfaction des convives et le coût des repas. Il est également
        possible de participer si une option végétarienne quotidienne est déjà mise en place dans votre établissement.
      </p>
      <v-checkbox v-if="canteen" v-model="canteen.vegetarianExpeParticipant" @change="onExpeCheckboxChange">
        <template v-slot:label>
          <span class="body-2 grey--text text--darken-3">
            Je suis volontaire pour participer à l’expérimentation.
          </span>
        </template>
      </v-checkbox>
      <v-btn
        color="primary"
        class="body-2 mt-n2 mb-2"
        v-if="canteen.vegetarianExpeParticipant"
        outlined
        small
        @click="() => (showExpeModal = true)"
      >
        Mettre à jour mes données
      </v-btn>

      <v-dialog v-model="showExpeModal" :width="$vuetify.breakpoint.mdAndUp ? 900 : undefined">
        <ExpeVegetarian v-if="showExpeModal" @close="() => (showExpeModal = false)" :canteen="canteen" />
      </v-dialog>
    </div>
  </div>
</template>

<script>
import { applicableDiagnosticRules } from "@/utils"
import ExpeVegetarian from "@/components/KeyMeasureDiagnostic/ExpeModals/ExpeVegetarian"

export default {
  props: {
    diagnostic: Object,
    readonly: {
      type: Boolean,
      default: false,
    },
    canteen: Object,
  },
  components: { ExpeVegetarian },
  data() {
    return {
      showExpeModal: false,
      diversificationPlanActions: [
        {
          label:
            "Agir sur les plats et les produits (diversification, gestion des quantités, recette traditionnelle, gout...)",
          value: "PRODUCTS",
        },
        {
          label: "Agir sur la manière dont les aliments sont présentés aux convives (visuellement attrayants)",
          value: "PRESENTATION",
        },
        {
          label: "Agir sur la manière dont les menus sont conçus en soulignant attributs positifs des plats",
          value: "MENU",
        },
        {
          label: "Agir sur la mise en avant des produits (plats recommandés, dégustation, mode de production...)",
          value: "PROMOTION",
        },
        {
          label:
            "Agir sur la formation du personnel, la sensibilisation des convives, l’investissement dans de nouveaux équipements de cuisine...",
          value: "TRAINING",
        },
      ],
      frequency: [
        {
          label: "Moins d'une fois par semaine",
          value: "LOW",
        },
        {
          label: "Une fois par semaine",
          value: "MID",
        },
        {
          label: "Plus d'une fois par semaine",
          value: "HIGH",
        },
        {
          label: "De façon quotidienne",
          value: "DAILY",
        },
      ],
      menuTypes: [
        {
          label: "Un menu végétarien en plat unique, sans choix",
          value: "UNIQUE",
        },
        {
          label: "Un menu végétarien composé de plusieurs choix de plats végétariens",
          value: "SEVERAL",
        },
        {
          label: "Un menu végétarien au choix, en plus d'autres plats non végétariens",
          value: "ALTERNATIVES",
        },
      ],
      menuBases: [
        {
          label: "De céréales et/ou les légumes secs (hors soja)",
          value: "GRAIN",
        },
        {
          label: "De soja",
          value: "SOY",
        },
        {
          label: "De fromage",
          value: "CHEESE",
        },
        {
          label: "D’œufs",
          value: "EGG",
        },
        {
          label: "De plats transformés prêts à l'emploi",
          value: "READYMADE",
        },
      ],
    }
  },
  computed: {
    applicableRules() {
      return applicableDiagnosticRules(this.canteen)
    },
    showExpeSegment() {
      return !!this.canteen && window.ENABLE_XP_VEGE
    },
  },
  methods: {
    onExpeCheckboxChange(checked) {
      this.$store
        .dispatch("updateCanteen", {
          id: this.canteen.id,
          payload: { vegetarianExpeParticipant: checked },
        })
        .catch((e) => this.$store.dispatch("notifyServerError", e))

      if (checked) this.showExpeModal = true
    },
  },
}
</script>

<style scoped>
fieldset {
  border: none;
}
</style>
