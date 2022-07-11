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
        <v-expansion-panel-header class="font-weight-bold" style="line-height: 20px;">
          {{ question.title }}
        </v-expansion-panel-header>
        <v-expansion-panel-content class="faq-answer">
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
          title: "L'inscription sur « ma-cantine » est-elle obligatoire ?",
          answer:
            "Non, elle est cependant fortement encouragée. « ma-cantine » est un service numérique opéré par le Ministère en charge de l’agriculture (MASA) avec l’appui de la Direction Interministérielle du numérique (DINUM). Cette plateforme est à la fois un outil d’accompagnement pour les gestionnaires, un outil d’information pour les convives citoyens et un outil de transmission d’information pour l’administration. L’inscription des gestionnaires, responsables légaux d’un service de restauration (dans les secteurs public et privé) est fortement recommandée pour bénéficier d'un accompagnement à la mise en place des mesures réglementaires des lois EGAlim et Climat et Résilience, de répondre à vos obligations d’information de vos convives et de faire remonter, par télédéclaration, les informations nécessaires pour le suivi de l’application de la loi, prévu dans le cadre du bilan statistique annuel.",
        },
        {
          title:
            "Qui peut s’inscrire sur « ma-cantine » ? Pour les restaurations en gestion concédée ou déléguée : qui doit remplir les données sur la plateforme « ma-cantine » ?",
          answer:
            "« ma-cantine » est destinée aux responsables légaux et aux gestionnaires publics et privés des services de restauration collective. Il leur revient de s’inscrire sur la plateforme et de créer leurs établissements. Dans le cas d’une gestion déléguée, si le donneur d’ordre n'a pas toutes les informations requises pour mettre à jour ses données dans « ma-cantine », il a deux options pour la transmission des données : soit il les demande à son prestataire et les renseigne lui-même dans son espace « cantine » ; soit il autorise le prestataire à les saisir lui-même dans la cantine dont il est gestionnaire, dans son espace « cantine ». Le prestataire doit se créer un compte dans « ma-cantine » et doit être autoriser à rejoindre la cantine par le donneur d’ordre.",
        },
        {
          title: "Nous sommes un RPI et avons une cantine dans la commune mais pas de gestionnaire, suis-je concerné ?",
          answer:
            "Vous pouvez inscrire votre cantine (qui est un satellite fourni par une cuisine centrale) et nous communiquer les informations sur votre correspondant de la cuisine centrale.",
        },
        {
          title: "Je suis en gestion concédée/approvisionné par un restaurateur privé, suis-je concerné ?",
          answer:
            "Vous êtes concerné et vous êtes encouragé à vous référencer sur « ma-cantine » (création de compte et création de cantine). Vous pourrez demander à votre prestataire les informations nécessaires - notamment sur les achats.",
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
        {
          title:
            "Pourquoi fournir les valeurs d’achat et pas les parts (en %) des produits durables et de qualité, et de produits bio à la place des valeurs d’achats ?",
          answer:
            "Le décret du 23 avril 2019, pris en application de la loi EGAlim du 30 octobre 2018 précise que ces parts (taux EGAlim) sont calculées à partir des valeurs d’achats HT des produits alimentaires. Seules les valeurs d’achat permettent de réaliser le bilan statistique annuel.",
        },
        {
          title:
            "Quelles sont les obligations pour le délégataire d’un donneur d’ordre, de lui transmettre les valeurs d’achat des produits alimentaires utiliser dans la fabrication des repas de son service de restauration tous les ans ? ",
          answer:
            "L’obligation d’atteinte des taux EGAlim s’impose aux donneurs d’ordre et ils sont responsables de l’information de leurs convives. Les taux EGAlim sont calculés à partir des valeurs d’achats HT des produits alimentaires. Seules les valeurs d’achat sont les informations qui permettront à l’administration de réaliser le bilan annuel qui doit être remis au parlement et rendu public. Cette obligation de transmission d’information peut être reportée dans le contrat qui lie le donneur d’ordre et son prestataire. ne convention de délégation pour la déclaration des éléments relatifs à l’établissement du bilan statistique annuel et la transmission des valeurs d’achat des denrées utilisées pour la fabrication des repas servis peut être établie entre la collectivité et les établissement (voir modèle proposé sur « ma cantine »).",
        },
        {
          title: "Cas particulier des cuisines centrales et leurs satellites",
          answer:
            "Les cuisines centrales sont des établissements dont tout ou partie de l'activité consiste en la fabrication de préparations culinaires destinées à être livrées à au moins un restaurant satellite. Les personnes morales ayant la charge d’un restaurant collectif informent à l’entrée du restaurant, par un affichage permanent, actualisé au moins une fois par an, lisible par tous les usagers, et au moins une fois par an par communication électronique, les usagers des restaurants collectifs de la part des produits dit « EGAlim » et de la part des produits issus de projets alimentaires territoriaux entrant dans la composition des repas servis (Article L. 230-5-3 du code rural). Pour que cette mesure puisse être mise en œuvre, la cuisine centrale doit fournir pour chacun de des restaurants satellites qu’elle livre, les données d’achat correspondant aux denrées utilisées pour la confection des repas des convives. Ainsi, il est recommandé dans « ma-cantine » que les restaurants satellites soit considérés comme des cantines et déclarés comme tels par les cuisines centrales qui les livrent.",
        },
        {
          title:
            "A qui les données relatives aux achats de denrées alimentaires déclarées dans « ma-cantine » sont-elles fournies ? Pour quoi faire ?",
          answer:
            "Les données télé-déclarées dans « ma-cantine » sont transmises à la DGAL (Direction générale de l’Alimentation - ministère de l’Agriculture et de la Souveraineté alimentaire (MASA) en vue d’alimenter le bilan annuel à remettre au Parlement qui sera un document public. Néanmoins, les données recueillies par télédéclaration seront traitées de manière agrégée pour réaliser le bilan annuel et aucune donnée individuelle ne sera rendue publique dans ce cadre. ",
        },
        {
          title:
            "Comment sont vérifiées les obligations des lois EGAlim et Climat et Résilience visant la restauration collective ?",
          answer:
            "A ce jour, la loi ne prévoit pas de sanctions, ni de contrôles pour ce qui concerne les mesures ciblant directement la restauration collective. Cependant la loi EGAlim et plus récemment la Climat et Résilience prévoient un renforcement de la transparence vis-à-vis des convives avec notamment l’obligation d’une information des convives sur leur lieu de repas, de la mise en œuvre des objectifs en matière de produits durables et de qualité entrant dans la composition des repas (Art. L. 230-5-3 du code rural) et d’une information aux citoyens au travers un bilan statistique annuel de l’application de ces objectifs, remis au Parlement par le Gouvernement et rendu public depuis le 1 er janvier 2022 (Article L. 230-5-1 du code rural).",
        },
      ],
    }
  },
}
</script>

<style scoped>
.faq-answer {
  white-space: pre-line;
}
</style>
