"""重要語 約70語（gate, guess, pause, restaurant ...）＋ poser 系・比較の -er の修正"""
import os as _os
TOOLS=_os.path.dirname(_os.path.abspath(__file__)); ROOT=_os.path.dirname(TOOLS)
import json
C = "2026-10-27"; PATH = _os.path.join(ROOT,'etymo-data.json')
def eo(entry, note): return [{"id": "etymonline", "entry": entry, "checked": C, "note": note}]
d = json.load(open(PATH))
U = "祖語未詳"
PIE = [
 ("*pel-(1)", "*pel-", "青白い・灰色の", "ラテン語 pallēre「青ざめている」（pale, pallid）へ", "nature", "pale", "pale (adj.) の項でラテン語 pallidus を pallēre「青ざめている」から、*pel-(1)「青白い」からと記載"),
 ("*rep-", None, "ひったくる", "ラテン語 rapere「奪い取る」（rapid）へ", "possession", "rapid", "rapid の項でラテン語 rapidus を rapere「ひったくる」から、*rep-「ひったくる」からと記載"),
 ("*leis-(2)", "*leis-", "小さい", "ゲルマン祖語 *laisizan（less, least）へ", "quantity", "lesser", "lesser の項で less をゲルマン祖語 *laisizan から、*leis-(2)「小さい」からと記載（little とは無関係）"),
 ("*kneu-", None, "木の実", "ゲルマン祖語 *hnut-（nut）へ", "nature", "nut", "nut の項でゲルマン祖語 *hnut- を *kneu-「木の実」からと記載"),
 ("*letro-", None, "革", "ゲルマン祖語 *lethran（leather）へ", "craft", "leather", "leather の項でゲルマン祖語 *lethran を *letro-「革」からと記載"),
 ("*reue-(2)", "*reue-", "打ち壊す・掘り出す", "ラテン語 ruere「崩れ落ちる」（ruin）へ", "craft", "ruin", "ruin (n.) の項でラテン語 ruere「突進する・崩れ落ちる」を *reue-(2)「打ち壊す・引き裂く・掘り出す」からと記載"),
 ("*(s)keg-", None, "跳ぶ・動く", "ゲルマン祖語 *skakanan（shake）へ（とする説）", "motion", "shake", "shake の項でゲルマン祖語 *skakanan を、*(s)keg-「跳ぶ・動く」からとする説があると記載（ゲルマン語外に確かな同源語なし）"),
 ("*skem-", None, "覆う（恥じて）", "ゲルマン祖語 *skamo（shame）へ（おそらく。*kem-「覆う」から）", "mind", "shame", "shame の項でゲルマン祖語 *skamo を語源不明としつつ、おそらく *skem-（*kem-「覆う」から）からと記載"),
 ("*seib-", None, "注ぐ・滴る", "ゲルマン祖語 *saipon「滴るもの・樹脂」（soap）へ", "nature", "soap", "soap の項でゲルマン祖語 *saipon を *soi-bon-（*seib-「注ぐ・滴る」から）からと記載"),
 ("*suro-", None, "酸っぱい・塩辛い", "ゲルマン祖語 *sura-（sour）へ", "body", "sour", "sour の項でゲルマン祖語 *sura- を *suro-「酸っぱい・塩辛い・苦い」からと記載（リトアニア語 sūras「塩辛い」と同源）"),
 ("*stak-", None, "立つ・しっかりする", "ゲルマン祖語 *stakhla-「しっかり立つもの」（steel）へ（とされる）", "posture", "steel", "steel の項でゲルマン祖語 *stakhlijan を *stakhla「しっかり立つ」（*stek-lo-、*stak-「立つ・据える・しっかりする」から）と関係するとされると記載"),
 ("*tenk-(2)", "*tenk-", "固まる・濃くなる", "ゲルマン祖語 *thinhta-（tight）へ（Watkins）", "nature", "tight", "tight の項でゲルマン祖語 *thinhta- を、Watkins により *tenk-(2)「固まる・凝固する・濃くなる」からと記載"),
 ("*wen-(2)", "*wen-", "打つ・傷つける", "ゲルマン祖語 *wuntho（wound）へ（Watkins）", "craft", "wound", "wound (n.) の項でゲルマン祖語 *wuntho を、おそらく *wen-(2)「打つ・傷つける」からと記載（Watkins）"),
 ("*urgh-", None, "縛る・締める", "ラテン語 urgēre「押す・迫る」（urge, urgent）へ", "craft", "urge", "urge の項でラテン語 urgēre を *urgh-「縛る・締める」からとし、de Vaan は「押さえつける」から「押す・迫る」へと説明（*ureg- 説は音変化から無理とする）"),
 ("*kwet-", None, "揺する", "ラテン語 quatere「揺する」（rescue）へ（Watkins）", "motion", "rescue", "rescue の項でラテン語 excutere を ex- ＋ quatere「揺する」の結合形から、quash の項で quatere を Watkins により *kwet-「揺する」からと記載"),
]
ex = {p["id"] for p in d["pie"]}
for pid, label, g, n, cat, entry, sn in PIE:
    assert pid not in ex, pid
    e = {"id": pid}
    if label: e["label"] = label
    e.update({"gloss": g, "note": n, "category": cat, "status": "verified", "src": eo(entry, sn)})
    d["pie"].append(e)
