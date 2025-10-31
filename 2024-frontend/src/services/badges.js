import badges from "@/data/badges.json"

const getFromAction = (name) => {
  const index = badges.canteen.findIndex((badge) => badge.actions.includes(name))
  return badges.canteen[index]
}

export default { getFromAction }
