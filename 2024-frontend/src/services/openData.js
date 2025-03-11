const apiAdresse = "https://api-adresse.data.gouv.fr/search/"

const findCities = (name) => {
  return fetch(`${apiAdresse}?q=${name}&type=municipality&autocomplete=1&limit=10`)
    .then((response) => response.json())
    .catch((error) => {
      console.log(error)
    })
}

export default { findCities }
