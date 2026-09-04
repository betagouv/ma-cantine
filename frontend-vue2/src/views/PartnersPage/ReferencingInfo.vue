<template>
  <div>
    <p>
      Ce catalogue référence, en continu, des acteurs privés ou publics en capacité de vous apporter une aide (gratuite)
      ou un service (payant) dans votre démarche d'alimentation durable.
    </p>
    <p>
      Ces acteurs s'auto-référencent en acceptant notamment la charte des acteurs de l'éco-système.
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
