<script setup>
import { ref } from "vue"
import AppModalIframe from "@/components/AppModalIframe.vue"

const props = defineProps(["title", "badge", "logo", "logoAlt", "documentation"])

/* Modal */
const opened = ref(false)
</script>
<template>
  <div class="ma-cantine--flex-between ma-cantine--flex-top ma-cantine--flex-gap-1 fr-mb-2w">
    <div>
      <h3 class="fr-h5" :class="props.badge ? 'fr-mb-1w' : 'fr-mb-0'">{{ props.title }}</h3>
      <DsfrBadge v-if="props.badge" :label="props.badge" type="new" small />
    </div>
    <div v-if="props.logo || props.documentation" class="ma-cantine--flex-start ma-cantine--flex-gap-1 ma-cantine--flex-shrink-0">
      <img v-if="props.logo" :src="props.logo" :alt="props.logoAlt" class="tunnel-teledeclaration-group-title__logos" />
      <DsfrButton v-if="props.documentation" label="En savoir plus" icon="fr-icon-add-line" icon-right tertiary size="sm" @click="opened = true" />
    </div>
  </div>
  <AppModalIframe v-if="props.documentation" :opened="opened" :title="props.title" :src="props.documentation" @close="opened = false" />
</template>

<style scoped lang="scss">
.tunnel-teledeclaration-group-title {

  &__logos {
    width: auto;
    height: 2rem;
  }
}
</style>
