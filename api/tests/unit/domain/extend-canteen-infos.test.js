const { extendCanteenInfos } = require('../../../domain/usecases/extend-canteen-infos');

jest.mock('../../../infrastructure/repositories/canteen');
const { updateCanteen } = require('../../../infrastructure/repositories/canteen');

describe('Extend canteen infos', () => {
  it('calls update on the canteen', async () => {
    await extendCanteenInfos("toto");

    expect(updateCanteen).toHaveBeenCalledWith("toto");
  });
});
