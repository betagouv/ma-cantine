import { verifyResponse } from "@/services/api.js"

const fetchManagers = (canteenId) => {
  return fetch(`/api/v1/canteens/${canteenId}/managers`, {
    method: "GET",
    headers: {
      "X-CSRFToken": window.CSRF_TOKEN || "",
    },
  })
    .then(verifyResponse)
    .then((response) => response)
    .catch((e) => e)
}

const fetchManagerInvitations = (canteenId) => {
  return fetch(`/api/v1/canteens/${canteenId}/managers/invitations`, {
    method: "GET",
    headers: {
      "X-CSRFToken": window.CSRF_TOKEN || "",
    },
  })
    .then(verifyResponse)
    .then((response) => response)
    .catch((e) => e)
}

const addManager = (canteenId, email) => {
  return fetch("/api/v1/addManager/", {
    method: "POST",
    headers: {
      "X-CSRFToken": window.CSRF_TOKEN || "",
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ canteenId, email }),
  })
    .then(verifyResponse)
    .then((response) => response)
    .catch((e) => e)
}

const removeManager = (canteenId, email) => {
  return fetch("/api/v1/removeManager/", {
    method: "POST",
    headers: {
      "X-CSRFToken": window.CSRF_TOKEN || "",
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ canteenId, email }),
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
  return fetch(`/api/v1/canteens/${id}/teamJoinRequest/`, {
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

export default {
  fetchManagers,
  fetchManagerInvitations,
  addManager,
  removeManager,
  claimCanteen,
  teamJoinRequest,
}
