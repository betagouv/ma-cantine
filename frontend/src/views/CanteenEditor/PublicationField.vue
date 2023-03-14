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
            <p
              class="text-body-2 grey--text text--darken-4 pb-0 my-0 ml-2"
              :class="{ 'pt-1': !originalCanteenIsPublished }"
            >
              J'accepte que les données relatives aux mesures EGAlim de ma cantine soient visibles sur
              <router-link
                :to="{
                  name: 'CanteensHome',
                }"
              >
                nos cantines
              </router-link>
              <br />
              <span v-if="originalCanteenIsPublished">
                Cette cantine est actuellement publiée sur
                <v-btn
                  @click.stop
                  :href="
                    $router.resolve({
                      name: 'CanteenPage',
                      params: { canteenUrlComponent: $store.getters.getCanteenUrlComponent(canteen) },
                    }).href
                  "
                  class="text-body-2 pl-0 text-decoration-underline"
                  id="canteen-page-link"
                  target="_blank"
                  small
                  text
                  plain
                >
                  nos cantines
                  <v-icon small color="grey darken-4" class="ml-1">mdi-open-in-new</v-icon>
                </v-btn>
              </span>
              <span v-else>
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
    originalCanteenIsPublished() {
      return this.canteen.publicationStatus === "published"
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
#canteen-page-link {
  vertical-align: inherit;
}
</style>
