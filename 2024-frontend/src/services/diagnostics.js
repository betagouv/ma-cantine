import { verifyResponse } from "@/services/api.js"

const createDiagnostic = (canteenId, payload) => {
  payload["creationSource"] = "APP"
  return fetch(`/api/v1/canteens/${canteenId}/diagnostics/`, {
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

const fetchDiagnosticsRecap = (canteenId) => {
  return fetch(`/api/v1/canteens/${canteenId}/diagnostics/recap`, {
    method: "GET",
    headers: {
      "X-CSRFToken": window.CSRF_TOKEN || "",
    },
  })
    .then(verifyResponse)
    .then((response) => response)
    .catch((e) => e)
}

export default { createDiagnostic, fetchDiagnosticsRecap }
