<template lang="pug">
  .h3.w-100.flex.flex-row.justify-end-ns.justify-center.items-center.router
    router-link(to="/").mr4-ns.mh2 Home
    router-link(to="../Commands").mr4-ns.mh2 Commands
    router-link(to="../Invite").mr4-ns.mh2 Invite
    router-link(to="../GitHub").mr4-ns.mh2 GitHub
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
