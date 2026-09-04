const getCanteenId = (url) => {
  return url.split("--")[0]
}

const getCanteenName = (url) => {
  const nameEncoded = url.split("--")[1]
  return decodeURIComponent(nameEncoded)
}

const getCanteenUrl = (canteen) => {
  return encodeURIComponent(`${canteen.id}--${canteen.name}`)
}

export default { getCanteenId, getCanteenName, getCanteenUrl }
