const { init } = require("../../server");
const { Canteen } = require("../../infrastructure/models/canteen");
const { User } = require("../../infrastructure/models/user");
const { createUserWithCanteen } = require('../../infrastructure/repositories/user');
const { generateJwtForUser } = require('../../domain/services/authentication');
const { sequelize } = require("../../infrastructure/postgres-database");

describe('Save diagnostic endpoint /save-diagnostics', () => {
  let server, user;

  beforeAll(async () => {
    server = await init();
    await Canteen.sync({ force: true });
    await User.sync({ force: true });
    user = await createUserWithCanteen({
      email: "test@example.com",
      firstName: "Camille",
      lastName: "Dupont",
    }, {
      name: "Test canteen",
      city: "Lyon",
      sector: "school"
    });
  });

  it('saves diagnostic data for associated canteen given valid user', async () => {
    const diagnostics = [
      {
        year: 2019,
        valueBio: 50000,
        valueFairTrade: 999,
        valueSustainable: 3333,
        valueTotal: 110000
      },
      {
        year: 2020,
        valueBio: 40000,
        valueFairTrade: 6000,
        valueSustainable: 10000,
        valueTotal: 98000,
        hasMadeWasteDiagnostic: true,
        hasMadeWastePlan: true,
        wasteActions: [
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
      }
    ];
    const res = await server.inject({
      method: 'POST',
      url: '/save-diagnostics',
      headers: {
        'Authorization': 'Bearer '+generateJwtForUser(user)
      },
      payload: {
        diagnostics
      }
    });
    expect(res.statusCode).toBe(201);
  });

  it('returns 401 given JWT with unknown email', async () => {
    const res = await server.inject({
      method: 'POST',
      url: '/save-diagnostics',
      headers: {
        'Authorization': 'Bearer '+generateJwtForUser({ email: "unknown@email.com" })
      }
    });
    expect(res.statusCode).toBe(401);
  });

  it('returns 400 given bad payload', async () => {
    const baseRequest = {
      method: 'POST',
      url: '/save-diagnostics',
      headers: {
        'Authorization': 'Bearer '+generateJwtForUser(user)
      }
    };
    baseRequest.payload = {};
    const missingDiagnosticsRes = await server.inject(baseRequest);
    expect(missingDiagnosticsRes.statusCode).toBe(400);

    baseRequest.payload = {
      diagnostics: [{
        valueBio: 0
      }]
    };
    const missingYearRes = await server.inject(baseRequest);
    expect(missingYearRes.statusCode).toBe(400);

    baseRequest.payload = {
      diagnostics: [{
        notAKey: "hi"
      }]
    };
    const unexpectedKeyRes = await server.inject(baseRequest);
    expect(unexpectedKeyRes.statusCode).toBe(400);
  });

  afterAll(async () => {
    await server.stop();
    await sequelize.close();
  });
});