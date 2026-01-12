const getDefaultErrorMessage = () => 'Une erreur est survenue, vous pouvez réessayer plus tard ou nous contacter directement à support-egalim@beta.gouv.fr'

const authenticationError = () => {
  return {
    name: "AuthenticationError",
    message: 'Votre session a expiré. Rechargez la page et reconnectez-vous pour continuer.',
  }
}

const badRequestError = (error) => {
  return {
    name: "BadRequestError",
    errorsList: error || [],
    errorDefaultMessage: getDefaultErrorMessage(),
  }
}

const verifyResponse = async (response) => {
  const contentType = response.headers.get("content-type")
  const hasJSON = contentType && contentType.startsWith("application/json")

  switch (true) {
    case response.ok && hasJSON:
      return response.json()
    case response.ok && !hasJSON:
      return response.text()
    case !response.ok && response.status === 403:
      throw authenticationError()
    case !response.ok && response.status === 400:
      const error = hasJSON ? await response.json() : response.text()
      throw badRequestError(error)
    case !response.ok:
      throw badRequestError()
    default:
      console.log("API Service - VerifyResponse : ", response)
  }
}

export { verifyResponse, getDefaultErrorMessage }
