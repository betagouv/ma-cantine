import Vuex from "vuex"
import VueRouter from "vue-router"
import Vuetify from "vuetify"
import { shallowMount, mount, createLocalVue, RouterLinkStub } from "@vue/test-utils"
import Header from "@/components/Header.vue"
import Constants from "@/constants"

const localVue = createLocalVue()
localVue.use(VueRouter)

describe("Header.vue", () => {
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
      const wrapper = shallowMount(Header, {
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
      const wrapper = shallowMount(Header, {
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
