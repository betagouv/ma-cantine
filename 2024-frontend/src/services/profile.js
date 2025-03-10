import { verifyResponse } from "@/services/api.js"

const updateProfile = (userId, payload) => {
  return fetch(`/api/v1/user/${userId}`, {
    method: "PATCH",
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

export default { updateProfile }
