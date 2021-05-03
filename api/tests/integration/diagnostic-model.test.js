const { sequelize } = require('../../infrastructure/postgres-database');
const { Canteen } = require('../../infrastructure/models/canteen');
const { createCanteen } = require('../../infrastructure/repositories/canteen');
const { NotFoundError } = require('../../infrastructure/errors');
const { Diagnostic } = require('../../infrastructure/models/diagnostic');
const { saveDiagnosticForCanteen, getResultsByCanteen } = require('../../infrastructure/repositories/diagnostic');

const diagnosticPayload = {
  year: 2019,
  valueBio: 50000,
  valueFairTrade: 999,
  valueSustainable: 3333,
  valueTotal: 110000,
  hasMadeWasteDiagnostic: true,
  hasMadeWastePlan: true,
  wasteActions:  [
    "raiseAwareness",
    "portionSize",
    "preRegistration",
    "training",
    "reorganization",
    "reuse"
  ],
  hasDonationAgreement: true,
  hasMadeDiversificationPlan: true,
  vegetarianFrequency: "once",
  vegetarianMenuType: "standalone",
  cookingFoodContainersSubstituted: true,
  serviceFoodContainersSubstituted: true,
  waterBottlesSubstituted: true,
  disposableUtensilsSubstituted: true,
  communicationSupport: [
    "email",
    "display",
    "website",
    "other"
  ],
  communicationSupportLink: "example.com",
  communicateOnFoodPlan: true
};

describe('Diagnostic results model', () => {
  let canteen;

  beforeAll(async () => {
    await Canteen.sync({ force: true });
    // test data
    canteen = (await createCanteen({
      name: "Test canteen",
      city: "Lyon",
      sector: "school"
    }));
  });

  beforeEach(async () => {
    await Diagnostic.sync({ force: true });
  });

  it('successfully adds one row of diagnostic results', async () => {
    const createdResult = await saveDiagnosticForCanteen(diagnosticPayload, canteen.id);
    const persistedResult = await Diagnostic.findOne({
      where: {
        canteenId: canteen.id,
        year: 2019
      }
    });
    expect(persistedResult.toJSON()).toMatchObject({
      ...diagnosticPayload,
      canteenId: canteen.id
    });
    expect(createdResult.toJSON()).toStrictEqual(persistedResult.toJSON());
  });

  it('updates data given existing canteen id and year combination', async () => {
    await saveDiagnosticForCanteen(diagnosticPayload, canteen.id);
    await saveDiagnosticForCanteen({
      year: 2019,
      valueBio: 1234
    }, canteen.id);
    const persistedResult = await Diagnostic.findOne({
      where: {
        canteenId: canteen.id,
        year: 2019
      }
    });
    expect(persistedResult.valueBio).not.toEqual(diagnosticPayload.valueBio);
    expect(persistedResult.valueBio).toEqual(1234);
    expect(persistedResult.valueSustainable).toEqual(diagnosticPayload.valueSustainable);
  });

  it('throws error and does not save data given invalid canteen id', async () => {
    await expect(saveDiagnosticForCanteen(diagnosticPayload, 99))
      .rejects.toThrow(NotFoundError);
    await expect(saveDiagnosticForCanteen(diagnosticPayload, 99))
      .rejects.toThrow(/99/);
    const allRows = await Diagnostic.findAll();
    expect(allRows.length).toEqual(0);
  });

  it('fetches all rows given canteen id', async () => {
    await saveDiagnosticForCanteen(diagnosticPayload, canteen.id);
    await saveDiagnosticForCanteen({
      ...diagnosticPayload,
      year: 2020,
      valueBio: 1234
    }, canteen.id);
    const allRows = await getResultsByCanteen(canteen.id);
    expect(allRows.length).toEqual(2);
    expect(allRows[0].valueBio).toEqual(diagnosticPayload.valueBio);
    expect(allRows[1].valueBio).toEqual(1234);
  });

  it('only returns rows for given canteen id', async () => {
    const secondCanteen = await createCanteen({
      name: "Second canteen",
      city: "Paris",
      sector: "other"
    });
    await saveDiagnosticForCanteen(diagnosticPayload, canteen.id);
    await saveDiagnosticForCanteen(diagnosticPayload, secondCanteen.id);
    const allRows = await getResultsByCanteen(secondCanteen.id);
    expect(allRows.length).toEqual(1);
    expect(allRows[0].canteenId).toEqual(secondCanteen.id);
  });

  it('throws error if no rows for given canteen id', async () => {
    await expect(getResultsByCanteen(canteen.id)).rejects.toThrow(NotFoundError);
    await expect(getResultsByCanteen(canteen.id)).rejects.toThrow(/1/);
  });

  afterAll(async () => {
    await sequelize.close();
  });
});
