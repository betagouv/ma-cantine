<template>
  <div class="pt-12">
    <p>
      <DownloadLink
        href="/static/documents/charte_de_referencement_Version01_janvier2023.pdf"
        label="En savoir plus sur les critères de référencement sur la charte ma cantine"
        sizeStr="191 ko"
        target="_blank"
      />
    </p>
    <p class="caption">
      Cette page n’engage pas l’administration ou l'équipe ma cantine ; elle constitue une proposition à l'attention des
      responsables légaux de restaurants collectifs. Les structures sont seules responsables de la véracité des
      informations qu’elles communiquent sur la page partenaire.
    </p>
  </div>
</template>

<script>
import DownloadLink from "@/components/DownloadLink"

export default {
  name: "ReferencingInfo",
  components: { DownloadLink },
}
</script>
