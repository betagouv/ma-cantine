<script setup>
import AppFormSendInquiry from "@/components/AppFormSendInquiry.vue"
import documentation from "@/data/documentation.json"

const showContactAlert = window.SHOW_CONTACT_ALERT
const links = [
  {
    to: { name: "CommunityPage" },
    title: "Webinaires",
  },
  {
    href: documentation.accueil,
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
    <DsfrAlert v-if="showContactAlert" class="fr-col-12 fr-col-md-8 fr-mb-4w" title="☀️ Pendant l'été, notre équipe fonctionne en effectif réduit" description="Nos délais de réponse peuvent être plus longs qu'à l'habitude. Soyez assurés que nous traitons chaque demande avec attention et vous répondrons dès que possible. Merci de votre compréhension et veuillez nous excuser pour la gêne occasionnée." />
    <AppFormSendInquiry />
  </section>
</template>

<style scoped>
ul {
  list-style: none;
}
</style>
