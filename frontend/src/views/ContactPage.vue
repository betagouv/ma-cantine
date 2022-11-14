<template>
  <div class="text-left">
    <BreadcrumbsNav :links="[{ to: { name: 'FaqPage' } }]" />
    <h1 class="text-h4 font-weight-black mt-12 mb-8">Contactez-nous</h1>
    <h2 class="mb-4">Ressources</h2>
    <ul class="text-body-2 mb-8">
      <li v-for="link in links" :key="link.title" class="my-1">
        <router-link
          :to="link.to || {}"
          :href="link.href"
          :target="link.href && '_blank'"
          :rel="link.href && 'noopener'"
        >
          <v-icon small color="primary">mdi-chevron-right</v-icon>
          {{ link.title }}
          <v-icon v-if="link.href" small color="primary">mdi-open-in-new</v-icon>
        </router-link>
      </li>
    </ul>
    <h2 class="mb-4">Avez-vous une autre question ?</h2>
    <GeneralContactForm></GeneralContactForm>
  </div>
</template>

<script>
import GeneralContactForm from "@/components/GeneralContactForm"
import BreadcrumbsNav from "@/components/BreadcrumbsNav"

export default {
  name: "ContactPage",
  components: { GeneralContactForm, BreadcrumbsNav },
  data() {
    return {
      links: [
        {
          to: { name: "FaqPage" },
          title: "Foire aux questions",
        },
        {
          to: { name: "CommunityPage" },
          title: "Webinaires à venir",
        },
        {
          href: "https://ma-cantine-1.gitbook.io/ma-cantine-egalim/nos-webinaires",
          title: "Webinaires précedents",
        },
        {
          href: "https://ma-cantine-1.gitbook.io/ma-cantine-egalim/",
          title: "Documentation sur les lois et ressources",
        },
        {
          to: { name: "BlogsHome" },
          title: "Blog",
        },
      ],
    }
  },
}
</script>

<style scoped>
ul {
  list-style: none;
}
/* https://developer.mozilla.org/en-US/docs/Web/CSS/list-style-type#accessibility_concerns */
ul li::before {
  content: "\200B";
}
</style>
