<template>
  <div class="text-left">
    <h1 class="text-h4 font-weight-black mt-12 mb-10">Contactez-nous</h1>
    <p>
      Consultez notre
      <router-link :to="{ name: 'FaqPage' }">foire aux questions</router-link>
      pour des résponses aux questions les plus fréquentes.
    </p>
    <GeneralContactForm></GeneralContactForm>
  </div>
</template>

<script>
import GeneralContactForm from "@/components/GeneralContactForm"

export default {
  name: "ContactPage",
  components: { GeneralContactForm },
}
</script>
