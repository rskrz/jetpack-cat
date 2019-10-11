<template lang="pug">
  div(id="Home")
    div.flex.center.items-center.justify-center.banner.h5
      h1 JETPACK
      img(src="../assets/kot2.png").pa3.w5
      h1.ml4 CAT
    div Functionality
</template>

<script lang="ts">
import { Vue } from "vue-property-decorator";

export default class Home extends Vue {}
</script>

<style scoped lang="scss">
#Home {
}
</style>
