// À supprimer ensuite du store
import { AuthenticationError, BadRequestError } from "@/utils.js"

const verifyResponse = function(response) {
  const contentType = response.headers.get("content-type")
  const hasJSON = contentType && contentType.startsWith("application/json")

  if (response.status < 200 || response.status >= 400) {
    if (response.status === 403) throw new AuthenticationError()
    else if (response.status === 400) {
      if (hasJSON) {
        throw new BadRequestError(response.json())
      } else {
        throw new BadRequestError()
      }
    } else throw new Error(`API responded with status of ${response.status}`)
  }

  return hasJSON ? response.json() : response.text()
}

const getServerError = (error) => {
  if (error instanceof BadRequestError) {
    return error.jsonPromise
      .then((errorDetail) => {
        const keys = Object.keys(errorDetail)
        const errors = []
        console.log(keys)
        keys.forEach((key) => {
          errors.push({
            name: key,
            message: errorDetail[key],
          })
        })
        return errors
      })
      .catch((e) => e)
  }
}

export { verifyResponse, getServerError }
