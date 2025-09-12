import { defineStore } from "pinia"
import { ref } from "vue"

const useStoreCanteen = defineStore("canteen", () => {
  const name = ref()
  const id = ref()
  const urlComponent = ref()

  function setUrlComponent(value) {
    urlComponent.value = value
    id.value = value.split("--")[0]
    name.value = value.split("--")[1]
  }

  return { setUrlComponent, name }
})

export { useStoreCanteen }
