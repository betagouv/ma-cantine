import { verifyResponse } from "@/services/api.js"

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

export default { fetchDiagnosticsRecap }
