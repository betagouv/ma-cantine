const { saveDiagnosticsHandler } = require('../../../application/routes/save-diagnostics');

const { hFake } = require('../../test-helper');

jest.mock('../../../domain/usecases/save-diagnostics');
const { saveDiagnosticsForUser } = require('../../../domain/usecases/save-diagnostics');

const diagnostics = [
  {
    year: 2019,
    valueTotal: 110000
  },
  {
    year: 2020,
    hasMadeWastePlan: false
  }
];

describe('Save diagnostic handler', () => {
  it('calls save diagnostic usecase with diagnostic in payload', async () => {
    const user = { email: "test@example.com" };
    const request = {
      auth: { credentials: { user: user } },
      payload: { diagnostics }
    };
    const res = await saveDiagnosticsHandler(request, hFake);
    expect(res.statusCode).toBe(201);
    expect(saveDiagnosticsForUser).toHaveBeenCalledWith(user, diagnostics);
  });
});