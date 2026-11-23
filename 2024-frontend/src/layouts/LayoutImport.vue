<script setup>
import { ref } from "vue"
import { useRoute } from "vue-router"
import ImportExplanation from "@/components/ImportExplanation.vue"
import ImportFilesExample from "@/components/ImportFilesExample.vue"
import ImportSchemaTable from "@/components/ImportSchemaTable.vue"
import ImportAdminCallout from "@/components/ImportAdminCallout.vue"
import ImportFileUpload from "@/components/ImportFileUpload.vue"
import ImportSuccessModal from "@/components/ImportSuccessModal.vue"
import ImportHelp from "@/components/ImportHelp.vue"

/* Router and Props */
const route = useRoute()
const props = defineProps({
  schemaFile: String,
  exampleFile: Object,
  filePreviews: Object,
  links: Array,
  apiUrl: String,
  apiImportType: String,
  schemaVersion: String,
  adminCallout: Boolean,
  successMessage: Function,
})

/* Success */
const showModal = ref(false)
const message = ref("")

const success = (count) => {
  message.value = props.successMessage(count)
  showModal.value = true
}
</script>

<template>
  <slot name="before-title"></slot>
  <h1>{{ route.meta.title }}</h1>
  <p v-if="$slots.default" class="fr-col-12 fr-col-md-7">
    <slot></slot>
  </p>
  <ImportExplanation :exampleFile :links />
  <ImportFilesExample v-if="filePreviews" :filePreviews />
  <ImportSchemaTable :schemaFile />
  <ImportAdminCallout v-if="adminCallout" />
  <ImportFileUpload
    @success="success"
    :apiUrl
    :apiImportType
    :schemaVersion
  />
  <ImportSuccessModal
    :opened="showModal"
    :message
    @close="showModal = false"
  />
  <ImportHelp />
</template>
