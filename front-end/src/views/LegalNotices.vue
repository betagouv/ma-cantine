<template>
  <div id="legal-notices">
    <h1>Mentions légales</h1>
    <h2>Éditeur de la Plateforme</h2>
    <p>La Plateforme <a href="/">https://ma-cantine.beta.gouv.fr/</a> est éditée par l'Incubateur de services numériques de la Direction interministérielle du numérique (DINUM).</p>
    <h3>Coordonnées</h3>
    <address>
      <img src="@/assets/dinum-logo.jpeg" alt="">
      <p>Adresse : DINUM, 20 avenue de Ségur, 75007 Paris<br>
        Tel. accueil : 01.71.21.01.70<br>
        SIRET : 12000101100010 (secrétariat général du gouvernement)<br>
        SIREN : 120 001 011
      </p>
    </address>
    <h2>Directeur de la publication</h2>
    <address>
      <img src="@/assets/Marianne.png" alt="">
      <p>
        MINISTÈRE DE L’AGRICULTURE - Direction Générale de l’Alimentation<br>
        Hôtel de Villeroy, 78, rue de Varenne; Paris 7e
      </p>
    </address>
    <h2>Hébergement de la Plateforme</h2>
    <p>Ce site est hébergé en propre par:</p>
    <address>Scalingo SAS, 15 avenue du Rhin, 67100 Strasbourg, France.</address>
    <h2>Accessibilité</h2>
    <p>La conformité aux normes d’accessibilité numérique est un objectif ultérieur dans le développement 
      itératif de la plateforme. Nous nous efforçons de créer un maximum de composants partagés et de les 
      rendre accessibles à toutes et tous.
    </p>
    <p>Pour en savoir plus : 
      <a href="http://references.modernisation.gouv.fr/accessibilite-numerique">http://references.modernisation.gouv.fr/accessibilite-numerique</a>.
    </p>
    <p>Pour nous signaler des problèmes ou suggestions d'amélioration concernant l'accessibilité de la plateforme, 2 options : </p>
    <ul>
      <li>nous signaler par email : <a href="mailto:contact@egalim.beta.gouv.fr">contact@egalim.beta.gouv.fr</a></li>
      <li>créer une “issue” sur <a href="https://github.com/betagouv/ma-cantine">le dépôt de code sur GitHub</a></li>
    </ul>
    
    <p>Le code source est ouvert et les contributions sont bienvenues. <a href="https://github.com/betagouv/ma-cantine">Voir le code source</a>.</p>

    <h2>Contactez-nous</h2>
    <p>Des questions ? Une difficulté ? Envoyez-nous un email à <a href="mailto:contact@egalim.beta.gouv.fr">contact@egalim.beta.gouv.fr</a>.</p>
  </div>
</template>

<style scoped lang="scss">
  #legal-notices {
    padding: 2em;
    max-width: 1200px;
    margin: auto;
    text-align: left;
  }

  address {
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
</style>