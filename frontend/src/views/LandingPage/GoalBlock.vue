<template>
  <div>
    <h2 class="text-h4 font-weight-black mb-8">L'enjeu de notre mission</h2>

    <p class="text-left">
      La restauration collective représente près de
      <b>4 milliards de repas servis par an</b>
      dans plus de 90 000 cantines, d’hopitaux, d’EPHAD, d’entreprises...
    </p>
    <p class="text-left">
      Agir sur la composition des assiettes est un levier fort pour améliorer l'impact sur notre santé et sur
      l'environnement tout en influençant positivement les filières d'agriculture biologique et de qualité.
    </p>
    <p class="text-left">
      Le cadre réglementaire et les lois EGalim (2018) et Climat et Résilience (2021) ont fixé des objectifs en termes
      de qualité de produits, de substitution du plastique, de diversification des protéines, de réduction du
      gaspillage, et d'information des convives.
    </p>
    <router-link class="mx-auto mt-4 mt-8 d-block" :to="{ name: 'KeyMeasuresHome' }">
      En savoir plus sur les mesures-phare des lois
    </router-link>
  </div>
</template>
