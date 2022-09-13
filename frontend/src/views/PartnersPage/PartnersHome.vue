<template>
  <div class="text-left">
    <BreadcrumbsNav />
    <v-row>
      <v-col cols="12" sm="7" md="8">
        <h1 class="font-weight-black text-h5 text-sm-h4 mb-4">
          Nos Partenaires
        </h1>
        <p>
          Les acteurs de la restauration collective au service des gestionnaires
        </p>
      </v-col>
      <v-col cols="0" sm="5" md="4" v-if="$vuetify.breakpoint.smAndUp" class="py-0 pr-8 d-flex">
        <v-spacer></v-spacer>
        <v-img src="/static/images/peeps-illustration-couple.png" contain max-width="140"></v-img>
      </v-col>
    </v-row>

    <v-row>
      <v-spacer></v-spacer>
      <v-col cols="12" sm="6">
        <DsfrPagination v-model="page" :length="Math.ceil(partnerCount / limit)" :total-visible="7" />
      </v-col>
      <v-spacer></v-spacer>
    </v-row>
    <v-row>
      <v-col v-for="partner in visiblePartners" :key="partner.id" style="height: auto;" cols="12" sm="6" md="4">
        <PartnerCard :partner="partner" />
      </v-col>
    </v-row>
  </div>
</template>

<script>
import BreadcrumbsNav from "@/components/BreadcrumbsNav"
import DsfrPagination from "@/components/DsfrPagination"
import PartnerCard from "@/views/PartnersPage/PartnerCard"

export default {
  name: "PartnersHome",
  components: { BreadcrumbsNav, DsfrPagination, PartnerCard },
  data() {
    return {
      limit: 6,
      page: null,
      types: [],
      visiblePartners: null,
      partnerCount: null,
      filters: [
        {
          key: "free",
          frenchKey: "gratuit",
          value: undefined, // will be set from URL query
        },
        {
          key: "category",
          frenchKey: "besoin",
          value: undefined,
        },
      ],
    }
  },
  computed: {
    loading() {
      return this.partnerCount === null
    },
    offset() {
      return (this.page - 1) * this.limit
    },
    query() {
      let query = {}
      if (this.page) query.page = String(this.page)
      this.filters.forEach((f) => {
        if (f.value) query[f.frenchKey] = f.value
      })
      return query
    },
  },
  methods: {
    fetchCurrentPage() {
      let queryParam = `limit=${this.limit}&offset=${this.offset}`
      this.filters.forEach((f) => {
        if (Array.isArray(f.value)) {
          f.value.forEach((v) => {
            queryParam += `&${f.key}=${v}`
          })
        } else if (f.value) queryParam += `&${f.key}=${f.value}`
      })
      return fetch(`/api/v1/partners/?${queryParam}`)
        .then((response) => {
          if (response.status < 200 || response.status >= 400) throw new Error(`Error encountered : ${response}`)
          return response.json()
        })
        .then((response) => {
          this.partnerCount = response.count
          this.visiblePartners = response.results
        })
        .catch((e) => {
          this.partnerCount = 0
          this.$store.dispatch("notifyServerError", e)
        })
    },
    populateParameters() {
      this.filters.forEach((f) => {
        f.value = this.$route.query[f.frenchKey]
      })
      this.page = this.$route.query.page ? parseInt(this.$route.query.page) : 1
    },
    changePage() {
      const override = this.page ? { page: this.page } : { page: 1 }
      const query = Object.assign(this.query, override)
      this.fetchCurrentPage().then(() => this.updateRouter(query))
    },
    updateRouter(query) {
      if (this.$route.query.page) {
        this.$router.push({ query }).catch(() => {})
      } else {
        this.$router.replace({ query }).catch(() => {})
      }
    },
  },
  watch: {
    page() {
      this.changePage()
    },
    $route() {
      this.populateParameters()
    },
  },
  mounted() {
    this.populateParameters()
  },
}
</script>
