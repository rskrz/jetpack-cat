<template lang="pug">
  div(id="Home")
    .flex.flex-row.banner.w-100.justify-center.items-start.outline
      .flex.flex-column.items-center.justify-center.center.mt5-ns.mt4
        h1.f1.fw1.tc.w-75-ns.w-100 Overwatch commands for your Discord Server!
        button(onclick="location.href='https://discordapp.com/oauth2/authorize?client_id=630828400981966848&permissions=321600&scope=bot'" type="button").invite.f3.flex.items-center.justify-center.mt4.w-33-l.w-75
          img(src="../assets/logos/discord.png").w3
          | Invite to Discord
    .flex.flex-column.w-100
      .w-70-l.w-90.center.mt4-ns.mt3
        .mt6-ns.mt3.flex.flex-row-ns.flex-column.items-center.justify-between
          img(src="../assets/images/tespa.png").br4.shadow.mt0-ns.mt5
          .mt5.br4.ml6-ns
            h1.f2.jpgray.tl-l.tc.lh-copy.b Overwatch Team Analysis
              p.f3.jpgray.normal.tl-ns.tc Easily recieve player and team information for any Tespa or Open Division team.
        .mt7-l.mt6.flex.flex-row-ns.flex-column-reverse.items-center.justify-around
          .mt5.br4
            h1.f2.jpgray.tl-l.tc.lh-copy.b Display Your Stats
              p.f3.jpgray.normal.tl-ns.tc Show your skill rating and top played heroes in each role.
          img(src="../assets/images/sr.png").br4.shadow
      .middle.mt5
        .w-70-l.w-90.center
          .mt7-l.mt6.flex.flex-row-ns.flex-column.items-center.justify-between.mb6-l
            img(src="../assets/images/team2.png").br4.shadow
            .mt5.br4.ml6-ns.foot
              h1.f2.tl-l.tc.lh-copy.b Overwatch League Info
                p.tan.f3.normal.tl-ns.tc Recieve information on Overwatch League teams, players, and more!

</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
@Component({
  name:'Home'
})

export default class Home extends Vue {}
</script>

<style scoped lang="scss">
#Home {
}
</style>
