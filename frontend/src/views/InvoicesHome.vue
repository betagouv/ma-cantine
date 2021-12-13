<template>
  <div class="text-left">
    <div class="d-flex">
      <div>
        <h1 class="font-weight-black text-h5 text-sm-h4 my-4" style="width: 100%">
          Mes Achats
        </h1>
        <p>
          Une alimentation saine et durable commence par un suivi comptable de vos achats
        </p>
        <v-btn class="primary" large>
          <v-icon>mdi-plus</v-icon>
          Ajouter une ligne
        </v-btn>
      </div>
      <v-spacer></v-spacer>

      <v-img
        src="/static/images/ChartDoodle.png"
        v-if="$vuetify.breakpoint.smAndUp"
        class="mx-auto rounded-0"
        contain
        max-width="150"
      ></v-img>
    </div>
    <v-text-field
      v-model="search"
      append-icon="mdi-magnify"
      label="Rechercher"
      single-line
      hide-details
      style="max-width: 400px;"
    ></v-text-field>
    <v-card outlined class="my-4">
      <!-- eslint-disable-next-line -->
      <v-data-table :headers="headers" :items="desserts" :search="search" @click:row="onRowClick">
        <template v-slot:[`item.category`]="{ item }">
          <v-chip small :color="getColor(item.category)" dark>
            {{ item.category }}
          </v-chip>
        </template>
        <template v-slot:[`item.price`]="{ item }">{{ item.price }} €</template>
      </v-data-table>
    </v-card>
  </div>
</template>

<script>
export default {
  name: "InvoicesHome",
  data() {
    return {
      search: "",
      headers: [
        {
          text: "Date",
          align: "start",
          filterable: false,
          value: "date",
        },
        { text: "Fournisseur", value: "provider" },
        { text: "Catégorie", value: "category" },
        { text: "Cantine", value: "canteen" },
        { text: "Prix", value: "price" },
      ],
      desserts: [
        {
          date: "3 décembre 2021",
          provider: "Boucherie Machin",
          category: "Viandes volailles",
          canteen: "La cantine d'Alex",
          price: 430,
        },
        {
          date: "3 décembre 2021",
          provider: "Légumes Toto",
          category: "Fuits et Légumes",
          canteen: "La cantine d'Alex",
          price: 80,
        },
        {
          date: "4 décembre 2021",
          provider: "Poissonerie Hors Sôle",
          category: "Pêche",
          canteen: "La cantine d'Alex",
          price: 387,
        },
        {
          date: "5 décembre 2021",
          provider: "Produits laitiers Ma Cantine",
          category: "Produits laitiers",
          canteen: "La cantine d'Alex",
          price: 822,
        },
        {
          date: "5 décembre 2021",
          provider: "Transformers",
          category: "Produits transformés",
          canteen: "La cantine d'Alex",
          price: 180,
        },
        {
          date: "6 décembre 2021",
          provider: "Produits laitiers Ma Cantine",
          category: "Produits laitiers",
          canteen: "La cantine d'Alex",
          price: 822,
        },
        {
          date: "6 décembre 2021",
          provider: "Transformers",
          category: "Produits transformés",
          canteen: "La cantine d'Alex",
          price: 180,
        },
        {
          date: "3 novembre 2021",
          provider: "Légumes Toto",
          category: "Fuits et Légumes",
          canteen: "La cantine d'Alex",
          price: 80,
        },
      ],
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
    onRowClick() {
      this.$router.push({ name: "InvoicePage" })
    },
  },
}
</script>
