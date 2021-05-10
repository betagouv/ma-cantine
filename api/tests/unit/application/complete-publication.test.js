const { completePublicationHandler } = require('../../../application/routes/complete-publication');
const { hFake } = require('../../test-helper');

jest.mock('../../../domain/usecases/complete-publication');
const { completePublication } = require('../../../domain/usecases/complete-publication');

describe('Complete publication handler', () => {
  it('triggers extend complete publication', async () => {
    const response = await completePublicationHandler(
      {
        auth: { credentials: { user: { canteenId: 3 } } },
        payload: {
          makeDataPublic: true
        }
      },
      hFake
    );

    expect(response.statusCode).toBe(204);
    expect(completePublication).toHaveBeenCalledWith(3, true);
  });
});
