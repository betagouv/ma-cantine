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

const deletePurchase = (id) => {
  return fetch(`/api/v1/purchases/${id}`, {
    method: "DELETE",
    headers: {
      "X-CSRFToken": window.CSRF_TOKEN || "",
    },
  })
    .then(verifyResponse)
    .then((response) => response)
}

const restorePurchases = (ids) => {
  return fetch(`/api/v1/purchases/restore/`, {
    method: "POST",
    headers: {
      "X-CSRFToken": window.CSRF_TOKEN || "",
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ ids }),
  })
    .then(verifyResponse)
    .then((response) => response)
}

const fetchInvoice = async (canteenId, purchaseId) => {
  return await fetch(`/api/v1/canteens/${canteenId}/purchases/${purchaseId}/facture`, {
    method: "GET",
    headers: {
      "X-CSRFToken": window.CSRF_TOKEN || "",
    },
  })
    .then(verifyResponse)
    .then((response) => response)
}

const uploadInvoice = async (payload) => {
  const { canteenId, purchaseId, body } = payload
  return await fetch(`/api/v1/canteens/${canteenId}/purchases/${purchaseId}/facture`, {
    method: "POST",
    headers: {
      "X-CSRFToken": window.CSRF_TOKEN || "",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  })
    .then(verifyResponse)
    .then((response) => response)
}

const deleteInvoice = async (canteenId, purchaseId) => {
  return await fetch(`/api/v1/canteens/${canteenId}/purchases/${purchaseId}/facture`, {
    method: "DELETE",
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
  fetchPurchasesOptions,
  updatePurchase,
  deletePurchase,
  restorePurchases,
  fetchInvoice,
  uploadInvoice,
  deleteInvoice,
}
