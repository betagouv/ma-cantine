<template>
  <DsfrBadge :mode="isPublished ? 'SUCCESS' : 'INFO'" :icon="isPublished ? 'mdi-circle' : 'mdi-circle-outline'">
    <span class="text-uppercase">
      {{ isPublished ? "En ligne" : "Non publiée" }}
    </span>
  </DsfrBadge>
</template>

<script>
import DsfrBadge from "@/components/DsfrBadge"
export default {
  name: "PublicationBadge",
  props: {
    isPublished: {
      type: Boolean,
      required: true,
    },
  },
  components: { DsfrBadge },
}
</script>
