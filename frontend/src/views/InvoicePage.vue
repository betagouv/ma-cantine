<template>
  <div class="text-left">
    <h1 class="font-weight-black text-h5 text-sm-h4 my-4" style="width: 100%">
      Modifier mon Achat
    </h1>
    <p>
      Vous pouvez modifier les données de cet achat dans le formulaire. Ces modifications seront visibles dans le
      diagnostic de la cantine choisie.
    </p>
    <v-row>
      <v-col cols="12" sm="8">
        <v-form>
          <v-row>
            <v-col cols="12" sm="8">
              <label class="body-2">Fournisseur</label>
              <v-text-field
                validate-on-blur
                hide-details="auto"
                solo
                v-model="purchase.provider"
                class="mt-2 mb-4"
              ></v-text-field>
            </v-col>
            <v-col cols="12" sm="4">
              <label class="body-2">Prix</label>
              <v-text-field
                validate-on-blur
                hide-details="auto"
                solo
                v-model="purchase.price"
                class="mt-2 mb-4"
                append-icon="mdi-currency-eur"
              ></v-text-field>
            </v-col>
          </v-row>
          <label class="body-2">Catégorie</label>
          <v-radio-group>
            <v-radio class="ml-8" v-for="item in categories" :key="item" :label="item" :value="item">
              <template v-slot:label>
                <v-chip small :color="getColor(item)" dark>
                  {{ item }}
                </v-chip>
              </template>
            </v-radio>
          </v-radio-group>

          <label class="body-2">Caractéristique</label>
          <v-row class="mb-4">
            <v-col cols="12" sm="6" md="4" class="py-0" v-for="type in productTypes" :key="type">
              <v-checkbox hide-details="auto" :multiple="true" :key="type" :value="type" :label="type" />
            </v-col>
          </v-row>
        </v-form>
      </v-col>
      <v-col cols="12" md="4">
        <label class="body-2">Facture</label>
        <FileDrop
          subtitle="Facture en PDF acceptée"
          :acceptTypes="['.csv', 'text/csv', '.tsv', 'text/tsv']"
          maxSize="10485760"
        />
      </v-col>
    </v-row>
  </div>
</template>

<script>
import FileDrop from "@/views/DiagnosticsImporter/FileDrop"

export default {
  name: "InvoicePage",
  components: { FileDrop },
  data() {
    return {
      purchase: {
        date: "3 décembre 2021",
        provider: "Légumes Toto",
        category: "Fuits et Légumes",
        canteen: "La cantine d'Alex",
        price: 80,
      },
      categories: ["Viandes volailles", "Fuits et Légumes", "Pêche", "Produits laitiers", "Produits transformés"],
      productTypes: ["Bio", "AOC/AOP", "RUP", "Label rouge", "Pêche durable", "Local", "HVE", "Commerce Équitable"],
    }
  },
  methods: {
    getColor(category) {
      switch (category) {
        case "Viandes volailles":
          return "deep-orange darken-1"
        case "Fuits et Légumes":
          return "green darken-1"
        case "Pêche":
          return "light-blue darken-1"
        case "Produits laitiers":
          return "lime darken-2"
        case "Produits transformés":
          return "deep-purple darken-1"
        default:
          return "blue-grey darken-1"
      }
    },
  },
}
</script>
