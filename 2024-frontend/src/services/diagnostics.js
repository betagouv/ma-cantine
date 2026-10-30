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

const updateDiagnostic = (canteenId, diagnosticId, payload) => {
  return fetch(`/api/v1/canteens/${canteenId}/diagnostics/${diagnosticId}`, {
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

const voletsUrl = {
  diversification: "menus-vegetariens",
}

const updateVolet = (canteenId, diagnosticId, volet, payload) => {
  return fetch(`/api/v2/canteens/${canteenId}/diagnostics/${diagnosticId}/${voletsUrl[volet]}`, {
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

const fetchDiagnostic = (canteenId, diagnosticId) => {
  return fetch(`/api/v1/canteens/${canteenId}/diagnostics/${diagnosticId}`, {
    method: "GET",
    headers: {
      "X-CSRFToken": window.CSRF_TOKEN || "",
    },
  })
    .then(verifyResponse)
    .then((response) => response)
    .catch((e) => e)
}

const fetchDiagnostics = (canteenId, limit) => {
  const query = limit ? `?limit=${limit}` : ""
  return fetch(`/api/v1/canteens/${canteenId}/diagnostics/${query}`, {
    method: "GET",
    headers: {
      "X-CSRFToken": window.CSRF_TOKEN || "",
    },
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

const fetchDiagnosticRecap = (canteenId, diagnosticId) => {
  return fetch(`/api/v1/canteens/${canteenId}/diagnostics/${diagnosticId}/recap`, {
    method: "GET",
    headers: {
      "X-CSRFToken": window.CSRF_TOKEN || "",
    },
  })
    .then(verifyResponse)
    .then((response) => response)
    .catch((e) => e)
}

const checkDiagnostic = (canteenId, diagnosticId) => {
  return fetch(`/api/v1/canteens/${canteenId}/diagnostics/${diagnosticId}/check`, {
    method: "GET",
    headers: {
      "X-CSRFToken": window.CSRF_TOKEN || "",
    },
  })
    .then(verifyResponse)
    .then((response) => response)
    .catch((e) => e)
}

const teledeclareDiagnostic = (canteenId, diagnosticId) => {
  return fetch(`/api/v1/canteens/${canteenId}/diagnostics/${diagnosticId}/teledeclaration/create`, {
    method: "POST",
    headers: {
      "X-CSRFToken": window.CSRF_TOKEN || "",
    },
  })
    .then(verifyResponse)
    .then((response) => response)
    .catch((e) => e)
}

const cancelTeledeclaration = (canteenId, diagnosticId) => {
  return fetch(`/api/v1/canteens/${canteenId}/diagnostics/${diagnosticId}/teledeclaration/cancel`, {
    method: "POST",
    headers: {
      "X-CSRFToken": window.CSRF_TOKEN || "",
    },
  })
    .then(verifyResponse)
    .then((response) => response)
    .catch((e) => e)
}

export default {
  createDiagnostic,
  updateDiagnostic,
  updateVolet,
  checkDiagnostic,
  fetchDiagnostic,
  fetchDiagnostics,
  fetchDiagnosticsRecap,
  fetchDiagnosticRecap,
  teledeclareDiagnostic,
  cancelTeledeclaration,
}
