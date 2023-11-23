<template>
  <nav role="navigation" class="fr-breadcrumb text-left" aria-label="vous êtes ici :">
    <button
      class="fr-breadcrumb__button text-decoration-underline"
      :aria-expanded="expanded"
      aria-controls="breadcrumb-1"
      v-if="!expanded && $vuetify.breakpoint.xs"
      @click="expanded = true"
    >
      Voir le fil d’Ariane
    </button>
    <v-expand-transition>
      <div class="fr-collapse" id="breadcrumb-1" v-show="$vuetify.breakpoint.smAndUp || expanded">
        <ol class="fr-breadcrumb__list pl-0">
          <li>
            <router-link class="fr-breadcrumb__link" :to="homePage.to">{{ homePage.title }}</router-link>
          </li>
          <li v-for="link in breadcrumbLinks" :key="link.title">
            <router-link class="fr-breadcrumb__link" :to="link.to">{{ link.title }}</router-link>
          </li>
          <li>
            <a class="fr-breadcrumb__link" aria-current="page">{{ pageTitle }}</a>
          </li>
        </ol>
      </div>
    </v-expand-transition>
  </nav>
</template>

<script>
import { routes } from "@/router"

export default {
  name: "BreadcrumbsNav",
  props: {
    links: {
      type: Array, // objects of to & (optionally) title
      required: false,
    },
    title: {
      type: String,
      required: false,
    },
  },
  data() {
    let breadcrumbRoutes = JSON.parse(JSON.stringify(routes))
    // flatten routes for simplicity
    breadcrumbRoutes.forEach((r) => {
      if (r.children) {
        breadcrumbRoutes.push(...r.children)
      }
    })
    return {
      breadcrumbRoutes,
      expanded: false,
    }
  },
  computed: {
    homePage() {
      const authenticationRequired = this.$route.meta?.authenticationRequired
      if (authenticationRequired)
        return {
          title: "Mon tableau de bord",
          to: { name: "ManagementPage" },
        }
      return {
        title: "Acceuil",
        to: { name: "LandingPage" },
      }
    },
    pageTitle() {
      return this.title || this.breadcrumbRoutes.find((r) => r.name === this.$route.name)?.meta?.title
    },
    breadcrumbLinks() {
      if (this.links) {
        this.links.forEach((link) => {
          if (!link.title) {
            link.title = this.breadcrumbRoutes.find((r) => r.name === link.to.name)?.meta?.title
          }
        })
      }
      return this.links
    },
  },
}
</script>

<style scoped>
nav {
  --text-mention-grey: rgb(102, 102, 102);
  --underline-max-width: 100%;
  --underline-hover-width: 0;
  --underline-idle-width: var(--underline-max-width);
  --underline-x: calc(var(--underline-max-width) * 0);
  --underline-img: linear-gradient(0deg, currentColor, currentColor);
  --grey-50-1000: #161616;
  --text-active-grey: var(--grey-50-1000);
}

a {
  color: var(--text-mention-grey) !important;
  text-decoration: none;
}

a:hover {
  text-decoration: underline;
}
/* https://gouvfr.atlassian.net/wiki/spaces/DB/pages/223019574/D+veloppeurs */
/*!
 * DSFR v1.7.2 | SPDX-License-Identifier: MIT | License-Filename: LICENSE.md | restricted use (see terms and conditions)
 */

/**
un padding de 4px et une marge négative en compensation sont mis en place afin d'éviter de couper le focus.
 */
.fr-breadcrumb {
  margin: 1rem 0 2rem;
  font-size: 0.75rem;
  line-height: 1.25rem;

  --text-spacing: 0 0 0.5rem;
  position: relative;

  /**
   * margin-bottom de 2v pour créer cet espace entre chaque ligne
   */
  color: var(--text-mention-grey);
}

.fr-breadcrumb__button {
  font-size: 0.75rem;
  line-height: 1.25rem;
  margin: 0;
  padding: 0;
  color: inherit;
}

.fr-breadcrumb .fr-collapse {
  margin-left: -4px;
  margin-right: -4px;
  padding-left: 4px;
  padding-right: 4px;
  transform: translateY(-4px);
}

.fr-breadcrumb__list {
  --ul-type: none;
  --ol-type: none;
  --ul-start: 0;
  --ol-start: 0;
  --xl-block: 0;
  --li-bottom: 0;
  --ol-content: none;
  transform: translateY(4px);
}

.fr-breadcrumb__list li {
  display: inline;
  line-height: 1.75rem;

  /**
  * flèche séparatrice en font-icon
  */
}

.fr-breadcrumb__list li:not(:first-child)::before {
  flex: 0 0 auto;
  display: inline-block;
  background-color: currentColor;
  width: var(--icon-size);
  height: var(--icon-size);
  -webkit-mask-size: 100% 100%;
  mask-size: 100% 100%;
  -webkit-mask-image: url("/static/icons/arrow-right-s-line.svg");
  mask-image: url("/static/icons/arrow-right-s-line.svg");
  --icon-size: 1rem;
  content: "";
  margin-left: 0.25rem;
  margin-right: 0.25rem;
  vertical-align: calc((1.05rem - var(--icon-size)) * 0.5);
}

.fr-breadcrumb__link {
  vertical-align: top;
  position: relative;
  font-size: 0.75rem;
  line-height: 1.25rem;
}

.fr-breadcrumb__link[aria-current]:not([href]) {
  pointer-events: none;
  cursor: default;
}

.fr-breadcrumb__link[aria-current] {
  color: var(--text-active-grey) !important;
}
@media (max-width: 62em) {
  /* mdAndDown */
  a:not([aria-current]) {
    text-decoration: underline;
  }
}
@media (min-width: 48em) {
  /*! media md */
  .fr-breadcrumb {
    margin-bottom: 2.5rem;
  }

  .fr-breadcrumb .fr-collapse {
    margin-left: 0;
    margin-right: 0;
    padding-left: 0;
    padding-right: 0;
    transform: none;
    visibility: inherit;
    overflow: visible;
    max-height: initial;
  }

  .fr-breadcrumb .fr-collapse::before {
    content: none;
  }

  .fr-breadcrumb__list {
    transform: none;
  }
  /*! media md */
}
</style>
