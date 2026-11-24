import { verifyResponse } from "@/services/api.js"

const getSectors = () => {
  return fetch("/api/v1/sectors/", { method: "GET" }).then(verifyResponse)
}

const getMinistries = () => {
  return fetch("/api/v1/ministries/", { method: "GET" }).then(verifyResponse)
}

const sortSectors = (sectors) => {
  const isOther = (sector) => sector.value.includes("_autre")
  const isOtherCategory = (sector) => sector.category === "autres"
  const sectorsSorted = [...sectors].sort((sectorBefore, sectorAfter) => {
    const beforeIsOtherCategory = isOtherCategory(sectorBefore)
    const afterIsOtherCategory = isOtherCategory(sectorAfter)
    const beforeIsOther = isOther(sectorBefore)
    const afterIsOther = isOther(sectorAfter)
    const beforeCategoryName = sectorBefore.categoryName
    const afterCategoryName = sectorAfter.categoryName
    const beforeName = sectorBefore.name
    const afterName = sectorAfter.name

    switch (true) {
      case beforeIsOtherCategory && !afterIsOtherCategory:
        return 1
      case !beforeIsOtherCategory && afterIsOtherCategory:
        return -1
      case beforeCategoryName < afterCategoryName:
        return -1
      case beforeCategoryName > afterCategoryName:
        return 1
      case beforeIsOther && !afterIsOther:
        return 1
      case !beforeIsOther && afterIsOther:
        return -1
      case beforeName < afterName:
        return -1
      case beforeName > afterName:
        return 1
      default:
        return 0
    }
  })
  return sectorsSorted
}

export default { getSectors, getMinistries, sortSectors }
