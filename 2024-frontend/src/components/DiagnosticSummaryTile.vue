<script setup>
import { computed } from "vue"
import IconLink from "@/components/IconLink.vue"
import AppSeparator from "@/components/AppSeparator.vue"
import IconAward from "@/components/IconAward.vue"

const props = defineProps(["thematiques", "anchorName", "isTeledeclared", "appro"])
const emit = defineEmits(["openAccordion"])
const clickLink = (index) => emit("openAccordion", index)

const egalimColor = computed(() => props.isTeledeclared ? "#1F7046" : "var(--border-default-grey)")
const siqoColor = computed(() => props.isTeledeclared ? "#29A86D" : "var(--border-default-grey)")
const bioColor = computed(() => props.isTeledeclared ? "#8AE4B3" : "var(--border-default-grey)")
const viandePoissonColor = computed(() => props.isTeledeclared ? "#695240" : "var(--border-default-grey)")
</script>

<template>
  <div class="diagnostic-summary-tile">
    <div class="fr-tile">
      <div class="fr-tile__title fr-grid-row fr-text--regular fr-text-title--grey fr-text--md">
        <div class="diagnostic-summary-tile__appro-container ma-cantine--flex-gap-1 fr-col-8 fr-pr-8w">
          <component :is="appro.macaron" status="empty" class="diagnostic-summary-tile__macaron" />
          <div class="ma-cantine--width-100">
            <div class="diagnostic-summary-tile__anchor">
              <a :href="`#${anchorName}`" @click="clickLink(0)" class="fr-text-default--grey">
                {{ appro.title }}
              </a>
              <VIcon name="ri-arrow-right-down-line" />
            </div>
            <div class="fr-grid-row fr-pt-1w">
              <IconLink class="fr-col-1" top="1.25rem" />
              <div class="fr-col-11">
                <ul class="ma-cantine--unstyled-list fr-pl-1w">
                  <li class="ma-cantine--flex-start ma-cantine--flex-gap-1">
                    <div class="diagnostic-summary-tile__square diagnostic-summary-tile__square--egalim"></div>
                    <p class="fr-mb-0 fr-text--sm">
                      {{ isTeledeclared ? "Résultat EGalim" : "Objectif EGalim" }}
                    </p>
                  </li>
                  <li class="ma-cantine--flex-start ma-cantine--flex-gap-1">
                    <div class="diagnostic-summary-tile__square diagnostic-summary-tile__square--siqo"></div>
                    <p class="fr-mb-0 fr-text--sm">
                      {{ isTeledeclared ? "Résultat SIQO" : "Objectif SIQO" }}
                    </p>
                  </li>
                  <li class="ma-cantine--flex-start ma-cantine--flex-gap-1">
                    <div class="diagnostic-summary-tile__square diagnostic-summary-tile__square--bio"></div>
                    <p class="fr-mb-0 fr-text--sm">
                      {{ isTeledeclared ? "Résultat Bio" : "Objectif Bio" }}
                    </p>
                  </li>
                </ul>
                <AppSeparator class="fr-my-3w" />
              </div>
            </div>
            <div class="fr-grid-row">
              <div class="fr-col-1">
                <IconAward class="diagnostic-summary-tile__award" />
              </div>
              <div class="fr-col-11">
                <p class="fr-mb-0 fr-text--sm">
                  {{ isTeledeclared ? "Résultat viande et poisson" : "Objectif viande et poisson" }}
                </p>
              </div>
            </div>
          </div>
        </div>
        <ul class="diagnostic-summary-tile__thematiques-container ma-cantine--unstyled-list fr-my-0 fr-col-4">
          <li v-for="(volet, index) in thematiques" :key="volet.title" class="ma-cantine--flex-start ma-cantine--flex-gap-1">
            <component :is="volet.macaron" status="empty" class="diagnostic-summary-tile__macaron" />
            <div class="diagnostic-summary-tile__anchor">
              <a :href="`#${anchorName}`" @click="clickLink(index + 1)" class="fr-text-default--grey">
                {{ volet.shortTitle }}
              </a>
              <VIcon name="ri-arrow-right-down-line" />
            </div>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<style lang="scss">
.diagnostic-summary-tile {

  &__appro-container {
    display: flex;
    align-items: flex-start;
    justify-content: flex-start;
    gap: 0.5rem;
    text-align: left;
  }

  &__thematiques-container {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    gap: 0.5rem;
  }

  &__anchor {
    display: flex;
    align-items: flex-end;
  }

  &__macaron {
    width: 2rem;
    height: 2rem;
  }

  &__square {
    width: 0.5rem;
    height: 0.5rem;

    &--egalim {
      background-color: v-bind(egalimColor);
    }
    &--siqo {
      background-color: v-bind(siqoColor);
    }
    &--bio {
      background-color: v-bind(bioColor);
    }
  }

  &__award {
    color: v-bind(viandePoissonColor);
  }
}
</style>
