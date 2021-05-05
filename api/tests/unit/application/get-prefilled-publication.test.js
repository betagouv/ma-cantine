const { getPrefilledPublicationHandler } = require('../../../application/routes/get-prefilled-publication');
const { hFake } = require('../../test-helper');

jest.mock('../../../domain/usecases/get-prefilled-publication');
const { getPrefilledPublication } = require('../../../domain/usecases/get-prefilled-publication');

describe('Get prefilled publication handler', () => {
  it('triggers get prefilled publication', async () => {
    const response = await getPrefilledPublicationHandler(
      { auth: { credentials: { user: { canteenId: 3 } } } },
      hFake
    );

    expect(response.statusCode).toBe(200);
    expect(getPrefilledPublication).toHaveBeenCalledWith(3);
  });
});
