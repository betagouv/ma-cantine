// Jasmine cannot spy on a function that isn't a property of an object
// as a result, this wraps the fetch function to allow testing

const fetch = require('node-fetch')

exports.fetch = fetch;