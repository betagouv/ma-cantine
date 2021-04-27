const { signUp } = require('../../domain/usecases/sign-up')

jest.mock('../../domain/services/authentication');
const { sendLoginLink } = require('../../domain/services/authentication');

jest.mock('../../infrastructure/repositories/user');
const { createUserWithCanteen } = require('../../infrastructure/repositories/user');
const { DuplicateUserError } = require('../../infrastructure/errors');

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

const loginUrl = "https://example.com/login?token=";

describe('Sign up', () => {
  it('triggers user and canteen creation and sends login link given valid data', async () => {
    createUserWithCanteen.mockReturnValue(user);
    await signUp(user, canteen, loginUrl);
    expect(createUserWithCanteen).toHaveBeenCalledWith(user, canteen);
    expect(sendLoginLink).toHaveBeenCalledWith(user, loginUrl);
  });

  it('triggers login link if user is duplicate', async () => {
    createUserWithCanteen.mockRejectedValue(new DuplicateUserError());
    await signUp(user, canteen, loginUrl);
    expect(createUserWithCanteen).toHaveBeenCalledWith(user, canteen);
    expect(sendLoginLink).toHaveBeenCalledWith(user, loginUrl);
  });

  it('throws if encounters unexpected error', async () => {
    createUserWithCanteen.mockRejectedValue(new Error('Another error'));
    await expect(async () => {
      await signUp(user, canteen, loginUrl);
    }).rejects.toThrow();
    expect(createUserWithCanteen).toHaveBeenCalledWith(user, canteen);
    expect(sendLoginLink).not.toHaveBeenCalled();
  });

  afterEach(() => {
    createUserWithCanteen.mockClear();
    sendLoginLink.mockClear();
  });
});
