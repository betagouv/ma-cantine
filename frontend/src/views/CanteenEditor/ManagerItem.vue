<template>
  <v-list-item>
    <v-list-item-icon>
      <v-icon :color="color">{{ icon }}</v-icon>
    </v-list-item-icon>
    <v-list-item-content>
      <v-list-item-title
        v-text="manager.lastName ? `${manager.firstName} ${manager.lastName}` : manager.email"
      ></v-list-item-title>
      <v-list-item-subtitle>
        {{ status }}
        <span class="mx-2" v-if="status && manager.lastName">-</span>
        <span v-if="!!manager.lastName">{{ manager.email }}</span>
      </v-list-item-subtitle>
    </v-list-item-content>
  </v-list-item>
</template>

<script>
export default {
  props: ["manager", "icon", "color", "status"],
}
</script>
