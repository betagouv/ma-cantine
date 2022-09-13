<template>
  <div class="text-left">
    <div v-if="partner">
      <BreadcrumbsNav :links="[{ to: { name: 'PartnersHome' } }]" :title="partner.name" />
      <div class="d-flex">
        <div v-if="partner.image && $vuetify.breakpoint.smAndUp" class="mr-4">
          <v-img :src="partner.image" max-width="260" contain></v-img>
        </div>
        <div class="d-flex flex-column">
          <h1 class="font-weight-black text-h5 text-sm-h4 mb-4">
            {{ partner.name }}
          </h1>
          <PartnerIndicators :partner="partner" class="grey--text text--darken-3 text-body-2" />
          <v-spacer></v-spacer>
          <v-btn outlined color="primary" v-if="partner.website" :href="partner.website" width="fit-content">
            <v-icon small class="mr-1">$global-fill</v-icon>
            Site web
          </v-btn>
        </div>
      </div>
      <v-divider class="my-4"></v-divider>
      <p v-html="partner.longDescription"></p>
    </div>
  </div>
</template>

<script>
import BreadcrumbsNav from "@/components/BreadcrumbsNav"
import PartnerIndicators from "@/components/PartnerIndicators"

export default {
  name: "PartnerPage",
  components: { BreadcrumbsNav, PartnerIndicators },
  data() {
    return {
      partner: null,
    }
  },
  props: {
    partnerUrlComponent: {
      type: String,
      required: true,
    },
  },
  methods: {
    setPartner(partner) {
      this.partner = partner
      if (partner) document.title = `${this.partner.name} - ${this.$store.state.pageTitleSuffix}`
    },
  },
  beforeMount() {
    const id = this.partnerUrlComponent.split("--")[0]
    return fetch(`/api/v1/partners/${id}`)
      .then((response) => {
        if (response.status != 200) throw new Error()
        response.json().then(this.setPartner)
      })
      .catch(() => {
        this.$store.dispatch("notify", {
          message: "Nous n'avons pas trouvé ce partenaire",
          status: "error",
        })
        this.$router.push({ name: "PartnersHome" })
      })
  },
}
</script>
