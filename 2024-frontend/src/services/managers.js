import { verifyResponse } from "@/services/api.js"

const headers = {
  "X-CSRFToken": window.CSRF_TOKEN || "",
  "Content-Type": "application/json",
}

const addManager = (canteenId, email) => {
  return fetch("/api/v1/addManager/", {
    method: "POST",
    headers,
    body: JSON.stringify({ canteenId, email }),
  })
    .then(verifyResponse)
    .then((response) => response)
    .catch((e) => e)
}

const removeManager = (canteenId, email) => {
  return fetch("/api/v1/removeManager/", {
    method: "POST",
    headers,
    body: JSON.stringify({ canteenId, email }),
  })
    .then(verifyResponse)
    .then((response) => response)
    .catch((e) => e)
}

export default {
  addManager,
  removeManager,
}
