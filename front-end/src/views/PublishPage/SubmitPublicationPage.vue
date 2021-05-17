<template>
  <div>
    <h2>Publication de mes données</h2>

    <form v-if="canteen" @submit.prevent="submit">
      <BaseCheckbox
        v-model="makeDataPublic"
        label="J'accepte que les données relatives aux mesures EGAlim de ma cantine soient visibles."
        inputId="data-public"
      />

      <input type="submit" id="submit" value="Publier">
    </form>
  </div>
</template>

<script>
  import BaseCheckbox from '@/components/KeyMeasureDiagnostic/Inputs/BaseCheckbox';
  import { completePublication } from "@/data/submit-actions.js";

  export default {
    components: {
      BaseCheckbox,
    },
    props: ['routeProps'],
    data() {
      return {
        makeDataPublic: true,
      }
    },
    computed: {
      canteen() {
        return this.routeProps;
      }
    },
    methods: {
      async submit() {
        const response = await completePublication(this.makeDataPublic);

        if (response.status === 204) {
          alert("Vos données ont bien été publiées");
          return this.$router.push({ name: 'KeyMeasuresHome' });
        } else {
          const error = await response.json();
          console.log(error);
          alert("Une erreur est survenue, vous pouvez nous contacter directement à contact@egalim.beta.gouv.fr");
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
