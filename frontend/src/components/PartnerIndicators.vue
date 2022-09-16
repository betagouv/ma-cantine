<template>
  <div>
    <p :class="{ 'my-0': true, inline: singleLine }" v-if="types">
      <v-icon small>$store-fill</v-icon>
      <span class="ml-1">{{ types }}</span>
    </p>
    <p :class="{ 'my-0': true, inline: singleLine }" v-if="partner.economicModel === 'public'">
      <v-icon small>$france-fill</v-icon>
      <span class="ml-1">Public</span>
    </p>
    <p :class="{ 'my-0': true, inline: singleLine }" v-if="partner.economicModel === 'private'">
      <v-icon small>$building-fill</v-icon>
      <span class="ml-1">Privée</span>
    </p>
    <p :class="{ 'my-0': true, inline: singleLine }" v-if="partner.free === true">
      <v-icon small v-if="partner.free === true">$money-euro-circle-fill</v-icon>
      <span class="ml-1">Gratuit</span>
    </p>
    <p :class="{ 'my-0': true, inline: singleLine }" v-if="partner.national">
      <v-icon small>$road-map-fill</v-icon>
      <span class="ml-1">Présent dans tout le territoire</span>
    </p>
    <p :class="{ 'my-0': true, inline: singleLine }" v-else-if="departments">
      <v-icon small>$road-map-fill</v-icon>
      <span class="ml-1">{{ departments }}</span>
    </p>
  </div>
</template>

<script>
import jsonDepartments from "@/departments.json"

export default {
  name: "PartnerIndicators",
  props: {
    partner: {
      type: Object,
      required: true,
    },
    singleLine: {
      type: Boolean,
      default: false,
    },
  },
  computed: {
    departments() {
      if (!this.partner.departments) return null
      const depCopy = jsonDepartments
      const departments = depCopy
        .filter((x) => this.partner.departments.indexOf(x.departmentCode) > -1)
        .map((x) => x.departmentName)
        .join(", ")
      return departments
    },
    types() {
      if (!this.partner.types) return null
      return this.partner.types.join(", ")
    },
  },
}
</script>

<style scoped>
.inline {
  display: inline;
}
</style>
