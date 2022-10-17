<template>
  <div>
    <v-expansion-panels hover accordion tile flat>
      <v-expansion-panel v-for="question in questions" :key="question.title">
        <v-expansion-panel-header class="px-3" expand-icon="mdi-plus" disable-icon-rotate v-slot="{ open }">
          <span :class="open && 'font-weight-bold'">{{ question.title }}</span>
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
          title: "Qu'est-ce que ma-cantine ?",
          answer:
            "ma cantine est un service numérique opéré par le Ministère en charge de l’agriculture (MASA) avec l’appui de la Direction Interministérielle du Numérique (DINUM). Son objectif est d'accompagner la transition alimentaire des services de restauration collective, les cantines vers une alimentation et une consommation plus durable. Cette plateforme est à la fois un outil d’accompagnement pour les gestionnaires, un outil d’information pour les convives citoyens et un outil de transmission d’information vers l’administration pour le suivi de cette transition.",
        },
        {
          title: "Pourquoi s'inscrire ?",
          answer:
            "L’inscription des gestionnaires, responsables légaux d’un service de restauration (dans les secteurs public et privé), leur permet de bénéficier d'un accompagnement à la mise en place des mesures réglementaires des lois EGAlim et Climat et Résilience et de répondre aux obligations d’information des convives. ma cantine est également la plateforme pour faire remonter, par télédéclaration chaque année, les données relatives aux achats de denrées alimentaires qui permettent de calculer les taux EGAlim requis par la loi pour que l’État réalise le bilan annuel du suivi des objectifs de la loi EGalim.",
        },
        {
          title: "L'inscription sur « ma-cantine » est-elle obligatoire ?",
          answer:
            "Oui.  Le décret du 23 avril 2019, pris en application de la loi EGAlim du 30 octobre 2018, prévoit la réalisation d’un bilan statistique de la mise en œuvre des obligations prévues par la loi, sur la base des éléments transmis, dans des conditions fixées par l'arrêté ministériel du 14 septembre 2022. Ce dernier précise la nature des informations à déclarer et le moyen de le faire par ma-cantine.",
        },
        {
          title: "Qui peut s’inscrire sur ma-cantine ?",
          answer:
            "ma cantine est destinée aux responsables légaux et aux gestionnaires publics et privés des services de restauration collective. Concrètement, il s'agit de plusieurs types de peronnes : Élu(e)s de collectivité, Directeur(trice) d’établissement, Gestionnaire administratif, Comptable, Responsable Restauration, Chef(fe) et ou cuisinier. Plusieurs personnes peuvent etre rattachées à une même cantine. Les services de restauration peuvent etre en gestion directe ou en gestion déléguée/concédée.",
        },
        {
          title: "Comment s’inscrire sur ma-cantine ?",
          answer:
            "Il faut procéder en plusieurs étapes qui sont documentées à ce lien (https://ma-cantine-1.gitbook.io/ma-cantine-egalim/tuto-utilisation-de-la-plateforme-ma-cantine) : se créer un compte sur ma-cantine.agriculture.gouv.fr, créer sa cantine avec son numéro SIRET et créer un diagnostic pour par année civile.",
        },
        {
          title: "Je représente une commune mais ne gère pas la restauration scolaire de celle-ci, suis-je concernée ?",
          answer:
            "C'est au gestionnaire de la collectivité ou du groupement de collectivités (EPCI, intercom, syndicats,...) de s'inscrire et de créer les établissements. Vous pouvez également demander à cette personne un accès gestionnaire sur ces établissements.",
        },
        {
          title: "Est-il possible d’ajouter plusieurs cantines sous le même numéro SIRET ?",
          answer:
            "Il n’est pas possible d’ajouter plusieurs cantines sous un seul et même SIRET. Dans la plupart des cas, chaque cantine dispose de son numéro de SIRET propre. Vous pouvez le trouver ici : https://annuaire-entreprises.data.gouv.fr/. Concernant les cantines scolaires, vous pouvez retrouver le SIRET de l’établissement rattaché à la cantine sur l’Annuaire de l’éducation : https://annuaire-education.fr/. Dans certains cas, il est possible que certaines cantines n’aient pas de SIRET : dans ce cas uniquement, il est possible d’indiquer le numéro de SIRET de la collectivité desservant ces cantines.",
        },
        {
          title: "Le SIRET est-il obligatoire pour créer ma cantine ?",
          answer:
            "Oui. Il est possible de le trouver ici : https://annuaire-entreprises.data.gouv.fr/. Concernant les cantines scolaires, vous pouvez retrouver le SIRET de l’établissement rattaché à la cantine sur l’Annuaire de l’éducation : https://annuaire-education.fr/.",
        },
        {
          title:
            "Je suis en gestion concédée/approvisionné par un restaurateur privé (société de restauration collective, traiteur, prestataire,...), suis-je concerné ?",
          answer:
            "Oui, vous êtes concerné. Dans le cas d’une gestion déléguée/concédée, si en tant que donneur d’ordre vous n'avez pas toutes les informations requises pour mettre à jour vos données d'achat dans ma-cantine, vous avez deux options: soit vous les demandez à votre prestataire et les renseignez dans votre espace cantine ; soit vous autorisez le prestataire à les saisir lui-même dans votre espace cantine. Dans ce cas, votre prestataire doit se créer un compte dans ma-cantine et vous devez l'ajouter en gestionnaire de l'établissement.",
        },
        {
          title:
            "Mon prestatiaire ou délégataire refuse de me transmettre mes données d'achats. Quelles obligations pour lui ?",
          answer:
            "L’obligation d’atteinte des taux EGAlim s’impose aux donneurs d’ordre et ils sont responsables d'en faire une information donnée à leurs convives. Les taux EGAlim sont calculés à partir des valeurs d’achats HT des produits alimentaires. D'autre part, les valeurs d’achat sont les informations qui permettront à l’administration de réaliser le bilan annuel qui doit être remis au parlement et rendu public. Cette obligation de transmission d’information peut être reportée dans le contrat qui lie le donneur d’ordre et son prestataire. Une convention de délégation pour la déclaration de ces éléments peut être établie entre le donneur d'ordre et le délégataire. Un modèle de convention est proposé dans la documentation de ma-cantine (https://ma-cantine-1.gitbook.io/ma-cantine-egalim/procedure-campagne-de-remontee-des-donnees-2022).",
        },
        {
          title: "Je suis gestionnaire d'une cuisine centrale, suis-je concerné par l'inscription sur ma-cantine ?",
          answer:
            "Les gestionnaires de cuisines centrales doivent se créer un compte, creer leur cantine en déclarant chaque restaurants satellites qu’elles livrent. Jusqu'à la campagne 2024 de remontées des données de l'année civile 2023, les informations sur la mise en place des mesures EGAlim peuvent être centralisées au niveau de la cuisine centrale. A moyen terme, les informations devront etre attribuées à chaque cuisines satellites.",
        },
        {
          title: "Je suis gestionnaire d'une cuisine satellite, suis-je concerné par l'inscription sur ma-cantine ?",
          answer:
            "Oui. Les gestionnaires de cuisines satellites peuvent se créer un compte et ajouter leur cantine, sauf si la cuisine centrale qui les dessert l’a déjà fait. Dans ce cas, je peux être gestionnaire additionnel de cet établissement, en demandant un accès à la cuisine centrale. A moyen terme, les cuisines satellites devront indiquer leurs propres données en matière d’approvisionnement.",
        },
        {
          title:
            "Pourquoi, dans mon diagnostic, fournir les valeurs d’achat et pas les parts (en %) des produits durables et de qualité, et de produits bio à la place des valeurs d’achats ?",
          answer:
            "Le décret du 23 avril 2019, pris en application de la loi EGAlim du 30 octobre 2018 précise que ces parts (taux EGAlim) sont calculées à partir des valeurs d’achats HT des produits alimentaires. Seules les valeurs d’achat permettent de réaliser le bilan statistique annuel.",
        },
        {
          title:
            "A qui les données relatives aux achats de denrées alimentaires déclarées dans ma cantine sont-elles fournies ? Pour quoi faire ?",
          answer:
            "Les données d'achat saisies dans ma cantine (dans le diagnostic) sont à télédéclarer tous les ans. Elles sont transmises à la DGAL (Direction générale de l’Alimentation - ministère de l’Agriculture et de la Souveraineté Alimentaire (MASA) en vue d'etablir le bilan annuel à remettre au Parlement qui sera un document public. Les données recueillies par télédéclaration seront traitées de manière agrégée pour réaliser le bilan annuel et aucune donnée individuelle ne sera rendue publique dans ce cadre.",
        },
        {
          title:
            "Comment sont vérifiées les obligations des lois EGAlim et Climat et Résilience visant la restauration collective ?",
          answer:
            "A ce jour, la loi ne prévoit pas de sanctions, ni de contrôles pour ce qui concerne l'atteinte des mesures EGAlim ciblant directement la restauration collective. Cependant la loi EGAlim et plus récemment la Climat et Résilience prévoient un renforcement de la transparence vis-à-vis des convives avec notamment l’obligation d’une information des convives sur leur lieu de repas, de la mise en œuvre des objectifs en matière de produits durables et de qualité entrant dans la composition des repas (Art. L. 230-5-3 du code rural) et d’une information aux citoyens au travers un bilan statistique annuel de l’application de ces objectifs, remis au Parlement par le Gouvernement et rendu public depuis le 1 er janvier 2022 (Article L. 230-5-1 du code rural).",
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

.v-expansion-panel {
  box-shadow: inset 0 1px 0 0 #ddd, 0 1px 0 0 #ddd;
}
</style>
