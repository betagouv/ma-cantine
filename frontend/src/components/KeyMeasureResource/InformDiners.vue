<template>
  <v-card :to="{ name: 'GeneratePosterPage' }" class="text-decoration-none text-left mt-4" hover>
    <DsfrCallout icon="mdi-bullhorn" class="text-body-2 mb-0" color="#C08C65">
      L’information convives, par mail et par affichage, de la part de bio, durable et commerce équitable est d’ores et
      déjà en vigueur. Pour générer votre affiche, tester notre formulaire.
    </DsfrCallout>
  </v-card>
</template>

<script>
import DsfrCallout from "@/components/DsfrCallout"

export default {
  components: { DsfrCallout },
}
</script>
