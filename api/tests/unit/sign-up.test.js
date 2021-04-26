const { signUp } = require('../../domain/usecases/sign-up')

jest.mock('../../domain/services/initiate-login', () => ({
  initiateMagicLinkLogin: jest.fn()
}));
const { initiateMagicLinkLogin } = require('../../domain/services/initiate-login');

jest.mock('../../infrastructure/repositories/user', () => {
  const origin = jest.requireActual('../../infrastructure/repositories/user');
  return {
    ...origin,
    createUserWithCanteen: jest.fn()
  };
});
const { createUserWithCanteen, DuplicateUserError } = require('../../infrastructure/repositories/user');

const canteen = {
  name: "Test canteen",
  city: "Lyon",
  sector: "school"
};

const user = {
  email: "test@example.com",
  firstName: "Camille",
  lastName: "Dupont",
};

describe('Sign up', () => {
  it('triggers user and canteen creation and sends login link given valid data', async () => {
    createUserWithCanteen.mockReturnValue(user);
    await signUp(user, canteen);
    expect(createUserWithCanteen).toHaveBeenCalledWith(user, canteen);
    expect(initiateMagicLinkLogin).toHaveBeenCalledWith(user.email);
  });

  it('triggers login link if user is duplicate', async () => {
    createUserWithCanteen.mockRejectedValue(new DuplicateUserError());
    await signUp(user, canteen);
    expect(createUserWithCanteen).toHaveBeenCalledWith(user, canteen);
    expect(initiateMagicLinkLogin).toHaveBeenCalledWith(user.email);
  });

  it('throws if encounters unexpected error', async () => {
    createUserWithCanteen.mockRejectedValue(new Error('Another error'));
    await expect(async () => {
      await signUp(user, canteen);
    }).rejects.toThrow();
    expect(createUserWithCanteen).toHaveBeenCalledWith(user, canteen);
    expect(initiateMagicLinkLogin).not.toHaveBeenCalled();
  });

  afterEach(() => {
    createUserWithCanteen.mockClear();
    initiateMagicLinkLogin.mockClear();
  });
});
