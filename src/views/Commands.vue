<template lang="pug">
  div(id="Commands").center
    h1.f-5-ns.f1.tc.jpgray Commands
    .flex.flex-row.justify-around.mb5-ns
      .commands-bg.pa3.br4.tan.w-70-l.w-90-m.w-100
        table.collapse.w-100.tl.f4
          thead
            tr.bb 
              th.pa2.w-25 Command
              th.w-25 Usage
              th.w-50.db-ns.dn Examples
          tbody.f5
            tr(@mouseover="active='tespa.png'").bb.sel 
              td.pa3 Get Tespa Team SR
              td .tespa https://link.to.team
              td.db-ns.dn  .tespa https://compete.tespa.org/tournament/145/team/123456
            tr(@mouseover="active='od.png'").bb.sel
              td.pa3 Get Open Division Team SR
              td .od "Team Name"
              td.db-ns.dn  .od "Cap'n Crunge"
            tr(@mouseover="active='sr.png'").bb.sel
              td.pa3 Get Player SR
              td .sr &lt;username#12345&gt;
              td.db-ns.dn  .sr skrz#11924
            tr(@mouseover="active='compare.png'").bb.sel
              td.pa3 Compare OWL Player Stats
              td .compare&lt;player1&gt; &lt;player2&gt;
              td.db-ns.dn  .compare jjonak viol2t
            tr(@mouseover="active='stats.png'").bb.sel 
              td.pa3 OWL Player Stats
              td .stats &lt;player name&gt;
              td.db-ns.dn  .stats jjonak
            tr(@mouseover="active='team.png'").bb.sel
              td.pa3 OWL Team Info
              td .team &lt;team&gt;
              td.db-ns.dn  .team dallas
            tr(@mouseover="active='schedule.gif'").bb.sel
              td.pa3 OWL Stage Schedule
              td .[schedule|sc]
              td.db-ns.dn .sc
            tr(@mouseover="active='standings.gif'").bb.sel
              td.pa3 OWL Stage Standings
              td .[standings|st]
              td.db-ns.dn .st
            tr.bb.sel 
              td.pa3 Random Hero
              td .[hero|heroes|comp] &lt;amount&gt;
              td.db-ns.dn  .hero 6
            tr.bb.sel 
              td.pa3 Random Role
              td .role
              td.db-ns.dn .role
        h2.f5.fw1.mb5-l *Usage format: .[command|alias] denotes an alias for a command
      .commands-bg.pa3.br4.tan.w-25.bot.db-l.dn
        img(v-bind:src="require('../assets/images/'+active)").br2
      
    
    
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
@Component({
  name:'Commands'
})

export default class Commands extends Vue {
  data() {
    return {
      active: "tespa.png"
    }
  }
}
</script>

<style scoped lang="scss">
#Commands {
}
</style>