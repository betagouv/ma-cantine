import { verifyResponse } from "@/services/api.js"

const importFile = (payload) => {
  const file = payload.file[0]
  const form = new FormData()
  const importType = payload.importType || "siret"
  form.append("file", file)
  form.append("type", importType)
  return fetch(`/api/v1/${payload.apiUrl}/`, {
    method: "POST",
    headers: {
      "X-CSRFToken": window.CSRF_TOKEN || "",
    },
    body: form,
  }).then(verifyResponse)
}

export { importFile }
