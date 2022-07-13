import { badges } from "@/utils"

describe("PublishedCanteenCard.vue", () => {
  let sectors = [
    { id: 1, name: "Scolaire", category: "education" },
    { id: 2, name: "Admin" },
    { id: 3, name: "Autre" },
  ]

  it("Appro badge earned", () => {
    let testCanteen = {
      sectors: [],
    }
    let testDiagnostic = {
      id: 1,
      valueBioHt: 5000,
      valuSiqoHt: 2000,
      valueTotalHt: 10000,
    }
    let canteenBadges = badges(testCanteen, testDiagnostic, sectors)
    expect(canteenBadges.appro.earned).toBe(true)
  })

  it("Appro badge not earned", () => {
    let testCanteen = {
      sectors: [],
    }
    let testDiagnostic = {
      id: 1,
      valueBioHt: 0,
      valuSiqoHt: 0,
      valueTotalHt: 10000,
    }
    let canteenBadges = badges(testCanteen, testDiagnostic, sectors)
    expect(canteenBadges.appro.earned).toBe(undefined)
  })

  it("Waste badge earned", () => {
    let testCanteen = {
      sectors: [],
      dailyMealCount: 2999,
    }
    let testDiagnostic = {
      id: 1,
      hasWasteDiagnostic: true,
      wasteActions: ["TEST"],
    }
    let canteenBadges = badges(testCanteen, testDiagnostic, sectors)
    expect(canteenBadges.waste.earned).toBe(true)
    testDiagnostic = {
      id: 1,
      hasWasteDiagnostic: true,
      wasteActions: ["TEST"],
      hasDonationAgreement: true,
    }
    testCanteen = {
      sectors: [],
      dailyMealCount: 3000,
    }
    canteenBadges = badges(testCanteen, testDiagnostic, sectors)
    expect(canteenBadges.waste.earned).toBe(true)
  })

  it("Waste badge not earned", () => {
    let testCanteen = {
      sectors: [],
      dailyMealCount: 20,
    }
    let testDiagnostic = {
      id: 1,
      hasWasteDiagnostic: false,
      wasteActions: ["TEST"],
    }
    let canteenBadges = badges(testCanteen, testDiagnostic, sectors)
    expect(canteenBadges.waste.earned).toBe(undefined)
    testDiagnostic = {
      id: 1,
      hasWasteDiagnostic: true,
      wasteActions: [],
    }
    canteenBadges = badges(testCanteen, testDiagnostic, sectors)
    expect(canteenBadges.waste.earned).toBe(undefined)
    testCanteen.dailyMealCount = 4000
    testDiagnostic = {
      id: 1,
      hasWasteDiagnostic: true,
      wasteActions: ["TEST"],
      hasDonationAgreement: false,
    }
    canteenBadges = badges(testCanteen, testDiagnostic, sectors)
    expect(canteenBadges.waste.earned).toBe(undefined)
  })

  it("Diversification badge earned - scolaire", () => {
    let testCanteen = {
      sectors: [1, 2],
    }
    let testDiagnostic = {
      id: 1,
      vegetarianWeeklyRecurrence: "MID",
    }
    let canteenBadges = badges(testCanteen, testDiagnostic, sectors)
    expect(canteenBadges.diversification.earned).toBe(true)
    testDiagnostic = {
      id: 1,
      vegetarianWeeklyRecurrence: "HIGH",
    }
    canteenBadges = badges(testCanteen, testDiagnostic, sectors)
    expect(canteenBadges.diversification.earned).toBe(true)
    testDiagnostic = {
      id: 1,
      vegetarianWeeklyRecurrence: "DAILY",
    }
    canteenBadges = badges(testCanteen, testDiagnostic, sectors)
    expect(canteenBadges.diversification.earned).toBe(true)
  })

  it("Diversification badge not earned - scolaire", () => {
    let testCanteen = {
      sectors: [1, 2],
    }
    let testDiagnostic = {
      id: 1,
      vegetarianWeeklyRecurrence: "LOW",
    }
    let canteenBadges = badges(testCanteen, testDiagnostic, sectors)
    expect(canteenBadges.diversification.earned).toBe(undefined)
    testDiagnostic = {
      id: 1,
    }
    canteenBadges = badges(testCanteen, testDiagnostic, sectors)
    expect(canteenBadges.diversification.earned).toBe(undefined)
  })

  it("Diversification badge earned - all other sectors", () => {
    let testCanteen = {
      sectors: [2, 3],
    }
    let testDiagnostic = {
      id: 1,
      vegetarianWeeklyRecurrence: "DAILY",
    }
    let canteenBadges = badges(testCanteen, testDiagnostic, sectors)
    expect(canteenBadges.diversification.earned).toBe(true)
  })

  it("Diversification badge not earned - all other sectors", () => {
    let testCanteen = {
      sectors: [2, 3],
    }
    let testDiagnostic = {
      id: 1,
      vegetarianWeeklyRecurrence: "LOW",
    }
    let canteenBadges = badges(testCanteen, testDiagnostic, sectors)
    expect(canteenBadges.diversification.earned).toBe(undefined)
    testDiagnostic = {
      id: 1,
      vegetarianWeeklyRecurrence: "MID",
    }
    canteenBadges = badges(testCanteen, testDiagnostic, sectors)
    expect(canteenBadges.diversification.earned).toBe(undefined)
    testDiagnostic = {
      id: 1,
      vegetarianWeeklyRecurrence: "HIGH",
    }
    canteenBadges = badges(testCanteen, testDiagnostic, sectors)
    expect(canteenBadges.diversification.earned).toBe(undefined)
    testDiagnostic = {
      id: 1,
    }
    canteenBadges = badges(testCanteen, testDiagnostic, sectors)
    expect(canteenBadges.diversification.earned).toBe(undefined)
  })

  it("Info badge earned", () => {
    let testCanteen = {
      sectors: [],
    }
    let testDiagnostic = {
      id: 1,
      communicatesOnFoodQuality: true,
    }
    let canteenBadges = badges(testCanteen, testDiagnostic, sectors)
    expect(canteenBadges.info.earned).toBe(true)
  })

  it("Info badge not earned", () => {
    let testCanteen = {
      sectors: [],
    }
    let testDiagnostic = {
      id: 1,
    }
    let canteenBadges = badges(testCanteen, testDiagnostic, sectors)
    expect(canteenBadges.info.earned).toBe(undefined)
  })
})
