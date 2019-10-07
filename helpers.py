def rankEmoji(skill_rating):
    if skill_rating < 1500:
        emoji = '<:b_:559923570252447764>'
    elif skill_rating < 2000:
        emoji = '<:s_:559923570357305354>'
    elif skill_rating < 2500:
        emoji = '<:g_:559923570268962816>'
    elif skill_rating < 3000:
        emoji = '<:p_:559923570105647107>'
    elif skill_rating < 3500:
        emoji = '<:d_:559923570323488768>'
    elif skill_rating < 4000:
        emoji = '<:m_:559923570378276889>'
    elif skill_rating >= 4000:
        emoji = '<:gm:559923570369626142>'
    else:
        emoji = ""
    return emoji

hero_dict = {
        "ana" : "<:Ana:591708294477905952>",
        "ashe" : "<:Ashe:591714749486465045>",
        "baptiste" : "<:Baptiste:591708294951862413>",
        "bastion": "<:Bastion:591708294826164225>",
        "brigitte": "<:Brigitte:591708295182680065>",
        "d.va": "<:DVa:591709680632594437>",
        "dVa" : "<:DVa:591709680632594437>",
        "doomfist" : "<:Doomfist:591708295396458498>",
        "genji" : "<:Genji:591708295484407818>",
        "hanzo" : "<:Hanzo:591708295501185034>",
        "junkrat" : "<:Junkrat:591708295409172521>",
        "lúcio" : "<:Lucio:591708295383744513>",
        "lucio" : "<:Lucio:591708295383744513>",
        "mccree" : "<:McCree:591708295673151509>",
        "mei" : "<:Mei:591708296092712971>",
        "mercy" : "<:Mercy:591708295555973140>",
        "moira" : "<:Moira:591708295287406603>",
        "orisa" : "<:Orisa:591708295551516672>",
        "pharah" : "<:Pharah:591708295522156544>",
        "reaper" : "<:Reaper:591708295388200992>",
        "reinhardt" : "<:Reinhardt:591708295509835807>",
        "roadhog" : "<:Roadhog:591708295589396480>",
        "sigma" : "<:Sigma:619259776144113664>",
        "soldier76" : "<:Soldier76:591708295719419922>",
        "sombra" : "<:Sombra:591708295484538892>",
        "symmetra" : "<:Symmetra:591708295413235717>",
        "torbjörn" : "<:Torbjorn:591708295249526815>",
        "torbjorn" : "<:Torbjorn:591708295249526815>",
        "tracer" : "<:Tracer:591708295471824906>",
        "widowmaker" : "<:Widowmaker:591708295555710995>",
        "winston" : "<:Winston:591708295769882624>",
        "wrecking ball" : "<:Wrecking_Ball:591708295715356692>",
        "wreckingball" : "<:Wrecking_Ball:591708295715356692>",
        "wreckingBall" : "<:Wrecking_Ball:591708295715356692>",
        "zarya" : "<:Zarya:591708295539195920>",
        "zenyatta" : "<:Zenyatta:591708295560036359>",
        "tank" : "<:Tank:619262646885154846>",
        "dps" : "<:Dps:619262646834692106>",
        "damage" : "<:Dps:619262646834692106>",
        "support" : "<:Support:619262646708863007>"
        }