const apiGeo = "https://geo.api.gouv.fr/"

const findCitiesFromPostalCode = (postcode) => {
  return fetch(`${apiGeo}communes?codePostal=${postcode}`)
    .then((response) => response.json())
    .catch((error) => error)
}

const findCitiesWithNameAutocompletion = (name) => {
  return fetch(`${apiGeo}communes?nom=${name}&limit=10`)
    .then((response) => response.json())
    .catch((error) => error)
}

export default { findCitiesFromPostalCode, findCitiesWithNameAutocompletion }
