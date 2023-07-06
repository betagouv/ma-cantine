<template>
  <div class="text-body-1">
    <h2 class="text-h2 mb-12">
      Nos partenaires
    </h2>

    <p class="text-center text-sm-left">
      « ma cantine » est une plateforme publique développée en collaboration avec la Direction Générale de
      l'Alimentation du Ministère de l'Agriculture et de l'Alimentation, suivant la méthode beta.gouv.fr de la DINUM
      (Direction Interministérielle du Numérique). C'est avec un objectif de partage et de complémentarité avec les
      acteurs de l'éco-système de la restauration collective que l'équipe s'efforce d'accompagner la transition
      alimentaire.
    </p>
    <v-row class="mt-8">
      <v-col
        v-for="partner in partners"
        :key="partner.imagePath"
        cols="6"
        sm="4"
        md="3"
        class="d-flex align-content-center justify-center"
      >
        <a
          class="d-flex"
          :style="`max-width: ${partner.maxWidth};`"
          :href="partner.href"
          target="_blank"
          rel="noopener noreferrer"
        >
          <v-img :src="partner.imagePath" :alt="partner.alt" contain></v-img>
          <span class="d-sr-only">{{ partner.alt }}</span>
        </a>
      </v-col>
    </v-row>
  </div>
</template>

<script>
export default {
  name: "StartupPartners",
  data() {
    return {
      partners: [
        {
          imagePath: "/static/images/Marianne.png",
          alt: "Ministère de l'Agriculture et de l'Alimentation",
          href: "https://agriculture.gouv.fr/thematique-generale/alimentation",
          maxWidth: "70%",
        },
        {
          imagePath: "/static/images/beta-gouv-logo.png",
          alt: "Beta.gouv",
          href: "https://beta.gouv.fr/",
          maxWidth: "65%",
        },
        {
          imagePath: "/static/images/partners/restau-co.png",
          alt: "Restau-Co",
          href: "https://restauco.fr/",
          maxWidth: "70%",
        },
        {
          imagePath: "/static/images/partners/unplusbio.jpeg",
          alt: "Un plus bio",
          href: "https://www.unplusbio.org/",
          maxWidth: "35%",
        },
        {
          imagePath: "/static/images/partners/opendata.png",
          alt: "Open Data France",
          href: "https://www.opendatafrance.net/",
          maxWidth: "60%",
        },
        {
          imagePath: "/static/images/partners/agores.jpeg",
          alt: "Agores",
          href: "https://www.agores.asso.fr/",
          maxWidth: "65%",
        },
        {
          imagePath: "/static/images/partners/les-pieds-dans-le-plat.jpeg",
          alt: "Les Pieds dans le Plat",
          href: "https://www.collectiflespiedsdansleplat.org/",
          maxWidth: "50%",
        },
        {
          imagePath: "/static/images/partners/logo-france-agri-mer.png",
          alt: "France Agri Mer",
          href: "https://www.franceagrimer.fr/",
          maxWidth: "65%",
        },
      ],
    }
  },
}
</script>
