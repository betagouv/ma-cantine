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
      <v-row>
        <v-col cols="12" sm="6">
          <DsfrTextField
            v-model="partner.name"
            label="Nom de votre structure / organisation"
            :rules="[validators.required]"
          />
          <DsfrRadio
            label="Secteur économique"
            :items="economicModels"
            v-model="partner.economicModel"
            :rules="[validators.required]"
          />
        </v-col>
        <v-col class="pa-10" cols="12" sm="6">
          <input ref="uploader" class="d-none" type="file" accept="image/*" @change="onImageChanged" id="logo" />
          <v-card
            @click="onImageUploadClick"
            rounded
            color="grey lighten-5"
            class="fill-height"
            style="overflow: hidden;"
            min-height="130"
          >
            <div v-if="partner.image" class="d-flex flex-column fill-height">
              <v-spacer></v-spacer>
              <v-img contain :src="partner.image" max-height="135"></v-img>
              <v-spacer></v-spacer>
            </div>
            <div v-else class="d-flex flex-column align-center justify-center fill-height">
              <v-icon class="pb-2">mdi-shape</v-icon>
              <p class="ma-0 text-center font-weight-bold body-2 grey--text text--darken-2">
                Ajoutez une image (optionnel)
              </p>
            </div>
            <div v-if="partner.image" style="position: absolute; top: 10px; left: 10px;">
              <v-btn fab small @click.stop.prevent="changeImage(null)">
                <v-icon aria-label="Supprimer l'image" aria-hidden="false" color="red">$delete-line</v-icon>
              </v-btn>
            </div>
          </v-card>
        </v-col>
      </v-row>
      <v-col class="mt-6 pa-0" cols="12" md="9">
        <DsfrSelect
          multiple
          clearable
          label="Sur quels aspects, pouvez-vous aider des gestionnaires de restaurants collectifs ?"
          :items="categories"
          v-model="partner.categories"
          :rules="[validators.required]"
        />
      </v-col>
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
      <v-col class="pa-0" cols="12" md="9">
        <v-checkbox hide-details class="mb-4" v-model="partner.national">
          <template v-slot:label>
            <span class="grey--text text--darken-4">
              Mon activité est présente sur tout le territoire national
            </span>
          </template>
        </v-checkbox>
      </v-col>
      <v-col v-if="showDepartmentSelector" class="pa-0 mb-n4" cols="12" md="9">
        <DsfrSelect
          label="Departements où votre activité est présente"
          multiple
          :items="departmentItems"
          v-model="partner.departments"
          :rules="[validators.required]"
        />
      </v-col>
      <DsfrRadio
        label="Quel type de service offrez-vous ?"
        :items="serviceCostOptions"
        v-model="partner.gratuityOption"
        :rules="[validators.required]"
        class="mt-8"
      />
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
      <v-row>
        <v-col cols="12" sm="6">
          <DsfrTextField v-model="partner.contactEmail" label="Votre email" :rules="[validators.email]" />
        </v-col>
        <v-col cols="12" sm="6">
          <DsfrTextField v-model="partner.contactName" label="Prénom et nom (optionnel)" />
        </v-col>
        <v-col cols="12" sm="6">
          <DsfrTextField
            label="Numéro téléphone (optionnel)"
            v-model="partner.contactPhoneNumber"
            :rules="[validators.isEmptyOrPhoneNumber]"
          />
        </v-col>
      </v-row>
      <DsfrTextarea v-model="partner.contactMessage" label="Commentaires sur votre demande (optionnel)" :rows="2" />
      <v-checkbox :rules="[validators.checked]" class="mb-6">
        <template v-slot:label>
          <span class="body-2 grey--text text--darken-3">
            Je déclare avoir lu et et être en accord avec la
            <a href="/static/documents/charte-referencement-1.pdf" target="_blank" @click.stop>
              charte de référencement
              <v-icon small color="primary">mdi-open-in-new</v-icon>
            </a>
            .
          </span>
        </template>
      </v-checkbox>
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
import { sectorsSelectList, toBase64, departmentItems } from "@/utils"

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
        contactPhoneNumber: user ? user.phone_number : "",
        national: true,
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
      serviceCostOptions: [
        {
          text: "Des services gratuits",
          value: "free",
        },
        {
          text: "Des services payants",
          value: "paid",
        },
        {
          text: "Les deux : services gratuits et payants",
          value: "mix",
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
      departmentItems,
    }
  },
  computed: {
    validators() {
      return validators
    },
    showDepartmentSelector() {
      return !this.partner.national
    },
  },
  methods: {
    createPartner() {
      this.$refs.form.validate()
      if (!this.formIsValid) {
        this.$store.dispatch("notifyRequiredFieldsError")
        return
      }
      if (this.partner.national) this.$set(this.partner, "departments", null)
      return this.$store
        .dispatch("createPartner", { payload: this.partner })
        .then(() => {
          this.$store.dispatch("notify", {
            status: "success",
            message: "Votre demande a bien été envoyé.",
          })
          this.$router.push({ name: "PartnersHome" })
        })
        .catch((e) => {
          this.$store.dispatch("notifyServerError", e)
        })
    },
    onImageUploadClick() {
      this.$refs.uploader.click()
    },
    onImageChanged(e) {
      this.changeImage(e.target.files[0])
    },
    changeImage(file) {
      if (!file) {
        this.partner.image = null
        return
      }
      toBase64(file, (base64) => {
        this.$set(this.partner, "image", base64)
      })
    },
  },
}
</script>
