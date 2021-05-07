require('dotenv').config();
const { generateJwtForUser } = require("../../../domain/services/authentication");

jest.mock('@hapi/jwt');
const Jwt = require('@hapi/jwt');

describe('Authentication service', () => {
  it('uses user email and secret key to generate JWT', () => {
    const mockedToken = "xxx.yyy.zzz";
    Jwt.token.generate.mockReturnValue(mockedToken);
    const email = "example@test.com";
    const jwt = generateJwtForUser({
      id: 5,
      email
    });
    expect(Jwt.token.generate).toHaveBeenCalledWith({ email }, process.env.JWT_SECRET_KEY);
    expect(jwt).toBe(mockedToken);
  });

  // TODO: test send login link

  // TODO: test send sign up link
});