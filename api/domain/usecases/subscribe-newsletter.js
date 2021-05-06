const fetch = require('node-fetch');

exports.subscribeNewsletter = async function(email) {
  const requestOptions = {
    method: "POST",
    headers: { "Content-Type": "application/json", "api-key": process.env.SENDINBLUE_API_KEY },
    body: JSON.stringify({
      email,
      listIds: [parseInt(process.env.SENDINBLUE_LIST_ID)],
      updateEnabled: true,
    })
  };

  return fetch("https://api.sendinblue.com/v3/contacts", requestOptions);
}
