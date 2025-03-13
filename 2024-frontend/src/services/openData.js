const apiGeo = "https://geo.api.gouv.fr/"

const findCitiesFromPostalCode = (postcode) => {
  return fetch(`${apiGeo}communes?codePostal=${postcode}`)
    .then((response) => response.json())
    .catch((error) => error)
}

export default { findCitiesFromPostalCode }
