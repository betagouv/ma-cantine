<template>
  <div class="text-left">
    <h1 class="text-h4 font-weight-black mt-12 mb-10">Contactez-nous</h1>
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
