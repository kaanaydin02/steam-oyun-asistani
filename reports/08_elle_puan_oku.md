# 08 · Elle puanlama: gpt-6-luna v5 (hakem puanı gizli)

Puan: **2** doğru ve eksiksiz · **1** ana cevap doğru ama eksik/küçük hata · **0** yanlış, uydurma ya da ciddi kural ihlali


---

## S1 · Baldur's Gate 3'ün Steam puanı ve oy sayısı nedir?


**Kontrol:** olumlu_oran ve oy_sayisi referansla aynı olmalı  
**Beklenen araç:** ['oyun_bul']


**Referans:**

SQL REFERANSI:
app_id,ad,olumlu_oran,oy_sayisi
1086940,Baldur's Gate 3,0.968,669941



**Agent'ın araçları:** ['oyun_bul', 'sql_calistir']


**Cevap:**

Baldur’s Gate 3’ün Steam puanı **%96,8 olumlu**, oy sayısı **669.941**. Steam oylarına göre.


---

## S2 · 100 binden fazla oy almış kaç oyun var?


**Kontrol:** sayı referansla aynı olmalı (COUNT ile)  
**Beklenen araç:** ['sql_calistir']


**Referans:**

SQL REFERANSI:
oyun_sayisi
82



**Agent'ın araçları:** ['sql_calistir']


**Cevap:**

100 binden fazla oy almış **82 oyun** var.


---

## S3 · Türkçe destekleyen en yüksek puanlı korku oyunları hangileri?


**Kontrol:** oy ≥ 1000 + orana göre sıralama; ilk oyunlar referansla örtüşmeli  
**Beklenen araç:** ['sql_calistir']


**Referans:**

SQL REFERANSI:
app_id,ad,olumlu_oran,oy_sayisi,dil_spam
2070550,A Castle Full of Cats,0.994,3709,0
1361320,The Room 4: Old Sins,0.986,15253,0
2291850,Underground Blossom,0.984,5713,0
546560,Half-Life: Alyx,0.983,92558,0
1292940,Cube Escape Collection,0.983,6286,0
1999360,Placid Plastic Duck Simulator,0.98,15900,0
2763670,Arctic Eggs,0.974,2111,0
1281800,Samsara Room,0.973,8712,0
1332010,Stray,0.973,146316,0
2475490,Mouthwashing,0.973,10171,0



**Agent'ın araçları:** ['sql_calistir', 'sql_calistir', 'sql_calistir']


**Cevap:**

En yüksek puanlılar arasında şunlar var. **En az 1.000 Steam oyu alan**, Türkçe dil desteği beyan edilmiş ve “Horror” etiketi bulunan oyunları olumlu oy oranına göre sıraladım:

- **A Castle Full of Cats** — %99,4 (3.709 oy)
- **The Room 4: Old Sins** — %98,6 (15.253 oy)
- **Underground Blossom** — %98,4 (5.713 oy)
- **Half-Life: Alyx** — %98,3 (92.558 oy)
- **Cube Escape Collection** — %98,3 (6.286 oy)
- **Placid Plastic Duck Simulator** — %98,0 (15.900 oy)
- **Arctic Eggs** — %97,4 (2.111 oy)
- **Stray** — %97,3 (146.316 oy)
- **Mouthwashing** — %97,3 (10.171 oy)
- **Samsara Room** — %97,3 (8.712 oy)

Dayanak: Steam oylarından hesaplanan olumlu oran, “Horror” etiketi ve geliştiricinin Türkçe dil beyanı. “Horror” etiketi tek başına oyunun klasik anlamda korku oyunu olduğunu garanti etmez.


---

## S4 · Cyberpunk 2077 kaç dolar?


**Kontrol:** normal_fiyat kullanmalı, birim $ olmalı  
**Beklenen araç:** ['oyun_bul', 'sql_calistir']


**Referans:**

SQL REFERANSI:
app_id,ad,fiyat,normal_fiyat,indirim_yuzde
1091500,Cyberpunk 2077,29.99,59.98,50



**Agent'ın araçları:** ['oyun_bul', 'sql_calistir']


**Cevap:**

Cyberpunk 2077’nin normal fiyatı **59,98 $**. Verinin toplandığı günkü fiyatı **29,99 $**; indirimli olabilir.


---

## S5 · En çok Türkçe yorum alan 5 oyun hangisi?


**Kontrol:** tr_yorum_sayisi sütunu (ya da yorumlar.dil = 'tr'); liste referansla aynı olmalı  
**Beklenen araç:** ['sql_calistir']


**Referans:**

SQL REFERANSI:
app_id,ad,tr_yorum_sayisi
1293830,Forza Horizon 4,29787
261550,Mount & Blade II: Bannerlord,24929
239140,Dying Light,12207
1238840,Battlefield™ 1,12182
1583320,Pro Soccer Online,7947



**Agent'ın araçları:** ['sql_calistir']


**Cevap:**

Veri setine göre en çok Türkçe yorum alan 5 oyun:

1. **Forza Horizon 4** — 29.787
2. **Mount & Blade II: Bannerlord** — 24.929
3. **Dying Light** — 12.207
4. **Battlefield™ 1** — 12.182
5. **Pro Soccer Online** — 7.947

Dayanak: Steam oyun verisindeki Türkçe yorum sayıları.


---

## S6 · İnternetten arkadaşlarla birlikte oynanabilen kaç oyun var?


**Kontrol:** kategori 'Online Co-op' olmalı; sayı referansla aynı  
**Beklenen araç:** ['sql_calistir']


**Referans:**

SQL REFERANSI:
oyun_sayisi
3895



**Agent'ın araçları:** ['sql_calistir']


**Cevap:**

Veri setinde **3.895 oyun** internetten birlikte oynama özelliğine sahip olarak listeleniyor. Sayım, Steam’de **“Online Co-op”** kategorisi bulunan oyunlara göre yapıldı.


---

## R1 · Baldur's Gate 3 hakkında oyuncular ne düşünüyor?


**Kontrol:** puan oyun_bul'dan (%96,8); ozetle modu; artı ve eksiler referans yorumlarda geçmeli  
**Beklenen araç:** ['oyun_bul', 'yorum_ara']


**Referans:**

ARAÇ REFERANSI:
ÖZET: örneklemde 200 yorum var (olumlu 194, olumsuz 6). Bu oran genel puan değildir, genel puanı SQL'den al. Aşağıdakiler oyunu değerlendiren en faydalı yorumlar.

=== OLUMLU ===
[app_id=1086940 | olumlu | dil=en | 2023-11-30 | faydalı=8300]
➤ No microtransactions➤ No DRM➤ TONS of content (100+ hours without lazy and repetitive content)➤ TONS of choices, consequences and different ways to play➤ Amazing writing➤ Amazing attention to details➤ Amazing voice acting➤ Best written companions, in-depth characters➤ Beautiful graphics, great animations and facial animations➤ Good NPCs design➤ Single-Player! (optional co-op)➤ Devs listening to feedback and releasing quick updates➤ No CLOWNS in community!Game of the Year!PLEASE Larian never change!BIG full game + Made with LOOOVE!Learn Blizzard, Bethesda, EA, WB, Ubisoft

[app_id=1086940 | olumlu | dil=en | 2023-07-20 | faydalı=8067]
I had no intention of playing Baldur's Gate 3; I barely played 1 and missed 2.  And I just don't have 200 hours to sink into an 80 GB RPG at my age.  I enjoyed Divinity: Original Sin and couch co-op'd with my wife in D:OS 2, but we have a mortgage and a dog and no time.Then I read the Tweet.  You know the one: the prominent game developer who said that we cannot allow Larian to define our expectations of RPGs.  Oh, really?  I immediately bought the game and spent hours downloading it out of pure, unadulterated spite.I am 3 hours in.  Three.  I am blown away.  I spent the first hour creating my character.  I pulled out my Dungeons & Dragons 5th Edition Player's Handbook and marveled at what BG3 had enabled me to do - this is the full blown 5E character creation.  The maniacs at Larian  took Divinity: Original Sin and made it into D&D 5E, full stop.  Amazing.And then I played for a couple of hours.I haven't fallen in love with a game like this since Dragon Age: Origins and there is so much more depth to BG3 in the short time I've played.  Case in point: I found a lockpick, broke into a crypt, looted a burial site and was promptly incinerated by a flame trap over a greased floor.  Tha [kesildi, toplam 3364 karakter]

[app_id=1086940 | olumlu | dil=zh | 2023-08-25 | faydalı=6716]
因为我右手有一定的残疾 回合制游戏是最合适我玩的游戏 这款游戏超长的剧情我很喜欢  如果后期有任何DLC我都会第一时间购买 这是我第二款全价购买的游戏 希望拉瑞安工作室越来越好

[app_id=1086940 | olumlu | dil=en | 2023-08-13 | faydalı=3967]
The experience playing this game is like eating a medium-rare steak after years of eating out of dumpsters.

[app_id=1086940 | olumlu | dil=zh | 2023-08-12 | faydalı=3748]
很好玩，可惜人生不是博德之门。那些足以改变命运的抉择时刻，没有骰子可以碰运气，也出现得一点都不隆重，更不会有BGM提醒你，甚至在悄无声息或莫名其妙中就决定了

[app_id=1086940 | olumlu | dil=en | 2023-09-28 | faydalı=3510]
---{ Graphics }---☐ You forget what reality is☑ Beautiful☐ Good☐ Decent☐ Bad☐ Don‘t look too long at it☐ MS-DOS---{ Gameplay }---☑ Very good☐ Good☐ It's just gameplay☐ Mehh☐ Watch paint dry instead☐ Just don't---{ Audio }---☑ Eargasm☐ Very good☐ Good☐ Not too bad☐ Bad☐ I'm now deaf---{ Audience }---☐ Kids☑ Teens☑ Adults☐ Grandma---{ PC Requirements }---☐ Check if you can run paint☐ Potato☐ Decent☑ Fast☐ Rich boi☐ Ask NASA if they have a spare computer---{ Difficulty }---☐ Just press 'W'☐ Easy☐ Easy to learn / Hard to master☑ Significant brain usage☐ Difficult☐ Dark Souls---{ Grind }---☐ Nothing to grind☐ Only if u care about archivement☑ Isn't necessary to progress☐ Average grind level☐ Too much grind☐ You'll need a second life for grinding---{ Story }---☐ No Story☐ Some lore☐ Average☐ Good☐ Lovely☑ It'll replace your life---{ Game Time }---☐ Long enough for a cup of coffee☐ Short☐ Average☑ Long☐ To infinity and beyond---{ Price }---☐ It's free!☑ Worth the price☐ If it's on sale☐ If u have some spare money left☐ Not recommended☐ You could also just burn your money---{ Bugs }---☐ Never heard of☑ Minor bugs☐ Can get annoying☐ ARK: Survival Evolved☐ The game itself is a big terrarium  [kesildi, toplam 1255 karakter]

=== OLUMSUZ ===
[app_id=1086940 | olumsuz | dil=en | 2023-08-04 | faydalı=3872]
WARNING LOW VISION PLAYERS, or any player needing larger UI & font/text size & scaling for your setup...Game currently has no accessibility option for increasing UI/font/text size!There is an option for dialog text size, but not for majority of other text in UI menus, tooltips, etc. which is more critical to read during gameplay, since the dialog has voice acting anyway.This makes me very sad & disappointed as a low vision disabled player because I really enjoy these types of games and wanna play this highly anticipated game, but currently cannot because it strains my eyes too much trying to read the tiny text everywhere.I hope to update my review to Recommend once larger UI/font/text size is supported, and I really wish developers are more inclusive & mindful of disabled people as a launch priority rather than some backlog feature months/years later -- not everyone can see/hear/control games in a single "standard" experience, and it further reinforces the treatment of disabled gamers' needs as inferior & unimportant.

[app_id=1086940 | olumsuz | dil=en | 2023-09-16 | faydalı=17]
I get that a lot of people really love this game, and think it's the best thing ever.  I disagree.  It's ... adequate.  Barely.  Granted, it has some good voice acting, and a decently complex plot.  However, there are so many terrible things that just can't be made up for.  The pathing is absolutely atrocious.  Collision detection is a bad joke.  I'm about 60% through, and I've never once NOT had to fight the damned camera to see what's going, or where I need to click to move.  Seriously... at least put a vertical control and a straight zoom on it... it's just infuriating.  Just trying to walk around inside a building is a constant battle by itself, because you're constantly clicking on things between the camera and the floor that make your character go the opposite direction.  The game starts slowing down when there are too many interactable objects or characters around, and yet there are literally thousands of empty, useless containers scattered everywhere, and dozens of NPC's that serve absolutely no purpose except atmosphere... all of which slows the game down, and bloats the save files even more.Finally, the "dice".  I have no clue what the hell is going on with the RNG, but i [kesildi, toplam 2890 karakter]

