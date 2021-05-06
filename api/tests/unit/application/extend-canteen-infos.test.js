const { extendCanteenInfosHandler } = require('../../../application/routes/extend-canteen-infos');
const { hFake } = require('../../test-helper');

jest.mock('../../../domain/usecases/extend-canteen-infos');
const { extendCanteenInfos } = require('../../../domain/usecases/extend-canteen-infos');

describe('Extend canteen infos handler', () => {
  it('triggers extend canteen infos', async () => {
    const response = await extendCanteenInfosHandler(
      {
        auth: { credentials: { user: { canteenId: 3 } } },
        payload: {
          name: "Poudlard",
          city: "Toulouse",
          sector: "scolaire",
        }
      },
      hFake
    );

    expect(response.statusCode).toBe(204);
    expect(extendCanteenInfos).toHaveBeenCalledWith({
      id: 3,
      name: "Poudlard",
      city: "Toulouse",
      sector: "scolaire",
    });
  });
});
