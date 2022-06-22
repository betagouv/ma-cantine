import Vuex from "vuex"
import VueRouter from "vue-router"
import Vuetify from "vuetify"
import { shallowMount, createLocalVue, RouterLinkStub } from "@vue/test-utils"
import AppHeader from "@/components/AppHeader.vue"

const localVue = createLocalVue()
localVue.use(VueRouter)

describe("AppHeader.vue", () => {
  let vuetify

  beforeEach(() => {
    vuetify = new Vuetify()
  })

  const router = new VueRouter({
    routes: [
      {
        path: "/",
        name: "LandingPage",
      },
    ],
  })

  describe("unauthenticated", () => {
    it("Includes login button", () => {
      const wrapper = shallowMount(AppHeader, {
        localVue,
        vuetify,
        stubs: {
          RouterLink: RouterLinkStub,
        },
        router: router,
        store: new Vuex.Store({
          state: {
            loggedUser: null,
            initialDataLoaded: true,
          },
        }),
      })
      expect(wrapper.find("v-btn-stub.header-login-button").exists()).toBe(true)
    })
  })

  describe("authenticated", () => {
    it("Includes a user menu", () => {
      // mocking breakpoint with thanks to https://github.com/vuetifyjs/vuetify/issues/11388#issuecomment-701410577
      const breakpoint = {
        init: jest.fn(),
        framework: {},
        smAndDown: true,
      }
      vuetify.framework.breakpoint = breakpoint
      const wrapper = shallowMount(AppHeader, {
        localVue,
        vuetify,
        stubs: {
          RouterLink: RouterLinkStub,
        },
        router: router,
        store: new Vuex.Store({
          state: {
            loggedUser: { id: 1, email: "test@example.com" },
            initialDataLoaded: true,
          },
        }),
      })
      expect(wrapper.find("v-menu-stub").exists()).toBe(true)
    })
  })
})
