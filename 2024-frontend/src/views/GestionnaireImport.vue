<script setup>
import { computed } from "vue"
import { useRoute } from "vue-router"

const route = useRoute()

const tiles = computed(() => {
  const tiles = []
  const childrenPages = getChildrenPages()

  childrenPages.forEach((page) => {
    tiles.push({
      title: page.meta.title,
      to: { name: page.name },
      icon: false,
    })
  })
  return tiles
})

const getChildrenPages = () => {
  const currentPage = route.matched[0]
  const children = currentPage.children
  const childrenWithouCurrent = children.filter((page) => page.name !== route.name)
  return childrenWithouCurrent
}
</script>

<template>
  <div>
    <h1>{{ route.meta.title }}</h1>
    <DsfrTiles :tiles="tiles" :horizontal="true" />
  </div>
</template>
