<template>
  <div id="legal-notices">
    <BreadcrumbsNav />
    <h1>Mentions légales</h1>
    <h2>Éditeur de la Plateforme</h2>
    <p>
      La Plateforme
      <router-link :to="{ name: 'LandingPage' }">https://ma-cantine.agriculture.gouv.fr/</router-link>
      est éditée par la Direction générale de l’alimentation du ministère de l’Agriculture et de la Souveraineté
      Alimentaire.
    </p>

    <h2>Directeur ou directrice de la publication</h2>
    <p>
      Maud FAIPOUX, directrice générale de l’alimentation du ministère de l’Agriculture et de la Souveraineté
      Alimentaire.
    </p>

    <h2>Hébergement de la Plateforme</h2>
    <p>Cette plateforme est hébergé par:</p>
    <p>Clevercloud</p>
    <address>3 rue de l'Allier, 44000 Nantes, France.</address>
    <h2>Accessibilité</h2>
    <p>
      La conformité aux normes d’accessibilité numérique est un objectif ultérieur mais nous tâchons de rendre cette
      plateforme accessible à toutes et à tous.
    </p>
    <p>
      Pour en savoir plus sur la politique d’accessibilité numérique de l’État :
      <a rel="noopener" href="https://accessibilite.numerique.gouv.fr/">
        https://accessibilite.numerique.gouv.fr/
      </a>
      .
    </p>
    <p>
      Pour nous signaler des problèmes ou suggestions d'amélioration concernant l'accessibilité de la plateforme, deux
      options :
    </p>
    <ul>
      <li>
        nous signaler par email :
        <a rel="noopener" href="mailto:support-egalim@beta.gouv.fr">support-egalim@beta.gouv.fr</a>
      </li>
      <li>
        créer une “issue” sur
        <a rel="noopener" href="https://github.com/betagouv/ma-cantine">le dépôt de code sur GitHub</a>
      </li>
    </ul>
    <p>
      Si vous n’obtenez pas de réponse rapide de notre part, vous êtes en droit de faire parvenir vos doléances ou une
      demande de saisine au Défenseur des droits.
    </p>
    <h2>Code source</h2>
    <p>
      Le code source est ouvert et les contributions sont bienvenues :
      <a rel="noopener" href="https://github.com/betagouv/ma-cantine">voir le code source</a>
      .
    </p>

    <h2>Signaler un dysfonctionnement ou une question</h2>
    <p>
      Envoyez-nous un courriel à
      <a rel="noopener" href="mailto:support-egalim@beta.gouv.fr">support-egalim@beta.gouv.fr</a>
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
  max-width: 1200px;
  margin: auto;
  text-align: left;
}

h2 {
  margin-top: 1.25em;
  margin-bottom: 0.5em;
}

address {
  display: flex;
  align-items: center;
  font-style: normal;
}

ul {
  list-style-type: disc;
  margin-left: 3em;
}
</style>
