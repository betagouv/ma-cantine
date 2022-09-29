<template>
  <v-card
    :to="{
      name: 'PartnerPage',
      params: { partnerUrlComponent: $store.getters.getPartnerUrlComponent(partner) },
    }"
    class="dsfr d-flex flex-column text-left fill-height"
    outlined
    :ripple="false"
  >
    <v-img :src="partner.image || '/static/images/partner-default-image.jpg'" height="120" max-height="120"></v-img>
    <v-card-title class="font-weight-bold">{{ partner.name }}</v-card-title>
    <v-card-subtitle>
      <PartnerIndicators :partner="partner" />
    </v-card-subtitle>
    <v-card-text>{{ partner.shortDescription }}</v-card-text>
    <v-spacer></v-spacer>
    <v-card-actions class="px-4 py-4">
      <v-spacer></v-spacer>
      <span class="icon i-arrow-right"></span>
    </v-card-actions>
  </v-card>
</template>

<script>
import PartnerIndicators from "@/components/PartnerIndicators"

export default {
  name: "PartnerCard",
  components: { PartnerIndicators },
  props: {
    partner: {
      type: Object,
      required: true,
    },
  },
}
</script>
