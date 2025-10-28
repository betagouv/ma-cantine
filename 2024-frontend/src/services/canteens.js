import { verifyResponse } from "@/services/api.js"

const createCanteen = (payload) => {
  payload["creationSource"] = "APP"
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

const canteenStatus = (searchBy, number) => {
  return fetch(`/api/v1/canteenStatus/${searchBy}/${number}`, {
    method: "GET",
    headers: {
      "X-CSRFToken": window.CSRF_TOKEN || "",
    },
  })
    .then(verifyResponse)
    .then((response) => response)
    .catch((e) => e)
}

const fetchCanteen = (id) => {
  return fetch(`/api/v1/canteens/${id}`, {
    method: "GET",
    headers: {
      "X-CSRFToken": window.CSRF_TOKEN || "",
    },
  })
    .then(verifyResponse)
    .then((response) => response)
    .catch((e) => e)
}

const updateCanteen = (payload, id) => {
  return fetch(`/api/v1/canteens/${id}`, {
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

const addSatellite = (payload, id) => {
  return fetch(`/api/v1/canteens/${id}/satellites/`, {
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

const fetchSatellites = (canteenId) => {
  return fetch(`/api/v1/canteens/${canteenId}/satellites/`, {
    method: "GET",
    headers: {
      "X-CSRFToken": window.CSRF_TOKEN || "",
    },
  })
    .then(verifyResponse)
    .then((response) => response)
    .catch((e) => e)
}

const unlinkSatellite = (centralId, satelliteId) => {
  return fetch(`/api/v1/canteens/${centralId}/satellites/${satelliteId}/unlink/`, {
    method: "POST",
    headers: {
      "X-CSRFToken": window.CSRF_TOKEN || "",
      "Content-Type": "application/json",
    },
  })
    .then(verifyResponse)
    .then((response) => response)
    .catch((e) => e)
}

const claimCanteen = (id) => {
  return fetch(`/api/v1/canteens/${id}/claim/`, {
    method: "POST",
    headers: {
      "X-CSRFToken": window.CSRF_TOKEN || "",
    },
  })
    .then(verifyResponse)
    .then((response) => response)
    .catch((e) => e)
}

const teamJoinRequest = (id, userInfos) => {
  return fetch(`/api/v1/teamJoinRequest/${id}/`, {
    method: "POST",
    headers: {
      "X-CSRFToken": window.CSRF_TOKEN || "",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(userInfos),
  })
    .then(verifyResponse)
    .then((response) => response)
    .catch((e) => e)
}

const fetchCanteensActions = () => {
  return fetch("/api/v1/canteenActions/", {
    method: "GET",
    headers: {
      "X-CSRFToken": window.CSRF_TOKEN || "",
    },
  })
    .then(verifyResponse)
    .then((response) => response)
    .catch((e) => e)
}

export default {
  createCanteen,
  canteenStatus,
  fetchCanteen,
  updateCanteen,
  claimCanteen,
  teamJoinRequest,
  addSatellite,
  fetchSatellites,
  unlinkSatellite,
  fetchCanteensActions,
}
