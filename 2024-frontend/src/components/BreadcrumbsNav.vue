<script setup>
import { computed } from "vue"
import { routes } from "@/router"
import { useRoute } from "vue-router"
import urlService from "@/services/urls"

const route = useRoute()

const breadcrumbRoutes = JSON.parse(JSON.stringify(routes))
// flatten routes for simplicity
breadcrumbRoutes.forEach((r) => {
  if (r.children) {
    breadcrumbRoutes.push(...r.children)
  }
})

const pageTitle = computed(() => route.meta?.title)
const canteenUrlComponent = computed(() => route.params?.canteenUrlComponent)

const breadcrumbLinks = computed(() => {
  const allLinks = [{ text: "Accueil", to: "/" }]
  if (route.meta?.breadcrumbs) {
    route.meta.breadcrumbs.forEach((link) => {
      if (link.useCanteenName && canteenUrlComponent.value) {
        const title = urlService.getCanteenName(canteenUrlComponent.value) || "Mon établissement"
        link.title = title.replace(/-/g, " ")
      } else if (link.useCanteenName) {
        console.error(
          "BreadcrumbsNav: cannot identify canteen for breadcrumbs, canteenUrlComponent required in current route"
        )
      } else if (!link.title && link.to?.name) {
        link.title = breadcrumbRoutes.find((r) => r.name === link.to.name)?.meta?.title
      }
      link.text = link.title // DSFR component uses different key to our legacy code
      allLinks.push(link)
    })
  }
  allLinks.push({ text: pageTitle })
  return allLinks
})
</script>

<template>
  <DsfrBreadcrumb breadcrumbId="ma-cantine-fil-dariane" :links="breadcrumbLinks" />
</template>
