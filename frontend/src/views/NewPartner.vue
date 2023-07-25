<template>
  <div class="text-left">
    <BreadcrumbsNav :links="[{ to: { name: 'PartnersHome' } }]" />
    <h1 class="font-weight-black text-h5 text-sm-h4 mb-4">Nouvel acteur de l'éco-système</h1>
    <p>
      Veuillez renseigner ce formulaire et notre équipe va vérifier votre demande et ajouter votre organisation dans
      notre base de données.
    </p>
    <p class="text-caption">
      Sauf mention contraire “(optionnel)” dans le label, tous les champs sont obligatoires
    </p>
    <v-form v-model="formIsValid" ref="form" @submit.prevent class="mt-8">
      <v-col class="pa-0" cols="12" sm="6">
        <DsfrTextField
          v-model="partner.name"
          label="Nom de votre structure / organisation"
          :rules="[validators.required]"
        />
      </v-col>
      <v-col class="pa-0" cols="12" md="9">
        <DsfrSelect
          multiple
          clearable
          label="Sur quels aspects, pouvez-vous aider des gestionnaires de restaurants collectifs ?"
          :items="categories"
          v-model="partner.categories"
          :rules="[validators.required]"
        />
      </v-col>
      <DsfrRadio
        label="Secteur économique"
        :items="economicModels"
        v-model="partner.economicModel"
        :rules="[validators.required]"
      />
      <v-col class="pa-0" cols="12" md="7">
        <DsfrSelect
          label="Type d'acteur"
          multiple
          :items="partnerTypes"
          v-model="partner.types"
          item-text="name"
          item-value="id"
          :rules="[validators.required]"
        />
      </v-col>
      <v-col class="pa-0" cols="12" md="9">
        <DsfrSelect
          label="Secteurs d'activité (optionnel)"
          multiple
          :items="sectors"
          v-model="partner.sectors"
          item-text="name"
          item-value="id"
        />
      </v-col>
      <DsfrRadio
        label="Est-ce que vous offrez des services gratuits ?"
        :items="serviceCostOptions"
        v-model="partner.free"
        :rules="[validators.required]"
      />
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
      <v-col class="pa-0" cols="12" sm="6">
        <DsfrTextField
          v-model="partner.website"
          label="URL du site"
          :rules="[validators.required, validators.urlOrEmpty]"
        />
      </v-col>
      <!-- TODO: optional image field -->
      <v-row>
        <v-col cols="12" sm="6">
          <DsfrTextField v-model="partner.contactEmail" label="Votre email" :rules="[validators.email]" />
        </v-col>
        <v-col cols="12" sm="6">
          <DsfrTextField v-model="partner.contactName" label="Prénom et nom (optionnel)" />
        </v-col>
      </v-row>
      <DsfrTextarea v-model="partner.contactMessage" label="Commentaires sur votre demande (optionnel)" :rows="2" />
    </v-form>
    <v-btn x-large color="primary" class="mt-0 mb-6" @click="createPartner">
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
import DsfrRadio from "@/components/DsfrRadio"
import { sectorsSelectList } from "@/utils"

export default {
  name: "NewPartner",
  components: { BreadcrumbsNav, DsfrTextField, DsfrTextarea, DsfrSelect, DsfrRadio },
  props: ["canteen"],
  data() {
    const user = this.$store.state.loggedUser
    return {
      formIsValid: true,
      partner: {
        contactEmail: user ? user.email : "",
        contactName: user ? `${user.firstName} ${user.lastName}` : "",
      },
      conditionsAccepted: false,
      sectors: sectorsSelectList(this.$store.state.sectors),
      partnerTypes: this.$store.state.partnerTypes,
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
      // TODO: update these options and backend to include mixed payment option
      serviceCostOptions: [
        {
          text: "Oui",
          value: true,
        },
        {
          text: "Non",
          value: false,
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
    createPartner() {
      this.$refs.form.validate()
      if (!this.formIsValid) {
        this.$store.dispatch("notifyRequiredFieldsError")
        return
      }
      // TODO: debug sector and actor type setting
      this.$store.dispatch("createPartner", { payload: this.partner }).then(() => {
        this.$store.dispatch("notify", {
          status: "success",
          message: "Votre demande a bien été envoyé.",
        })
        this.$router.push({ name: "PartnersHome" })
      })
      // TODO: rate limit requests?
    },
  },
}
</script>