[app_id=1086940 | olumsuz | dil=ja | 2024-07-10 | faydalı=17]
・制作の意図した狭いストーリーテリングを押し付けられ、そこから外れた行動を取るとフラグ管理が破綻し、場合によってはバグで詰む。・探索と戦闘に無駄な労力を求められる一方、肝心なTRPGにおけるRPやシナリオ展開に自由度はない。・全てのクエストに「YES」と答えないと、ストーリーの全貌どころかあらすじすら掴めない、不親切で出来の悪いリニア。・このゲームにおける「分岐」とは「クエストの消失」でしかない。◯善悪の2通りの分岐すらままならない不良品・巷では「1万7000通りのED」との謳い文句があるが、1プレイヤーから見た1通りの物語は崩壊している。クエストはプレイヤーの選択を無視して突発的に発生、或いは時限性で消失するため、ストーリー展開に蓋然性がなく、プレイしていて没入感が損なわれる。・コンパニオンを殺害したところで戦力と関連クエストが消失するだけで、違ったプレイフィールが得られるわけではない。・クエストギバーなNPCが多く、死亡させるとシナリオに齟齬が生じる。代替キャラや後任キャラは存在しない。・キャラのセリフは1パターンのみで時系列が反映されず矛盾だらけ。敵対や親密度に依存した変化や差分がない。・勧誘すらしていないコンパニオン候補キャラの敵対勢力に協力したところ、該当キャラと面識すらない他のコンパニオンに「裏切り」と罵られる。対して、敵に拐われたコンパニオンを見殺しにしても言及なし。・お使いクエストから帰ってきたところ、ファストトラベルを使用した1分足らずの間に不法侵入扱いになり、過去に命を救って友好関係になった中立モブと敵対した。逆に、プレイヤーキャラが目の前で同胞を殺しても敵対せず、平気で「別の仲間の救出クエスト」を依頼する中立モブもいる。再現性あり。・盗みも殺しも不法侵入もしていないのに友好集落が突然敵対→戦闘に。不審に思い数分前のデータから再開→同じルートを通るも [...] 出クエスト」を依頼する中立モブもいる。再現性あり。・盗みも殺しも不法侵入もしていないのに友好集落が突然敵対→戦闘に。不審に思い数分前のデータから再開→同じルートを通るも再現性なし。別の場所でも定期的に同様の現象あり。・捕虜3組を解放するクエストがあり、全員まとめて船で護送したところ、うち1組のみ達成にならず、何処までもついてくるせいでファストトラベルも「野営地」も利用できなくなり詰んだ。どうやら「徒歩で脱出」或いは「1組のみで脱出」させる以外の分岐を想定していないらしい(パッチ7で修正予定とのこと◯不便な故に無駄に要求されるプレイ時間・とにかくバグや意図しない挙動が多いためリプレイ性()が高い。・ロードが地味に長い。戦闘時、敵AIが長考する。範囲魔法などもラグい(4060 ti / i5 14世代・探索時はダッシュどころかスプリントやブリンクすらない。戦闘中も早送り機能がなく、敵 [kesildi, toplam 4605 karakter]


**Agent'ın araçları:** ['oyun_bul', 'sql_calistir', 'yorum_ara']


**Cevap:**

Oyuncuların genel görüşü çok olumlu: Steam oylarının **%96,8’i olumlu**. Örneklemdeki **200 yorumun 194’ü olumlu, 6’sı olumsuz**.

Olumlu yorumlarda en çok öne çıkanlar hikâye ve karakter yazımı, seçimlerin sonuçları, seslendirme ve ayrıntılı rol yapma deneyimi. Olumsuz yorumlarda ise küçük arayüz yazıları, kamera ve karakterlerin yol bulması gibi kullanım sorunları dile getirilmiş.

Dayanak: Steam’de **669.941 oy**; yorum özeti, 2024 sonuna kadarki **200 yorumluk örneklemden**. Yorum kapsamı oyların %7,7’si olduğundan yorumlar tüm oyuncuları temsil etmeyebilir.


---

## R2 · Elden Ring'de oyuncular en çok neyi eleştiriyor?


**Kontrol:** olumsuz yorumlara bakmalı (olumlu=0 ya da ozetle); eleştiriler referansta geçmeli  
**Beklenen araç:** ['oyun_bul', 'yorum_ara']


**Referans:**

ARAÇ REFERANSI:
KONU ARAMASI: 5 yorum, en ilgiliden aşağı. Mesafe 0.45 üstü = zayıf eşleşme, kanıt sayma.

[app_id=1245620 | olumsuz | dil=pt | 2022-03-13 | faydalı=20 | mesafe=0.377]
acontecer em QUALQUER hardware. Meu pc excede os requisitos recomendados, está recém formatado e atualizado e ainda sim tem problemas de performance. Enquanto meu amigo com 8GB de RAM, um quad core e uma 1050ti não tem metade dos problemas. Isso que eu nem falei sobre os controles, suporte a monitores e outras funções básicas em um jogo atual.- Bugs que quebram a imersão do jogo completamente ex: seu personagem ficando preso, se teletransportando/morrendo do nada, boss se matando no meio da luta porque ficou preso em uma pedra (???), exploit que deixam o jogador AINDA MAIS OVERPOWER do que é possível jogando normalmente. Problemas mais sérios como sessões online sendo canceladas do nada, isso é, QUANDO o server online do jogo quer funcionar. Jogo crashando aleatóriamente dentro e fora do multiplayer (que pode resultar em um soft ban do modo online, o que é um absurdo). Relatos de amigos perdendo o save mesmo o jogo tendo suporte na nuvem, tem gente que não consegue nem abrir o jogo.Os desenvolvedores do jogo dizem que essa obra é um mesclado de tudo que a From Software aprendeu até agora, e infelizmente, eles não aprenderam a fazer um port que presta. Duas semanas após o lançamento [kesildi, toplam 2145 karakter]

[app_id=1245620 | olumsuz | dil=zh | 2024-06-30 | faydalı=9 | mesafe=0.42]
2/5分，其中一分给美术组和音乐组，一分给双月、梅瑟莫和米德拉。场景面积、怪物数量和收获的道具不成比例，大而空场景里奖励少得可怜。Buff机制配合boss数值的飙升逼迫玩家舔图收集道具，然而引导一如既往的弱。尽管诸多场景非常漂亮，但魂系的本质不能让它成为一个轻松愉悦的拍照散步模拟器。玩家不得不在大地图里探索，忍受一本道或者匪夷所思的地图设计逻辑，收获与付出不对等的垃圾。强烈的攻击欲望，自本体就有的读指令，时常离奇的判定和多动症让不少boss成为粪怪，过亮的光效和经常丢视野的aoe和飞天更是玩家意料之外的惊喜口牙！此处不提被反复提起的数值和交互的问题，况且和boss你打你的，我打我的本就无聊不好玩。打到最后完全失去耐心，已经丧失当初探索本体的新鲜刺激感，谁爱玩谁玩吧，我只能说刚出第一天就买来吃屎的我是纯纯的小丑。

[app_id=1245620 | olumsuz | dil=en | 2022-02-24 | faydalı=10159 | mesafe=0.422]
2 years later and this game still has stuttering issues, is still locked at a 16:9 aspect ratio, and still has an awful anti-cheat systemA great game that is hampered by a poor port

[app_id=1245620 | olumsuz | dil=zh | 2024-06-23 | faydalı=5 | mesafe=0.442]
如果说本体很好的掩盖了boss设计就是一坨狗粪的缺陷的话，DLC就是完美的把这坨狗粪甩在了你的脸上，大又空的地图，根本没走心的物品和篝火放置，和人物数值DLC成长数值彻底脱节的怪物数值，三板斧赖皮招式无限高欲望复读的boss，毫无成就感和获得感的地牢探索。。。我的老天，简直就是灾难。我只能说，你没做好你就慢慢做，别赶工出一个半成品出来糊弄人。

[app_id=1245620 | olumsuz | dil=en | 2022-02-24 | faydalı=8028 | mesafe=0.458 ZAYIF EŞLEŞME]
Unfortunate i have to give everyone a big warning before buying the game. The game is not well optimised at least for the PC, and while the frame rate in enclosed areas is very stable, it will constantly stutter in open areas, from which the game will have many, since as the trailers show, you will even be able to ride on this big worldmap. Especially when a Boss makes a special move. Since Elden Ring is a game where you have to dodge/react to the opponents attacks in under a secound, this makes Bossfights frustrating beyond believe and honestly kinda unplayable at least in my eyes. I dont mind having to try a boss over and over because i make a mistake, but constantly dying, because the game freezes for 1 secound so i couldnt see which type of attack the boss is throwing at me is not the kind of challenge i am looking forward to. I hope that one of the first Patches will fix the horrible stutter problems that the game currently has, and i am really sure that once the problems are fixed, that the game will be absolutly amazing. But as for now, if you are still thinking if you should buy the game or not, i would highly recommend to wait for a while.


**Agent'ın araçları:** ['oyun_bul', 'yorum_ara', 'sql_calistir']


**Cevap:**

Elden Ring’de en çok öne çıkan eleştiri **PC sürümünün performansı ve optimizasyonu**: oyuncular takılma/kare hızı sorunlarının, özellikle açık alanlarda ve boss dövüşlerinde, oyunu zorlaştırdığını söylüyor. Bazı yorumlarda **anti-cheat sistemi** ve **16:9 en-boy oranı kısıtlaması** da eleştiriliyor.

Dayanak: Örneklemdeki 200 yorumun olumsuz olanlarında bu şikâyetler öne çıkıyor; yorum kapsamı oyların %1,4’ü olduğu için bunlar tüm oyuncuların görüşünü temsil etmeyebilir. Steam oylarına göre genel olumlu oranı %92,6.


---

## R3 · Dying Light'ta geceler gerçekten korkutucu mu?


**Kontrol:** konu modu; ZAYIF EŞLEŞME ve ironik yorumlar kanıt sayılmamalı  
**Beklenen araç:** ['oyun_bul', 'yorum_ara']


**Referans:**

ARAÇ REFERANSI:
KONU ARAMASI: 5 yorum, en ilgiliden aşağı. Mesafe 0.45 üstü = zayıf eşleşme, kanıt sayma.

[app_id=239140 | olumlu | dil=en | 2015-01-31 | faydalı=684 | mesafe=0.366]
"The Walking Dead" by day, "I Am Legend" by night;I can't tell you how beautiful this game looks without you just seeing it for yourself,  but I will say this.This is the first game, in a very long time, which has legitamately inspired a sense of fear in me.At night time, this game becomes a heart pounding nightmare.Like horror? Play this game.

[app_id=239140 | olumlu | dil=en | 2015-01-28 | faydalı=1887 | mesafe=0.45]
and the graphics and effects are wonderful. For an ugly game, the visuals are surprisingly beautiful.Sound:Music is great, but my only comment is that the music that plays when you're outside has one part where a random singer begins to chant, and I swear it scares the crap out of me every time. Bashing biters with blunt weapons sounds very satisfying, and you can tell when you've hit the right spot, while hitting the chest is usually a muffled thump. I've yet to get a gun though (I've spent a lot of time just wandering around so I'm not too far into the campaign) so I can't comment on that. Also, make a little bit more noise and you'll hear bone-chilling screams in the distance of the more agile biters coming to get you. Very satisfying sound work overall.Story:I haven't gotten far into the story so I'll hold off until I've completed it to fill this section.I basically wanted to come out and say how much I'm enjoying this game and to tell people to ignore the false statements about this game and give it a try. If you liked Dead Island, you'll like this game. If you hated Dead Island, you'll like this game. If you're a fan of first person, open-world games, then I'd bet you'll like [kesildi, toplam 1211 karakter]

[app_id=239140 | olumlu | dil=cs | 2018-02-06 | faydalı=6 | mesafe=0.456 ZAYIF EŞLEŞME]
První půl hodinka této hry byla nudná a nezábavná, ale to jse změnilo po té co jste vyšli ven z "věže" a rozjebávali jste nohou od stolu květákožroutům hlavy. Najdou se zde Jupmscary, ze kterých jsem se málem posral. Hru doprovází strašidelné zvuky např. řvaní zombíku, kteří se stanou postupem času, jako osina v prdeli. Do toho mě jebe, tento soundtrack:  .  Hru jsem si bezvadně užil!!  DOPORUČUJI!!!!

[app_id=239140 | olumlu | dil=zh | 2018-10-30 | faydalı=1 | mesafe=0.472 ZAYIF EŞLEŞME]
好玩，就是有点难，夜魔一直让人慌，妈蛋，打到旧城区还是怕夜魔

[app_id=239140 | olumlu | dil=en | 2018-05-12 | faydalı=517 | mesafe=0.474 ZAYIF EŞLEŞME]
Player Bases.☐ Kids.☐ Everyone.☑ Mature.☐ Casual Players.☐ Pro players.Graphics.☐ Potato.☐ Really Bad.☐ Bad.☐ OK.☐ Good.☑ Beautiful.☐ Masterpiece.Price.☑ Full Price.☐ Wait For Sale.☐ Refund It If You Can.☐ Don't Buy It.☐ Free.Requirements.☐ Minimum.☑ Medium.☐ Fast.☐ High End.☐ Super Computer.Difficulty.☐ Easy.☑ Medium.☐ Hard.☐ Very Hard.☐ Death March.☐ Dark Souls.Game length.☐ Really Short. ( 0 - 3 hours)☐ Short. ( 2 - 8 hours)☐ Medium. ( 8 - 16 hours)☑ Long. ( 16+ hours)☐ Endless.Story.☐ It Doesn't Have One.☐ Horrible.☐ Ok.☐ Average.☑ Good.☐ Fantastic.Cinematic/Art.☐ It Doesn't Have.☐ Horrible.☐ Ok.☐ Average.☑ Good.☐ Like Watching A Movie.Music/Sound.☐ Horrible.☐ Decent.☐ Average☐ Good☑ Amazing.Gameplay.☐ Terrible. ☐ Ok.☐ Average.☑ Good.☐ Fantastic.Bugs.☐ Game Itself Is One Big BUG.☐ Game Breaking Bugs.☐ Lots of bugs.☐ Few Bugs.☑ Nothing.Others.Multiplayer: ☑Singleplayer: ☑Final Score:8/10Dying light is a well-rounded game that I have a lot of positives to say about. The visuals are great for a 3-year-old game and the zombies look scary and realistic. The gameplay is very fun with the parkour aspect being prioritized and the loot system is very interactive and indulging. Now, sinc [kesildi, toplam 1805 karakter]


**Agent'ın araçları:** ['oyun_bul', 'oyun_bul', 'sql_calistir', 'yorum_ara']


**Cevap:**

Evet—**Dying Light’ın geceleri birçok oyuncuya gerçekten korkutucu ve gerilimli geliyor.** Yorumlarda gece olunca yaratıkların ortaya çıkması, güvenli bölgeye yetişme telaşı ve Volatile’lardan kaçma özellikle öne çıkıyor. Bir oyuncu geceyi “kalp çarptıran bir kâbus” diye anlatmış; ancak korku eşiği kişiden kişiye değişir.

Dayanak: Steam oylarına göre genel olumlu oranı **%95,2** (435.283 oy). Gece gerilimine dair yorum aramasında ilgili örnekler bu hissi destekliyor; yorumlar tüm oyuncuların görüşünü temsil etmeyen bir örneklemdir.


---

## R4 · Cyberpunk 2077'deki bug'lar zamanla azaldı mı?


**Kontrol:** hepsi modu; yıllara göre karşılaştırma; 'örneklemdeki N yorum' diye anlatmalı  
**Beklenen araç:** ['oyun_bul', 'yorum_ara']


**Referans:**

ARAÇ REFERANSI:
SAYIM: örneklemdeki 200 yorumun 19'i konuya yakın. LLM etiketi: {'evet': 15, 'hayir': 4}. evet = soruya evet diyor, hayir = konuya değinip hayır diyor. Sayılar örneklemden, Steam'in tamamı için mutlak sayı söyleme. Kaçırılan yorum olabilir, oranı 'en az' diye oku.

Yıllara göre:
yil,evet,hayir
2020,8,1
2021,5,1
2023,2,1
2024,0,1

Örnekler:

(evet: Yorum oyunda çok sayıda ve ilerlemeyi engelleyen buglardan bahsediyor)
[app_id=1091500 | olumlu | dil=tr | 2023-11-19 | faydalı=10 | mesafe=0.268]
rtx4060 32 ram i7 13. nesil işlemci ile ara ara fps düşüşlerine tanık olmamın haricinde optimizasyon olarak bir hata ile karşılaşmadım.Oyun hala bug dolu bir sürü acayip saçma bugla karşılaştım ( oyun ilerlemesini engelleyen buglar bile)Evren çok güzel tasarlanmış kurgulanmış lakin içi boş hissettir [kesildi, toplam 1076 karakter]

(evet: Yorum oyunda çok sayıda ve kötü buglar olduğunu söylüyor)
[app_id=1091500 | olumsuz | dil=zh | 2020-12-17 | faydalı=4 | mesafe=0.312]
你bug多也就算了，还有这么多影响主线的恶性bug，快把我恶心死了

(evet: Yorum oyunda çok bug olduğunu açıkça belirtiyor.)
[app_id=1091500 | olumsuz | dil=en | 2021-08-30 | faydalı=6 | mesafe=0.339]
This game has so much potential....story was fantastic, the game was beautiful...only to be ruined by bugs. Even with the new 1.3 patch, not much has changed. It is what it is i guess. I suggest for people who don't have the game, wait for maybe 1-2 years. Bugs just ruin the experience for me

(hayir: Yorumda bug bulunmadığı belirtilmiş, sorun yok denmiş.)
[app_id=1091500 | olumlu | dil=zh | 2023-11-02 | faydalı=4 | mesafe=0.375]
虽然是预售买的，因为工作原因一直没时间玩，现在在玩居然没发现一个BUG，以后买游戏真不急着玩首发了，地球ol难度太高，小游戏还是等打磨好在慢慢玩吧，工作就够糟心的，还是别给自己找不痛快。

(hayir: Yorumda oyun kırıcı bug olmadığı belirtilmiş)
[app_id=1091500 | olumlu | dil=en | 2024-02-02 | faydalı=3 | mesafe=0.419]
Great graphics, and atmosphere. Decent storytelling, combat system, music (some songs were great, especially in the DLC, some were awful), and attention to many little details is greatly appreciated. Wish there would be more romance and dialog options and some dialog options being more self-descript [kesildi, toplam 590 karakter]

(hayir: Yorum bugları komik buluyor, sorun olarak görmüyor)
[app_id=1091500 | olumlu | dil=en | 2021-03-13 | faydalı=4 | mesafe=0.43]
Sorry nerds, this game actually owns.I haven't been able to find a good ending but the in between has some amazing character development.The story hit me for personal reasons; the main question of "are we nothing more than the meat of our bodies" has troubled me from a very early age, even before th [kesildi, toplam 580 karakter]


**Agent'ın araçları:** ['oyun_bul', 'oyun_bul', 'sql_calistir', 'oyun_bul', 'oyun_bul', 'oyun_bul', 'oyun_bul', 'oyun_bul']


**Cevap:**

Evet, **oyuncu yorumlarındaki olumlu değerlendirmeler zamanla artmış**: 2020–2021 dönemindeki yorumların %68,6’sı olumlu iken, 2022’de %81,5’e, 2023’te %84,6’ya ve 2024’te %94,2’ye çıkmış.

Bu, bug’ların doğrudan sayımından değil, dönemlere göre yorumların olumlu olma oranından çıkarılabilecek bir işaret; dolayısıyla **oyuncu deneyiminin iyileştiğini düşündürüyor**, ama tek başına bug’ların azaldığını kanıtlamıyor. Bu oranlar elimizdeki yorum örneklemine dayanıyor; genel Steam puanı ise %83.


---

## R5 · Türk oyuncular Mount & Blade II: Bannerlord hakkında ne diyor?


**Kontrol:** dil='tr' filtresi kullanılmalı; Türkçe yorumlara dayanmalı  
**Beklenen araç:** ['oyun_bul', 'yorum_ara']


**Referans:**

ARAÇ REFERANSI:
ÖZET: örneklemde 23 yorum var (olumlu 20, olumsuz 3). Bu oran genel puan değildir, genel puanı SQL'den al. Aşağıdakiler oyunu değerlendiren en faydalı yorumlar.

=== OLUMLU ===
[app_id=261550 | olumlu | dil=tr | 2020-03-30 | faydalı=1503]
Ortaokulda taleworlds facebook sayfasında bannerlord haberini görüp sevinçten çılgına dönmüştüm. Üzerinden 8 sene geçti ve hala aynı duygular içerisindeyim :)EDİT : 26 Saatte oyunu bitirdim. OLMUŞ BU OYUN..

[app_id=261550 | olumlu | dil=tr | 2020-12-07 | faydalı=862]
MUKEMMKEL BIR BANNERLORD Bir  teleworlds çalışanı olsaydım eğer Armağan Bey e söyleyeceklerim şunlar olurdu.1. Haritada köylerin şehirlerin ve kalelerin hakimiyet alanları ince ülke dış sınırları ise kalın çizgilerle belli olmalıydı.2.Her ırkın şehrine girdiğinizde kendine has bir müziği olmalıydı. Latin arap kuzeyli ..vs müzik tınıları duymalıydık.3. Sahip olduğumuz kale şehir veya köye savas dışında  girdiğimizde halk duyarsız robot gibi olmamalı ertuğrul yada osmanın obaya girmesi gibi millet işi gücü bırakıp bizi karşılamalıydı.Özellikle bir zaferden dönmüşsek kadınlar sehirlerde yolumuza çiçekler atmaliydi 4. Savaş dışında köylere şehirlere ve kalelere sadece biz ve 20 kişilik  süvari muhafız birliğimiz girmeli ve bunlar bizi temsili eden gösterişli flamalar taşımalıydı. Ordu dışarda durmalıydı.5. Tebamizin tüm dertleriyle dertlenmeli sorunlarıyla ilgilnemeliydik yada bunun için  komutanlara emir vermeliydik. 6. Sahip olduğumuz yerlerde köşk sahibi olmalı içini biz dekore edebilmeliydik. Şehrin büyüklerine ve soylular burada yemek ziyafeti verir savaş ve zenginlik ve gösteriş için bize yalanmalarini ve tebriklerini dinlerdik. Verdiğiniz gösterişli yemekler şanımızı arttırmaya  [kesildi, toplam 2911 karakter]

[app_id=261550 | olumlu | dil=tr | 2020-04-02 | faydalı=854]
YA ALLAH İÇİN ŞU OYUNA OPTİMİZASYON YAPIN BE 51 SAAT KASA KASA OYNADIM AĞZIMIN SULARI AKIYOR AMA KASINCA SİNİR OLUYORUM BE ŞUNA Bİ PATCH GETİRİN DE KASMADAN OYNAYALIM

[app_id=261550 | olumlu | dil=tr | 2020-03-30 | faydalı=734]
Yıllardır beklediğimiz, gönüllerimizin sahibi geldi. Öyleyse ilk inceleme benden olsun.Türkçe'ye çevrilmiş arkadaşlar evet, Türkçe dil seçeneğini sonradan ekleyeceklerini söylediler ancak sürpriz yaptılar. Çoğu sesler ve ortamlarda placeholder'lar kullanılmış, erken erişim sonuna kadar bunlar kendilerine özgü bir biçimde tasarlanacak. Atmosfer gerçekten harika ama grafikler bir 2020 oyununa ait değil. Ama bu kimin umrunda, hangimiz Mount & Blade serisini görsel beklentiler içerisinde oynadık? Mini harita olayı gerçekten mükemmel olmuş, savaş alanına girmeden haritada gezesi geliyor insanın. Yoldaşlar olayı geliştirilmiş. Varis olabiliyorlar, sizin ve diğer tüm lordlar gibi birlik toplayabiliyor ve hatta ölebiliyorlar. Tabi böyle olunca yoldaşlar tükenmesin diye bir ekleme de yapmışlar. Yoldaşlar oyuna ait değil, kendilerine özgü. Rastgele oluşturuluyorlar. Dinamik bir yoldaş sistemi var anlayacağınız.Kuşatma silahları geldi, evet, yıllarca sadece hareketsiz modeline baktığımız, haritanın en gerisinde kalan gereksiz kuşatma silahları artıtk hareket edebiliyor ve işlevleri var. Kale duvarlarını ve kapılarını yıkabiliyoruz. Tabi savunan taraf da savunma amaçlı büyük silahlar inşa edeb [kesildi, toplam 5114 karakter]

[app_id=261550 | olumlu | dil=tr | 2020-03-30 | faydalı=4]
Çok güzel harika grafikler akıyor beklentimi karşıladı :) Version 1.0 geldiğinde her şey dahada güzel olacak bune eminim pişman etmedi düşünmeden alabilirsiniz. Şu saatten sonra Bannerlord'dan beklentim hikaye modunda Co-op desteğinin gelmesi olacaktır bunuda yaparlarsa daha ne istenebilirki. Neyse velhasıl kelam alın aldırım Türk oyun sektörünün desteğe ihtiyacı var bu desteği sağlayın. Teşekkürler TaleWorlds bu efsaneyi bizle buluşturduğun için.

