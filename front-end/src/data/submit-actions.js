const api_url = process.env.VUE_APP_API_URL || 'http://localhost:3000';
const login_url = `${process.env.VUE_APP_SITE_URL || "http://localhost:8080"}/connexion?token=`;

function extendCanteenInfo(canteen) {
  return authenticatedPost("extend-canteen-infos", canteen);
}

function completePublication(makeDataPublic) {
  return authenticatedPost("complete-publication", { makeDataPublic });
}

function saveDiagnosticsOnServer(diagnostics) {
  return authenticatedPost("save-diagnostics", { diagnostics });
}

function signUp(user, canteen) {
  return unauthenticatedPost("sign-up", { user, canteen, loginUrl: login_url });
}

function login(email) {
  return unauthenticatedPost("login", { email, loginUrl: login_url });
}

function completeLogin(token, diagnostics) {
  return unauthenticatedPost("complete-login", { token, diagnostics });
}

function subscribeNewsletter(email) {
  return unauthenticatedPost("subscribe-newsletter", { email });
}

function subscribeBetaTester(betaTester) {
  return unauthenticatedPost("subscribe-beta-tester", betaTester);
}

function authenticatedPost(route, body) {
  return post(route, body, true);
}

function unauthenticatedPost(route, body) {
  return post(route, body, false);
}

async function post(route, body, withAuthentication) {
  let headers = {
    'Content-Type': 'application/json',
  };
  if (withAuthentication) {
    headers['Authorization'] = 'Bearer ' + localStorage.getItem('jwt');
  }

  const response = await fetch(`${api_url}/${route}`, {
    method: "POST",
    headers,
    body: JSON.stringify(body),
  });

  if (response.status === 401) {
    localStorage.removeItem('jwt');
    location.reload();
  }

  return response;
}

export {
  extendCanteenInfo,
  completePublication,
  saveDiagnosticsOnServer,
  signUp,
  login,
  completeLogin,
  subscribeNewsletter,
  subscribeBetaTester,
};
