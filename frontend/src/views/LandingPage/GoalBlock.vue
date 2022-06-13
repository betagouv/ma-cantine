<template>
  <div>
    <h2 class="text-h4 font-weight-black mb-8">L'enjeu de notre mission</h2>
    <v-row>
      <v-col cols="12" md="8" class="pr-2 pr-md-12">
        <p class="text-left">
          La restauration collective représente près de
          <b>4 milliards de repas servis par an</b>
          dans plus de 90 000 de cantines, d’hopitaux, d’EPHAD, d’entreprises...
        </p>
        <p class="text-left">
          Agir sur la composition des assiettes est un levier fort pour améliorer l'impact sur notre santé et sur
          l'environnement tout en influançant positivement les filières d'agriculture biologique et de qualité.
        </p>
        <p class="text-left">
          Le cadre réglementaire et les deux lois EGAlim (2018) et la loi Climat et Résilience (2021) ont fixé des
          objectifs en termes de produits, de substitution du plastique, de diversification des protéines, de réduction
          du gaspillage...
        </p>
      </v-col>
      <v-col cols="12" md="4" v-if="$vuetify.breakpoint.mdAndUp" class="d-flex align-center">
        <v-card outlined class="pa-0">
          <v-card-text>
            <video style="width: 100%; background: #333;" poster="/static/images/video-poster-intro.webp" controls>
              <source
                type="video/mp4"
                src="https://cellar-c2.services.clever-cloud.com/ma-cantine-egalim/videos/presentation-egalim.mp4"
              />
              Votre navigateur ne peut pas afficher des vidéos.
            </video>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>