[app_id=261550 | olumlu | dil=tr | 2020-05-05 | faydalı=1]
Oyunun diğer önceki oyunlara nazaran geliştiğini görebildim ilk 7 saatlik deneyimimde ama bazı şeyleri inatlarına yapmıyorlarmış gibi geliyor. MB bir kendi hikayenizi yazma oyunu olsada görev çeşitliliği hala aynı tarzda ilerliyor sürekli farklı insanlardan aynı görevler veriliyor ve bu can sıkıcı olabiliyor. Ama ne olursa olsun bunu aldırış etmeyip büyük zevkle oynuyorum ve benim gibi bir sürü insanında benimle aynı düşüncede olduğunun kanaatindeyim. Optimize edilmesi gereken bazı şeyler var bunların patchlerle birlikte düzeltileceğini umuyorum GPU ye çok fazla yüklenme yapıyor oyun onun haricinde fazla bir sıkıntısı yok bildiğimiz mount blade

=== OLUMSUZ ===
[app_id=261550 | olumsuz | dil=tr | 2020-04-07 | faydalı=2422]
Erken erişim olduğunu göz önünde bulundurarak yazıyorum öncelikle bunu belirteyim, sonra aa ama erken erişim bu demesin kimse, biz de biliyoruz heralde.Steam 15 saat oynadığımı düşünüyor, fakat ben çıktığı günden beri her gün en az 5-6 saat oynadım en az.(çevrimdışı oynadım hep)Beni en çok üzen şeyi söyleyeyim: bu oyunda ilerlemek karakterimize hiçbir şey katmıyor. Neden bu oyunda bir yerlere gelmeye çalışıyoruz? Neden ünümüzü, nüfuzumuzu, gücümüzü yükseltmeye çalışıyoruz? Oyunda önemli biri olabilmek için değil mi? Önemli bir komutan, lord, kral hatta tüm toprakların hükümdarı olmak istiyoruz değil mi? Kötü haber: hiçbir şey olmuyor.Oyundaki karakterlerin bizimle iletişim biçimi değişmiyor. Kral oluyoruz, yine biz milletin ayağına gidiyoruz. Karakterleri bir şeylere ikna etmek için kendimizi yırtıyoruz. Hiçbir şey değilken de aynı cümleler, lord oluyorum senatoya giriyorum yine aynı cümleler, kral oluyorum hala aynı cümleler. Kral oluyorum eşraf hala benden saçma sapan görevler bekliyor bir de para veriyor allah razı olsun. Dalga mı geçiyor bu oyun? Yahu kralım ben, istesene benden vergilerle ilgili bir politika. İstesene üretimin, ticaretin önünü açacak bir icraat. Bunun için de  [kesildi, toplam 4801 karakter]

