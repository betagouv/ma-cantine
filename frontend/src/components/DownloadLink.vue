<template>
  <div class="fr-download">
    <p class="mb-0 primary--text">
      <a :href="href" download class="fr-download__link" :target="target">
        {{ label }}
        <span class="fr-download__detail grey--text text--darken-1">
          {{ type }} – {{ sizeStr }}
          <!-- e.g. JPG – 61,88 ko -->
        </span>
      </a>
    </p>
  </div>
</template>

<script>
export default {
  props: ["href", "label", "sizeStr", "target"],
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
.fr-download__link {
  z-index: 1;
  display: inline;
}

.fr-download {
  position: relative;
  padding-bottom: 1.5rem;
  margin: 0 0 1rem 0;
}

.fr-download .fr-download__link {
  font-size: 1rem;
  line-height: 1.5rem;
  padding: 0 0;
  overflow: initial;
  max-width: 100%;
  max-height: none;
}

.fr-download .fr-download__link::after {
  --icon-size: 1rem;
  margin-right: -0.125rem;
  margin-left: 0.5rem;
  flex: 0 0 auto;
  display: inline-block;
  vertical-align: calc((0.75em - var(--icon-size)) * 0.5);
  background-color: currentColor;
  width: var(--icon-size);
  height: var(--icon-size);
  -webkit-mask-size: 100% 100%;
  mask-size: 100% 100%;
  -webkit-mask-image: url("/static/icons/download-line.svg");
  mask-image: url("/static/icons/download-line.svg");
  content: "";
}

.fr-download .fr-download__link::before {
  content: none;
}

.fr-download__desc {
  font-size: 0.875rem;
  line-height: 1.5rem;
  font-weight: 400;
  display: none;
}

.fr-download__detail {
  position: absolute;
  bottom: 0;
  left: 0;
  font-size: 0.75rem;
  line-height: 1.25rem;
  font-weight: 400;
  max-width: 100%;
  white-space: nowrap;
  pointer-events: none;
  cursor: text;
  overflow: hidden;
  text-overflow: ellipsis;
}

.fr-download__detail abbr {
  text-decoration: none;
}
</style>
