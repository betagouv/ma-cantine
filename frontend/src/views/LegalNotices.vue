<template>
  <div id="legal-notices">
    <BreadcrumbsNav />
    <h1>Mentions légales</h1>
    <h2>Éditeur de la Plateforme</h2>
    <p>
      La Plateforme
      <a href="/">https://ma-cantine.beta.gouv.fr/</a>
      est éditée par l'Incubateur de services numériques de la Direction interministérielle du numérique (DINUM).
    </p>
    <h3>Coordonnées</h3>
    <address>
      <img src="/static/images/dinum-logo.jpeg" alt="" />
      <p>
        Adresse : DINUM, 20 avenue de Ségur, 75007 Paris
        <br />
        Tel. accueil : 01.71.21.01.70
        <br />
        SIRET : 12000101100010 (secrétariat général du gouvernement)
        <br />
        SIREN : 120 001 011
      </p>
    </address>
    <h2>Directeur de la publication</h2>
    <address>
      <img src="/static/images/Marianne.png" alt="" />
      <p>
        MINISTÈRE DE L’AGRICULTURE - Direction Générale de l’Alimentation
        <br />
        Hôtel de Villeroy, 78, rue de Varenne; Paris 7e
      </p>
    </address>
    <h2>Hébergement de la Plateforme</h2>
    <p>Ce site est hébergé en propre par:</p>
    <address>Clevercloud, 3 rue de l'Allier, 44000 Nantes, France.</address>
    <h2>Accessibilité</h2>
    <p>
      La conformité aux normes d’accessibilité numérique est un objectif ultérieur dans le développement itératif de la
      plateforme. Nous nous efforçons de créer un maximum de composants partagés et de les rendre accessibles à toutes
      et tous.
    </p>
    <p>
      Pour en savoir plus :
      <a href="http://references.modernisation.gouv.fr/accessibilite-numerique">
        http://references.modernisation.gouv.fr/accessibilite-numerique
      </a>
      .
    </p>
    <p>
      Pour nous signaler des problèmes ou suggestions d'amélioration concernant l'accessibilité de la plateforme, 2
      options :
    </p>
    <ul>
      <li>
        nous signaler par email :
        <a href="mailto:contact@egalim.beta.gouv.fr">contact@egalim.beta.gouv.fr</a>
      </li>
      <li>
        créer une “issue” sur
        <a href="https://github.com/betagouv/ma-cantine">le dépôt de code sur GitHub</a>
      </li>
    </ul>

    <p>
      Le code source est ouvert et les contributions sont bienvenues.
      <a href="https://github.com/betagouv/ma-cantine">Voir le code source</a>
      .
    </p>

    <h2>Données personnelles, suivi d’audience et gestion des cookies</h2>

    <div id="cookies-definition">
      <img src="/static/images/cookie.png" />
      <p>
        Le cookie est un petit fichier texte enregistré par le navigateur de votre ordinateur, tablette ou smartphone et
        qui permet de conserver des données utilisateur afin de faciliter la navigation et de permettre certaines
        fonctionnalités.
      </p>
    </div>

    <h3>A quoi nous servent-ils ?</h3>
    <p>Cela nous permet de mesurer le nombre de visites et de comprendre quelles sont les pages les plus consultées.</p>

    <h3>Ce site n’affiche pas de bannière de consentement aux cookies, pourquoi ?</h3>
    <p>
      C’est vrai, vous n’avez pas eu à cliquer sur un bloc qui recouvre la moitié de la page pour dire que vous êtes
      d’accord avec le dépôt de cookies — même si vous ne savez pas ce que ça veut dire !
    </p>
    <p>
      Rien d’exceptionnel, pas de passe-droit lié à un .gouv.fr. Nous respectons simplement la loi, qui dit que certains
      outils de suivi d’audience, correctement configurés pour respecter la vie privée, sont exemptés d’autorisation
      préalable.
    </p>
    <p>
      Nous utilisons pour cela
      <a href="https://matomo.org/">Matomo</a>
      , un outil
      <a href="https://matomo.org/free-software/">libre</a>
      , paramétré pour être en conformité avec la
      <a href="https://www.cnil.fr/fr/solutions-pour-la-mesure-daudience">recommandation « Cookies »</a>
      de la CNIL. Cela signifie que votre adresse IP, par exemple, est anonymisée avant d’être enregistrée. Il est donc
      impossible d’associer vos visites sur ce site à votre personne.
    </p>

    <h3>Je contribue à enrichir vos données, puis-je y accéder ?</h3>
    <p>
      Bien sûr ! Les statistiques d’usage de la majorité de nos produits, dont
      <a href="https://beta.gouv.fr/">beta.gouv.fr</a>
      , sont disponibles en accès libre sur
      <a
        href="https://stats.data.gouv.fr/index.php?module=CoreHome&action=index&idSite=21&period=range&date=previous30#?module=VisitsSummary&action=index&idSite=21&period=range&date=previous30"
      >
        stats.data.gouv.fr
      </a>
      .
    </p>

    <h2>Contactez-nous</h2>
    <p>
      Des questions ? Une difficulté ? Envoyez-nous un email à
      <a href="mailto:contact@egalim.beta.gouv.fr">contact@egalim.beta.gouv.fr</a>
      .
    </p>
  </div>
</template>

<script>
import BreadcrumbsNav from "@/components/BreadcrumbsNav"

export default {
  name: "LegalNotices",
  components: { BreadcrumbsNav },
}
</script>

<style scoped lang="scss">
#legal-notices {
  padding: 2em;
  max-width: 1200px;
  margin: auto;
  text-align: left;
}

address,
div#cookies-definition {
  display: flex;
  align-items: center;
  font-style: normal;

  img {
    height: 5em;
    margin-right: 1em;
  }
}

ul {
  list-style-type: disc;
  margin-left: 3em;
}

@media (max-width: 400px) {
  img {
    display: none;
  }
}
</style>
