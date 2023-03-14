<template>
  <div>
    <PublicationPreviewDialog
      v-if="!isNewCanteen"
      :canteen="canteen"
      :value="showPreview"
      @close="showPreview = false"
    />
    <v-row v-if="!isNewCanteen">
      <v-col cols="12">
        <v-checkbox hide-details="auto" class="mt-0" color="primary" :input-value="value" @change="updateValue">
          <template v-slot:label>
            <p class="text-body-2 grey--text text--darken-4 pb-0 my-0 ml-2" :class="{ 'pt-1': isDraft }">
              J'accepte que les données relatives aux mesures EGAlim de ma cantine soient visibles sur
              <router-link
                :to="{
                  name: 'CanteensHome',
                }"
              >
                nos cantines
              </router-link>
              <br />
              <span v-if="isDraft">
                <v-btn
                  @click.stop="showPreview = true"
                  class="text-body-2 px-0 text-decoration-underline grey--text text--darken-4"
                  small
                  text
                  plain
                >
                  Voir un aperçu de la publication
                </v-btn>
              </span>
            </p>
          </template>
        </v-checkbox>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import PublicationPreviewDialog from "@/views/ManagementPage/PublicationPreviewDialog"

export default {
  name: "PublicationField",
  components: { PublicationPreviewDialog },
  props: {
    canteen: {
      type: Object,
      required: true,
    },
    value: {
      type: Boolean,
      required: true,
    },
  },
  data() {
    return {
      showPreview: false,
    }
  },
  computed: {
    isNewCanteen() {
      return !this.canteen.id
    },
    isDraft() {
      return this.canteen.publicationStatus === "draft"
    },
  },
  methods: {
    updateValue(val) {
      this.$emit("input", val)
    },
  },
}
</script>

<style scoped>
.v-btn--plain:not(.v-btn--active):not(.v-btn--loading):not(:focus):not(:hover) >>> .v-btn__content {
  opacity: 1;
}
</style>
