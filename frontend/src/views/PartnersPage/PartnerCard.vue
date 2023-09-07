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
    <v-img contain :src="partner.image" height="120" max-height="120" v-if="partner.image"></v-img>
    <v-img src="/static/images/partner-default-image.jpg" height="120" max-height="120" v-else></v-img>
    <v-card-title class="font-weight-bold">{{ partner.name }}</v-card-title>
    <v-card-subtitle>
      <PartnerIndicators :partner="partner" />
    </v-card-subtitle>
    <v-card-text>{{ partner.shortDescription }}</v-card-text>
    <v-spacer></v-spacer>
    <v-card-actions class="px-4 py-4">
      <v-spacer></v-spacer>
      <v-icon color="primary">$arrow-right-line</v-icon>
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
