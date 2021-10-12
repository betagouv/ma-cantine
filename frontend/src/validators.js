function email(input) {
  const errorMessage = "Ce champ doit contenir un email valide"
  if (typeof input === "string" && /\S+@\S+\.\S+/.test(input)) return true
  return errorMessage
}

export default {
  required(input) {
    const errorMessage = "Ce champ ne peut pas être vide"
    if (typeof input === "undefined") return errorMessage
    if (typeof input === "object") {
      if (input === null) return errorMessage
      return Object.keys(input).length > 0 ? true : errorMessage
    }
    if (typeof input === "boolean") return true
    if (typeof input === "number") return true
    if (typeof input === "string") return input.trim().length > 0 ? true : errorMessage
    if (!input) return errorMessage
    return input.length && input.length > 0 ? true : errorMessage
  },
  checked(input) {
    const errorMessage = "Ce champ doit être accepté"
    const isChecked = typeof input === "boolean" && input === true
    return isChecked ? true : errorMessage
  },
  greaterThanZero(input) {
    const errorMessage = "Ce champ doit contenir une chiffre supérieure à zéro"
    if (parseFloat(input) > 0) return true
    return errorMessage
  },
  nonNegativeOrEmpty(input) {
    const isEmpty = !input || input.length === 0
    if (isEmpty) return true

    const isNonNegative = parseFloat(input) >= 0
    if (isNonNegative) return true

    const errorMessage = "Ce champ doit contenir un nombre positif ou rester vide"
    return errorMessage
  },
  lteOrEmpty(max) {
    return (input) => {
      if (!input || input <= max) return true
      return `Le nombre saisi ne peut pas dépasser ${max}`
    }
  },
  urlOrEmpty(input) {
    if (!input || input.length === 0) return true
    let url
    const errorMessage = 'Le lien doit être une URL valide (par ex. "https://exemple.com")'
    try {
      url = new URL(input)
    } catch (_) {
      return errorMessage
    }
    const isValid = url.protocol === "http:" || url.protocol === "https:"
    return isValid ? true : errorMessage
  },
  email(input) {
    return email(input)
  },
  emailOrEmpty(input) {
    return input ? email(input) : true
  },
  maxCharsXPName(input) {
    if (!input) return true
    return input.length <= 70 || "Ce champ ne doit pas dépasser les 70 caractères"
  },
  maxSelected(maxNumer) {
    return (input) => {
      if (!input || input.length <= maxNumer) return true
      return `Vous pouvez sélectionner jusqu'à ${maxNumer} élements`
    }
  },
  length(exactLength) {
    return (input) => {
      if (!input || input.length !== exactLength) {
        return `${exactLength} caractères attendus`
      } else return true
    }
  },
  luhn(input) {
    if (!input) return true
    const reversed = input.split("").reverse()
    let checksum = 0
    let error = false
    reversed.forEach((char, idx) => {
      const num = parseInt(char, 10)
      if (isNaN(num)) {
        error = true
      } else if (idx % 2) {
        const double = num * 2
        if (double < 10) {
          checksum += double
        } else {
          checksum += double - 10 + 1
        }
      } else {
        checksum += num
      }
    })
    error = error || checksum % 10
    return error ? "Le numéro SIRET n'est pas valide" : true
  },
  gteSum(values, message) {
    return (input) => {
      let sum = 0
      values.forEach((v) => {
        if (v) sum += Number(v)
      })
      message = message || "Cette valeur doit être plus haute ou égale au somme"
      return input < sum ? message : true
    }
  },
}
