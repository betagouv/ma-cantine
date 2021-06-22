<template>
  <v-expansion-panel>
    <v-expansion-panel-header>
      <template v-slot:default="{ open }">
        <v-row no-gutters>
          <v-col cols="7" class="font-weight-bold">
            <v-icon class="mr-2" :color="iconColour">
              {{ icon }}
            </v-icon>
            {{ heading }}
          </v-col>
          <v-col cols="5" class="text--secondary text-right pr-2 align-self-center align-self-center">
            <v-fade-transition leave-absolute>
              <span v-if="!open && formIsValid" key="0">
                {{ summary }}
              </span>
              <span v-if="!open && !formIsValid" key="1" class="red--text">
                Vérifier les champs en rouge
              </span>
            </v-fade-transition>
          </v-col>
        </v-row>
      </template>
    </v-expansion-panel-header>
    <v-expansion-panel-content>
      <slot />
    </v-expansion-panel-content>
  </v-expansion-panel>
</template>

<script>
export default {
  name: "DiagnosticExpansionPanel",
  props: ["iconColour", "icon", "heading", "formIsValid", "summary"],
}
</script>
