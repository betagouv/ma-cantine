const { signUp } = require("../controllers/sign-up");

exports.register = async function(server) {
  server.route([{
    method: "POST",
    path: "/sign-up",
    handler: signUp
  }]);
};
