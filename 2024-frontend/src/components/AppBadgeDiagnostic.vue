<script setup>
import { computed } from "vue"
import { storeToRefs } from "pinia"
import { useStoreCampaignDates } from "@/stores/campaignDates.js"
import diagnosticsBadgeService from "@/services/diagnosticsBadge.js"

const props = defineProps(["action"])

const campaignDatesStore = useStoreCampaignDates()
const { currentCampaignInformations } = storeToRefs(campaignDatesStore)

const badge = computed(() => diagnosticsBadgeService.getBadge(props.action, currentCampaignInformations.value))
</script>

<template>
  <DsfrBadge v-if="badge.label" :label="badge.label" :type="badge.type" :no-icon="!badge.icon" />
</template>
