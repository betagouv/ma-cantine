<script setup>
import { ref, computed } from "vue"
import diagnosticsFieldsService from "@/services/diagnosticsFields"

const props = defineProps(["name"])
const data = computed(() => diagnosticsFieldsService.getField(props.name))

/* Field */
const field = ref(null)
const isNumber = computed(() => data.value.type === "number")
const isRequired = computed(() => data.value.required)
const label = computed(() => data.value.label)
</script>
<template>
  <DsfrInputGroup v-if="isNumber" :modelValue="field" :label="label" :label-visible="true" :name="props.name" type="number" :required="isRequired" @change="updateField" />
  <pre v-else>{{ field }}</pre>
</template>
