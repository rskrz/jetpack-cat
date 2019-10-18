<template lang="pug">
  div(id="Home")
    .flex.flex-row.banner.w-100.justify-center.items-start.outline
      .flex.flex-column.items-center.justify-center.center.mt5
        h1.f1.fw1.tc.w-75 Overwatch commands for your Discord Server!
        button(onclick="location.href='https://discordapp.com/oauth2/authorize?client_id=630828400981966848&permissions=321600&scope=bot'" type="button").invite.f3.flex.items-center.justify-center.mt4
          img(src="../assets/logos/discord.png").w3
          | Invite to Discord
    .flex.flex-column.w-100
      .w-70.center.mt4
        .mt6.flex.items-center.justify-between
          img(src="../assets/images/tespa.png").br4.shadow
          .textblock.mt5.br4.ml5
            h1.f2.jpgray.tl.lh-copy.b Overwatch Team Analysis
              p.f3.jpgray.normal Easily recieve player and team information for any Tespa or Open Division team.
        .mt7.flex.items-center.justify-around
          .textblock.mt5.br4
            h1.f2.jpgray.tl.lh-copy.b Display Your Stats
              p.f3.jpgray.normal Show your skill rating and top played heroes in each role.
          img(src="../assets/images/sr.png").br4.shadow
      .middle.mt5
        .w-70.center
          .mt7.flex.items-center.justify-between.mb6
            img(src="../assets/images/team2.png").br4.shadow
            .textblock.mt5.br4.ml5.foot
              h1.f2.tl.lh-copy.b Overwatch League Info
                p.tan.f3.normal Recieve information on Overwatch League teams, players, and more!

</template>

<script lang="ts">
import { Vue } from "vue-property-decorator";

export default class Home extends Vue {}
</script>

<style scoped lang="scss">
#Home {
}
</style>
