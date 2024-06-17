import Vuex from "vuex"
import VueRouter from "vue-router"
import Vuetify from "vuetify"
import { shallowMount, createLocalVue } from "@vue/test-utils"
import PublishedCanteenCard from "@/views/CanteensPage/PublishedCanteenCard"

const localVue = createLocalVue()
localVue.use(VueRouter)

describe("PublishedCanteenCard.vue", () => {
  let vuetify
  let testCanteen = {
    id: 1,
    name: "Wasabi",
    city: "Lyon",
    dailyMealCount: 100,
    badges: {},
  }

  let store = new Vuex.Store({
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
    expect(wrapper.find("h3").text()).toBe(testCanteen.name)
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
})
