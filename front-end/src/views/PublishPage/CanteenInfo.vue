<template>
  <div>
    <h2>Information sur ma cantine</h2>

    <p>
      Mieux vous connaître. <br> Dîtes-nous en un peu plus sur votre établissement.
      Cela permettra d'identifier facilement votre cantine parmi celles qui ont fait le choix de publier.
    </p>

    <form v-if="canteen" @submit.prevent="submit">
      <BaseInput
        v-model="canteen.name"
        label="Nom de la cantine"
        inputId="canteen-name"
        type="text"
      />

      <BaseInput
        v-model="canteen.city"
        label="Ville / commune"
        inputId="canteen-city"
        type="text"
      />

      <BaseInput
        v-model="canteen.mealCount"
        label="Nombre de couverts moyen par jour"
        inputId="canteen-meal-count"
        type="number"
        min=0
      />

      <BaseSelect
        v-model="canteen.sector"
        label="Secteur d'activité"
        inputId="canteen-sector"
        :options="sectors"
      />

      <input type="submit" id="submit" value="Valider">
    </form>
  </div>
</template>

<script>
  import BaseInput from '@/components/KeyMeasureDiagnostic/Inputs/BaseInput';
  import BaseSelect from '@/components/KeyMeasureDiagnostic/Inputs/BaseSelect';
  import sectors from "@/data/sector-tags.json";
  import { extendCanteenInfo } from "@/data/submit-actions.js";

  export default {
    components: {
      BaseInput,
      BaseSelect,
    },
    props: ['routeProps'],
    data() {
      return {
        sectors,
      }
    },
    computed: {
      canteen() {
        return this.routeProps;
      }
    },
    methods: {
      async submit() {
        const response = await extendCanteenInfo(this.canteen);

        if (response.status === 204) {
          return this.$router.push({ name: 'PublishMeasurePage', params: { id: 'qualite-des-produits' } });
        } else {
          const error = await response.json();
          console.log(error);
          alert("Une erreur est survenue, vous pouvez nous contacter directement à contact@egalim.beta.gouv.fr")
        }
      },
    },
  }
</script>

<style scoped lang="scss">
  form {
    margin-top: 30px;
    display: flex;
    flex-direction: column;

    .sector {
      text-align: left;
      width: 90%;
      font-size: 24px;
      margin-top: 1em;

      select {
        font-size: 20px;
        padding: 5px;
        border: none;
        background-color: white;
        border-radius: 5px;
        box-shadow: 0 0 5px $light-grey;
      }
    }

    #submit {
      color: $white;
      font-size: 24px;
      background-color: $orange;
      width: 10em;
      padding: 0.2em;
      border-radius: 1em;
      cursor: pointer;
      margin-left: auto;
      text-align: center;
      border: none;
      margin-top: 10px;
      margin-bottom: 10px;
    }
  }
</style>
