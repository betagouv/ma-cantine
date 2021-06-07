export default {
  notEmpty(input) {
    const errorMessage = "Ce champ ne peut pas être vide"
    if (typeof input === "undefined") return errorMessage
    if (typeof input === "object" && input === null) return errorMessage
    if (typeof input === "boolean") return true
    if (typeof input === "number") return true
    if (typeof input === "string") return input.trim().length > 0 ? true : errorMessage
    if (!input) return errorMessage
    return input.length && input.length > 0 ? true : errorMessage
  },
  positiveNumberOrEmpty(input) {
    if (!input || input.length === 0 || parseFloat(input) === 0) return true
    const errorMessage = "Ce champ doit contenir un nombre positif ou rester vide"
    return errorMessage
  },
  isUrlOrEmpty(input) {
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
  isEmail(input) {
    const errorMessage = "Ce champ doit contenir un email valide"
    if (typeof input === "string" && /\S+@\S+\.\S+/.test(input)) return true
    return errorMessage
  },
  isYear(input) {
    const errorMessage = "Ce champ doit contenir une année (par exemple, 2001)"
    if (typeof input === "string" && /^[12][0-9]{3}$/.test(input.trim())) return true
    return errorMessage
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
}
