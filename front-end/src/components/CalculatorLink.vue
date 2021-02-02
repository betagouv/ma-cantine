<template>
  <a :href="`${publicPath}Diagnostic approvisionnement (ma-cantine-alpha) v0.2.ods`" download>
   {{message}}
  </a>
</template>

<script>
  export default {
    name: "CalculatorLink",
    props: {
      message: String
    },
    data() {
      return {
        publicPath: process.env.BASE_URL,
      };
    },
  }
</script>
