const { signUp } = require('../../../../domain/usecases/sign-up')

jest.mock('../../../../domain/services/authentication');
const { sendLoginLink } = require('../../../../domain/services/authentication');

jest.mock('../../../../infrastructure/repositories/user');
const { createUserWithCanteen } = require('../../../../infrastructure/repositories/user');

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

  afterEach(() => {
    createUserWithCanteen.mockClear();
    sendLoginLink.mockClear();
  });
});
