import { verifyResponse } from "@/services/api.js"

const createPurchase = (payload) => {
  payload["creationSource"] = "APP"
  return fetch("/api/v1/purchases/", {
    method: "POST",
    headers: {
      "X-CSRFToken": window.CSRF_TOKEN || "",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  })
    .then(verifyResponse)
    .then((response) => response)
    .catch((e) => e)
}

export default {
  createPurchase
}
