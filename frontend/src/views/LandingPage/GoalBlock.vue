<template>
  <div class="text-left text-body-1">
    <h2 class="text-h2 mb-8 text-center">L'enjeu de notre mission</h2>

    <p>
      La restauration collective représente près de
      <b>4 milliards de repas servis par an</b>
      dans plus de 90 000 cantines, d’hopitaux, d’EPHAD, d’entreprises...
    </p>
    <p>
      Agir sur la composition des assiettes est un levier fort pour améliorer l'impact sur notre santé et sur
      l'environnement tout en influençant positivement les filières d'agriculture biologique et de qualité.
    </p>
    <p>
      Le cadre réglementaire et les lois EGAlim (2018) et Climat et Résilience (2021) ont fixé des objectifs en termes
      de qualité de produits, de substitution du plastique, de diversification des protéines, de réduction du
      gaspillage, et d'information des convives.
    </p>
    <router-link
      color="primary"
      class="mx-auto mt-4 text-decoration-underline mt-8 d-block"
      :to="{ name: 'KeyMeasuresHome' }"
    >
      En savoir plus sur les mesures-phare des lois
    </router-link>
  </div>
</template>
