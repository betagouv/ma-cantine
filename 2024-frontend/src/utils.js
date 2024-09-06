// this function takes vuelidate error messages and concatenates them
export const formatError = (data) => {
  return data.$errors.map((e) => e.$message).join(" ")
}

export class AuthenticationError extends Error {
  constructor(...params) {
    super(...params)
    // Maintains proper stack trace for where our error was thrown (only available on V8)
    if (Error.captureStackTrace) {
      Error.captureStackTrace(this, AuthenticationError)
    }
    this.name = "AuthenticationError"
  }
}

export class BadRequestError extends Error {
  constructor(jsonPromise, ...params) {
    super(...params)
    // Maintains proper stack trace for where our error was thrown (only available on V8)
    if (Error.captureStackTrace) {
      Error.captureStackTrace(this, BadRequestError)
    }
    this.name = "BadRequestError"
    this.jsonPromise = jsonPromise
  }
}