ex = {p["id"] for p in d["pie"]}
def part(pid, label, kind, gloss, origin, branch, pie, forms, entry, note, pnote=None, etym=None):
    for x in pie: assert x in ex, (pid, x)
    e = {"id": pid}
    if label: e["label"] = label
    e.update({"kind": kind, "gloss": gloss, "origin": origin, "branch": branch, "pie": pie})
    if etym: e["etym"] = etym
    if forms: e["forms"] = forms
    if pnote: e["note"] = pnote
    e.update({"status": "verified", "src": eo(entry, note)})
    return e
G, L, K, N_ = "germanic", "latin", "greek", "nonie"
R = [
 part("geat", "geat", "root", "門・開口部", "OE geat", G, [], ["gate"], "gate", "gate (n.) の項で古英語 geat「門・開口部」をゲルマン祖語 *gatan から、語源不明と記載。掲載語: gate", U),
 part("haet", "hæt", "root", "頭巾・帽子", "OE hæt", G, [], ["hat"], "hat", "hat の項で古英語 hæt「頭巾」をゲルマン祖語 *hattuz から、語源不詳と記載。掲載語: hat", U),
 part("hitta", "hitta", "root", "出会う・当たる", "ON hitta", G, [], ["hit"], "hit", "hit (v.) の項で後期古英語 hyttan を古ノルド語 hitta「出会う・行き当たる」から、ゲルマン祖語 *hitjan は語源不詳と記載。掲載語: hit", U),
 part("hurr", "hurren", "root", "慌てて動く", "ME hurren", G, [], ["hurr"], "hurry", "hurry の項で、語源不詳とし、harry の異形か、中英語 hurren（ゲルマン祖語 *hurza-）からかと記載。掲載語: hurry", U + "（harry の異形とも）"),
 part("knifr", "knīfr", "root", "小刀", "ON knīfr", G, [], ["knife"], "knife", "knife の項で後期古英語 cnif を古ノルド語 knīfr から、ゲルマン祖語 *knibaz は語源不詳と記載。掲載語: knife", U),
 part("cnotta", "cnotta", "root", "結び目", "OE cnotta", G, [], ["knot"], "knot", "knot の項で古英語 cnotta をゲルマン祖語 *knuttan- からと記載（祖語の記載なし）。掲載語: knot", U),
 part("lamb", "lamb", "root", "子羊", "OE lamb", G, [], ["lamb"], "lamb", "lamb の項で古英語 lamb をゲルマン祖語 *lambaz から、ゲルマン語外に同源語なしと記載。掲載語: lamb", U),
 part("hlot", "hlot", "root", "くじ・分け前", "OE hlot", G, [], ["lot"], "lot", "lot の項で古英語 hlot「くじ・分け前・運命」をゲルマン祖語 *khlut- から、語源不明と記載。lottery はイタリア語 lotteria（lotto から、ゲルマン語由来）。掲載語: lot", U),
 part("nearu", "nearu", "root", "狭い", "OE nearu", G, [], ["narrow"], "narrow", "narrow の項で古英語 nearu を西ゲルマン語 *narwaz から、語源不明と記載。掲載語: narrow", U),
 part("pak", "pak / pac", "root", "包み・荷", "ME pak / MDu. pac", G, [], ["pack"], "pack", "pack (n.) の項で中英語 pak を、おそらく中世オランダ語 pac などの低地ゲルマン語から、語源不詳と記載。掲載語: pack, package", U),
 part("pol", "pōl", "root", "水たまり・池", "OE pōl", G, [], ["pool"], "pool", "pool (n.1) の項で古英語 pōl を西ゲルマン語 *pōl- から、語源不詳（基層語か）と記載。掲載語: pool", U + "（基層語か）"),
 part("gissen", "gessen", "root", "推し量る", "ME gessen / MDu. gissen", G, ["*ghend-"], ["guess"], "guess", "guess (v.) の項で中英語 gessen を、おそらくスカンジナビア語または中世オランダ語 gissen から、ゲルマン祖語 *getan「得る」（get と同じ）、*ghend-「つかむ」からと記載。掲載語: guess"),
 part("gunn", "Gunnhildr", "root", "戦い（女性名から）", "ON Gunnhildr", G, ["*gwhend-"], ["gun"], "gun", "gun の項で、おそらく女性名 Gunilda（古ノルド語 Gunnhildr = gunnr「戦い」＋ hildr「戦い」）の愛称から（大型の投石機などの名）とし、gunnr を *gwhen-「打つ・殺す」からと記載。掲載語: gun"),
 part("laes", "lǣs", "root", "より小さい", "OE lǣs / lǣssa", G, ["*leis-(2)"], ["less", "least"], "lesser", "lesser の項で less を古英語 lǣs・lǣssa からと記載。least の項で古英語 lǣst（lǣsest の縮約、little の最上級として用いる）と記載。掲載語: less, least, lesser"),
 part("lether", "leðer", "root", "革", "OE leðer", G, ["*letro-"], ["leather"], "leather", "leather の項で古英語 leðer と記載。掲載語: leather"),
 part("gemaed", "gemǣdd", "root", "気がふれた", "OE gemǣdd", G, ["*mei-(1)"], ["mad"], "mad", "mad (adj.) の項で古英語 gemǣdd を gemǣdan「狂わせる」から、ゲルマン祖語 *gamaidjan、*moito-（*mei-(1)「変える」の過去分詞形）から（とみられる）と記載。掲載語: mad"),
 part("hnecca", "hnecca", "root", "首", "OE hnecca", G, [], ["neck"], "neck", "neck (n.) の項で古英語 hnecca をゲルマン祖語 *hnekk- から、確かな同源語なし（Klein は *knok- とする）と記載。掲載語: neck", U),
 part("hnutu", "hnutu", "root", "木の実", "OE hnutu", G, ["*kneu-"], ["nut"], "nut", "nut の項で古英語 hnutu と記載。掲載語: nut"),
 part("gol", "gol", "root", "境界・限界", "ME gol", G, [], ["goal"], "goal", "goal の項で1530年代に初出、中英語 gol「境界・限界」（14世紀初めに一度だけ記録）からとし、語源は諸説あり不明と記載。掲載語: goal", "語源不明（中英語 gol「境界」か）", "unknown"),
 part("jump", "jump", "root", "跳ぶ", "Mod.E jump (1520s)", G, [], ["jump"], "jump", "jump (v.) の項で1520年代に初出、語源不詳、擬音的かと記載（ゲルマン語に似た語がある）。掲載語: jump", "語源不明（擬音的か）", "unknown"),
 part("heros", "hērōs", "root", "英雄・半神", "Gk. hērōs > Lat. hērōs", K, [], ["hero"], "hero", "hero の項でラテン語 hērōs をギリシア語 hērōs「半神・英雄」から、語源不詳とし、古くは *ser-(1)「守る」からとされたが、Beekes は先ギリシア語とすると記載。掲載語: hero", U + "（*ser-(1) 説・先ギリシア語説）"),
 part("ahuge", "ahuge", "root", "巨大な", "OF ahuge", L, [], ["huge"], "huge", "huge の項で古フランス語 ahuge「巨大な」から、語源不明と記載。掲載語: huge", U),
 part("parc", "parc", "root", "囲い地", "OF parc / ML parricus", G, [], ["park"], "park", "park (n.) の項で古フランス語 parc「囲い地」を中世ラテン語 parricus から、西ゲルマン語起源と記載（祖語の記載なし）。掲載語: park", U),
 part("pott", "pott / pot", "root", "鍋・つぼ", "OF pot / VL *pottus", L, [], ["pot"], "pot", "pot (n.1) の項で後期古英語 pott・古フランス語 pot を俗ラテン語 *pottus から、語源不明と記載。掲載語: pot", U),
 part("pulv", "pulv / powd", "root", "ちり・粉", "Lat. pulvis / pulverem", L, [], ["powd", "pulv"], "powder", "powder の項で古フランス語 poudre をラテン語 pulverem（pulvis「ちり・粉」の対格）からと記載（祖語の記載なし）。掲載語: powder", U),
 part("pall", "pall / pale", "root", "青ざめる", "Lat. pallēre / pallidus", L, ["*pel-(1)"], ["pale", "pall"], "pale", "pale (adj.) の項で古フランス語 paile をラテン語 pallidus から（pallid は二重語）と記載。掲載語: pale, pallid"),
 part("poke", "poque / poke", "root", "袋", "ONF poque / Frankish *pokka", G, ["*beu-"], ["pocket"], "pocket", "pocket の項でアングロフランス語 pokete を古北フランス語 poque「袋」の指小形から、フランク語 *pokka、ゲルマン祖語 *puk- からとし、*beu-（「膨らむ」を表す擬音的な語根）からとみられると記載。掲載語: pocket"),
 part("polire", "polire / polit", "root", "磨く", "Lat. polīre / polītus", L, ["*pel-(5)"], ["polit", "polish"], "polite", "polite の項でラテン語 polītus「磨かれた」を polīre から、*pel-(5)「押す・打つ」からとする（他にも説あり）と記載。polish (v.) は古フランス語 poliss-（polir の語幹）から。掲載語: polite, polish"),
 part("pouren", "pouren", "root", "注ぐ", "ME pouren", G, [], ["pour"], "pour", "pour (v.) の項で1300年ごろに初出、語源不明とし、古フランス語 purer「（液体を）澄ます」、ラテン語 pūrāre（pūrus「清い」）からとする説もあると記載。掲載語: pour", "語源不明（ラテン語 pūrus からとする説も）", "unknown"),
 part("rap", "rap", "root", "奪い取る", "Lat. rapere / rapidus", L, ["*rep-"], ["rap"], "rapid", "rapid の項でラテン語 rapidus「速い・急な」を rapere「ひったくる」からと記載。掲載語: rapid"),
 part("quat", "quat / cuss", "root", "揺する", "Lat. quatere / -cutere", L, ["*kwet-"], ["cue", "cuss", "quat"], "rescue", "rescue の項で古フランス語 rescorre を re- ＋ escourre「振り払う」から、ラテン語 excutere（ex- ＋ quatere「揺する」）からと記載。掲載語: rescue"),
 part("paus", "paus / pose", "root", "止まる・休む", "Gk. pausis / Late Lat. pausāre", K, [], ["paus", "pose"], "pause", "pause (n.) の項でラテン語 pausa をギリシア語 pausis「停止」から、pauein「止める」からと記載（確かな語源なし）。propose・compose の項で古フランス語 poser「置く」を後期ラテン語 pausāre「止まる・休む」からとし、ponere とは語源的に無関係（似た語幹の混同で「置く」の意を得た）と記載。掲載語: pause, pose, compose, propose, repose, purpose", "祖語未詳。フランス語 poser「置く」はラテン語 pōnere と混同されたが別語"),
 part("ru", "ru / ruin", "root", "崩れ落ちる", "Lat. ruere / ruīna", L, ["*reue-(2)"], ["ruin"], "ruin", "ruin (n.) の項でラテン語 ruīna「崩壊」を ruere「突進する・崩れ落ちる」からと記載。掲載語: ruin"),
 part("segl", "segl", "root", "帆・幕", "OE segl", G, ["*sek-"], ["sail"], "sail", "sail (n.) の項で古英語 segl をゲルマン祖語 *seglom から、語源はあいまいだが Klein と OED は *sek-「切る」（切った布）と結びつけると記載。掲載語: sail"),
 part("sceacan", "sceacan", "root", "揺り動かす", "OE sceacan", G, ["*(s)keg-"], ["shake"], "shake", "shake (v.) の項で古英語 sceacan「すばやく前後に動く・逃げる」をゲルマン祖語 *skakanan から、*(s)keg- とする説があると記載。掲載語: shake"),
 part("scamu", "scamu", "root", "恥", "OE scamu", G, ["*skem-"], ["shame"], "shame", "shame (n.) の項で古英語 scamu をゲルマン祖語 *skamo からと記載。掲載語: shame"),
 part("seric", "sēricum / sioloc", "root", "絹（セーレス人の布）", "OE sioloc < Lat. sēricum < Gk. sērikos", K, [], ["silk", "seric"], "silk", "silk の項で古英語 sioloc をラテン語 sēricum、ギリシア語 Sērikos「セーレス人の」（絹を得た東方の民、おそらく中国北部）からとし、究極の語源は不明（中国語「絲」と関係するかとも）と記載。掲載語: silk", U + "（中国語からとも）"),
 part("smoth", "smōð", "root", "滑らかな", "OE smōð", G, [], ["smooth"], "smooth", "smooth (adj.) の項で古英語 smōð（smēðe の異形）を語源不明、同源語なしと記載。掲載語: smooth", "語源不明（古英語で行き止まり）", "unknown"),
 part("sape", "sāpe", "root", "石けん・軟膏", "OE sāpe", G, ["*seib-"], ["soap"], "soap", "soap (n.) の項で古英語 sāpe をゲルマン祖語 *saipon「滴るもの・樹脂」からと記載（ラテン語 sāpō はゲルマン語からの借用）。掲載語: soap"),
 part("sup", "soupe / sop", "root", "浸したパン・汁", "Fr. soupe < Late Lat. suppa < Gmc.", G, ["*seue-(2)"], ["soup"], "soup", "soup (n.) の項でフランス語 soupe を後期ラテン語 suppa「汁に浸したパン」から、ゲルマン語（中世オランダ語 sop など、ゲルマン祖語 *sup-）、*seue-(2)「液体を取る」からと記載。掲載語: soup"),
 part("sur", "sūr", "root", "酸っぱい", "OE sūr", G, ["*suro-"], ["sour"], "sour", "sour (adj.) の項で古英語 sūr「酸っぱい・発酵した」と記載。掲載語: sour"),
 part("spon", "spōn", "root", "木片", "OE spōn / ON spánn", G, [], ["spoon"], "spoon", "spoon (n.) の項で古英語 spōn「木片・削りくず」をゲルマン祖語 *spe-nu- から、以前は *spe-(2)「細長い木片」からとされたと記載。食器の意は古ノルド語 spánn の影響か。掲載語: spoon", U + "（以前は *spe-(2) からとされた）"),
 part("stelan", "stelan", "root", "盗む", "OE stelan", G, [], ["steal", "stol"], "steal", "steal (v.) の項で古英語 stelan をゲルマン祖語 *stelanan から、*stel-（*ster-「奪う」の異形）からとも言われるが、Boutkan は良い印欧語語源がないとすると記載。掲載語: steal", U + "（*stel- とする説もある）"),
 part("stahl", "stȳle / stēle", "root", "鋼", "OE stȳle", G, ["*stak-"], ["steel"], "steel", "steel (n.) の項で古英語 stȳle をゲルマン祖語 *stakhlijan「鋼でできた」から（ゲルマン語外に対応語なし）と記載。掲載語: steel"),
 part("swapan", "swāpan", "root", "掃く", "OE swāpan", G, [], ["sweep"], "sweep", "sweep (v.) の項で14世紀初めの swepen を古英語 swāpan「掃く」と関係づけ（swope の過去形からか、スカンジナビア語からか）、swoop の項でゲルマン祖語 *swaip- を挙げる（祖語の記載なし）。掲載語: sweep", U),
 part("getael", "getæl / tal", "root", "すばやい・有能な", "OE getæl / ME tal", G, [], ["tall"], "tall", "tall (adj.) の項で古英語 getæl「すばやい・活発な」（ゲルマン祖語 *(ga-)tala-）から、おそらく中英語 tal「美しい・ふさわしい」を経て「背の高い」へと記載（OED も意味変化は著しいとする）。掲載語: tall", U),
 part("theof", "þēof", "root", "泥棒", "OE þēof", G, [], ["thief", "thef"], "thief", "thief の項で古英語 þēof をゲルマン祖語 *theuba- から、語源不詳と記載。theft の項で古英語 þēofð（*theubaz ＋ 抽象名詞の接尾辞 *-itha）と記載。掲載語: thief, theft", U),
 part("throte", "þrote", "root", "のど", "OE þrote", G, [], ["throat"], "throat", "throat の項で古英語 þrote（þrotbolla「のど仏」から推定）をゲルマン祖語 *thrut- から、þrutian「膨らむ」と関係し、語源不詳と記載。掲載語: throat", U),
 part("thiht", "þéttr / -þiht", "root", "密な・固い", "ON þéttr / OE -þiht", G, ["*tenk-(2)"], ["tight"], "tight", "tight (adj.) の項で中英語 tyght（thight の変形）を古ノルド語 þéttr「水を通さない・密な」と古英語 -þiht から、ゲルマン祖語 *thinhta- からと記載。掲載語: tight"),
 part("turr", "turris / torr", "root", "塔", "OE torr / OF tur < Lat. turris", L, [], ["tower", "turr"], "tower", "tower (n.) の項で古英語 torr をラテン語 turris「塔・城塞」から、おそらく先印欧語の地中海の言語からと記載。掲載語: tower", U + "（先印欧語の地中海の言語からか）"),
 part("uggr", "uggr", "root", "恐れ", "ON uggr / uggligr", G, [], ["ug"], "ugly", "ugly の項で、おそらく古ノルド語 uggligr「恐ろしい」（uggr「恐れ」＋ -ligr「〜のような」）などのスカンジナビア語からと記載（祖語の記載なし）。掲載語: ugly", U),
 part("wund", "wund", "root", "傷", "OE wund", G, ["*wen-(2)"], ["wound"], "wound", "wound (n.) の項で古英語 wund「傷」と記載。掲載語: wound"),
 part("urg", "urg", "root", "押す・迫る", "Lat. urgēre", L, ["*urgh-"], ["urg"], "urge", "urge (v.) の項でラテン語 urgēre「押す・駆り立てる・迫る」からと記載（urgent も同語から）。掲載語: urge, urgent"),
 part("tener", "tener / tender", "root", "柔らかい・か弱い", "OF tendre < Lat. tener", L, ["*ten-"], ["tender"], "tender", "tender (adj.) の項で古フランス語 tendre をラテン語 tenerem（tener「柔らかい・か弱い」）から、*ten-「伸ばす」からと記載（フランス語の -d- は非語源的）。掲載語: tender"),
]
S = [
 part("-er(2)", "-er", "suffix", "より〜（比較級）", "OE -ra / -re", G, [], None, "-er", "-er (2)：比較級の接尾辞、古英語 -ra・-re をゲルマン祖語 *-izon から（*-yos-）と記載。lesser の項で less ＋ 比較の -er（二重比較）と記載。upper の項で up の比較級と記載。掲載語: upper, lesser, inner, elder, former, further"),
]
ep = {p["id"] for p in d["parts"]}
for p in R + S: assert p["id"] not in ep, p["id"]
i = max(i for i, x in enumerate(d["parts"]) if x["kind"] == "root") + 1
d["parts"][i:i] = R
i = max(i for i, x in enumerate(d["parts"]) if x["kind"] == "suffix") + 1
d["parts"][i:i] = S
P = {p["id"]: p for p in d["parts"]}
def addsrc(pid, entry, note, form=None):
    p = P[pid]
    if form:
        fs = p.setdefault("forms", [])
        if form not in fs: fs.append(form)
    p["src"].append({"id": "etymonline", "entry": entry, "checked": C, "note": note})
