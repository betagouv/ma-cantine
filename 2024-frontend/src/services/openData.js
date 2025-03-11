const apiGeo = "https://geo.api.gouv.fr/"

const getCities = (postcode) => {
  return fetch(`${apiGeo}communes?codePostal=${postcode}`)
    .then((response) => response.json())
    .catch((error) => error)
}

export default { getCities }
