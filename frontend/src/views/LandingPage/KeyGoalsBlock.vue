<template>
  <div>
    <h2 class="text-h2 mb-12">Les objectifs de la loi EGAlim</h2>

    <v-row class="mb-8 text-body-1">
      <v-col cols="12" sm="4">
        <v-icon color="grey darken-3" class="mb-2" x-large>$seedling-fill</v-icon>
        <p class="mt-4 text-center text-sm-left">
          Promouvoir une alimentation saine et respectueuse de l'environnement.
        </p>
      </v-col>

      <v-col cols="12" sm="4">
        <v-icon color="grey darken-3" class="mb-2" x-large>$team-fill</v-icon>
        <p class="mt-4 text-center text-sm-left">
          Réduire les inégalités d'accès à une alimentation durable et de qualité.
        </p>
      </v-col>

      <v-col cols="12" sm="4">
        <v-icon color="grey darken-3" class="mb-2" x-large>$money-euro-box-fill</v-icon>
        <p class="mt-4 text-center text-sm-left">
          Assurer la juste rémunération des agriculteurs du secteur agricole.
        </p>
      </v-col>
    </v-row>
    <v-row justify="center">
      <DownloadLink
        label="Télécharger le livret de la loi EGAlim concernant la restauration collective"
        href="/static/documents/2208_Mesures-LoiEgalim_BRO_V3.pdf"
        sizeStr="482 ko"
      />
    </v-row>
  </div>
</template>

<script>
import DownloadLink from "@/components/DownloadLink"

export default {
  components: { DownloadLink },
}
</script>
