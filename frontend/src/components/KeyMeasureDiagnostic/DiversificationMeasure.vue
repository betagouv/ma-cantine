<template>
  <div>
    <v-checkbox
      hide-details="auto"
      v-model="diagnostic.hasDiversificationPlan"
      label="Si ma cantine fabrique plus de 200 repas par jour en moyenne, j'ai mis en place un plan pluriannuel de diversification des protéines incluant des alternatives à base de protéines végétales"
      :readonly="readonly"
      :disabled="readonly"
    />

    <p class="text-left mt-6 mb-2">Ce plan comporte, par exemple, les actions suivants (voir guide du CNRC) :</p>
    <v-checkbox
      hide-details="auto"
      class="ml-8"
      v-model="diagnostic.diversificationPlanActions"
      :multiple="true"
      v-for="item in diversificationPlanActions"
      :key="item.value"
      :value="item.value"
      :label="item.label"
      :readonly="readonly"
      :disabled="readonly"
    />

    <p class="text-left mt-6 mb-2">J'ai mis en place un menu végétarien dans ma cantine :</p>
    <v-radio-group v-model="diagnostic.vegetarianWeeklyRecurrence">
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

    <p class="text-left mt-6 mb-2">Le menu végétarien proposé est :</p>
    <v-radio-group v-model="diagnostic.vegetarianMenuType">
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

    <p class="text-left mt-6 mb-2">Le plat principal de mon menu végétarien est majoritairement à base de :</p>
    <v-checkbox
      hide-details="auto"
      class="ml-8"
      v-model="diagnostic.vegetarianMenuBases"
      :multiple="true"
      v-for="item in menuBases"
      :key="item.value"
      :value="item.value"
      :label="item.label"
      :readonly="readonly"
      :disabled="readonly"
    />
  </div>
</template>

<script>
export default {
  data() {
    return {
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
          label: "Agir sur la manière dont les menus sont conçus ces plats en soulignant leurs attributs positifs",
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
          label: "Un menu végétarien en plat unique",
          value: "UNIQUE",
        },
        {
          label: "Un menu végétarien composé de plusieurs plats végétariens",
          value: "SEVERAL",
        },
        {
          label: "Un menu végétarien en plus d’autres menus non végétariens",
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
  props: {
    diagnostic: Object,
    readonly: {
      type: Boolean,
      default: false,
    },
  },
}
</script>
