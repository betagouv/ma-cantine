<template>
  <v-card outlined class="pa-8 pb-2 fr-downloads-group">
    <h3 class="mb-6">{{ groupTitle }}</h3>
    <ul>
      <li v-for="(link, idx) in links" :key="idx">
        <DownloadLink v-bind="link" />
      </li>
    </ul>
  </v-card>
</template>

<script>
import DownloadLink from "./DownloadLink"

export default {
  components: { DownloadLink },
  props: ["groupTitle", "links"],
  computed: {
    type() {
      const strParts = this.href.split(".")
      return strParts[strParts.length - 1].toUpperCase()
    },
  },
}
</script>

<style scoped>
/*!
 * DSFR v1.7.2 | SPDX-License-Identifier: MIT | License-Filename: LICENSE.md | restricted use (see terms and conditions)
 */
/* .fr-downloads-group__title {
  font-weight: 700;
  font-size: 1.375rem;
  line-height: 1.75rem;
} */

.fr-downloads-group > ul {
  margin-top: 0;
  margin-bottom: 0;
}

.fr-downloads-group > ul > li {
  padding-bottom: 0;
}

.fr-downloads-group li::marker {
  --primary: #0c7f46;
  color: var(--primary);
}

@media (min-width: 48em) {
  /*! media md */

  /*! media md */
  .fr-downloads-group__title {
    font-size: 1.5rem;
    line-height: 2rem;
  }

  .fr-downloads-group--bordered {
    padding: 2rem 2rem 0.5rem;
  }

  .fr-downloads-group .fr-download {
    margin-bottom: 1.5rem;
  }
}
</style>
