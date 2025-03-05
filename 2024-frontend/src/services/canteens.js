import { verifyResponse } from "@/services/api.js"

const createCanteen = (payload) => {
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

const verifySiret = (siret) => {
  return fetch(`/api/v1/canteenStatus/siret/${siret}`, {
    method: "GET",
    headers: {
      "X-CSRFToken": window.CSRF_TOKEN || "",
    },
  })
    .then(verifyResponse)
    .then((response) => response)
    .catch((e) => e)
}

export default { createCanteen, verifySiret, claimCanteen }
