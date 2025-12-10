<script setup>
import AppFormSendInquiry from "@/components/AppFormSendInquiry.vue"

const links = [
  {
    to: { name: "FoireAuxQuestions" },
    title: "Foire aux questions",
  },
  {
    to: { name: "CommunityPage" },
    title: "Webinaires",
  },
  {
    href: "https://ma-cantine.crisp.help/fr/",
    title: "Documentation",
  },
  {
    to: { name: "BlogsHome" },
    title: "Blog",
  },
]
</script>

<template>
  <h1>Contactez-nous</h1>
  <section>
    <h2>Ressources</h2>
    <ul class="fr-pl-0">
      <li v-for="link in links" :key="link.title">
        <router-link v-if="link.to" :to="link.to" class="fr-link fr-icon-arrow-right-line fr-link--icon-right">
          {{ link.title }}
        </router-link>
        <a
          v-else
          :href="link.href"
          :title="`${link.title} - ouvre une nouvelle fenêtre`"
          target="_blank"
          class="fr-text-title--blue-france"
        >
          {{ link.title }}
        </a>
      </li>
    </ul>
  </section>
  <section>
    <h2 class="mb-4">Avez-vous une autre question ?</h2>
    <AppFormSendInquiry />
  </section>
</template>

<style scoped>
ul {
  list-style: none;
}
</style>
