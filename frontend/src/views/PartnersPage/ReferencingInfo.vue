<template>
  <div>
    <p>
      Ce service est en expérimentation pendant six mois. Les acteurs se sont référencés eux mêmes en respectant notre
      charte.
    </p>
    <p>
      Cette page n’engage pas l’administration ou l'équipe ma cantine ; elle constitue une proposition à l'attention des
      responsables légaux de restaurants collectifs
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
