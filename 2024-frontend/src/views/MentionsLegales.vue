<script setup>
import LayoutOneColumn from "@/layouts/LayoutOneColumn.vue"
</script>

<template>
  <LayoutOneColumn>
    <section>
      <h2>Éditeur de la Plateforme</h2>
      <p>
        La Plateforme
        <router-link :to="{ name: 'Vue2Home' }">https://ma-cantine.agriculture.gouv.fr/</router-link>
        est éditée par la Direction générale de l’alimentation du ministère de l’Agriculture, de l’Agro-alimentaire et
        de la Souveraineté alimentaire.
      </p>
    </section>
    <section>
      <h2>Directeur ou directrice de la publication</h2>
      <p>
        Maud FAIPOUX, directrice générale de l’alimentation du ministère de l’Agriculture, de l’Agro-alimentaire et de
        la Souveraineté alimentaire.
      </p>
    </section>
    <section>
      <h2>Hébergement de la Plateforme</h2>
      <p>Cette plateforme est hébergé par:</p>
      <address class="fr-mb-3w">
        Clever Cloud
        <br />
        3 rue de l'Allier
        <br />
        44000 Nantes
        <br />
        France
      </address>
    </section>
    <section>
      <h2>Accessibilité</h2>
      <p>
        La conformité aux normes d’accessibilité numérique est un objectif ultérieur mais nous tâchons de rendre cette
        plateforme accessible à toutes et à tous.
      </p>
      <p>
        Pour en savoir plus sur la politique d’accessibilité numérique de l’État :
        <a target="_blank" href="https://accessibilite.numerique.gouv.fr/">
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
          <a target="_blank" href="https://github.com/betagouv/ma-cantine">le dépôt de code sur GitHub</a>
        </li>
      </ul>
      <p>
        Si vous n’obtenez pas de réponse rapide de notre part, vous êtes en droit de faire parvenir vos doléances ou une
        demande de saisine au Défenseur des droits.
      </p>
    </section>
    <section>
      <h2>Code source</h2>
      <p>
        Le code source est ouvert et les contributions sont bienvenues :
        <a target="_blank" href="https://github.com/betagouv/ma-cantine">voir le code source</a>
        .
      </p>
    </section>
    <section>
      <h2>Signaler un dysfonctionnement ou une question</h2>
      <p>
        Envoyez-nous un courriel à
        <a rel="noopener" href="mailto:support-egalim@beta.gouv.fr">support-egalim@beta.gouv.fr</a>
        .
      </p>
    </section>
  </LayoutOneColumn>
</template>
