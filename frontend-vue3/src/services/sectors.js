import { verifyResponse } from "@/services/api.js"

const getSectors = () => {
  return fetch("/api/v1/sectors/", { method: "GET" }).then(verifyResponse)
}

const getMinistries = () => {
  return fetch("/api/v1/ministries/", { method: "GET" }).then(verifyResponse)
}

export default { getSectors, getMinistries }
