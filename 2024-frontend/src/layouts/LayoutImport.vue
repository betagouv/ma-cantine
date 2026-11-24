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
const props = defineProps(["schemaFile", "exampleFile", "filePreviews", "links", "apiUrl", "apiImportType", "schemaVersion", "adminCallout", "successMessage"])

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
  <div class="fr-col-12 fr-col-md-7">
    <h1>{{ route.meta.title }}</h1>
    <p v-if="$slots.default">
      <slot></slot>
    </p>
  </div>
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
