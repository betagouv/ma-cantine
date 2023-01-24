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
      <p class="my-4" v-html="partner.longDescription"></p>

      <v-divider class="mt-12"></v-divider>

      <div class="pt-12">
        <p>
          <DownloadLink
            href="/static/documents/charte_de_referencement_Version01_janvier2023.pdf"
            label="En savoir plus sur les critères de référencement sur la charte ma cantine"
            sizeStr="191 ko"
            target="_blank"
          />
        </p>
        <p class="caption">
          Cette page n’engage pas l’administration ou l'équipe ma cantine ; elle constitue une proposition à l'attention
          des responsables légaux de restaurants collectifs. Les structures sont seules responsables de la véracité des
          informations qu’elles communiquent sur la page partenaire.
        </p>
      </div>
    </div>
  </div>
</template>

<script>
import BreadcrumbsNav from "@/components/BreadcrumbsNav"
import PartnerIndicators from "@/components/PartnerIndicators"
import DownloadLink from "@/components/DownloadLink"

export default {
  name: "PartnerPage",
  components: { BreadcrumbsNav, PartnerIndicators, DownloadLink },
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
          message: "Nous n'avons pas trouvé cet acteur",
          status: "error",
        })
        this.$router.push({ name: "PartnersHome" })
      })
  },
}
</script>
