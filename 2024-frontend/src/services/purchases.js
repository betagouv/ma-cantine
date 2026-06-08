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

const fetchPurchase = (id) => {
  return fetch(`/api/v1/purchases/${id}`, {
    method: "GET",
    headers: {
      "X-CSRFToken": window.CSRF_TOKEN || "",
    },
  })
    .then(verifyResponse)
    .then((response) => response)
    .catch((e) => e)
}

const updatePurchase = (payload, id) => {
  return fetch(`/api/v1/purchases/${id}`, {
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

const fetchPurchasesOptions = () => {
  return fetch(`/api/v1/purchaseOptions/`, {
    method: "GET",
    headers: {
      "X-CSRFToken": window.CSRF_TOKEN || "",
    },
  })
    .then(verifyResponse)
    .then((response) => response)
}

export default {
  createPurchase,
  fetchPurchase,
  updatePurchase,
  fetchPurchasesOptions,
}
