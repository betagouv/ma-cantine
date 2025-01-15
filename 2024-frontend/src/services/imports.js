import { verifyResponse } from "@/services/api.js"

const importPurchases = (payload) => {
  const file = payload.file[0]
  const form = new FormData()
  form.append("file", file)
  return fetch("/api/v1/importPurchases/", {
    method: "POST",
    headers: {
      "X-CSRFToken": window.CSRF_TOKEN || "",
    },
    body: form,
  }).then(verifyResponse)
}

export { importPurchases }
