<template>
  <div class="text-left pb-10">
    <h1 class="font-weight-black text-h4 my-4">
      {{ isNewCantine ? "Nouvelle cantine" : "Modifier ma cantine" }}
    </h1>
    <div class="mb-8 mt-2" v-if="!isNewCantine">
      <v-chip small :color="canteen.dataIsPublic ? 'green lighten-4' : 'grey lighten-4'" label>
        {{ canteen.dataIsPublic ? "Publiée" : "Pas encore publiée" }}
      </v-chip>
      <v-btn text small class="text-decoration-underline">
        {{ canteen.dataIsPublic ? "Enlever la publication" : "Publier ma cantine" }}
      </v-btn>
    </div>
    <v-form v-model="formIsValid" lazy-validation>
      <v-row>
        <v-col cols="12" md="8">
          <p class="body-2 my-2">Nom de la cantine</p>
          <v-text-field hide-details="auto" :rules="[validators.notEmpty]" solo v-model="canteen.name"></v-text-field>
        </v-col>
        <v-col cols="12" md="8">
          <p class="body-2 my-2">SIRET</p>
          <v-text-field hide-details="auto" solo v-model="canteen.siret"></v-text-field>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="12" md="4">
          <p class="body-2 my-2">Ville / commune</p>
          <v-text-field hide-details="auto" :rules="[validators.notEmpty]" solo v-model="canteen.city"></v-text-field>
        </v-col>
        <v-col cols="12" md="4">
          <p class="body-2 my-2">Département</p>
          <v-select
            solo
            v-model="canteen.department"
            :rules="[validators.notEmpty]"
            :items="departments"
            :item-text="(item) => `${item.departmentCode} - ${item.departmentName}`"
            item-value="departmentCode"
            hide-details="auto"
          ></v-select>
        </v-col>

        <v-col cols="12" md="4">
          <p class="body-2 my-2">Nombre de couverts moyen par jour</p>
          <v-text-field
            hide-details="auto"
            :rules="[validators.greaterThanZero]"
            solo
            v-model="canteen.dailyMealCount"
          ></v-text-field>
        </v-col>

        <v-col cols="12">
          <v-divider></v-divider>
        </v-col>

        <v-col cols="12" md="8">
          <p class="body-2 my-2">Secteurs d'activité</p>
          <v-select
            multiple
            :items="sectors"
            solo
            v-model="canteen.sectors"
            item-text="name"
            item-value="id"
          ></v-select>
        </v-col>

        <v-col cols="12" md="4">
          <p class="body-2 my-2">Mode de gestion</p>
          <v-radio-group v-model="canteen.managementType">
            <v-radio
              class="ml-8"
              v-for="item in managementTypes"
              :key="item.value"
              :label="item.text"
              :value="item.value"
            ></v-radio>
          </v-radio-group>
        </v-col>
      </v-row>
    </v-form>

    <v-sheet rounded color="grey lighten-4 pa-3" class="d-flex">
      <v-spacer></v-spacer>
      <v-btn x-large color="primary">Valider</v-btn>
    </v-sheet>

    <div v-if="!isNewCantine">
      <h2 class="font-weight-black text-h5 mt-10">
        Mes diagnostics pour cette cantine
      </h2>
      <v-btn text color="primary" class="mt-2 mb-8 ml-n4">
        <v-icon class="mr-2">mdi-plus</v-icon>
        Ajouter un diagnostic
      </v-btn>
      <v-row>
        <v-col cols="12" v-for="diagnostic in canteen.diagnostics" :key="`diagnostic-${diagnostic.id}`">
          <DiagnosticCard :diagnostic="diagnostic" class="fill-height" />
        </v-col>
      </v-row>
    </div>
  </div>
</template>

<script>
import validators from "@/validators"
import DiagnosticCard from "@/components/DiagnosticCard"
import departments from "@/departments.json"

export default {
  name: "CanteenEditor",
  components: { DiagnosticCard },
  props: {
    canteenUrlComponent: {
      type: String,
      required: false,
    },
  },
  data() {
    return {
      canteen: {},
      formIsValid: true,
      managementTypes: [
        {
          text: "Directe",
          value: "direct",
        },
        {
          text: "Concédée",
          value: "conceded",
        },
      ],
    }
  },
  computed: {
    validators() {
      return validators
    },
    sectors() {
      return this.$store.state.sectors
    },
    departments() {
      return departments
    },
    isNewCantine() {
      return !this.canteenUrlComponent
    },
  },
  mounted() {
    if (this.isNewCantine) return
    const canteen = this.$store.getters.getCanteenFromUrlComponent(this.canteenUrlComponent)
    if (canteen) this.canteen = JSON.parse(JSON.stringify(canteen))
    else this.$router.push({ name: "NewCanteen" })
  },
}
</script>
