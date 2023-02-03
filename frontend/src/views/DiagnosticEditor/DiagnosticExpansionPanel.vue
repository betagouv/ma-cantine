<template>
  <v-expansion-panel :disabled="disabled">
    <v-expansion-panel-header :color="color">
      <template v-slot:default="{ open }">
        <v-row no-gutters>
          <v-col cols="7" class="font-weight-bold">
            <span class="d-flex">
              <v-icon class="mr-2" :color="iconColour">
                {{ icon }}
              </v-icon>
              <h2 class="text-body-1 font-weight-bold">{{ heading }}</h2>
            </span>
          </v-col>
          <v-col cols="5" class="text--secondary text-right pr-2 align-self-center align-self-center">
            <v-fade-transition leave-absolute>
              <span v-if="showSummary" key="0">
                {{ summary }}
              </span>
              <span v-if="!open && !formIsValid" key="1" class="red--text">
                Veuillez vérifier les champs saisis.
              </span>
            </v-fade-transition>
          </v-col>
        </v-row>
      </template>
    </v-expansion-panel-header>
    <v-expansion-panel-content eager>
      <slot />
    </v-expansion-panel-content>
  </v-expansion-panel>
</template>

<script>
export default {
  name: "DiagnosticExpansionPanel",
  props: ["iconColour", "icon", "heading", "formIsValid", "summary", "disabled"],
  data() {
    return {
      open: undefined,
    }
  },
  computed: {
    color() {
      if (this.disabled) return "grey lighten-3"
      if (!this.open && !this.formIsValid) return "red lighten-5"
      return "white"
    },
    showSummary() {
      return !this.disabled && !this.open && this.formIsValid
    },
  },
}
</script>
