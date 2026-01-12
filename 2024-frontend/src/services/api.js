const getDefaultErrorMessage = () => 'Une erreur est survenue, vous pouvez réessayer plus tard ou nous contacter directement à support-egalim@beta.gouv.fr'

const authenticationError = () => {
  return {
    status: "error",
    name: "AuthenticationError",
    title: "Votre session a expirée",
    message: "Rechargez la page et reconnectez-vous pour continuer.",
  }
}

const badRequestError = (error) => {
  const list = getErrorList(error)
  const message = list.map(error => error.message).join(". ")

  return {
    status: "error",
    name: "BadRequestError",
    list,
    message,
  }
}

const getErrorList = (error) => {
  let errorList = []

  const isNull = !error
  const isArray = Array.isArray(error)
  const isString = typeof error === "string"
  const isObject = typeof error === "object"

  if(isNull) errorList = [getDefaultErrorMessage()]
  else if (isString) errorList = [error]
  else if (isArray) errorList = error
  else if (isObject) {
    const keys = Object.keys(error)
    keys.forEach(key => {
      errorList.push({
        field: key,
        message: error[key],
      })
    })
  }

  return errorList
}

const verifyResponse = async (response) => {
  const contentType = response.headers.get("content-type")
  const hasJSON = contentType && contentType.startsWith("application/json")
  let error = null

  switch (true) {
    case response.ok && hasJSON:
      return response.json()
    case response.ok && !hasJSON:
      return response.text()
    case !response.ok && response.status === 403:
      throw authenticationError()
    case !response.ok && response.status === 400:
      error = hasJSON ? await response.json() : response.text()
      throw badRequestError(error)
    case !response.ok:
      throw badRequestError()
    default:
      console.log("API Service - VerifyResponse : ", response)
  }
}

export { verifyResponse, getDefaultErrorMessage }