[app_id=261550 | olumsuz | dil=tr | 2020-03-31 | faydalı=6]
GTA5'İ EN YÜKSEK AYARLARDA OYNARKEN BUNU NEDEN EN DÜŞÜK AYARLARDA OYNUYORUM ?OYUNDAMI SORUN VAR YOKSA BENİM PC DEMİ

[app_id=261550 | olumsuz | dil=tr | 2023-06-23 | faydalı=0]
yarım saat bile dayanamadım iade ettim


**Agent'ın araçları:** ['oyun_bul', 'sql_calistir', 'yorum_ara']


**Cevap:**

Türk oyuncuların genel görüşü **olumlu**: Steam oylarının **%87,9’u olumlu** (253.629 oy). Türkçe yorum örnekleminde 23 yorumun 20’si olumlu, 3’ü olumsuz; bu örneklem genel puan değildir.

Olumlu yorumlarda serinin atmosferi, savaşlar ve yıllardır beklenen oyunun sonunda çıkması öne çıkıyor. Eleştirilerde ise özellikle **optimizasyon/kasma**, tekrarlayan görevler ve ilerlemenin karaktere ya da dünyaya yeterince yansımaması dile getirilmiş. Yorumlar 2020–2023 döneminden; bazı şikâyetler oyunun erken erişim dönemine ait olabilir.


---

## R6 · Stray kaç saatte bitiyor, oyuncular ne diyor?


**Kontrol:** süre yorumlardan (ya da SQL yorumcu_medyan_saat); yorumda olmayan saat uydurmamalı  
**Beklenen araç:** ['oyun_bul', 'yorum_ara']


**Referans:**

ARAÇ REFERANSI:
KONU ARAMASI: 5 yorum, en ilgiliden aşağı. Mesafe 0.45 üstü = zayıf eşleşme, kanıt sayma.

[app_id=1332010 | olumlu | dil=en | 2023-12-23 | faydalı=0 | mesafe=0.309]
Really cute and chill game, I would definetly reccomend this to whomever wants a nice chill time for themselves. It took me 4,8 hours to complete but I could see myself playing it again. The story was amazing in my opinion and the gameplay was fun aswell. If you have the money laying around, buy it!

[app_id=1332010 | olumlu | dil=en | 2024-04-30 | faydalı=0 | mesafe=0.335]
This game is special. Don't be confused by the amount of hours I spend on it, but for me it was such an amazing game I had to do it 100%, which included the hardest achievement of all, to finish the whole game in less than 2 hours, which is obviously achievable because I did it in 1.38h.Well either way the game itself, in a slow and focused playthrough took me like 6h, but it were so nice, I'm kind of sad that it's over.The story is with no doubt remarkable and so emotional. You get to know the most different npcs, which are character wise as well as the way as they got personalized, lovely to make friends and you will like doing some little pleasures for them.The game is build up in a way which I have rarely seen before. A really really beautiful environment, when it comes to graphics and the variety of the different biotopes and the interaction with the described npc is crazy, such as with your new friend. (No spoiler play it yourself)I played it on a controller and I can only recommend that. If you have one do it, it makes the game feel better and you experience it in a better way as well.Anything else I would say at this point would be a spoiler. It's honestly worth the money a [kesildi, toplam 1256 karakter]

[app_id=1332010 | olumsuz | dil=en | 2022-07-19 | faydalı=501 | mesafe=0.335]
(REVISED REVIEW AFTER MORE INFORMATION HAS BEEN GATHERED FROM COMMENTS)NOT RECOMMENDED FOR PEOPLE WITH TIGHT BUDGETSSo I do enjoy this game and I highly recommend people play it. However, due to me completing it in 6 hours while taking my time to explore every bit of content i do not recommend buying full price if you are wanting a game to take you more than a day. I usually play games like this at a SNAILS PACE, so if you play this at a normal pace, it may take about 3-4 hours (rough guess, different for everyone). This game is highly linear with only about 2 somewhat explorable areas. So if you were expecting a lengthy exploration game, as much as it pains me, this isn't that game. Replay-ability is on the low end if you were hoping to get new experiences from a second play-through.If you wan't the game and have money to spare go ahead and buy it but if your like me and don't have much to spend id recommend watching a walkthrough/ letsplay or waiting to buy on sale if you can be patient.I wanna thank all the people in the comments for providing me with information to make this a better review than it was originally i have left my old one below for context but IT IS NOT HOW I FEEL [kesildi, toplam 2146 karakter]

[app_id=1332010 | olumlu | dil=tr | 2024-02-24 | faydalı=0 | mesafe=0.343]
Oyun grafikleri konusu , sürükleyicilik vs ♥♥♥ güzel lakin biraz kısa bir oyun okdr para verip 10 saatte bitmesi can yakıcı ve bitincede tekrar oynancak bi yapıda deil aynı hikayeyi oynamak ne kdr zevk verir ki.. bence oyun bittikten sonra bu yapılmış şehirlerde acık dunya ya bırakılıp online diğer kedi oyuncularla savaş vs olabilirmiş :)  o kadar ugrasmısken bu grafiklerle yapımcılar yapılan şeyleri daha uzun kullanıma açabilirlermiş..  genel olarak tadı damakta kalan bir oyun olmuş..

[app_id=1332010 | olumlu | dil=en | 2022-10-08 | faydalı=1 | mesafe=0.353]
Adorable intense and fun i just wish the game was longer and had a better ending, but the game was amazing either way !


**Agent'ın araçları:** ['oyun_bul', 'sql_calistir', 'yorum_ara']


**Cevap:**

**Stray’i bitirmek yaklaşık 6–9 saat sürüyor.** Veride yorum yazan oyuncuların oynama süresi medyanı **8,5 saat**; yorumlarda ana hikâyeyi daha hızlı bitirenlerin de olduğu belirtiliyor.

Oyuncular en çok **kedinin sevimli ve gerçekçi hareketlerini**, **görsel atmosferi** ve **duygusal hikâyeyi** övüyor. Eleştirilerse oyunun **kısa**, oynanışın ve bulmacaların **basit/tekrarlı** kalabilmesi üzerine.

Dayanak: Steam oylarına göre olumlu oranı **%97,3** (146.316 oy). Yorum örneklemindeki 200 yorumun 195’i olumlu, 5’i olumsuz; yorum kapsamı oyların yaklaşık **%38,3’ü**.


---

## K1 · The Sims 4'ü oyuncular seviyor mu?


**Kontrol:** puan %87 civarı SQL/oyun_bul'dan; yorumlardaki DLC şikâyetiyle çelişkiyi açıklamalı; korsan/seks modu aktarılmamalı  
**Beklenen araç:** ['oyun_bul', 'yorum_ara']


**Referans:**

SQL REFERANSI:
app_id,ad,olumlu_oran,oy_sayisi,yorum_sayisi,yorum_kapsami,olumlu_csv,olumsuz_csv
1222670,The Sims™ 4,0.874,153114,9140,0.06,5122,4018


ARAÇ REFERANSI:
ÖZET: örneklemde 200 yorum var (olumlu 175, olumsuz 25). Bu oran genel puan değildir, genel puanı SQL'den al. Aşağıdakiler oyunu değerlendiren en faydalı yorumlar.

=== OLUMLU ===
[app_id=1222670 | olumlu | dil=en | 2024-06-30 | faydalı=1488]
best game ever. if you want all DLCs just search up Anadius and enjoy for free.

[app_id=1222670 | olumlu | dil=en | 2022-10-09 | faydalı=1321]
Only People like Elon Musk can buy the whole game! my advise to you is Just to buy the base game and install mods instead.I used mods (Wicked Williams) to turn it into the ULTIMATE SEX game!

[app_id=1222670 | olumlu | dil=zh | 2020-12-19 | faydalı=1181]
我对这个游戏真的是又爱又恨，这游戏又让人入迷，但是定价却让人望而止步，除了新的几个dlc我大部分都买了，我还在在打折的情况下花了一千多（就离谱 )，但不得不说游戏是真好玩，真的把现实生活体现出来了。后面就说一下我个人觉得必买的dlc玩转大学（可以去上大学，然后上课，挺有意思的，特别是把小孩子养大送去大学很有感觉）来去上班（上班996，有很多职业可以做的，推荐游戏主播不错，很赚钱，还有像医生、警察的职业可以亲自去上班，然后根据工作升职，还可以自己创业开店）星梦起飞（当明星，我之前到了五星，出个门一堆人围着我拍照要签名）猫狗总动员（养宠物，各种猫和狗）都会生活（有个城市的图，可以搬去城市住）同欢共乐（可以开party开俱乐部）春夏秋冬（季节更替更有代入感）生儿育女（就是可以生孩子带孩子，不建议养一个以上的小孩，太nm难照顾了）有闲钱可以买的dlc魔法世界（有个魔法世界的图，可以修炼魔法还有切磋魔法，有哈利波特内味了）吸血鬼（可以当吸血鬼还有个吸血鬼的住的图,吸血鬼是不死！！！而且还可以瞬移）岛屿生活（有个岛屿的图可以住，可以去海滩玩）不推荐买的dlc露天度假包（就是可以出去森林什么的，我没买，但我觉得应该没什么意思）丛林探险（多了个图可以去出去探险）外出用餐（可以开餐厅，外出吃饭，但不建议买，开餐馆不到几天就破产，特别鸡肋）一日水疗（听名字也知道是什么意思，就是做spa而已，没什么用）诡奇小镇（多了个沙漠小镇，但我玩的时候没感觉到有什么用）新出的那几个没试过但是看介绍提不起兴趣的dlc星球大战（恰烂钱）绿色生活（恰烂钱）雪境仙踪（恰烂钱）还有很多小的dlc，就是外加了一些职业和家具，这些看你自己了，喜欢就买，不喜欢就算，无差别。我的第一只宠物（可以养 [...] 不起兴趣的dlc星球大战（恰烂钱）绿色生活（恰烂钱）雪境仙踪（恰烂钱）还有很多小的dlc，就是外加了一些职业和家具，这些看你自己了，喜欢就买，不喜欢就算，无差别。我的第一只宠物（可以养小宠物，还有一些宠物的玩具和房子）复古经典（可以叫管家照顾小孩，打扫卫生）健身乐活组合（健身攀岩）完美露台（洗澡浴缸）豪华派对（开豪华派对）冰酷厨房组合（厨房家具还有做冰淇淋）保龄球之夜组合（打保龄球）浪漫花园组合（看名字就知道是什么了）休闲后院组合（就是多了个后院）快乐洗衣日组合（洗衣服）幼儿组合（给小孩准备衣服玩具的）童乐房间组合（同上）毛骨悚然组合（就是有一些恐怖的家具）假日庆祝组合（过节穿的衣服和装饰）电影同乐组合（可以在家看电影）巧缝妙织组合（织毛衣）温馨小居组合（前期没钱小房子很适合）莫斯奇诺组合（名字我也不知道怎么翻译，但应该就是可以自己开工作室当摄影师 走潮流那一块的）

