import { verifyResponse } from "@/services/api.js"

const createCanteen = (payload) => {
  console.log("string", JSON.stringify(payload))
  return fetch("/api/v1/canteens/", {
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

export { createCanteen }
