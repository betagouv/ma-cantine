import { AuthenticationError, BadRequestError } from "@/utils.js"

// const headers = {
//   "X-CSRFToken": window.CSRF_TOKEN || "",
//   "Content-Type": "application/json",
// }

const verifyResponse = function(response) {
  console.log("in VERIFY RESPONSe")
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

export { verifyResponse }
