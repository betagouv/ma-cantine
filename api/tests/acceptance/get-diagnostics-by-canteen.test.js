const { init } = require("../../server");
const { Canteen } = require("../../infrastructure/models/canteen");
const { User } = require("../../infrastructure/models/user");
const { createUserWithCanteen } = require('../../infrastructure/repositories/user');
const { generateJwtForUser } = require('../../domain/services/authentication');
const { sequelize } = require("../../infrastructure/postgres-database");
const { Diagnostic } = require("../../infrastructure/models/diagnostic");
const { saveDiagnosticsForCanteen } = require("../../infrastructure/repositories/diagnostic");

describe('Get diagnostics by canteen endpoint /get-diagnostics-by-canteen', () => {
  let server, user;

  beforeAll(async () => {
    server = await init();
    await Diagnostic.sync({ force: true });
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
    await saveDiagnosticsForCanteen(1, [
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
        communicationSupports: [
          "email",
          "display",
          "website",
          "other"
        ],
        communicationSupportLink: "example.com",
        communicateOnFoodPlan: true
      },
      {
        year: 2022,
        valueBio: 1000,
        valueFairTrade: 200,
        valueSustainable: 222,
        valueTotal: 20200
      }
    ]);
  });

  it('gets diagnostic data for associated canteen given valid user', async () => {
    const response = await server.inject({
      method: 'GET',
      url: '/get-diagnostics-by-canteen',
      headers: {
        'Authorization': 'Bearer '+generateJwtForUser(user)
      }
    });
    expect(response.statusCode).toBe(200);
    expect(response.result.previous).toStrictEqual({
      year: 2019,
      valueBio: 50000,
      valueFairTrade: 999,
      valueSustainable: 3333,
      valueTotal: 110000,
      communicateOnFoodPlan: null,
      communicationSupportLink: null,
      communicationSupports: null,
      cookingFoodContainersSubstituted: null,
      disposableUtensilsSubstituted: null,
      hasDonationAgreement: null,
      hasMadeDiversificationPlan: null,
      hasMadeWasteDiagnostic: null,
      hasMadeWastePlan: null,
      serviceFoodContainersSubstituted: null,
      vegetarianFrequency: null,
      vegetarianMenuType: null,
      wasteActions: null,
      waterBottlesSubstituted: null
    });
    expect(response.result.latest).toStrictEqual({
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
      communicationSupports: [
        "email",
        "display",
        "website",
        "other"
      ],
      communicationSupportLink: "example.com",
      communicateOnFoodPlan: true
    });
    expect(response.result.provisionalYear1).toStrictEqual({
      year: 2021,
      valueBio: null,
      valueFairTrade: null,
      valueSustainable: null,
      valueTotal: null,
      communicateOnFoodPlan: false,
      communicationSupportLink: null,
      communicationSupports: [],
      cookingFoodContainersSubstituted: false,
      disposableUtensilsSubstituted: false,
      hasDonationAgreement: false,
      hasMadeDiversificationPlan: false,
      hasMadeWasteDiagnostic: false,
      hasMadeWastePlan: false,
      serviceFoodContainersSubstituted: false,
      vegetarianFrequency: null,
      vegetarianMenuType: null,
      wasteActions: [],
      waterBottlesSubstituted: false
    });
    expect(response.result.provisionalYear2).toStrictEqual({
      year: 2022,
      valueBio: 1000,
      valueFairTrade: 200,
      valueSustainable: 222,
      valueTotal: 20200,
      communicateOnFoodPlan: null,
      communicationSupportLink: null,
      communicationSupports: null,
      cookingFoodContainersSubstituted: null,
      disposableUtensilsSubstituted: null,
      hasDonationAgreement: null,
      hasMadeDiversificationPlan: null,
      hasMadeWasteDiagnostic: null,
      hasMadeWastePlan: null,
      serviceFoodContainersSubstituted: null,
      vegetarianFrequency: null,
      vegetarianMenuType: null,
      wasteActions: null,
      waterBottlesSubstituted: null
    });
  });

  afterAll(async () => {
    await server.stop();
    await sequelize.close();
  });
});