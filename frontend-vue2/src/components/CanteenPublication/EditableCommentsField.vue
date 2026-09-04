<template>
  <v-col v-if="!editDescription && (value || editable)" cols="12" sm="6" class="px-0 pb-2">
    <div v-if="value">
      <h2 class="fr-text grey--text text--darken-4 mb-6">
        {{ label }}
      </h2>
      <div class="ml-n8">
        <DsfrHighlight>
          <p>
            {{ value }}
          </p>
        </DsfrHighlight>
      </div>
    </div>
    <v-btn
      v-if="editable"
      @click="
        editDescription = true
        oldComments = value
      "
      outlined
      small
      color="primary"
      :class="{ 'fr-btn--tertiary px-2': true, 'mt-4': !!value }"
    >
      <v-icon color="primary" x-small class="mr-1">mdi-pencil-outline</v-icon>
      {{ cta || "Modifier" }}
    </v-btn>
  </v-col>
  <v-col v-else-if="editable" cols="12" sm="6">
    <v-form v-model="formIsValid" ref="commentsForm">
      <DsfrTextarea
        v-model="canteen[valueKey]"
        :counter="charLimit"
        :rules="[validators.maxChars(charLimit)]"
        rows="5"
        class="mt-2"
      >
        <template v-slot:label>
          <span class="fr-label mb-1">{{ label }}</span>
          <span v-if="helpText" class="fr-hint-text mb-2">
            {{ helpText }}
          </span>
          <slot name="help-text" />
        </template>
      </DsfrTextarea>
      <v-btn @click="saveDescription" class="primary">Enregistrer</v-btn>
    </v-form>
  </v-col>
</template>

<script>
import DsfrTextarea from "@/components/DsfrTextarea"
import DsfrHighlight from "@/components/DsfrHighlight"
import validators from "@/validators"

export default {
  name: "EditableCommentsField",
  props: {
    canteen: Object,
    valueKey: String,
    editable: Boolean,
    label: String,
    helpText: String,
    cta: String,
    charLimit: Number,
  },
  components: { DsfrTextarea, DsfrHighlight },
  data() {
    return {
      editDescription: false,
      formIsValid: true,
      oldComments: this.canteen[this.valueKey],
    }
  },
  computed: {
    validators() {
      return validators
    },
    value() {
      return this.canteen[this.valueKey]
    },
  },
  methods: {
    saveDescription() {
      if (this.canteen[this.valueKey] === this.oldComments) {
        this.editDescription = false
        return
      }
      this.$refs.commentsForm.validate()
      if (!this.formIsValid) {
        this.$store.dispatch("notifyRequiredFieldsError")
        return
      }
      const payload = {}
      payload[this.valueKey] = this.canteen[this.valueKey]
      this.$store
        .dispatch("updateCanteen", {
          id: this.canteen.id,
          payload,
        })
        .then(() => {
          this.$store.dispatch("notify", {
            status: "success",
            message: "Commentaires mises à jour",
          })
          this.editDescription = false
        })
        .catch(() => {
          this.$store.dispatch("notifyServerError")
        })
    },
  },
}
</script>

<style></style>
