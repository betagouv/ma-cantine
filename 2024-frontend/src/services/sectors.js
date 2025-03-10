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
  const activities = []
  for (let i = 0; i < sectors.length; i++) {
    const currentSector = sectors[i]
    const name = currentSector.name
    const id = currentSector.id
    const hasLineMinistry = currentSector.hasLineMinistry
    const index = activities.findIndex((sector) => sector.name === name)
    if (index < 0) activities.push({ index: i, id, name, hasLineMinistry })
  }
  const activitiesSortedAlphabetical = activities.sort((activityBefore, activityAfter) => {
    if (activityBefore.name < activityAfter.name) return -1
    else if (activityBefore.name > activityAfter.name) return 1
    else return 0
  })
  return activitiesSortedAlphabetical
}

export default { getSectors, getMinistries, getCategories, getActivities }