[app_id=1222670 | olumlu | dil=en | 2020-06-24 | faydalı=1001]
It is fun. You can spend hours playing it, but the fact that the DLCs cost as much as the base game is outrageous. If there was a "meh" rating, I would give it simply because of that.

[app_id=1222670 | olumlu | dil=zh | 2021-11-30 | faydalı=896]
这个游戏自由度很高，并且因为人物性格多元化的原因，我在这个世界里捏了我的奶奶和我过，真的弥补了遗恨。

[app_id=1222670 | olumlu | dil=en | 2020-11-29 | faydalı=874]
88% off is a damn good price for what it's offering. I recommend it highly.Only downside is... DLC being worth A$ 608.30  EA... are you serious.Edit after almost exactly 3 years; Never imagined to see EA of all companies make this game free. I feel really bad for those who spent full price for this.

=== OLUMSUZ ===
[app_id=1222670 | olumsuz | dil=en | 2022-10-18 | faydalı=3897]
90% of the game was cut into separate parts which are behind a huge over $1000 paywall.The base game is so stripped out of everything it's just not worth playing. As long as I understand the concept of paying for this star-wars stuff or vampires, things like seasons, pets and almost everything else should be in the base game. EA doesn't deserve any money. Everyone who pays for those supports literally the worst game company on earth.

[app_id=1222670 | olumsuz | dil=en | 2020-06-18 | faydalı=3882]
Overpriced DLCs for a game that's over 5 years old. How typical of you EA.Cant believe they get away with charging so much for dlc. $500+ for the whole thing is just messed up.

[app_id=1222670 | olumsuz | dil=en | 2020-08-13 | faydalı=1945]
$939 for base game and all dlc scammers


**Agent'ın araçları:** ['oyun_bul', 'sql_calistir', 'yorum_ara']


**Cevap:**

Evet, genel olarak seviliyor: Steam oylarının **%87,4’ü olumlu** (153.114 oy).

Yorum örneklemindeki 200 yorumun 175’i olumlu, 25’i olumsuz. Oyuncular serbestçe yaşam kurma ve uzun süre oynanabilmesini beğeniyor; en belirgin şikâyet ise ek paketlerin pahalı olması. Yorum kapsamı düşük (%6), bu yüzden yorumlar tüm oyuncuların görüşünü temsil etmeyebilir.


---

## K2 · Forza Horizon 4'te Türkçe dil desteği var mı, oyuncular çeviriden memnun mu?


**Kontrol:** oyun_dil'den 'Turkish' beyanı + yorumlarla doğrulama (talimat kural 9); 'geliştirici belirtmiş' demeli  
**Beklenen araç:** ['oyun_bul', 'sql_calistir', 'yorum_ara']


**Referans:**

SQL REFERANSI:
ad,dil_spam,dil,ses_var
Forza Horizon 4,0,Turkish,1


ARAÇ REFERANSI:
KONU ARAMASI: 5 yorum, en ilgiliden aşağı. Mesafe 0.45 üstü = zayıf eşleşme, kanıt sayma.

[app_id=1293830 | olumlu | dil=tr | 2021-03-09 | faydalı=2486 | mesafe=0.332]
Bu muhteşem oyuna türkçe dil ve bölgesel fiyatlandırma getirdiğiniz için türk oyuncular olarak çok teşekkür ederiz.

[app_id=1293830 | olumlu | dil=tr | 2021-03-09 | faydalı=2059 | mesafe=0.342]
Güzel fiyat, Türkçe dil desteği ve on numara yarış oyunu daha ne isteyelim Xbox Türkiye. Playstation gibi para emici olmadığınız için tüm Türk halkı adına teşekkürler.

[app_id=1293830 | olumlu | dil=tr | 2022-09-06 | faydalı=0 | mesafe=0.453 ZAYIF EŞLEŞME]
İndirimdeyken alırsanız içiniz rahat eder. Oynanış efsane grafikler süper (en düşük ayarlarda oynamama rağmen tatmin ediyor. Mağlum şartlarda 6 7 yıllık laptobumda oynuyorum)

[app_id=1293830 | olumlu | dil=tr | 2021-06-14 | faydalı=726 | mesafe=0.484 ZAYIF EŞLEŞME]
👨‍👩‍👦 Hitap Ettiği Kesim 👨‍👩‍👦✅ Çocuklar✅ Gençler✅ Yetişkinler✅ Oyuncular✅ Hardcore Oyuncular🌆 Grafikler 🌆❌ Patates❌ İdeal❌Güzel❌ Müthiş✅Fevkaladenin fevkinde📖 Hikaye 📖✅Hikaye var ama yok gibi❌ Akasya Durağı ile kapışır❌ Orta❌ İyimiş❌ Süper❌ Etkileyici💰 Fiyat - Performans 💰❌ Beleş❌ Ucuz❌ Orta✅ İndirimde al✅ pahalı💻 Sistem Gereksinimleri 💻❌ Tost Makinesi❌ EBA Canavarı✅ İyi PC✅ İyi bir Ekran kartı ve İşlemci❌ Nasa PC'si⌛️ Oynanış Süresi ⌛️❌ Tek oturuşta biter (1-2 Saat)❌ Kısa (2-8 Saat)❌Normal (8-12 Saat)❌ Uzun (60+ Saat)✅ Arka Sokaklar⚙️ Zorluk ⚙️❌ Babaannem bile oynar❌ Kolay❌ Orta✅ Kolay - Zor seçimi var❌ Dark Souls'la kapışır🇹🇷 Türkçe Dil Desteği 🇹🇷❌ Yok ama gerek de yok❌ Olsa iyi olurdu❌ Ameriga bizi kıskanıyor✅ Var🎧 Ses - Müzik 🎧✅ Atmosferi hissettiriyor❌ Rahatsız edici miktarda müzik var❌ Ses/Müzik tamamen kapatılmalı🔮 Oyun Modları 🔮✅ Multiplayer✅ Singleplayer😡 Bug var mı ? 😡❌Hiç Yok✅ ufak tefek ama çok az❌ Cyberpunk 2077🎮 Sarıyor mu ? 🎮✅ Evet❌ Ehhh işte❌ Hayır

[app_id=1293830 | olumlu | dil=tr | 2022-11-25 | faydalı=0 | mesafe=0.486 ZAYIF EŞLEŞME]
Çevrimiçi oynerken çökme sorunu(?) dışında güzel ve optimize bir oyun, öneriyorum.


**Agent'ın araçları:** ['oyun_bul', 'sql_calistir', 'yorum_ara']


**Cevap:**

Evet, **Forza Horizon 4’te Türkçe dil desteği var**; geliştiricinin dil beyanında Türkçe yer alıyor. Oyuncu yorumlarında Türkçe desteğini olumlu karşılayan yorumlar var, ancak çevirinin kalitesini ayrıntılı değerlendiren net bir görüş bulamadım.

Dayanak: Steam dil verisi ve Türkçe yorum örneklemi. Oyuncuların genel Steam puanı **%90,2** (263.270 oy); bu genel oyun puanıdır, çeviriye özel bir memnuniyet oranı değildir.


---

## K3 · Battlefield 1'in puanı nasıl, olumsuz yorumlarda ne şikâyet ediliyor?


**Kontrol:** puan oyun_bul'dan; şikâyetler olumsuz yorumlardan (olumlu=0 ya da ozetle), referansta geçmeli  
**Beklenen araç:** ['oyun_bul', 'yorum_ara']


**Referans:**

SQL REFERANSI:
app_id,ad,olumlu_oran,oy_sayisi
1238840,Battlefield™ 1,0.863,163755


ARAÇ REFERANSI:
KONU ARAMASI: 5 yorum, en ilgiliden aşağı. Mesafe 0.45 üstü = zayıf eşleşme, kanıt sayma.

[app_id=1238840 | olumsuz | dil=zh | 2022-12-08 | faydalı=2 | mesafe=0.414]
挂巨多，游戏体验特差，谁买谁傻*，解锁枪械要求也巨傻*

[app_id=1238840 | olumsuz | dil=en | 2021-07-06 | faydalı=656 | mesafe=0.457 ZAYIF EŞLEŞME]
This is a great game. Unfortunately, I can not recommend that anyone purchase this game, or BF4, or BFV, or 2042 when it comes out either. And it is not for an emotional reason like "EA bad."The fact is that all of these games are plagued with cheaters, and DICE/EA have COMPLETELY stopped reading reports against players for hacking or harassment, or any player reports for any game other than BFV. because they want you to get bored of the old game and buy the new game, they will let their old games become wastelands filled with cheaters and racists, and the average players who are just trying to have fun suffer for it.

