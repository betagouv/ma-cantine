<template>
  <div class="text-left" v-if="canteen">
    <h1 class="text-h4 font-weight-black">
      {{ canteen.name }}
    </h1>
    <CanteenIndicators :canteen="canteen" :singleLine="true" class="grey--text text--darken-3" />
    <CanteenPublication :canteen="canteen" />
    <v-btn class="primary" target="_parent" :href="link">
      Voir sur la plateforme
      <v-icon small class="ml-2">mdi-open-in-new</v-icon>
    </v-btn>
  </div>
</template>

<script>
import CanteenPublication from "@/components/CanteenPublication"
import CanteenIndicators from "@/components/CanteenIndicators"
import labels from "@/data/quality-labels.json"

export default {
  data() {
    return {
      canteen: undefined,
      labels,
      claimSucceeded: false,
    }
  },
  components: {
    CanteenPublication,
    CanteenIndicators,
  },
  props: {
    canteenUrlComponent: {
      type: String,
      required: true,
    },
  },
  computed: {
    loggedUser() {
      return this.$store.state.loggedUser
    },
    showClaimCanteen() {
      return this.canteen && this.canteen.canBeClaimed
    },
    currentPage() {
      return window.location.pathname
    },
    link() {
      const l = document.location
      const prefixLength = "/widgets".length
      return `${l.origin}${l.pathname.slice(prefixLength)}`
    },
  },
  methods: {
    setCanteen(canteen) {
      this.canteen = canteen
      if (canteen) document.title = `${this.canteen.name} - ${this.$store.state.pageTitleSuffix}`
    },
  },
  beforeMount() {
    const previousIdVersion = this.canteenUrlComponent.indexOf("--") === -1
    const id = previousIdVersion ? this.canteenUrlComponent : this.canteenUrlComponent.split("--")[0]
    return fetch(`/api/v1/publishedCanteens/${id}`)
      .then((response) => {
        if (response.status != 200) throw new Error()
        response.json().then(this.setCanteen)
      })
      .catch(() => {
        this.$store.dispatch("notify", {
          message: "Nous n'avons pas trouvé cette cantine",
          status: "error",
        })
        this.$router.push({ name: "CanteensHome" })
      })
  },
}
</script>
