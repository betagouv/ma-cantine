import Vuex from "vuex"
import VueRouter from "vue-router"
import Vuetify from "vuetify"
import { shallowMount, createLocalVue } from "@vue/test-utils"
import PublishedCanteenCard from "@/views/CanteensPage/PublishedCanteenCard"

const localVue = createLocalVue()
localVue.use(VueRouter)

describe("PublishedCanteenCard.vue", () => {
  let vuetify
  let testDiagnostics = [
    {
      id: 1,
      year: 2021,
      valueBioHt: 5000,
      valueSustainableHt: 2000,
      valuePatHt: 1000,
      valueTotalHt: 10000,
      cookingPlasticSubstituted: true,
      servingPlasticSubstituted: true,
      plasticBottlesSubstituted: true,
      plasticTablewareSubstituted: true,
      communicatesOnFoodQuality: true,
    },
  ]
  let testCanteen = {
    id: 1,
    name: "Wasabi",
    city: "Lyon",
    sectors: [1, 3],
    dailyMealCount: 100,
    diagnostics: testDiagnostics,
  }

  let sectors = [
    { id: 1, name: "Scolaire" },
    { id: 2, name: "Admin" },
    { id: 3, name: "Autre" },
  ]

  let store = new Vuex.Store({
    state: { sectors },
    getters: {
      getCanteenUrlComponent: () => () => "1-Wasabi",
    },
  })

  beforeEach(() => {
    vuetify = new Vuetify()
  })

  it("Includes the name of the canteen", () => {
    const wrapper = shallowMount(PublishedCanteenCard, {
      localVue,
      propsData: { canteen: testCanteen },
      vuetify,
      store,
    })
    expect(wrapper.find("v-card-title-stub").text()).toBe(testCanteen.name)
  })

  it("Includes canteen indicators", () => {
    const wrapper = shallowMount(PublishedCanteenCard, {
      localVue,
      propsData: { canteen: testCanteen },
      vuetify,
      store,
    })
    expect(wrapper.find("canteenindicators-stub").exists()).toBe(true)
  })

  it("Includes enabled appro badge", () => {
    const wrapper = shallowMount(PublishedCanteenCard, {
      localVue,
      propsData: { canteen: testCanteen },
      vuetify,
      store,
    })
    expect(wrapper.find('v-img-stub[src="/static/images/badges/appro.svg"]').exists()).toBe(true)
    expect(wrapper.find('v-img-stub[src="/static/images/badges/appro-disabled.svg"]').exists()).toBe(false)
  })

  it("Includes disabled waste badge", () => {
    const wrapper = shallowMount(PublishedCanteenCard, {
      localVue,
      propsData: { canteen: testCanteen },
      vuetify,
      store,
    })
    expect(wrapper.find('v-img-stub[src="/static/images/badges/waste.svg"]').exists()).toBe(false)
    expect(wrapper.find('v-img-stub[src="/static/images/badges/waste-disabled.svg"]').exists()).toBe(true)
  })

  it("Includes enabled plastic badge", () => {
    const wrapper = shallowMount(PublishedCanteenCard, {
      localVue,
      propsData: { canteen: testCanteen },
      vuetify,
      store,
    })
    expect(wrapper.find('v-img-stub[src="/static/images/badges/plastic.svg"]').exists()).toBe(true)
    expect(wrapper.find('v-img-stub[src="/static/images/badges/plastic-disabled.svg"]').exists()).toBe(false)
  })

  it("Includes disabled diversification badge", () => {
    const wrapper = shallowMount(PublishedCanteenCard, {
      localVue,
      propsData: { canteen: testCanteen },
      vuetify,
      store,
    })
    expect(wrapper.find('v-img-stub[src="/static/images/badges/diversification.svg"]').exists()).toBe(false)
    expect(wrapper.find('v-img-stub[src="/static/images/badges/diversification-disabled.svg"]').exists()).toBe(true)
  })

  it("Includes enabled information badge", () => {
    const wrapper = shallowMount(PublishedCanteenCard, {
      localVue,
      propsData: { canteen: testCanteen },
      vuetify,
      store,
    })
    expect(wrapper.find('v-img-stub[src="/static/images/badges/info.svg"]').exists()).toBe(true)
    expect(wrapper.find('v-img-stub[src="/static/images/badges/info-disabled.svg"]').exists()).toBe(false)
  })
})
