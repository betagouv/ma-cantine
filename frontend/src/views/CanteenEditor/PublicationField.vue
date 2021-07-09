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
        <p class="body-1 mb-3 mt-4 font-weight-black">Publication</p>

        <v-alert color="amber darken-3" class="mb-1 body-2" v-if="originalCanteenIsPending" outlined>
          <span class="grey--text text--darken-2">
            <v-icon class="mb-1 mr-2">mdi-information</v-icon>
            Cette cantine est en attente de validation. Une fois validé par notre équipe, vous recevrez un email
            confirmant sa publication.
          </span>
        </v-alert>

        <v-checkbox hide-details="auto" class="mt-0" :color="checkboxColor" :input-value="value" @change="updateValue">
          <template v-slot:label>
            <p class="text-body-2 grey--text text--darken-4 pt-1 pb-0 my-0 ml-2">
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
                  :ripple="false"
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
                  :ripple="false"
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
    originalCanteen() {
      return this.$store.state.userCanteens.find((x) => x.id === this.canteen.id)
    },
    originalCanteenIsPublished() {
      return this.originalCanteen ? this.originalCanteen.publicationStatus === "published" : false
    },
    originalCanteenIsPending() {
      return this.originalCanteen ? this.originalCanteen.publicationStatus === "pending" : false
    },
    checkboxColor() {
      return this.originalCanteenIsPending ? "amber darken-2" : "primary"
    },
  },
  methods: {
    updateValue(val) {
      this.$emit("input", val)
    },
  },
}
</script>
