import { verifyResponse } from "@/services/api.js"

const getSectors = () => {
  return fetch("/api/v1/sectors/", { method: "GET" }).then(verifyResponse)
}

const getMinistries = () => {
  return fetch("/api/v1/ministries/", { method: "GET" }).then(verifyResponse)
}

const getCategories = (sectors) => {
  const sectorCategories = []
  for (let i = 0; i < sectors.length; i++) {
    const currentSector = sectors[i]
    const key = currentSector.category
    const name = currentSector.categoryName
    const index = sectorCategories.findIndex((sector) => sector.value === key)
    if (index < 0) sectorCategories.push({ value: key, text: name })
  }
  return sectorCategories
}

const getActivities = (sectors) => {
  const sectorActivities = []
  for (let i = 0; i < sectors.length; i++) {
    const currentSector = sectors[i]
    const name = currentSector.name
    const id = currentSector.id
    const hasLineMinistry = currentSector.hasLineMinistry
    const index = sectorActivities.findIndex((sector) => sector.name === name)
    if (index < 0) sectorActivities.push({ index: i, id, name, hasLineMinistry })
  }
  return sectorActivities
}

export default { getSectors, getMinistries, getCategories, getActivities }
