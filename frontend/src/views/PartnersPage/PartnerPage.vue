<template>
  <div class="text-left">
    <div v-if="partner">
      <BreadcrumbsNav :links="[{ to: { name: 'PartnersHome' } }]" :title="partner.name" />
      <h1 class="font-weight-black text-h5 text-sm-h4 mb-4">
        {{ partner.name }}
      </h1>
      <PartnerIndicators :partner="partner" class="grey--text text--darken-3 text-body-2" />
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