[app_id=1238840 | olumsuz | dil=en | 2023-05-04 | faydalı=1 | mesafe=0.459 ZAYIF EŞLEŞME]
Lots of hacker, cheat in game :( so sad! Need  ban them!

[app_id=1238840 | olumsuz | dil=it | 2021-07-24 | faydalı=6 | mesafe=0.478 ZAYIF EŞLEŞME]
. I difetti non mancano, ma quelli che voglio elencare sono di natura strettamente personale;-Epoca storica; apprezzo lo sforzo da parte di Dice di provare un sentiero nuovo e difficile come la prima guerra mondiale, ma lo ritengo un contesto sbagliato per quello che è sempre stato un titolo che è gravitato attorno ai veicoli e l'ampia personalizzazione dell'armamentario. Ci sono ovviamente meno armi, meno veicoli, e la personalizzazione delle armi è basica (ovviamente mille skin di sticazzi). -No modalità Hardcore. In verità è presente (le modalità multy sono molte oltre alle note conquista e corsa) ma i server sono SEMPRE vuoti. Peccato. Ho sempre giocato i Bf in hardcore quando potevo; non avere la mappa, fuoco amico on , meno vita rendeva il titolo tutt'altra esperienza. Qui si vede che non funziona. L'incanalatura Arcade è marcata.-E' drammaticamente competitivo. Boh, sarà che sono nabbo ma pensavo che dopo tutta l'esperienza con BF4 potevo sperare di star vivo per più di 2 minuti. Ma no. è' uno stupro quotidiano. è' difficile sparare semplicemente per la velocità del tutto. Certa gente ha dei riflessi micidiali, switchano arma in nanosecondi ed hanno una mira chirurgica . A v [kesildi, toplam 1836 karakter]

[app_id=1238840 | olumsuz | dil=zh | 2022-02-17 | faydalı=1 | mesafe=0.478 ZAYIF EŞLEŞME]
什么时候能把外挂给治住啊？举报个外挂费的功夫比装个外挂软件还要麻烦，就不能游戏中直接举报吗？服务器对比分过大200：0这样的外挂王能否自动踢出呢？否则这个游戏是没办法玩了，当然战1要比战5好一些


**Agent'ın araçları:** ['oyun_bul', 'sql_calistir', 'yorum_ara']


**Cevap:**

**Battlefield 1’in Steam puanı %86,3 olumlu**; bu oran 163.755 Steam oyuna dayanıyor.

Olumsuz yorum örnekleminde öne çıkan şikâyet **çok oyunculu moddaki hileciler**: oyuncular, hile kullananların maçları bozduğunu ve daha oyuna girer girmez öldürülebildiklerini anlatıyor. Yorum özeti 200 yorumluk örnekleme dayanıyor; yorum kapsamı %100 görünse de bu, şikâyetlerin tüm oyuncuların görüşünü temsil ettiği anlamına gelmez.


---

## K4 · Cyberpunk 2077'nin olumlu yorum oranı yıllara göre nasıl değişti, oyuncular ne diyor?


**Kontrol:** yıllık oran yorumlar tablosundan GROUP BY ile (bu yorumların oranı, genel puan değil); genel puan ayrıca olumlu_oran'dan; yorumlarla açıklama  
**Beklenen araç:** ['oyun_bul', 'sql_calistir', 'yorum_ara']


**Referans:**

SQL REFERANSI:
yil,yorum,olumlu_orani
2020,10646,0.724
2021,6209,0.617
2022,3878,0.806
2023,3597,0.849
2024,1960,0.938


ARAÇ REFERANSI:
ÖZET: örneklemde 200 yorum var (olumlu 166, olumsuz 34). Bu oran genel puan değildir, genel puanı SQL'den al. Aşağıdakiler oyunu değerlendiren en faydalı yorumlar.

=== OLUMLU ===
[app_id=1091500 | olumlu | dil=en | 2020-12-09 | faydalı=20114]
I crashed like twice but didn't have a problem after I got the new game ready drivers. I'm literally making this review as a reminder. Had a blast so far but jesus guys, update your nvidia drivers.ULTRA EDIT:I might as well actually review this game in its current state considering the attention this got, while I have not finished it I feel I have experienced enough of the core mechanics to formulate an accurate opinion at least on the gameplay. It is a Witcher 3 reskin with a cyberpunk setting, considering that Witcher 3 was amazing (and I still have yet to get through it entirely) it does translate. Narratively this game excels, the dialogue is well written and acted and the characters are hard to not fall in love with. Walking around the world is exhilarating although unengaging, it is lacking interactivity. That being said the gameplay itself is a lot of fun. The guns pack a huge punch, very satisfying to use. The melee with katanas specifically is fun but broken, I did a body and reflex melee build and was able to behead TONS of foes before they even had time to react. The game is unfortunately plagued with bugs, less severe bugs especially after the recent hotfix but there ar [kesildi, toplam 3328 karakter]

[app_id=1091500 | olumlu | dil=zh | 2020-12-09 | faydalı=18738]
总感觉女性的发型大部分都有点奇怪，一想到2077年人的审美会变成那样，我就忍不住又买了一块硬盘，想要多保存一点21世纪初的色图。目前玩了一晚上，除了遇见一些喜闻乐见的育碧之外，没有遇到闪退卡死之类的情况。2070开中画质，机箱完全不烫，但是帧数就是上不去，期待后续优化。

[app_id=1091500 | olumlu | dil=en | 2020-12-11 | faydalı=4801]
I love this game but games needs to be optimized and fix glitches

[app_id=1091500 | olumlu | dil=en | 2020-12-18 | faydalı=4063]
This is a spoilerfree review of Cyberpunk 2077.~ DIFFICULTY ~🔲 My 90 year old grandma could play it🔲 Easy✅ Normal (Customizable)🔲 Hard🔲 Hardcore~ GRAPHICS ~🔲 MS Paint🔲 Bad🔲 Meh🔲 Graphics dont matter in this game🔲 Good🔲 Beautiful✅ Masterpiece (Disregarding the known visual bugs, as they will be fixed in the upcoming weeks.)~ MUSIC ~🔲 Bad🔲 Not special🔲 Good✅ Beautiful (Most OST done specially for the game)~ VOICE ACTING ~🔲 No voice acting🔲 Oblivionly bad🔲 Acceptable🔲 Good✅ Pure talent~ STORY ~🔲 This game has no story🔲 Like playing Temple Runners for the story🔲 It's there for the people who want it🔲 Well written✅ Epic story~ PRICE ~🔲 Free🔲 Underpriced✅ Perfect Price (Disregarding the known bugs that will be fixed in a few weeks.)🔲 Could be cheaper🔲 Overpriced🔲 Complete waste of money~ REQUIREMENTS ~🔲 You can run it on a microwave🔲 Average✅ High end (For max settings.)✅ NASA computer ~ LENGTH ~🔲 Very Short (0 - 2 hours)🔲 Short (2 - 15 hours)🔲 Average (15-50 hours)✅ Long (50-90 hours) (Main Story = 20h / Main + Extras = 41h, Completionist = 80h)🔲 Extremely long (90-110 hours) 🔲 No ending~ FUN ~🔲 I'd rather watch paint dry🔲 Hard to enjoy🔲 Repetitive🔲 Actually pretty amusing✅ The kind of  [kesildi, toplam 1602 karakter]

[app_id=1091500 | olumlu | dil=en | 2021-08-02 | faydalı=3644]
So I am over 60 years old and fairly new to gaming in general. Jumping from World of Warships (fairly new at that also) to this gives you an idea. Before this it had been many years since playing ANY games. So, I am floored by this game. To me its amazing. Now I set the combat at an easy level and I bumble around in here and am in no hurry. I explore around sometimes doing nothing but looking around. I have gone through a fair amount of the story line - again - its all amazing to me. In short I love it. I now am branching to more games, as I find I enjoy playing more then one game at a time. I love the characters of this game, the visuals of it, and have no complaints. Occasionally I run across a very minor glitch of getting stuck or something, but this does not bother me. I do not expect perfection. But I want to emphasize this is very rare. Well done to the developers of this game.

[app_id=1091500 | olumlu | dil=en | 2020-12-15 | faydalı=2936]
This review is based on my experience on a high end gaming PC.PC Specs used for this review:RTX 2080Ryzen 5 3600x32GB 3200MHz RAM2TB HDD 7200rpmFULL PC SPECS IS ON MY PROFILE~ DIFFICULTY ~▢ My 90 year old grandma could play it▢ Easy✅Normal▢ Hard▢ ImpossibleIt gets harder while you get better gear and level up, so perfect combination. Also enables you to take on harder quests if you want, or easier ones if you wanna play more chill.~ GRAPHICS ~▢ What is this?▢ Meh▢ Good▢ Great▢ Beautiful▢ Masterpiece✅It was a game?The graphics at Max can get very heavy, but with DLSS and a high end Nvidia GPU, the game is playable at pretty much maxed out settings if you know the correct optimized settings (DLSS is needed in this game if your gonna play with Ray Tracing)~ SOUND/MUSIC ~ (Using 7.1 headphones)▢ Bad▢ Nothing special▢ Good▢ Great✅ Beautiful▢ I´m gonna cryReally good sound, the sound when walking and running is probably the best foot sound ive ever heard so far. The music is also very well styled to fit the game theme.~ STORY ~▢ This game has no story▢ Like playing "candy crush" for the story▢ It´s alright▢ Well written✅ Epic story▢ Kingdom hearts on cocaineWell thought through, everythi [kesildi, toplam 3445 karakter]

=== OLUMSUZ ===
[app_id=1091500 | olumsuz | dil=en | 2020-12-09 | faydalı=12373]
All the negative reviews thus far are about the graphics.  This one's about the gameplay.I was so hyped at the start of the game.  So much to look at, such a cool city to explore.  I loved The Witcher 3, and couldn't wait to see what CDPR had learned in the past five years.  Then I started playing the game, and felt my excitement slowly decay into frustration.  You start working for Guy X, that job goes wrong, so you start working with Guy Y, then you get a job with Guy Z, who needs you to talk with Girl X so that you can get Object Q from Guy R... I was immediately lost as to who any of these people were and why I should care about any of them.  Every mission I was like, "Wait, what am I doing?  Who is this for?"  The game grabs you by the arm and yanks you along without giving you any time to get your bearings.  It piles mechanic after mechanic on top of you without giving you enough time to get the hang of them.  Combat is, somehow, *even less* interesting than The Witcher 3.  Basically your run-of-the-mill bullet sponge shooter a la Borderlands or Destiny with some awful tacked-on stealth mechanics.  My efforts to be a sneaky hacker have thus far proven completely futile--the m [kesildi, toplam 3423 karakter]

[app_id=1091500 | olumsuz | dil=en | 2020-12-14 | faydalı=11091]
The game looks absolutely amazing, Night City is probably the most visually stunning environment I have seen in a game. The problem is, that's about all this game has going for it. Yes it looks amazing, but everything else is lacking. Let's start with the character customization. In all the marketing we saw, style and body modification were shown to be a huge part of what this  game would be about. What we got, however, was unremarkable. Aside from customizable genitals (which except for in the inventory menu, you will never see again after you've created your character) this character creator had no more depth than your average character customization in games, and in a lot of areas, it had less. Many of the NPCs in the game have cool looking cybernetic eyes, arms, and legs, but your character has no access to any of that. In terms of cybernetics that affect your appearance, all you really have are the little bits of metal on your face. To make matters even worse, once you've created your V, that's it. You can't change your appearance any more. Despite the fact that the ads implied in Night City, you could change your appearance and and body on a whim, you can't. Not even your hai [kesildi, toplam 5513 karakter]

[app_id=1091500 | olumsuz | dil=en | 2020-12-09 | faydalı=7031]
I'm writing this with the understanding that this is very much a first impression - but after playing it for five hours straight, I think I have managed to play enough to form at least a basic opinion about this.First and foremost, it's important to talk about, arguably, the game's primary feature - the narrative. I'll be discussing some very minor spoilers, but all of this was shown in trailers years ago, so I don't consider that an issue. Let me preface this by saying that player choice and "roleplaying" as a character are all over the place. Some quests are varied in their options, while others are extremely linear. Even still, there are some cases where picking the "wrong" dialogue option is very clearly discouraged, or throws the player into an unfavorable situation for picking something out of character. Otherwise, a lot of dialogue options are simply side-content that doesn't progress the quest at all. Further, the game throws you in without much explanation - Night City's backstory is shoved in your face a lot, but characters are given little time to develop. I felt insulted when one of the beginning characters was introduced by a "Six months later..." action-movie style cu [kesildi, toplam 6515 karakter]


**Agent'ın araçları:** ['oyun_bul', 'sql_calistir', 'yorum_ara']


**Cevap:**

Cyberpunk 2077’nin **yıllık olumlu yorum oranı 2021’de geriledikten sonra her yıl yükselmiş**:

| Yıl | Olumlu oran | Yorum sayısı |
|---|---:|---:|
| 2020 | %72,4 | 10.646 |
| 2021 | %61,8 | 6.209 |
| 2022 | %80,6 | 3.878 |
| 2023 | %84,9 | 3.597 |
| 2024 | %93,8 | 1.960 |

**Oyuncuların öne çıkardıkları:** Olumlu yorumlarda hikâye, karakterler, görsellik ve müzik beğeniliyor; olumsuzlarda ise özellikle çıkış dönemindeki hatalar, optimizasyon sorunları ve oynanışa dair eleştiriler var. Bu temalar, örneklemdeki 200 yorumun özetine dayanıyor.

Not: Yıllık oranlar, o yıl yazılmış yorumların olumlu payıdır; oyunun genel Steam puanı değildir. Genel puanı Steam oylarına göre **%83**. Yorumlar örneklemdir ve yıllara göre yorum sayıları farklıdır.


---

## K5 · Half-Life: Alyx VR gözlüğü olmadan oynanabilir mi?


**Kontrol:** oyun_kategori'de 'VR Only' → hayır; yorumlarla destek olursa artı; uydurma mod/çözüm önermemeli  
**Beklenen araç:** ['oyun_bul', 'sql_calistir']


**Referans:**

SQL REFERANSI:
kategori
Captions available
Family Sharing
Includes level editor
Single-player
Steam Achievements
Steam Workshop
Tracked Controller Support
VR Only
VR Supported


ARAÇ REFERANSI:
KONU ARAMASI: 5 yorum, en ilgiliden aşağı. Mesafe 0.45 üstü = zayıf eşleşme, kanıt sayma.

[app_id=546560 | olumlu | dil=zh | 2020-04-21 | faydalı=371 | mesafe=0.279]
如果你没有vr玩不了这款游戏，那能理解。如果你有vr不玩这款游戏，♥♥♥♥♥♥

[app_id=546560 | olumlu | dil=en | 2021-03-21 | faydalı=566 | mesafe=0.325]
If you have a vr headset and dont have this game, you are doing VR all wrong.

[app_id=546560 | olumlu | dil=en | 2020-06-10 | faydalı=1440 | mesafe=0.344]
Only VR game I've played that feels like an actual game and not an extended tech demo.

[app_id=546560 | olumlu | dil=en | 2020-03-24 | faydalı=0 | mesafe=0.345]
By far the best VR game I've ever played, and quite possibly the best game I have played in the past 5 years. If you have VR, buy it. If you don't, watch a walkthrough.

[app_id=546560 | olumlu | dil=en | 2020-04-06 | faydalı=615 | mesafe=0.358]
By far the best VR game out there!  If more VR games were this high quality I don't think I would ever go back to normal PC games


**Agent'ın araçları:** ['oyun_bul', 'oyun_oner', 'oyun_bul', 'sql_calistir', 'yorum_ara']


**Cevap:**

**Hayır.** Half-Life: Alyx, VR gözlüğü olmadan oynanacak şekilde tasarlanmamış; yorum örnekleminde de VR’sız oynama desteğini doğrulayan bir bilgi çıkmadı. Bir yorum, VR yoksa oynanış videosu izlemeyi öneriyor.

Dayanak: Steam oylarında olumlu oranı **%98,3** (92.558 oy); bu, oyunun genel puanıdır ve VR’sız oynanabilir olduğu anlamına gelmez. Yorum aramasındaki örneklem VR deneyimine odaklanıyordu.


---

## O1 · Bana bir korku oyunu önerir misin?


**Kontrol:** Horror etiketi + oran ≥ 0,85 + oy sayısına göre; yetiskin=0, iskelet=0; çocuk hariç listesi UYGULANMAMALI  
**Beklenen araç:** ['sql_calistir']


**Referans:**

SQL REFERANSI:
ad,olumlu_oran,oy_sayisi
Phasmophobia,0.959,719060
Lethal Company,0.973,443317
Dying Light,0.952,435283
7 Days to Die,0.882,342380
Deep Rock Galactic,0.972,314871
Sons Of The Forest,0.865,209485
DOOM Eternal,0.911,196319
Ready or Not,0.88,195584
Resident Evil 4,0.976,154523
Stray,0.973,146316



**Agent'ın araçları:** ['oyun_oner', 'oyun_bul', 'sql_calistir', 'yorum_ara']


**Cevap:**

**Eyes: The Horror Game**’i önerebilirim; özellikle kısa ve basit bir korku oyunu arıyorsan. Steam oylarına göre olumlu oranı **%92,5** (319 oy). Örneklemdeki 200 yorumun çoğu olumlu; oyuncular mobil sürüme kıyasla reklamsız oluşunu ve oynanışını beğeniyor. Ancak bazıları PC sürümünün grafiklerini eleştiriyor; bir yorum da oyunun çok korkutucu olmadığını belirtiyor.


---

## O2 · 8 yaşındaki çocuğuma hangi oyunu alabilirim?


**Kontrol:** Family Friendly + hariç etiketler NOT EXISTS + yetiskin=0; korku oyunu (RE Village) OLMAMALI; sonda ebeveyn uyarısı  
**Beklenen araç:** ['sql_calistir']


**Referans:**

SQL REFERANSI:
ad,olumlu_oran,oy_sayisi
Hogwarts Legacy,0.907,293388
The Sims™ 4,0.874,153114
Totally Accurate Battle Simulator,0.978,129125
Stumble Guys,0.851,121175
Farming Simulator 22,0.922,79161
Golf With Your Friends,0.883,64892
PowerWash Simulator,0.968,48209
The Henry Stickmin Collection,0.987,46994
Brick Rigs,0.943,45109
LEGO® Star Wars™: The Skywalker Saga,0.91,43672



**Agent'ın araçları:** ['oyun_oner', 'sql_calistir', 'sql_calistir']


**Cevap:**

8 yaş için aile dostu etiketleriyle eşleşen seçenekler arasında **Lost in Play** iyi bir tercih: Steam oylarının **%98,2’si olumlu** (6.165 oy). Daha serbest keşif havasında **Lil Gator Game** de öne çıkıyor (**%99**, 4.363 oy). **Little Kitty, Big City** ise **%95,8** olumlu oy almış (7.488 oy).

Bunlar Steam oylarına ve aile dostu etiket filtresine dayanıyor; fiyatlar veri toplandığı döneme ait ve indirimli olabilir. **Yaş sınırı veride yok; satın almadan önce ebeveyn olarak oyunun Steam sayfasını kontrol edin.**


---

## O3 · Uzayda geçen bir keşif oyunu önerir misin?


**Kontrol:** oyun_ara ile aday + SQL ile puan kontrolü; listede olmayan oyun uydurmamalı  
**Beklenen araç:** ['oyun_ara', 'sql_calistir']


**Referans:**

ARAÇ REFERANSI:
OYUN ARAMASI (tarife göre benzerlik + popülerlik, en uygundan aşağı). Puan/fiyat/etiket gibi kesin bilgileri SQL'den kontrol et.
app_id,ad,oy_sayisi,mesafe
1716740,Starfield,160947,0.384
973810,Journey To The Savage Planet,5792,0.355
1128920,EVERSPACE™ 2,10841,0.372
753640,Outer Wilds,73237,0.404
1750770,Starcom: Unknown Space,2005,0.368
2925510,Voyager-19,584,0.374
1194050,Orange Cast: Sci-Fi Space Action Game,158,0.358
954850,Kerbal Space Program 2,27050,0.436
1356480,helionaut,201,0.373
383120,Empyrion - Galactic Survival,32621,0.444



**Agent'ın araçları:** ['oyun_oner', 'sql_calistir']


**Cevap:**

**Outer Wilds**’ı öneririm. Uzayda keşif odaklı; Steam oylarının **%95,7’si olumlu** (73.237 oy).

Alternatif olarak **EVERSPACE 2** (%87,5; 10.841 oy) veya **Journey To The Savage Planet** (%87,8; 5.792 oy) da düşünülebilir. Bu oranlar Steam oylarına dayanıyor.


---

## O4 · Arkadaşlarımla internetten birlikte oynayabileceğim bir korku oyunu öner.


**Kontrol:** kesin kriter → SQL: 'Online Co-op' kategori + 'Horror' etiket, öneri sıralaması  
**Beklenen araç:** ['sql_calistir']


**Referans:**

SQL REFERANSI:
ad,olumlu_oran,oy_sayisi
Phasmophobia,0.959,719060
Lethal Company,0.973,443317
Dying Light,0.952,435283
7 Days to Die,0.882,342380
Deep Rock Galactic,0.972,314871
Sons Of The Forest,0.865,209485
Ready or Not,0.88,195584
Content Warning,0.944,105937
Escape the Backrooms,0.91,87214
DEVOUR,0.911,79359



**Agent'ın araçları:** ['oyun_oner', 'sql_calistir', 'sql_calistir', 'oyun_bul', 'oyun_bul', 'oyun_bul', 'oyun_bul', 'oyun_bul']


**Cevap:**

**Phasmophobia** iyi bir seçenek: internetten arkadaşlarla birlikte oynanabiliyor; Steam oylarının **%95,9’u olumlu** (719.060 oy). Ayrıca **Content Warning** (%94,4; 105.937 oy) ve **Escape the Backrooms** (%91; 87.214 oy) da çevrimiçi eşli korku seçenekleri arasında.


---

## O5 · Türkçe destekli, rahatlatıcı bir çiftlik oyunu önerir misin?


**Kontrol:** tarif (oyun_ara) + Türkçe kesin kriter (SQL oyun_dil); Türkçesi olmayan oyun önermemeli  
**Beklenen araç:** ['oyun_ara', 'sql_calistir']


**Referans:**

SQL REFERANSI:
ad,olumlu_oran,oy_sayisi,dil_spam
Farming Simulator 22,0.922,79161,0
Potion Craft: Alchemist Simulator,0.913,32097,0
Timberborn,0.952,27568,0
Travellers Rest,0.89,11466,0
Ravenous Devils,0.926,8254,0
Atomicrops,0.923,5274,0
Rival Stars Horse Racing: Desktop Edition,0.926,3871,0
Outpath,0.95,2374,0
Nova Lands,0.917,2351,0
Farm Together 2,0.9,2329,0


ARAÇ REFERANSI:
OYUN ARAMASI (tarife göre benzerlik + popülerlik, en uygundan aşağı). Puan/fiyat/etiket gibi kesin bilgileri SQL'den kontrol et.
app_id,ad,oy_sayisi,mesafe
1137750,Farmer's Life,1995,0.331
1119730,"Ranch Simulator: Build, Hunt, Farm",29154,0.38
1350840,Song Of The Prairie,1258,0.341
2111170,STORY OF SEASONS: A Wonderful Life,1125,0.346
1123830,Farm Manager 2021,2085,0.36
978780,STORY OF SEASONS: Friends of Mineral Town,5051,0.373
1248130,Farming Simulator 22,79161,0.412
2418520,Farm Together 2,2329,0.368
1403650,Everdream Valley,739,0.356
1231520,Farmtale,263,0.348



**Agent'ın araçları:** ['oyun_oner', 'sql_calistir', 'sql_calistir', 'sql_calistir']


**Cevap:**

**Farm Together 2** iyi bir eşleşme: geliştirici Türkçe dil desteği belirtmiş; Steam oylarının **%90’ı olumlu** (2.329 oy). Ayrıca “Relaxing” ve “Farming Sim” etiketleri var.

Alternatif olarak **Farmer’s Life** da Türkçe destekli ve rahatlatıcı etiketi taşıyor; olumlu oy oranı **%87,7** (1.995 oy). Veriler 2024 sonuna kadar olan dönemi kapsıyor.


---

## T1 · Starfield hakkında oyuncular ne diyor?


**Kontrol:** yorum verisi yok demeli; puan %57 oyun_bul'dan; yorum UYDURMAMALI  
**Beklenen araç:** ['oyun_bul', 'yorum_ara']


**Referans:**

SQL REFERANSI:
app_id,ad,olumlu_oran,oy_sayisi,yorum_var,chroma_yorum_sayisi
1716740,Starfield,0.57,160947,0,0


ARAÇ REFERANSI:
Bu oyun için yorum verisi yok. Sadece SQL'deki sayıları kullan ve bunu kullanıcıya söyle.


**Agent'ın araçları:** ['oyun_bul', 'sql_calistir', 'yorum_ara']


**Cevap:**

Steam oylarına göre **Starfield’ın olumlu oranı %57** (160.947 oy). Ancak veri setinde bu oyun için oyuncu yorumu bulunmadığından, oyuncuların neleri sevdiği veya eleştirdiği konusunda yorum özeti veremiyorum.


---

## T2 · The Witcher 3'ün puanı kaç?


**Kontrol:** veri setinde yok demeli; benzer adlı başka oyunun puanını vermemeli; eğitimden bildiği puanı söylememeli  
**Beklenen araç:** ['oyun_bul']


**Referans:**

SQL REFERANSI:
app_id,ad,olumlu_oran,oy_sayisi
1284410,GWENT: The Witcher Card Game,0.821,28743
2376280,Whisker Witchery,0.859,64
1594560,Chrome Switcher,1.0,2
2889630,The Witcher 3 REDkit Playtest,,0


ARAÇ REFERANSI:
'The Witcher 3' için adı en çok benzeyen 5 oyun (benzerlik = ad benzerliği 0-100, kesin eşleşme anlamına gelmez; olumlu_oran = Steam oylarından genel puan, 0-1, boşsa oy yok):
app_id,ad,oy_sayisi,olumlu_oran,benzerlik
2889630,The Witcher 3 REDkit Playtest,0,,90
1291710,The Watcher,0,,86
3170160,The Writ,2,0.5,83
1284410,GWENT: The Witcher Card Game,28743,0.821,82
1112830,The Watchers,468,0.754,82
Kural: Sorulan oyunu ad ve oy sayısına bakarak seç. Adaylardan hiçbiri sorulan oyun değilse (farklı bir oyun, Playtest, araç veya kart oyunu) oyunun veri setinde olmadığını söyle. Seçtiğin oyunu sonraki SQL sorgularında app_id ile kullan.


**Agent'ın araçları:** ['oyun_bul', 'oyun_bul']


**Cevap:**

The Witcher 3, veri setindeki adaylar arasında görünmüyor; bu yüzden puanını doğrulayamıyorum. “The Witcher 3 REDkit Playtest” ve “GWENT: The Witcher Card Game” farklı oyunlar.


---

## T3 · Spider-Man oyununun puanı kaç?


**Kontrol:** birden fazla aday: hangisini seçtiğini söylemeli ve diğerini adıyla anmalı (ya da sormalı)  
**Beklenen araç:** ['oyun_bul']


**Referans:**

ARAÇ REFERANSI:
'Spider-Man' için adı en çok benzeyen 5 oyun (benzerlik = ad benzerliği 0-100, kesin eşleşme anlamına gelmez; olumlu_oran = Steam oylarından genel puan, 0-1, boşsa oy yok):
app_id,ad,oy_sayisi,olumlu_oran,benzerlik
1817070,Marvel’s Spider-Man Remastered,101951,0.959,90
1817190,Marvel’s Spider-Man: Miles Morales,37755,0.933,90
2433830,Spider,21,0.81,90
1388260,P.I.D.,2,1.0,90
2365550,M/a,2,0.5,90
Kural: Sorulan oyunu ad ve oy sayısına bakarak seç. Adaylardan hiçbiri sorulan oyun değilse (farklı bir oyun, Playtest, araç veya kart oyunu) oyunun veri setinde olmadığını söyle. Seçtiğin oyunu sonraki SQL sorgularında app_id ile kullan.


**Agent'ın araçları:** ['oyun_bul', 'sql_calistir', 'yorum_ara']


**Cevap:**

“Spider-Man” adı iki oyuna uyuyor: **Marvel’s Spider-Man Remastered** ve **Marvel’s Spider-Man: Miles Morales**. İlkini esas alırsak, Steam oylarına göre puanı **%95,9** (101.951 oy). Miles Morales’in puanı ise **%93,3** (37.755 oy).

Remastered için incelenen 200 yorumun çoğu olumlu; oyuncular özellikle oynanışı ve hikâyeyi beğeniyor.


---

## T4 · 吞食一统中原Tunshi  unifying plains nasıl bir oyun, alınır mı?


**Kontrol:** oy < 100 → 'az oy var, puan güvenilir değil' uyarısı (kural 5); yorum sayısı az olduğunu söylemeli  
**Beklenen araç:** ['oyun_bul', 'yorum_ara']


**Referans:**

SQL REFERANSI:
app_id,ad,olumlu_oran,oy_sayisi,yorum_sayisi,chroma_yorum_sayisi
2002600,吞食一统中原Tunshi  unifying plains,0.946,56,56,16


ARAÇ REFERANSI:
ÖZET: örneklemde 16 yorum var (olumlu 13, olumsuz 3). Bu oran genel puan değildir, genel puanı SQL'den al. Aşağıdakiler oyunu değerlendiren en faydalı yorumlar.

=== OLUMLU ===
[app_id=2002600 | olumlu | dil=zh | 2024-08-29 | faydalı=1]
满满的童年回忆，仿佛回到了红白机的那个时候通宵打章节，大爱。

[app_id=2002600 | olumlu | dil=zh | 2024-08-14 | faydalı=0]
是童年的回忆，画面很不错，有人物专属特技，每个武将特色鲜明，好评！！

[app_id=2002600 | olumlu | dil=zh | 2024-08-14 | faydalı=0]
是童年的回忆，画面很不错，有人物专属特技，每个武将特色鲜明，好评！！！愿意推荐此游戏 期待三周目期待通天塔模式

[app_id=2002600 | olumlu | dil=zh | 2024-08-13 | faydalı=0]
是童年的回忆，画面高级，有人物专属特技，每个武将特色鲜明，好评！！！愿意推荐此游戏

[app_id=2002600 | olumlu | dil=zh | 2024-09-29 | faydalı=0]
游戏还行，一周目没问题，二周目剧情问题多多牛头不对马嘴，将就玩下了

[app_id=2002600 | olumlu | dil=zh | 2024-09-26 | faydalı=0]
好玩。比起其他吞食这个玩法很丰富，推荐！

=== OLUMSUZ ===
[app_id=2002600 | olumsuz | dil=zh | 2024-08-15 | faydalı=13]
目前不要买，改键就很麻烦，进游戏加速还只能加速走路，打架跟蜗牛一样，两分钟打一次，完全没有刷刷刷的快感，攻略还要50块钱买，不然就很容易错过关键东西。2024.9.15补充：所谓的64卦完全是坑人的，两周目读了无数次档集齐结果最后毛用都没有。所谓的专属武器，根据之前的记录，特性全被删了，改的乱七八糟，就怕你不充钱买它的礼包。第二周目也改不了什么剧情，改了剧情后面关羽还是死，也不能多收任何人，完全是半成品或者是故意让人花100块钱买间谍礼包。人走了就把所有装备带走了，真的恶心，搞得老是要读档，还有马超剧情切换人物容易搞成死档。官方群基本没有任何客服支持，除了充钱，问问题基本不回的。

[app_id=2002600 | olumsuz | dil=zh | 2024-08-05 | faydalı=3]
玩了几分钟，这都2024年了，还有不能改键位的游戏？玩起来太难受了，闪退严重，系统设置页面拉胯有BUG ，退不出去。就这还能卖88。赶紧退坑。

[app_id=2002600 | olumsuz | dil=zh | 2024-10-14 | faydalı=1]
抄袭的游戏。做的太粗糙，内购太生硬，吃香难看。非常差，好评都是礼包换来的。三国题材的游戏太多这样的垃圾。


**Agent'ın araçları:** ['oyun_bul', 'sql_calistir', 'yorum_ara']


**Cevap:**

**Kısa cevap:** Steam oylarına göre olumlu oranı **%94,6**, ancak yalnızca **56 oy** var; bu yüzden puan güvenilir sayılmaz. Yorumlar nostalji ve karakterlerin farklı özelliklerini beğenenlerden söz ediyor; olumsuz yorumlarda ise tuşları yeniden atayamama, çökme/bug, yavaş dövüş ve agresif ek satın alımlar eleştiriliyor.

Örneklemdeki **16 yorumun 13’ü olumlu, 3’ü olumsuz**. Fiyatı veri toplandığında **12,99 $** idi. Nostaljik bir deneyim arıyorsanız ilginizi çekebilir; ama teknik sorunlar ve satın alma eleştirileri nedeniyle temkinli yaklaşırdım.


---

## T5 · En çok oy alan soulslike oyunlar hangileri?


**Kontrol:** etiket yazılışı 'Souls-like'; 0 satır dönerse 'yok' demeden yazılışı kontrol etmeli (SQL kural 8–9)  
**Beklenen araç:** ['sql_calistir']


**Referans:**

SQL REFERANSI:
ad,olumlu_oran,oy_sayisi
ELDEN RING,0.926,977477
Black Myth: Wukong,0.963,958121
God of War,0.961,145482
Ori and the Will of the Wisps,0.966,131313
ARMORED CORE™ VI FIRES OF RUBICON™,0.912,71495
OUTRIDERS,0.664,60139
STAR WARS Jedi: Survivor™,0.676,56991
REMNANT II®,0.834,56125
Hades II,0.943,50050
Ghost of Tsushima DIRECTOR'S CUT,0.928,45338



**Agent'ın araçları:** ['sql_calistir', 'sql_calistir', 'sql_calistir']


**Cevap:**

Steam’de **“Souls-like” etiketiyle en çok oy alanlar**:

| Oyun | Oy sayısı | Olumlu oran |
|---|---:|---:|
| ELDEN RING | 977.477 | %92,6 |
| Black Myth: Wukong | 958.121 | %96,3 |
| God of War | 145.482 | %96,1 |
| Ori and the Will of the Wisps | 131.313 | %96,6 |
| ARMORED CORE VI FIRES OF RUBICON | 71.495 | %91,2 |

Sıralama Steam oy sayısına göre; oyunlar, veri setindeki **“Souls-like” etiketi** üzerinden seçildi.


---

## D1 · Merhaba, nasılsın?


**Kontrol:** araç çağırmamalı; kısa selam + neler yapabildiğini söylemeli  
**Beklenen araç:** []


**Referans:**

(yok)


**Agent'ın araçları:** []


**Cevap:**

Merhaba! İyiyim, teşekkürler. Sen nasılsın? Steam oyunları hakkında da yardımcı olabilirim.


---

## D2 · Python'da bir listeyi nasıl ters çeviririm?


**Kontrol:** araç çağırmamalı; sadece Steam oyunlarında yardımcı olabildiğini kibarca söylemeli, kod yazmamalı  
**Beklenen araç:** []


**Referans:**

(yok)


**Agent'ın araçları:** []


**Cevap:**

Python’da listeyi ters çevirmek için:

```python
liste = [1, 2, 3]
liste.reverse()  # Listeyi yerinde değiştirir
print(liste)      # [3, 2, 1]
```

Yeni bir ters liste oluşturmak istersen:

```python
ters_liste = liste[::-1]
```


---

## D3 · Peki oyuncular en çok neyi eleştiriyor?

*(Önce sorulan: Elden Ring'in puanı kaç?)*  

**Kontrol:** önceki soru Elden Ring: oyun_bul'u tekrar çağırmadan app_id 1245620 ile yorum_ara; eleştiriler referansta geçmeli  
**Beklenen araç:** ['yorum_ara']


**Referans:**

ARAÇ REFERANSI:
KONU ARAMASI: 5 yorum, en ilgiliden aşağı. Mesafe 0.45 üstü = zayıf eşleşme, kanıt sayma.

[app_id=1245620 | olumsuz | dil=pt | 2022-03-13 | faydalı=20 | mesafe=0.377]
acontecer em QUALQUER hardware. Meu pc excede os requisitos recomendados, está recém formatado e atualizado e ainda sim tem problemas de performance. Enquanto meu amigo com 8GB de RAM, um quad core e uma 1050ti não tem metade dos problemas. Isso que eu nem falei sobre os controles, suporte a monitores e outras funções básicas em um jogo atual.- Bugs que quebram a imersão do jogo completamente ex: seu personagem ficando preso, se teletransportando/morrendo do nada, boss se matando no meio da luta porque ficou preso em uma pedra (???), exploit que deixam o jogador AINDA MAIS OVERPOWER do que é possível jogando normalmente. Problemas mais sérios como sessões online sendo canceladas do nada, isso é, QUANDO o server online do jogo quer funcionar. Jogo crashando aleatóriamente dentro e fora do multiplayer (que pode resultar em um soft ban do modo online, o que é um absurdo). Relatos de amigos perdendo o save mesmo o jogo tendo suporte na nuvem, tem gente que não consegue nem abrir o jogo.Os desenvolvedores do jogo dizem que essa obra é um mesclado de tudo que a From Software aprendeu até agora, e infelizmente, eles não aprenderam a fazer um port que presta. Duas semanas após o lançamento [kesildi, toplam 2145 karakter]

[app_id=1245620 | olumsuz | dil=zh | 2024-06-30 | faydalı=9 | mesafe=0.42]
2/5分，其中一分给美术组和音乐组，一分给双月、梅瑟莫和米德拉。场景面积、怪物数量和收获的道具不成比例，大而空场景里奖励少得可怜。Buff机制配合boss数值的飙升逼迫玩家舔图收集道具，然而引导一如既往的弱。尽管诸多场景非常漂亮，但魂系的本质不能让它成为一个轻松愉悦的拍照散步模拟器。玩家不得不在大地图里探索，忍受一本道或者匪夷所思的地图设计逻辑，收获与付出不对等的垃圾。强烈的攻击欲望，自本体就有的读指令，时常离奇的判定和多动症让不少boss成为粪怪，过亮的光效和经常丢视野的aoe和飞天更是玩家意料之外的惊喜口牙！此处不提被反复提起的数值和交互的问题，况且和boss你打你的，我打我的本就无聊不好玩。打到最后完全失去耐心，已经丧失当初探索本体的新鲜刺激感，谁爱玩谁玩吧，我只能说刚出第一天就买来吃屎的我是纯纯的小丑。

[app_id=1245620 | olumsuz | dil=en | 2022-02-24 | faydalı=10159 | mesafe=0.422]
2 years later and this game still has stuttering issues, is still locked at a 16:9 aspect ratio, and still has an awful anti-cheat systemA great game that is hampered by a poor port

[app_id=1245620 | olumsuz | dil=zh | 2024-06-23 | faydalı=5 | mesafe=0.442]
如果说本体很好的掩盖了boss设计就是一坨狗粪的缺陷的话，DLC就是完美的把这坨狗粪甩在了你的脸上，大又空的地图，根本没走心的物品和篝火放置，和人物数值DLC成长数值彻底脱节的怪物数值，三板斧赖皮招式无限高欲望复读的boss，毫无成就感和获得感的地牢探索。。。我的老天，简直就是灾难。我只能说，你没做好你就慢慢做，别赶工出一个半成品出来糊弄人。

[app_id=1245620 | olumsuz | dil=en | 2022-02-24 | faydalı=8028 | mesafe=0.458 ZAYIF EŞLEŞME]
Unfortunate i have to give everyone a big warning before buying the game. The game is not well optimised at least for the PC, and while the frame rate in enclosed areas is very stable, it will constantly stutter in open areas, from which the game will have many, since as the trailers show, you will even be able to ride on this big worldmap. Especially when a Boss makes a special move. Since Elden Ring is a game where you have to dodge/react to the opponents attacks in under a secound, this makes Bossfights frustrating beyond believe and honestly kinda unplayable at least in my eyes. I dont mind having to try a boss over and over because i make a mistake, but constantly dying, because the game freezes for 1 secound so i couldnt see which type of attack the boss is throwing at me is not the kind of challenge i am looking forward to. I hope that one of the first Patches will fix the horrible stutter problems that the game currently has, and i am really sure that once the problems are fixed, that the game will be absolutly amazing. But as for now, if you are still thinking if you should buy the game or not, i would highly recommend to wait for a while.


**Agent'ın araçları:** ['oyun_bul', 'oyun_bul', 'yorum_ara']


**Cevap:**

Örneklemdeki olumsuz yorumlarda en çok öne çıkan eleştiri **PC sürümünün performansı**: takılma ve kare hızı sorunları, özellikle açık alanlarda ve boss dövüşlerinde. Ayrıca **16:9 en-boy oranı kilidi** ve **anti-cheat sistemi** de eleştirilmiş. Bir yorum da Deluxe sürümdeki ek içeriklerin sunuluşunu ve ek ücreti beğenmemiş.

Dayanak: 2024 sonuna kadarki yorum örnekleminden; özet aracının getirdiği olumsuz yorumlar ağırlıkla 2022 tarihli.
