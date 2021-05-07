const { sequelize } = require('../../infrastructure/postgres-database');
const { Canteen } = require('../../infrastructure/models/canteen');
const { createCanteen } = require('../../infrastructure/repositories/canteen');
const { NotFoundError } = require('../../infrastructure/errors');
const { Diagnostic } = require('../../infrastructure/models/diagnostic');
const { saveDiagnosticsForCanteen, getAllDiagnosticsByCanteen } = require('../../infrastructure/repositories/diagnostic');

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
  communicationSupports: [
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

  it('saves multiple diagnostics', async () => {
    await saveDiagnosticsForCanteen(canteen.id, [diagnosticPayload, { year: 2020, valueBio: 6000 }]);

    const allRows = await Diagnostic.findAll();
    expect(allRows.length).toBe(2);
    expect(allRows[0]).toMatchObject(diagnosticPayload);
    expect(allRows[1]).toMatchObject({ canteenId: 1, year: 2020, valueBio: 6000 });
  });

  it('overwrites data given existing canteen id and year combination', async () => {
    await Diagnostic.create({ canteenId: 1, year: 2020, valueBio: 3000, hasDonationAgreement: true });

    await saveDiagnosticsForCanteen(canteen.id, [{ year: 2020, valueBio: 6000 }]);

    const allRows = await Diagnostic.findAll();
    expect(allRows.length).toBe(1);
    expect(allRows[0].valueBio).toBe(6000);
    expect(allRows[0].hasDonationAgreement).toBeNull();
  });

  it('throws error and does not save diagnostics given invalid canteen id', async () => {
    await expect(saveDiagnosticsForCanteen(99, [{ year: 2020 }]))
      .rejects.toThrow(NotFoundError);
    await expect(saveDiagnosticsForCanteen(99, [{ year: 2020 }]))
      .rejects.toThrow(/99/);
    const allRows = await Diagnostic.findAll();
    expect(allRows.length).toEqual(0);
  });

  it('fetches all rows given canteen id', async () => {
    await Diagnostic.create({ ...diagnosticPayload, canteenId: 1 });
    await Diagnostic.create({ year: 2020, valueBio: 1234, canteenId: 1 });

    const allRows = await getAllDiagnosticsByCanteen(1);

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
    await Diagnostic.create({ ...diagnosticPayload, canteenId: 1 });
    await Diagnostic.create({ ...diagnosticPayload, canteenId: 2 });

    const allRows = await getAllDiagnosticsByCanteen(secondCanteen.id);

    expect(allRows.length).toEqual(1);
    expect(allRows[0].canteenId).toEqual(secondCanteen.id);
  });

  afterAll(async () => {
    await sequelize.close();
  });
});