# 修正: purpose は poser（pausāre）から
P["pos"]["src"] = [s for s in P["pos"]["src"] if s["entry"] != "purpose"]
P["pos"]["note"] = P["pos"]["note"] + "。フランス語経由の -pose（compose, propose, purpose など）は pausāre からの poser で別語"
addsrc("re-", "restaurant", "restaurant の項でラテン語 restaurāre = re-「再び」＋ -staurāre と記載。repose の項で後期ラテン語 repausāre（re- ＋ pausāre）と記載。rescue の項で re- ＋ escourre（強意か）と記載。掲載語: restaurant, repose, rescue")
addsrc("sta", "restaurant", "restaurant の項でフランス語 restaurer「回復させる」を古フランス語 restorer、ラテン語 restaurāre（instaurāre と同根、*sta-「立つ・しっかりさせる」から）からと記載。掲載語: restaurant", "staur")
addsrc("-ent", "restaurant", "restaurant の項でフランス語 restaurer の現在分詞（「元気を回復させる食べ物」）と記載。掲載語: restaurant, urgent")
addsrc("ex-", "rescue", "rescue の項でラテン語 excutere = ex-「外へ」＋ quatere と記載。掲載語: rescue")
addsrc("con-", "compose", "compose の項で古フランス語 composer = com-「共に」＋ poser と記載。掲載語: compose")
addsrc("pro-", "propose", "propose の項で古フランス語 proposer = pro-「前へ」＋ poser と記載。掲載語: propose, purpose")
addsrc("-id", "pale", "pale の項でラテン語 pallidus（pallid は二重語）と記載。rapid の項でラテン語 rapidus と記載。掲載語: pallid, rapid")
addsrc("-age", "package", "package の項で pack ＋ -age と記載。掲載語: package")
addsrc("-ly", "ugly", "ugly の項で古ノルド語 uggligr = uggr ＋ -ligr「〜のような」と記載。掲載語: ugly")
addsrc("-th", "theft", "theft の項でゲルマン祖語 *theubitho = *theubaz ＋ 抽象名詞の接尾辞 *-itha と記載。掲載語: theft")
addsrc("ton", "tune", "tune (n.) の項で語源は説明されていないが一般に tone の異形とされると記載。掲載語: tune", "tun")
if "ton" not in P["ton"]["forms"]: P["ton"]["forms"].insert(0, "ton")
addsrc("the", "treasure", "treasure の項で古フランス語 tresor をラテン語 thēsaurus、ギリシア語 thēsauros「蓄え・宝庫」から、tithenai「置く」と関係し *dhe- の重複形からとされると記載。掲載語: treasure", "treasure")
addsrc("upp", "upper", "upper の項で up (adj.) の比較級と記載。掲載語: upper", "upp")
addsrc("tend", "tender", "tender (adj.) は tendere ではなくラテン語 tener「柔らかい」から（別の根 tener へ移した）")
P["tend"]["src"].pop()  # 記録不要（上の行は確認用）
# 修正: 比較の -er
FIX = {"former": ["first", "-er(2)"], "elder": ["old", "-er(2)"], "further": ["fore", "-er(2)"], "inner": ["inn", "-er(2)"],
       "purpose": ["pro-", "paus"], "tender": ["tener"]}
