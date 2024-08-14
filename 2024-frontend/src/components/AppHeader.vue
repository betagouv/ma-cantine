<script setup>
import { computed } from "vue"
import { useRootStore } from "@/stores/root"

const store = useRootStore()

const logoText = ["Ministère", "de l’Agriculture", "et de la Souveraineté", "Alimentaire"]

const quickLinks = computed(() => {
  if (!store.loggedUser) {
    const login = { to: "/s-identifier", label: "S'identifier" }
    const signup = { to: "/creer-mon-compte", label: "Créer mon compte" }
    return [login, signup]
  }
  // TODO: logout action
  if (store.loggedUser.isDev) {
    const apis = { to: { name: "DeveloperPage" }, label: "Développement et APIs" }
    return [apis]
  }
  const mesCantines = { to: { name: "ManagementPage" }, label: "Mon tableau de bord" }
  return [mesCantines]
})
</script>

<template>
  <DsfrHeader
    :logo-text
    operatorImgSrc="/static/images/ma-cantine-logo-light.jpg"
    operatorImgAlt="ma cantine"
    operatorImgStyle="height: 65px;"
    :quickLinks
  />
</template>
