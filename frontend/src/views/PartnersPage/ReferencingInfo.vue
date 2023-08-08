<template>
  <div>
    <p>
      Ce service est en expérimentation jusqu'à décembre 2023. Les acteurs se sont référencés eux mêmes en respectant
      notre charte.
    </p>
    <DownloadLink
      href="/static/documents/charte-referencement-acteurs-de-l-ecosysteme.pdf"
      label="Télécharger la charte de référencement"
      sizeStr="187.3 ko"
    />
  </div>
</template>

<script>
import DownloadLink from "@/components/DownloadLink"

export default {
  name: "ReferencingInfo",
  components: { DownloadLink },
}
</script>
