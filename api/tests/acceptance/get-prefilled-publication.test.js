const { init } = require("../../server");
const { Canteen } = require("../../infrastructure/models/canteen");
const { Diagnostic } = require("../../infrastructure/models/diagnostic");
const { User } = require("../../infrastructure/models/user");
const { createUserWithCanteen } = require('../../infrastructure/repositories/user');
const { saveDiagnosticsForCanteen } = require('../../infrastructure/repositories/diagnostic');
const { generateJwtForUser } = require('../../domain/services/authentication');
const { sequelize } = require("../../infrastructure/postgres-database");

describe('Get prefilled publication endpoint /get-prefilled-publication', () => {
  let server, user;

  beforeAll(async () => {
    server = await init();
    await Diagnostic.sync({ force: true });
    await Canteen.sync({ force: true });
    await User.sync({ force: true });

    user = await createUserWithCanteen({
      email: "test@example.fr",
      firstName: "Camille",
      lastName: "Dupont",
    }, {
      name: "Test canteen",
      city: "Lyon",
      sector: "school",
      mealCount: 150,
    });

    await saveDiagnosticsForCanteen(user.canteenId, [{
      year: 2020,
      valueBio: 40000,
      valueFairTrade: 6000,
      valueSustainable: 10000,
      valueTotal: 98000,
      hasMadeWasteDiagnostic: true,
      hasMadeWastePlan: true,
      wasteActions: ["training"],
      hasDonationAgreement: true,
      hasMadeDiversificationPlan: true,
      vegetarianFrequency: "once",
      vegetarianMenuType: "standalone",
      cookingFoodContainersSubstituted: true,
      serviceFoodContainersSubstituted: true,
      waterBottlesSubstituted: true,
      disposableUtensilsSubstituted: true,
      communicationSupports: ["email"],
      communicationSupportLink: "example.com",
      communicateOnFoodPlan: true
    }]);
  });

  it('get prefilled publication for user\'s canteen', async () => {
    const response = await server.inject({
      method: 'GET',
      url: '/get-prefilled-publication',
      headers: {
        'Authorization': 'Bearer ' + generateJwtForUser(user)
      },
    });

    expect(response.statusCode).toBe(200);
    expect(response.result).toStrictEqual({
      canteen: {
        name: "Test canteen",
        city: "Lyon",
        sector: "school",
        mealCount: 150,
      },
      diagnostics: {
        latest: {
          year: 2020,
          valueBio: 40000,
          valueFairTrade: 6000,
          valueSustainable: 10000,
          valueTotal: 98000,
          hasMadeWasteDiagnostic: true,
          hasMadeWastePlan: true,
          wasteActions: ["training"],
          hasDonationAgreement: true,
          hasMadeDiversificationPlan: true,
          vegetarianFrequency: "once",
          vegetarianMenuType: "standalone",
          cookingFoodContainersSubstituted: true,
          serviceFoodContainersSubstituted: true,
          waterBottlesSubstituted: true,
          disposableUtensilsSubstituted: true,
          communicationSupports: ["email"],
          communicationSupportLink: "example.com",
          communicateOnFoodPlan: true
        },
        previous: {
          year: 2019,
          valueBio: null,
          valueFairTrade: null,
          valueSustainable: null,
          valueTotal: null,
          hasMadeWasteDiagnostic: false,
          hasMadeWastePlan: false,
          wasteActions: [],
          hasDonationAgreement: false,
          hasMadeDiversificationPlan: false,
          vegetarianFrequency: null,
          vegetarianMenuType: null,
          cookingFoodContainersSubstituted: false,
          serviceFoodContainersSubstituted: false,
          waterBottlesSubstituted: false,
          disposableUtensilsSubstituted: false,
          communicationSupports: [],
          communicationSupportLink: null,
          communicateOnFoodPlan: false,
        }
      }
    });
  });

  afterAll(async () => {
    await server.stop();
    await sequelize.close();
  });
});
