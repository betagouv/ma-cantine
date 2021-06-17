export const timeAgo = (date, displayPrefix = false) => {
  if (typeof date === "string") {
    date = new Date(Date.parse(date))
  }

  let prefix = ""
  if (displayPrefix) {
    prefix = "il y a "
  }

  const seconds = (new Date() - date) / 1000
  if (seconds < 60) {
    return "à l'instant"
  }
  const minutes = Math.round(seconds / 60)
  if (minutes < 60) {
    return `${prefix}${minutes} m`
  }
  const hours = Math.round(seconds / 3600)
  if (hours < 24) {
    return `${prefix}${hours} h`
  }
  const days = Math.round(seconds / 3600 / 24)
  if (days < 7) {
    return `${prefix}${days} j`
  }

  prefix = "le "

  if (days < 120) {
    return prefix + date.toLocaleString("fr-FR", { month: "long", day: "numeric" })
  }
  return prefix + date.toLocaleString("fr-FR", { month: "long", day: "numeric", year: "numeric" })
}
