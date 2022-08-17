import Vuex from "vuex"
import VueRouter from "vue-router"
import Vuetify from "vuetify"
import { shallowMount, createLocalVue } from "@vue/test-utils"
import ManagerItem from "@/views/CanteenEditor/ManagerItem"

const localVue = createLocalVue()
localVue.use(VueRouter)

describe("ManagerItem.vue", () => {
  let vuetify

  beforeEach(() => {
    vuetify = new Vuetify()
  })

  it("Includes delete button if manager is not the authenticated user", () => {
    const wrapper = shallowMount(ManagerItem, {
      localVue,
      propsData: {
        manager: {
          email: "invited@example.com",
        },
      },
      vuetify,
      stubs: ["AdminRemovalDialog"],
      store: new Vuex.Store({
        state: {
          loggedUser: {
            email: "test@example.com",
          },
        },
      }),
    })
    expect(wrapper.find("adminremovaldialog-stub").exists()).toBe(true)
  })

  it("Hides the delete button if manager is the authenticated user", () => {
    const wrapper = shallowMount(ManagerItem, {
      localVue,
      propsData: {
        manager: {
          email: "test@example.com",
        },
      },
      vuetify,
      stubs: ["AdminRemovalDialog"],
      store: new Vuex.Store({
        state: {
          loggedUser: {
            email: "test@example.com",
          },
        },
      }),
    })
    expect(wrapper.find("adminremovaldialog-stub").exists()).toBe(false)
  })

  it("Renders an orange icon with a clock when dealing with an invitation", () => {
    const wrapper = shallowMount(ManagerItem, {
      localVue,
      propsData: {
        manager: {
          email: "invited@example.com",
        },
      },
      vuetify,
      stubs: ["AdminRemovalDialog"],
      store: new Vuex.Store({
        state: {
          loggedUser: {
            email: "test@example.com",
          },
        },
      }),
    })
    const iconWrapper = wrapper.find("v-icon-stub")
    expect(iconWrapper.exists()).toBe(true)
    expect(iconWrapper.attributes().color).toBe("secondary")
    expect(iconWrapper.text()).toBe("mdi-account-clock")
  })

  it("Renders a green icon with a check when dealing with an manager", () => {
    const wrapper = shallowMount(ManagerItem, {
      localVue,
      propsData: {
        manager: {
          email: "manager@example.com",
          firstName: "Manager",
          lastName: "Doe",
        },
      },
      vuetify,
      stubs: ["AdminRemovalDialog"],
      store: new Vuex.Store({
        state: {
          loggedUser: {
            email: "test@example.com",
          },
        },
      }),
    })
    const iconWrapper = wrapper.find("v-icon-stub")
    expect(iconWrapper.exists()).toBe(true)
    expect(iconWrapper.attributes().color).toBe("primary")
    expect(iconWrapper.text()).toBe("mdi-account-check")
  })
})
