const createCopy = (array) => {
  return JSON.parse(JSON.stringify(array))
}

export default { createCopy }
