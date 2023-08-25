<template>
  <div>
    <h1>Test DSFR</h1>
    <DsfrAlert title="Testing" />
    <router-link :to="{ path: 'test' }">Testing</router-link>
  </div>
</template>

<script>
export default {
  name: "LandingPage",
}
</script>
