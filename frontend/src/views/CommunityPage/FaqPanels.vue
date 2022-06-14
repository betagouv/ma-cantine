<template>
  <div>
    <h2 class="font-weight-black text-h5 mb-4">Foire aux questions</h2>
    <p>
      Vous n'êtes pas familier avec les obligations réglementaires ? Vous vous posez des questions sur votre
      responsabilité ? Vous avez besoin d'aide sur plusieurs aspects techniques ou légaux ? Rassurez-vous ! Vous n'êtes
      pas les seuls à vous poser ces questions.
    </p>
    <v-expansion-panels>
      <v-expansion-panel v-for="question in questions" :key="question.title">
        <v-expansion-panel-header class="font-weight-medium">
          {{ question.title }}
        </v-expansion-panel-header>
        <v-expansion-panel-content>
          {{ question.answer }}
        </v-expansion-panel-content>
      </v-expansion-panel>
    </v-expansion-panels>

    <div class="mt-6 d-flex">
      <v-btn large :to="{ name: 'ContactPage' }" outlined color="primary">
        <v-icon class="mr-2">mdi-help-circle</v-icon>
        Soumettre une nouvelle question
      </v-btn>
    </div>
  </div>
</template>

<script>
export default {
  name: "FaqPanels",
  data() {
    return {
      questions: [
        {
          title: "L'inscription sur Ma Cantine est-elle obligatoire ?",
          answer:
            "L'inscription est fortement recommandée dès maintenant pour bénéficier d'un accompagnement à la mise en place des mesures réglementaires des lois EGAlim et Climat et résilience. Elle est aussi un moyen de répondre à vos obligations d'information de vos convives et de faire remonter les informations nécessaires pour le suivi de l'application de la loi (bilan statistique annuel).",
        },
        {
          title: "Qui est le responsable restauration, qui doit etre désigné sous ma cantine ?",
          answer:
            "La structure/personne responsable légal du service de restauration : élu, responsable administratif de la collectivité D'autres personnes peuvent être associées à votre compte cantine : personne qui fait les commandes, celle qui reçoit les repas et met en chauffe, le prestataire peut aussi participer au renseignement des informations concernant votre cantine si vous lui donnez un accès à votre compte « cantine ». Il suffit d'indiquer son mail dans la partie « gestionnaire additionnel » de votre profil. Exemple : si la gestion des repas est assurée par un SIVU par le biais d'une cuisine centrale. Le SIVU doit créer un compte dans ma cantine pour inscrire sa cantine et déclarer le nombre de cantines sites (satellites) desservis et vous pouvez aussi créer votre cantine le satellite desservis par cette cuisine centrale.",
        },
        {
          title: "Nous sommes satellites, faut-il se référencer dans ma cantine ?",
          answer:
            "Oui. Il est également nécessaire de donner l'info (SIRET) sur sa cuisine centrale qui dessert la cantine.",
        },
        {
          title: "Nous sommes un RPI et avons une cantine dans la commune mais pas de gestionnaire, suis-je concerné ?",
          answer:
            "Vous pouvez inscrire votre cantine (qui est un satellite fourni par une cuisine centrale) et nous communiquer les informations sur votre correspondant de la cuisine centrale.",
        },
        {
          title: "Je suis en gestion concédée/approvisionné par un restaurateur privé, suis-je concerné ?",
          answer:
            "Vous êtes concerné et vous êtes encouragé à vous référencer sur ma cantine (création de compte et création de cantine). Vous pourrez demander à votre prestataire les informations nécessaires - notamment sur les achats.",
        },
        {
          title:
            "Il y a confusion, ma commune n’est pas dans le département indiqué dans le mail reçu, suis-je concerné ?",
          answer: "Si, vous êtes bien concerné et c'est une erreur d'homonymie suite à l'envoi d'un mail type.",
        },
        {
          title: "Je n’ai pas d’école ni de cantine dans ma commune, suis-je concerné ?",
          answer: "Non, vous n'êtes pas concerné.",
        },
      ],
    }
  },
}
</script>
