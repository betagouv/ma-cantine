<template>
  <div v-if="canteen">
    <p>
      « {{ canteen.name }} » est une cuisine centrale sans lieu de consommation. Les diagnostics concernent
      <b>uniquement les lieux de restauration recevant des convives.</b>
    </p>
    <p>
      Vous pouvez
      <router-link :to="{ name: 'NewCanteen' }">ajouter une cantine satellite</router-link>
      ou indiquer que
      <router-link
        :to="{
          name: 'CanteenModification',
          params: { canteenUrlComponent: $store.getters.getCanteenUrlComponent(canteen) },
        }"
      >
        votre cantine reçoit des convives sur place.
      </router-link>
    </p>
  </div>
</template>

<script>
export default {
  props: {
    canteen: {
      type: Object,
    },
  },
}
</script>
