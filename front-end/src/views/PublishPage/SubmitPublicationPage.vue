<template>
  <div>
    <h2>Publication de mes données</h2>

    <div id="preamble">
      <i class="fas fa-clipboard-list"></i>
      <div>
        <p>
          Vous avez rempli votre auto-diagnostic et les données ont bien été enregistrées. Vous pouvez à présent décider de rendre publiques ces données afin d'accroître la transparence pour vos convives, les élu.e.s de votre collectivité...
        </p>
        <p>
          Le cas échéant, un encart dédié à votre établissement apparaitra sur la page <router-link :to="{ name: 'CanteensHome' }">nos cantines</router-link>.
          Seront mis en avant vos initiatives, indicateurs et démarches entreprises pour une alimentation plus saine et durable.
          C'est aussi un bon moyen de répondre à
            <router-link :to="{ name: 'KeyMeasurePage', params: { id: 'information-des-usagers' } }">l'obligation réglementaire de télédéclaration</router-link>
          des parts de produits bio et durables qui sera en vigueur dès fin 2022.
        </p>
      </div>
    </div>

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
  #preamble {
    display: flex;
    align-items: center;

    .fa-clipboard-list {
      color: $blue;
      font-size: 12em;
    }

    p {
      margin-left: 2em;
      text-align: left;
    }
  }

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
