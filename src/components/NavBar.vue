<template lang="pug">
  .h4.w-100.flex.flex-row.items-center.router.justify-between
    .flex
      img(src="../assets/logos/kot2.png").h4.w4.mh5
      h1 Jetpack Cat
    .flex
      router-link(to="/").mr4-ns.mh2.rl Home
      router-link(to="../Commands").mr4-ns.mh2.rl Commands
      a(href="https://discordapp.com/oauth2/authorize?client_id=630828400981966848&permissions=321600&scope=bot").mr4-ns.mh2.rl Invite
      a(href="https://github.com/rskrz/jetpack-cat").mr4-ns.mh2.rl GitHub
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
@Component({
  name: "NavBar"
})
export default class NavBar extends Vue {}
</script>

<style lang="scss" scoped>
#navbar {
}
</style>
