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

const unlinkSatellite = (canteenId, satelliteId) => {
  return fetch(`/api/v1/canteens/${canteenId}/satellites/${satelliteId}/unlink/`, {
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

const linkSatellite = (canteenId, satelliteId) => {
  return fetch(`/api/v1/canteens/${canteenId}/satellites/${satelliteId}/link/`, {
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

const fetchCanteensActions = (year) => {
  return fetch(`/api/v1/canteenActions/${year}`, {
    method: "GET",
    headers: {
      "X-CSRFToken": window.CSRF_TOKEN || "",
    },
  })
    .then(verifyResponse)
    .then((response) => response)
    .catch((e) => e)
}

const deleteCanteen = (canteenId) => {
 return fetch(`/api/v1/canteens/${canteenId}`, {
    method: "DELETE",
    headers: {
      "X-CSRFToken": window.CSRF_TOKEN || "",
    }
  })
    .then(verifyResponse)
    .then((response) => response)
    .catch((e) => e)
}

const exportCanteens = () => {
  // Waiting for endpoint to be implemented
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve(true)
    }, 1000)
  })
 }

export default {
  createCanteen,
  canteenStatus,
  fetchCanteen,
  updateCanteen,
  claimCanteen,
  deleteCanteen,
  teamJoinRequest,
  fetchSatellites,
  linkSatellite,
  unlinkSatellite,
  fetchCanteensActions,
  exportCanteens,
}
