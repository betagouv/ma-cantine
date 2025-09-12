const getCanteenId = (url) => {
  return url.split("--")[0]
}

const getCanteenName = (url) => {
  return url.split("--")[1]
}

const getCanteenUrl = (canteen) => {
  return `${canteen.id}--${canteen.name}`
}

export default { getCanteenId, getCanteenName, getCanteenUrl }