WD = {w["id"]: w for w in d["words"]}
for k, v in FIX.items():
    print("fix", k, WD[k]["parts"], "->", v); WD[k]["parts"] = v
WD["tender"]["literal"] = "か弱い（ラテン語 tener）"
WD["purpose"]["literal"] = "前に置くこと（古フランス語 porposer）"
N = [
 ("gate", "geat", "門", "古英語 geat「門・開口部」から"),
 ("hat", "haet", "帽子", "古英語 hæt「頭巾」から"),
 ("hit", "hitta", "打つ・当たる", "行き当たる（古ノルド語 hitta）"),
 ("hurry", "hurr", "急ぐ", "慌てて動く"),
 ("knife", "knifr", "ナイフ", "古ノルド語 knīfr「小刀」から"),
 ("knot", "cnotta", "結び目", "古英語 cnotta「結び目」から"),
 ("lamb", "lamb", "子羊", "古英語 lamb「子羊」から"),
 ("lot", "hlot", "くじ・たくさん", "くじ・分け前（古英語 hlot）"),
 ("narrow", "nearu", "狭い", "古英語 nearu「狭い」から"),
 ("pack", "pak", "包み・詰める", "包み・荷"),
 ("package", "pak,-age", "小包", "包んだもの"),
 ("pool", "pol", "プール・水たまり", "古英語 pōl「池」から"),
 ("guess", "gissen", "推測する", "（考えを）つかみ取る"),
 ("gun", "gunn", "銃", "女性名 Gunnhildr（戦い＋戦い）"),
 ("less", "laes", "より少ない", "より小さい"),
 ("least", "laes", "最も少ない", "最も小さい（古英語 lǣsest）"),
 ("lesser", "laes,-er(2)", "より小さい方の", "より少ない＋さらに比較"),
 ("leather", "lether", "革", "古英語 leðer「革」から"),
 ("mad", "gemaed", "気が狂った・怒った", "変えられた（気がふれた）"),
 ("neck", "hnecca", "首", "古英語 hnecca「首」から"),
 ("nut", "hnutu", "木の実", "古英語 hnutu「木の実」から"),
 ("goal", "gol", "目標・ゴール", "境界・限界（中英語 gol）"),
 ("jump", "jump", "跳ぶ", "（擬音的か）"),
 ("hero", "heros", "英雄", "半神（ギリシア語 hērōs）"),
 ("huge", "ahuge", "巨大な", "古フランス語 ahuge「巨大な」から"),
 ("park", "parc", "公園", "囲い地"),
 ("pot", "pott", "鍋・つぼ", "俗ラテン語 *pottus「つぼ」から"),
 ("powder", "pulv", "粉", "ちり（ラテン語 pulvis）"),
 ("pale", "pall", "青白い", "青ざめた（ラテン語 pallidus）"),
 ("pallid", "pall,-id", "青ざめた", "青ざめている"),
 ("pocket", "poke", "ポケット", "小さな袋"),
 ("polite", "polire", "礼儀正しい", "磨かれた"),
 ("polish", "polire", "磨く", "磨く（ラテン語 polīre）"),
 ("pour", "pouren", "注ぐ", "中英語 pouren「注ぐ」から"),
 ("rapid", "rap,-id", "速い", "ひったくるような"),
 ("rescue", "re-,ex-,quat", "救助する", "振り払って（取り戻す）"),
 ("pause", "paus", "休止", "止まること（ギリシア語 pausis）"),
 ("pose", "paus", "ポーズ・提起する", "置く（← 休ませる）"),
 ("compose", "con-,paus", "構成する・作曲する", "共に置く"),
 ("propose", "pro-,paus", "提案する・結婚を申し込む", "前に置く"),
 ("repose", "re-,paus", "休息", "休ませる"),
 ("restaurant", "re-,sta,-ent", "レストラン", "元気を回復させる（もの）"),
 ("ruin", "ru", "破滅・廃墟", "崩れ落ちること"),
 ("sail", "segl", "帆・航海する", "（切った）布"),
 ("shake", "sceacan", "振る・揺れる", "古英語 sceacan「揺り動かす」から"),
 ("shame", "scamu", "恥", "（顔を覆う）恥"),
 ("silk", "seric", "絹", "セーレス人の（布）"),
 ("smooth", "smoth", "滑らかな", "古英語 smōð「滑らかな」から"),
 ("soap", "sape", "石けん", "滴るもの・樹脂"),
 ("soup", "sup", "スープ", "汁に浸したパン"),
 ("sour", "sur", "酸っぱい", "古英語 sūr「酸っぱい」から"),
 ("spoon", "spon", "スプーン", "木片"),
 ("steal", "stelan", "盗む", "古英語 stelan「盗む」から"),
 ("steel", "stahl", "鋼", "しっかり立つもの"),
 ("sweep", "swapan", "掃く", "古英語 swāpan「掃く」から"),
 ("tall", "getael", "背の高い", "すばやい・有能な（古英語 getæl）"),
 ("thief", "theof", "泥棒", "古英語 þēof「泥棒」から"),
 ("theft", "theof,-th", "盗み", "盗むこと"),
 ("throat", "throte", "のど", "古英語 þrote「のど」から"),
 ("tight", "thiht", "きつい", "密な"),
 ("tower", "turr", "塔", "ラテン語 turris「塔」から"),
 ("ugly", "uggr,-ly", "醜い", "恐ろしいような"),
 ("wound", "wund", "傷", "古英語 wund「傷」から"),
 ("urge", "urg", "促す・衝動", "押す・迫る"),
 ("urgent", "urg,-ent", "緊急の", "押し迫っている"),
 ("upper", "upp,-er(2)", "上の", "より上の"),
 ("tune", "ton", "曲・調子", "音・調子（tone の異形）"),
 ("treasure", "the", "宝", "蓄え（ギリシア語 thēsauros）"),
]
W = {w["id"] for w in d["words"]}; skip = []
for w, ps, ja, lit in N:
    if w in W: skip.append(w); continue
    d["words"].append({"id": w, "parts": ps.split(","), "ja": ja, "literal": lit}); W.add(w)
allids = {x["id"] for x in d["parts"]}
miss = sorted({p for w in d["words"] for p in w["parts"] if p not in allids}); assert not miss, miss
def block(key): return '  "' + key + '": [\n' + ",\n".join("    " + json.dumps(x, ensure_ascii=False) for x in d[key]) + "\n  ]"
head = ",\n".join("  " + json.dumps(k) + ": " + json.dumps(d[k], ensure_ascii=False) for k in ("version", "about", "sources"))
txt = "{\n" + head + ",\n" + ",\n".join(block(k) for k in ("categories", "branches", "pie", "parts", "words")) + "\n}\n"
json.loads(txt); open(PATH, "w").write(txt)
print("skipped", skip)
print("PIE", len(d["pie"]), "| parts", len(d["parts"]), "| words", len(d["words"]), "(+%d)" % (len(N) - len(skip)))
