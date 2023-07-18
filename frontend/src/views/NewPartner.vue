<template>
  <div class="text-left">
    <BreadcrumbsNav :links="[{ to: { name: 'PartnersHome' } }]" />
    <h1>Nouvel acteur de l'éco-système</h1>
    <p>
      Veuillez renseigner ce formulaire et notre équipe va vérifier votre demande et ajouter votre organisation dans
      notre base de données.
    </p>
    <p>
      Sauf mention contraire “(optionnel)” dans le label, tous les champs sont obligatoires
    </p>
    <v-form v-model="formIsValid" ref="form" @submit.prevent>
      <v-col class="pa-0" cols="12" sm="6">
        <DsfrTextField
          v-model="partner.name"
          label="Nom de votre structure / organisation"
          :rules="[validators.required]"
        />
      </v-col>
      <v-col class="pa-0" cols="12" sm="6">
        <DsfrTextField v-model="partner.website" label="URL du site" :rules="[validators.required]" />
      </v-col>
      <!-- TODO: optional image -->
      <v-col class="pa-0" cols="12" md="9">
        <DsfrSelect
          multiple
          clearable
          label="Sur quels aspects, pouvez-vous aider des gestionnaires de restaurants collectifs ?"
          :items="categories"
          v-model="partner.categories"
        />
      </v-col>
      <!-- TODO: actor type -->
      <!-- TODO: create a DsfrRadio component and use that instead -->
      <!-- https://www.systeme-de-design.gouv.fr/elements-d-interface/composants/bouton-radio -->
      <v-col class="pa-0" cols="12" md="4">
        <DsfrSelect label="Secteur économique" :items="economicModels" v-model="partner.economicModel" />
      </v-col>
      <!-- TODO: actor provides free and/or paying services? -->
      <v-col class="pa-0" cols="12" md="9">
        <DsfrSelect
          label="Secteurs d'activité"
          multiple
          :items="sectors"
          v-model="partner.sectors"
          item-text="name"
          item-value="id"
        />
      </v-col>
      <!-- TODO: actor region/department OR national -->
      <DsfrTextarea
        v-model="partner.longDescription"
        label="Comment présentez-vous en détail votre activité ?"
        :rules="[validators.required]"
      />
      <DsfrTextarea
        v-model="partner.shortDescription"
        label="Comment présentez-vous votre activité en quelques mots ?"
        :rules="[validators.required]"
        :rows="2"
      />
      <v-row>
        <v-col cols="12" sm="6">
          <DsfrTextField v-model="contactEmail" label="Votre email" :rules="[validators.email]" validate-on-blur />
        </v-col>
        <v-col cols="12" sm="6">
          <DsfrTextField v-model="contactName" label="Prénom et nom (facultatif)" validate-on-blur />
        </v-col>
      </v-row>
      <DsfrTextarea v-model="message" label="Message" :rules="[validators.required]" />
      <p class="caption text-left grey--text text--darken-1 mt-n1 mb-6">
        Ne partagez pas d'informations sensibles (par ex. mot de passe, numéro de carte bleue, etc).
      </p>
      <!-- TODO: accept conditions -->
    </v-form>
    <v-btn x-large color="primary" class="mt-0 mb-6" @click="sendEmail">
      <v-icon class="mr-2">mdi-send</v-icon>
      Envoyer
    </v-btn>
  </div>
</template>

<script>
import validators from "@/validators"
import BreadcrumbsNav from "@/components/BreadcrumbsNav"
import DsfrTextField from "@/components/DsfrTextField"
import DsfrTextarea from "@/components/DsfrTextarea"
import DsfrSelect from "@/components/DsfrSelect"
import { sectorsSelectList } from "@/utils"

export default {
  name: "NewPartner",
  components: { BreadcrumbsNav, DsfrTextField, DsfrTextarea, DsfrSelect },
  props: ["canteen"],
  data() {
    const user = this.$store.state.loggedUser
    return {
      formIsValid: true,
      partner: {},
      contactEmail: user ? user.email : "",
      contactName: user ? `${user.firstName} ${user.lastName}` : "",
      message: "",
      sectors: sectorsSelectList(this.$store.state.sectors),
      economicModels: [
        {
          text: "Public",
          value: "public",
        },
        {
          text: "Privé",
          value: "private",
        },
      ],
      categories: [
        {
          value: "appro",
          text: "Améliorer ma part de bio / durable",
        },
        {
          value: "plastic",
          text: "Substituer mes plastiques",
        },
        {
          value: "asso",
          text: "Donner à une association",
        },
        {
          value: "waste",
          text: "Diagnostiquer mon gaspillage",
        },
        {
          value: "training",
          text: "Me former ou former mon personnel",
        },
        {
          value: "suivi",
          text: "Assurer mon suivi d'approvisionnement",
        },
        {
          value: "vege",
          text: "Diversifier mes sources de protéines",
        },
      ],
    }
  },
  computed: {
    validators() {
      return validators
    },
  },
  methods: {
    sendEmail() {
      this.$refs.form.validate()
      if (!this.formIsValid) {
        this.$store.dispatch("notifyRequiredFieldsError")
        return
      }
      // TODO: backend request to create draft partner
      // and email confirmation to the contact with our reply address?
    },
  },
}
</script>
