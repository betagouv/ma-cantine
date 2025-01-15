const getFields = async (url) => {
  return await fetch(url)
    .then((response) => response.json())
    .then((json) => json.fields)
}

export default { getFields }
