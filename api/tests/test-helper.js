exports.hFake = {
  response(json) {
    this.result = json;
    return this;
  },
  code(number) {
    this.statusCode = number;
    return this;
  }
};