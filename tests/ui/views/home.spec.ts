import { shallowMount, Wrapper } from "@vue/test-utils";
import Home from "@/views/Home.vue";

describe("Home.vue", () => {
  class HomeWrapper {
    constructor(public wrapper: Wrapper<Home>) {}

    get main(): Wrapper<Home> {
      return this.wrapper.find("#main") as Wrapper<Home>;
    }
  }
  it("should render main div", () => {
    const wrapper = new HomeWrapper(
      shallowMount(Home, {
        stubs: ["router-link"]
      })
    );
    expect(wrapper.main.isVisible()).toBe(true);
  });
});
