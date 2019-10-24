<template lang="pug">
  div
    .h4-ns.w-100.flex.flex-row.items-center.router.justify-between
      link(rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css")
      .flex.items-center
        img(src="../assets/logos/kot2.png").h3.h4-l.mh5-l.mh3
        h1.f1-l.f2 Jetpack Cat
      .flex.dn.db-ns
        router-link(to="/").mr4.rl Home
        router-link(to="/Commands").mr4-ns.rl Commands
        a(href="https://discordapp.com/oauth2/authorize?client_id=630828400981966848&permissions=321600&scope=bot").mr4.rl Invite
        a(href="https://github.com/rskrz/jetpack-cat").mr4.rl GitHub
      .dn-ns.mr2
        button(@click="display=!display").menubutton
          i.fa.fa-bars
    div(v-if="display").topnav.dn-ns.f3
      router-link(to="/").menulink Home
      router-link(to="commands").menulink Commands
      a(href="https://discordapp.com/oauth2/authorize?client_id=630828400981966848&permissions=321600&scope=bot").menulink Invite
      a(href="https://github.com/rskrz/jetpack-cat").menulink GitHub
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
@Component({
  name: "NavBar"
})
export default class NavBar extends Vue {
  data() {
    return {
      display: false
    }
  }
}
</script>

<style lang="scss" scoped>
#navbar {
}
</style>
