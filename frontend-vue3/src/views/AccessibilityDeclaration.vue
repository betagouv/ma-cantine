<template>
  <div class="text-left">
    <!-- <BreadcrumbsNav /> -->
    <h1 class="my-6 fr-h1">Déclaration d'accessibilité</h1>
    <p>Cette page n'est pas une page d'aide.</p>
    <p>
      Elle vise à présenter nos engagements en matière d’accessibilité numérique puis à définir le niveau de conformité
      de ce présent site à la réglementation et aux référentiels en vigueur.
    </p>
    <h2 class="fr-h2">Qu’est-ce que l’accessibilité numérique ?</h2>
    <p>
      L’accessibilité numérique est un ensemble de règles et de bonnes pratiques qui couvrent notamment les aspects
      fonctionnels, graphiques, techniques et éditoriaux.
    </p>
    <p>
      Le suivi de ces règles et bonnes pratiques permet de s’assurer que les supports numériques (sites web,
      applications mobiles, documents PDF, etc.) sont accessibles aux personnes en situation de handicap.
    </p>
    <p>
      Un site accessible permet par exemple de :
    </p>
    <ul>
      <li>
        Personnaliser son affichage via le système d’exploitation et/ou le navigateur (agrandissement ou rétrécissement
        des caractères, changement de la typographie, modification des couleurs, arrêt des animations, etc.).
      </li>
      <li>
        Naviguer à l’aide de technologies d’assistance comme une synthèse vocale ou une plage braille.
      </li>
      <li>Naviguer sans utiliser la souris, avec le clavier uniquement, des contacteurs ou via un écran tactile.</li>
      <li>Consulter les vidéos et les contenus audio à l’aide de sous-titres et/ou de transcriptions.</li>
      <li>Etc.</li>
    </ul>
    <h2 class="fr-h2">Engagements d’accessibilité numérique</h2>
    <p>
      Le ministère de l'agriculture et de l'alimentation s’engage à rendre accessibles ses sites web (internet, intranet
      et extranet), ses applications mobiles, ses progiciels et son mobilier urbain numérique conformément à l’article
      47 de la loi n°2005-102 du 11 février 2005.
    </p>
    <!-- TODO: complete after a11y meeting in september 2023
    <p>
      À cette fin, elle met en œuvre la stratégie et les actions suivantes :
    </p>
    <ul>
      <li>
        Schéma pluriannuel de mise en accessibilité AAAA-AAAA.
      </li>
      <li>
        Plan d’action AAAA-AAAA.
      </li>
    </ul>
    -->
    <h2 class="fr-h2">Déclaration de non-conformité au RGAA</h2>
    <p>
      Cette déclaration s’applique au site « ma-cantine.agriculture.gouv.fr ».
    </p>
    <h3 class="fr-h3">
      État de conformité
    </h3>
    <p>
      Ce présent site est non conforme avec le RGAA (Référentiel Général d’Amélioration de l’Accessibilité) - version
      4.1.2 en raison des non-conformités énumérées ci-après.
    </p>
    <h3 class="fr-h3">
      Résultats des tests
    </h3>
    <p>
      L’audit de conformité au RGAA version 4.1.2 réalisé en juillet 2023 par la société Ideance révèle que, sur
      l’échantillon, le taux de conformité global est de 37,9%. (Obtenu en divisant le nombre de critères conformes par
      le nombre de critères applicables.)
    </p>
    <h3 class="fr-h3">
      Contenus non accessibles
    </h3>
    <h4 class="fr-h4">
      Non-conformités
    </h4>
    <p>
      Liste des critères non conformes :
    </p>
    <ul>
      <li>
        1.1 - Des images porteuses d’information n’ont pas d’alternative textuelle.
      </li>
      <li>1.2 - Des images décoratives ne sont pas ignorées par les technologies d’assistance.</li>
      <li>1.3 - Des alternatives textuelles d’images porteuses d’information ne sont pas pertinentes.</li>
      <li>3.1 - Des informations sont données uniquement par la couleur.</li>
      <li>3.2 - Des contrastes entre couleur de texte et couleur d’arrière-plan ne sont pas suffisamment élevés.</li>
      <li>4.1 - Des vidéos ne possèdent pas de transcription textuelle ou d’audiodescription.</li>
      <li>4.3 - Des vidéos ne sont pas sous-titrées.</li>
      <li>4.7 - Des vidéos ne sont pas clairement identifiables.</li>
      <li>4.8 - Des médias non temporels ne possèdent pas d’alternative.</li>
      <li>4.9 - Des alternatives de médias non temporels ne sont pas pertinentes.</li>
      <li>
        4.12 - La consultation de médias non temporels n’est pas contrôlable par le clavier et tout dispositif de
        pointage.
      </li>
      <li>4.13 - Des vidéos et des médias non temporels ne sont pas compatibles avec les technologies d’assistance.</li>
      <li>6.1 - Des liens ne sont pas explicites.</li>
      <li>6.2 - Des liens n’ont pas d’intitulé.</li>
      <li>7.1 - Des scripts ne sont pas compatibles avec les technologies d’assistance.</li>
      <li>7.3 - Des scripts ne sont pas contrôlables par le clavier et par tout dispositif de pointage.</li>
      <li>7.4 - Des changements de contexte initiés par des scripts ne sont pas signalés ou contrôlables.</li>
      <li>7.5 - Des messages de statut ne sont pas correctement restitués par les technologies d’assistance.</li>
      <li>8.2 - Le code source généré n’est pas valide selon le type de document spécifié.</li>
      <li>8.7 - Des changements de langue ne sont pas indiqués.</li>
      <li>8.9 - Des balises sont utilisées uniquement à des fins de présentation.</li>
      <li>9.1 - Des informations ne sont pas structurées par l’utilisation appropriée de titres.</li>
      <li>9.2 - La structure des pages n’est pas cohérente.</li>
      <li>9.3 - Des listes ne sont pas correctement structurées.</li>
      <li>10.1 - Des feuilles de styles ne sont pas utilisées pour contrôler la présentation.</li>
      <li>
        10.2 - Des contenus visibles porteurs d’information ne sont pas présents lorsque les feuilles de styles sont
        désactivées.
      </li>
      <li>
        10.4 - Des textes ne sont pas lisibles lorsque la taille des caractères est augmentée jusqu’à 200%, au moins.
      </li>
      <li>10.5 - Des déclarations CSS de couleurs de fond et de police ne sont pas correctement utilisées.</li>
      <li>10.7 - La prise de focus d’éléments interactifs n’est pas visible.</li>
      <li>10.8 - Des contenus cachés n’ont pas vocation à être ignorés par les technologies d’assistance.</li>
      <li>
        10.11 - Des contenus ne peuvent pas être présentés sans avoir recours à un défilement horizontal pour une
        fenêtre ayant une largeur de 320px.
      </li>
      <li>11.1 - Des champs de formulaire n’ont pas d’étiquette.</li>
      <li>
        11.3 - Des étiquettes de champ de formulaire ayant la même fonction et répétées plusieurs fois dans une même
        page ou dans un ensemble de pages ne sont pas cohérentes.
      </li>
      <li>11.5 - Des champs de même nature ne sont pas regroupés.</li>
      <li>11.10 - Des contrôles de saisie ne sont pas utilisés de manière pertinente.</li>
      <li>
        11.13 - La finalité de champs de saisie ne peut pas être déduite pour faciliter leur remplissage automatique
        avec les données de l’utilisateur.
      </li>
      <li>12.3 - La page « Plan du site » n’est pas pertinente.</li>
      <li>
        12.6 - Des zones de regroupement de contenus présentes dans plusieurs pages (entête, navigation principale,
        contenu principal, pied de page et moteur de recherche) ne peuvent pas être atteintes ou évitées.
      </li>
      <li>12.7 - Un lien d’évitement ou d’accès rapide à la zone de contenu principal est absent.</li>
      <li>13.1 - Des limites de temps modifiant le contenu ne sont pas contrôlables.</li>
      <li>13.3 - Des documents bureautiques en téléchargement ne possèdent pas de version accessible.</li>
    </ul>
    <h4 class="fr-h4">
      Contenus non soumis à l’obligation d’accessibilité
    </h4>
    <p>
      Le gestionnaire de cookies « crisp » a été exempté. Il n’a donc pas fait l’objet d’un audit complet et détaillé.
    </p>
    <p>
      Il a toutefois été vérifié que sa présence n’empêche pas l’utilisation et la consultation du reste du site.
    </p>
    <p>
      À noter également qu’il est en contrepartie possible de contacter « ma cantine » depuis le formulaire de contact
      ainsi que par email à l’adresse suivante
      <a href="mailto:support-egalim@beta.gouv.fr">support-egalim@beta.gouv.fr</a>
      .
    </p>
    <h3 class="fr-h3">
      Établissement de cette déclaration
    </h3>
    <p>
      Cette déclaration a été établie le 27/07/2023.
    </p>
    <h4 class="fr-h4">
      Technologies utilisées pour la réalisation du site
    </h4>
    <ul>
      <li>
        HTML5
      </li>
      <li>SVG</li>
      <li>ARIA</li>
      <li>CSS</li>
      <li>JavaScript</li>
    </ul>
    <h4 class="fr-h4">
      Environnement de test
    </h4>
    <p>
      Les tests ont été effectués avec les combinaisons de navigateur web et lecteur d’écran suivantes :
    </p>
    <ul>
      <li>Firefox 115 et NVDA 2023.1</li>
      <li>Firefox 115 et JAWS 2022</li>
      <li>Safari et VoiceOver (macOS 13.4)</li>
      <li>Safari et VoiceOver (iOS 16.5)</li>
    </ul>
    <h4 class="fr-h4">
      Outils pour évaluer l’accessibilité
    </h4>
    <ul>
      <li>Pika (analyse de contraste)</li>
      <li>Contrast Finder</li>
      <li>Outils de développement Firefox</li>
      <li>Web Developer (extension Firefox)</li>
    </ul>
    <h4 class="fr-h4">
      Pages du site ayant fait l’objet de la vérification de conformité
    </h4>
    <ul>
      <!-- <li><router-link :to="{ name: 'LandingPage' }">Accueil</router-link></li>
      <li><router-link :to="{ name: 'DiagnosticPage' }">Auto évaluation</router-link></li>
      <li><router-link :to="{ name: 'CanteensHome' }">Index des cantines</router-link></li>
      <li><router-link :to="{ name: 'FaqPage' }">FAQ</router-link></li>
      <li>
        <a href="https://ma-cantine.agriculture.gouv.fr/nos-cantines/14--Cantine%20de%20Misson/">
          Exemple d’une fiche détaillée
        </a>
      </li>
      <li><router-link :to="{ name: 'CommunityPage' }">Page entraide/communauté</router-link></li>
      <li><router-link :to="{ name: 'ContactPage' }">Contact</router-link></li>
      <li><router-link :to="{ name: 'LegalNotices' }">Mentions légales</router-link></li>
      <li><a href="/s-identifier">Authentification</a></li>
      <li><a href="/creer-mon-compte">Création d’un compte</a></li>
      <li><router-link :to="{ name: 'SiteMap' }">Plan du site</router-link></li>
      <li><router-link :to="{ name: 'AccessibilityDeclaration' }">Accessibilité</router-link></li> -->
    </ul>
    <h3 class="fr-h3">
      Plan d’action
    </h3>
    <p>
      Vous pouvez suivre notre progrès sur l'amélioration de nos non-confirmités sur
      <a href="https://github.com/betagouv/ma-cantine/issues?q=is%3Aissue+is%3Aopen+label%3Aa11y">
        GitHub
        <v-icon small color="grey darken-4">mdi-open-in-new</v-icon>
      </a>
      .
    </p>
    <h3 class="fr-h3">
      Retour d’information et contact
    </h3>
    <p>
      Si vous n’arrivez pas à accéder à un contenu ou à un service de ce site, vous pouvez nous contacter via un des
      moyens ci-dessous pour être orienté vers une alternative accessible ou obtenir le contenu sous une autre forme.
    </p>
    <ul>
      <li>
        Envoyez-nous un message via notre
        <!-- <router-link :to="{ name: 'ContactPage' }">formulaire de contact</router-link> -->
        .
      </li>
      <li>
        Écrivez-nous à l’adresse email :
        <a href="mailto:support-egalim@beta.gouv.fr">support-egalim@beta.gouv.fr</a>
        .
      </li>
      <li>Appelez-nous au +33 6 59 63 44 43.</li>
      <li>Écrivez-nous par voie postale à l’adresse suivante : 20 avenue de Ségur, 75007, Paris</li>
    </ul>
    <h3 class="fr-h3">
      Voies de recours
    </h3>
    <p>
      Cette procédure est à utiliser dans le cas suivant.
    </p>
    <p>
      Vous avez signalé au responsable du site internet un défaut d’accessibilité qui vous empêche d’accéder à un
      contenu ou à un des services et vous n’avez pas obtenu de réponse satisfaisante.
    </p>
    <ul>
      <li>Écrire un message au Défenseur des droits.</li>
      <li>Contacter le délégué du Défenseur des droits dans votre région.</li>
      <li>
        Envoyer un courrier par la poste (gratuit, ne pas mettre de timbre) à l’adresse suivante : Défenseur des droits
        Libre réponse 71120 75342 Paris CEDEX 07
      </li>
    </ul>
  </div>
</template>

<script>
// import BreadcrumbsNav from "@/components/BreadcrumbsNav"

export default {
  name: "AccessibilityDeclaration",
  // components: { BreadcrumbsNav },
}
</script>

<style scoped>
h2,
h3,
h4 {
  margin-top: 1.5em;
}
</style>
