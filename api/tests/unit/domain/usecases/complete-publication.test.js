const { completePublication } = require('../../../../domain/usecases/complete-publication');

jest.mock('../../../../infrastructure/repositories/canteen');
const { updateCanteen } = require('../../../../infrastructure/repositories/canteen');

describe('Extend canteen infos', () => {
  it('completes the publication process for a canteen', async () => {
    await completePublication(420, true);

    expect(updateCanteen).toHaveBeenCalledWith({
      id: 420,
      hasPublished: true,
      dataIsPublic: true,
    });
  });
});
