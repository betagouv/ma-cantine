<template>
  <v-data-table
    :options.sync="options"
    :loading="loading"
    :headers="headers"
    :items="processedVisiblePurchases"
    @click:row="selectable && onRowClick"
    :show-select="selectable"
  >
    <template v-slot:[`item.description`]="{ item }">
      <router-link :to="{ name: 'PurchasePage', params: { id: item.id } }">
        {{ item.description }}
        <span class="d-sr-only">, {{ item.date }}</span>
      </router-link>
    </template>
    <template v-slot:[`item.family`]="{ item }">
      <v-chip outlined small :color="getProductFamilyDisplayValue(item.family).color" dark class="font-weight-bold">
        {{ capitalise(getProductFamilyDisplayValue(item.family).shortText) }}
      </v-chip>
    </template>
    <template v-slot:[`item.characteristics`]="{ item }">
      {{ getProductCharacteristicsDisplayValue(item.characteristics) }}
    </template>
    <template v-slot:[`item.priceHt`]="{ item }">
      {{ item.priceHt.toLocaleString("fr-FR", { style: "currency", currency: "EUR" }) }}
    </template>
    <template v-slot:[`item.hasAttachment`]="{ item }">
      <v-icon small color="grey" v-if="item.hasAttachment" aria-label="Has invoice file" :aria-hidden="false">
        mdi-paperclip
      </v-icon>
    </template>

    <template v-slot:[`no-data`]>
      <div class="mx-10 my-10">
        Cliquer sur le bouton "Ajouter une ligne" pour rentrer vos achats.
      </div>
    </template>
  </v-data-table>
</template>

<script>
import { formatDate, capitalise } from "@/utils"
import Constants from "@/constants"

export default {
  name: "PurchasesTable",
  props: {
    purchases: Array,
    selectable: Boolean,
  },
  data() {
    return {
      loading: false,
      purchaseCount: null,
      limit: 10,
      options: {
        sortBy: [],
        sortDesc: [],
        page: 1,
      },
      headers: [
        {
          text: "Date",
          align: "start",
          filterable: false,
          value: "date",
          sortable: true,
        },
        { text: "Produit", value: "description", sortable: true },
        { text: "Famille", value: "family", sortable: true },
        { text: "Caratéristiques", value: "characteristics", sortable: false },
        { text: "Cantine", value: "canteen__name", sortable: true },
        { text: "Prix HT", value: "priceHt", sortable: true, align: "end" },
        { text: "", value: "hasAttachment", sortable: false },
      ],
      productFamilies: [],
      characteristics: [],
    }
  },
  computed: {
    processedVisiblePurchases() {
      const canteens = this.$store.state.userCanteenPreviews
      return this.purchases.map((x) => {
        const canteen = canteens.find((y) => y.id === x.canteen)
        const date = x.date ? formatDate(x.date) : null
        const hasAttachment = !!x.invoiceFile
        return Object.assign(x, { canteen__name: canteen?.name, date, hasAttachment })
      })
    },
  },
  methods: {
    getProductFamilyDisplayValue(family) {
      if (Object.prototype.hasOwnProperty.call(Constants.ProductFamilies, family))
        return Constants.ProductFamilies[family]
      return { text: "", shortText: "", color: "" }
    },
    getProductCharacteristicsDisplayValue(characteristics) {
      const priorityOrder = Object.keys(Constants.Characteristics)
      characteristics = characteristics.filter((c) => priorityOrder.indexOf(c) > -1)
      characteristics.sort((a, b) => {
        return priorityOrder.indexOf(a) - priorityOrder.indexOf(b)
      })
      const displayCount = 3
      const remaining = characteristics.length - displayCount
      characteristics.splice(displayCount)
      let str = characteristics.map((c) => this.getCharacteristicDisplayValue(c).text).join(", ")
      if (remaining > 0) str += ` et ${remaining} autre${remaining > 1 ? "s" : ""}`
      return str
    },
    getCharacteristicDisplayValue(characteristic) {
      if (Object.prototype.hasOwnProperty.call(Constants.Characteristics, characteristic))
        return Constants.Characteristics[characteristic]
      return { text: "" }
    },
    onRowClick(purchase) {
      // TODO: maybe if not selectable, navigate to purchase
      const purchaseIndex = this.selectedPurchases.findIndex((p) => p.id === purchase.id)
      if (purchaseIndex === -1) this.selectedPurchases.push(purchase)
      else this.selectedPurchases.splice(purchaseIndex, 1)
    },
    capitalise,
  },
}
</script>

<style scoped>
.v-data-table >>> tbody tr:not(.v-data-table__empty-wrapper),
.v-data-table >>> .v-chip {
  cursor: pointer;
}

/* Hides items-per-row */
.v-data-table >>> .v-data-footer__select {
  visibility: hidden;
}
</style>
