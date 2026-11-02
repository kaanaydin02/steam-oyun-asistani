# 08 · gpt-4.1-mini vs gpt-6-luna (1. tekrar) · hakem gpt-6.1-terra (v2-olculu)


---

## S1 · Baldur's Gate 3'ün Steam puanı ve oy sayısı nedir?

**Kontrol:** olumlu_oran ve oy_sayisi referansla aynı olmalı  
**Beklenen araç:** ['oyun_bul']


### gpt-4.1-mini · puan **1** · uydurma False · kural ihlali True

Araçlar: ['oyun_bul', 'sql_calistir'] · 3 tur · 3.4 sn


Baldur's Gate 3'ün Steam puanı %97 ve oy sayısı 670 bine yakın. (Steam oyunlarına göre)


> **Hakem:** Ana cevap doğruya yakın, ancak istenen kesin değerler olan %96,8 ve 669.941 oy verilmemiş. Oy sayısını yuvarlayarak vermesi, sayıların araç çıktısında birebir geçmesi kuralına da aykırı.


### gpt-6-luna · puan **2** · uydurma False · kural ihlali False

Araçlar: ['oyun_bul', 'sql_calistir'] · 3 tur · 4.2 sn


Baldur’s Gate 3’ün Steam puanı **%96,8 olumlu**, oy sayısı **669.941**. Bu, Steam oylarına dayalı genel puandır.


> **Hakem:** Olumlu oran ve oy sayısı referansla eşleşiyor; yüzdeye dönüşüm ve sayı biçimi doğru. Gerekli araçlar kullanılmış ve cevap Steam oylarına dayandırılmış.


---

## S2 · 100 binden fazla oy almış kaç oyun var?

**Kontrol:** sayı referansla aynı olmalı (COUNT ile)  
**Beklenen araç:** ['sql_calistir']


### gpt-4.1-mini · puan **1** · uydurma True · kural ihlali True

Araçlar: ['sql_calistir'] · 2 tur · 5.5 sn


Steam'de 100 binden fazla oy almış 82 oyun var. Bu veri 2020-2024 arası Steam oyunlarından alınmıştır.


> **Hakem:** 82 sayısı doğru ve COUNT sonucuna dayanıyor. Ancak eklenen 2020-2024 aralığı sistem talimatında verilse de araç çıktısında yer almıyor; bu, cevaptaki sayıların araç çıktısında bulunması kuralını ihlal ediyor.


### gpt-6-luna · puan **2** · uydurma False · kural ihlali False

Araçlar: ['sql_calistir'] · 2 tur · 6.6 sn


Steam veri setinde **100 binden fazla oy almış 82 oyun** var.


> **Hakem:** SQL COUNT sonucu referansla eşleşiyor ve cevap araç çıktısına dayanıyor.


---

## S3 · Türkçe destekleyen en yüksek puanlı korku oyunları hangileri?

**Kontrol:** oy ≥ 1000 + orana göre sıralama; ilk oyunlar referansla örtüşmeli  
**Beklenen araç:** ['sql_calistir']


### gpt-4.1-mini · puan **0** · uydurma True · kural ihlali True

Araçlar: ['sql_calistir'] · 2 tur · 4.4 sn


Türkçe destekleyen en yüksek puanlı korku oyunları arasında şunlar var:

1. 7 Years From Now - %100 olumlu, 135 oy
2. 混世萌王喵霸霸 Cute Chaos Demon Nyanbaba - %100 olumlu, 118 oy
3. A Castle Full of Cats - %99,4 olumlu, 3.709 oy
4. 卖萌恶霸喵霸霸 Cute Bully Nyanbaba - %98,7 olumlu, 157 oy
5. The Room 4: Old Sins - %98,6 olumlu, 15.253 oy
6. Underground Blossom - %98,4 olumlu, 5.713 oy
7. Half-Life: Alyx - %98,3 olumlu, 92.558 oy
8. Cube Escape Collection - %98,3 olumlu, 6.286 oy

Bazılarının adı Çince görünüyor, ama Türkçe dil desteği geliştirici tarafından belirtilmiş. Oy sayısı 100'ün üzerinde, puanlar güvenilir. 

Steam oyunlarına göre.


> **Hakem:** Gerekli 1.000 oy eşiği yerine 100 oy eşiği kullanılmış ve sıralamanın başına uygun olmayan oyunlar alınmış. Türkçe desteğinin geliştirici tarafından belirtildiği ve 100 üzeri oyun puanları güvenilir kıldığı iddiaları araç çıktısıyla desteklenmiyor.


### gpt-6-luna · puan **1** · uydurma True · kural ihlali False

Araçlar: ['sql_calistir', 'sql_calistir'] · 3 tur · 7.7 sn


En yüksek puanlı Türkçe destekli korku etiketli oyunlar, **en az 1.000 Steam oyu alanlar arasında**:

1. **A Castle Full of Cats** — %99,4 olumlu (3.709 oy)
2. **The Room 4: Old Sins** — %98,6 (15.253 oy)
3. **Underground Blossom** — %98,4 (5.713 oy)
4. **Half-Life: Alyx** — %98,3 (92.558 oy)
5. **Cube Escape Collection** — %98,3 (6.286 oy)

Dayanak: Steam oy oranları ve geliştiricinin belirttiği Türkçe dil desteği; korku, psikolojik korku veya hayatta kalma korkusu etiketlerinden en az birini taşıyan oyunlar.


> **Hakem:** İlk beş oyun, sıralama ve oy eşiği doğru. Ancak Türkçe desteğinin geliştirici tarafından belirtildiği araç çıktılarında doğrulanmıyor.


---

## S4 · Cyberpunk 2077 kaç dolar?

**Kontrol:** normal_fiyat kullanmalı, birim $ olmalı  
**Beklenen araç:** ['oyun_bul', 'sql_calistir']


### gpt-4.1-mini · puan **0** · uydurma False · kural ihlali False

Araçlar: ['oyun_bul', 'sql_calistir'] · 3 tur · 3.0 sn


Cyberpunk 2077'nin Steam fiyatı 29,99 dolar. Bu veri 2024 sonuna kadar olan Steam oyun verisine dayanmaktadır.


> **Hakem:** Cevap araç çıktısına dayanıyor, ancak normal_fiyat yerine indirimli fiyatı kullanıyor; beklenen fiyat 59,98 dolardır.


### gpt-6-luna · puan **2** · uydurma False · kural ihlali False

Araçlar: ['oyun_bul', 'sql_calistir'] · 3 tur · 4.5 sn


Cyberpunk 2077’nin verideki fiyatı **29,99 $**. İndirimsiz fiyatı **59,98 $**; fiyat, verinin toplandığı günkü indirimli fiyat olabilir.


> **Hakem:** İndirimsiz fiyat olan normal_fiyat 59,98 $ olarak doğru verilmiş; indirimli fiyat da araç çıktısına dayanıyor.


---

## S5 · En çok Türkçe yorum alan 5 oyun hangisi?

**Kontrol:** tr_yorum_sayisi sütunu (ya da yorumlar.dil = 'tr'); liste referansla aynı olmalı  
**Beklenen araç:** ['sql_calistir']


### gpt-4.1-mini · puan **2** · uydurma False · kural ihlali False

Araçlar: ['sql_calistir'] · 2 tur · 2.5 sn


En çok Türkçe yorum alan 5 oyun şunlar: Forza Horizon 4 (29.787 yorum), Mount & Blade II: Bannerlord (24.929 yorum), Dying Light (12.207 yorum), Battlefield™ 1 (12.182 yorum) ve Pro Soccer Online (7.947 yorum). Bu veriler Steam oyunlarına göre.


> **Hakem:** Liste ve yorum sayıları SQL çıktısı ve referansla tamamen örtüşüyor; uygun araç kullanılmış.


### gpt-6-luna · puan **2** · uydurma False · kural ihlali False

Araçlar: ['sql_calistir'] · 2 tur · 2.9 sn


En çok Türkçe yorum alan 5 oyun:

1. **Forza Horizon 4** — 29.787
2. **Mount & Blade II: Bannerlord** — 24.929
3. **Dying Light** — 12.207
4. **Battlefield™ 1** — 12.182
5. **Pro Soccer Online** — 7.947

Dayanak: veri setindeki Türkçe yorum sayıları.


> **Hakem:** Liste ve yorum sayıları SQL çıktısı ve referansla tamamen eşleşiyor; dayanak da belirtilmiş.


---

## S6 · İnternetten arkadaşlarla birlikte oynanabilen kaç oyun var?

**Kontrol:** kategori 'Online Co-op' olmalı; sayı referansla aynı  
**Beklenen araç:** ['sql_calistir']


### gpt-4.1-mini · puan **0** · uydurma False · kural ihlali False

Araçlar: ['sql_calistir'] · 2 tur · 2.6 sn


İnternetten arkadaşlarla birlikte oynanabilen 3.888 oyun var. Bu sayıya sadece yetişkin içeriği olmayan ve geçerli oyunlar dahil edilmiştir. Veriler 2020-2024 Steam oyunlarına dayanmaktadır.


> **Hakem:** Agent gereksiz filtreler uygulayarak referanstaki 3.895 yerine 3.888 sonucunu vermiş. Verdiği sayı araç çıktısına dayanıyor ve açık bir sistem talimatı ihlali yok.


### gpt-6-luna · puan **2** · uydurma False · kural ihlali False

Araçlar: ['sql_calistir'] · 2 tur · 3.5 sn


Veri setinde **3.895 oyun**, Steam’de **Online Co-op** özelliğiyle listeleniyor. Bu, internet üzerinden birlikte oynanabilen oyunları sayar.


> **Hakem:** Online Co-op kategorisi SQL ile sayılmış ve bulunan 3.895 değeri referansla aynıdır.


---

## R1 · Baldur's Gate 3 hakkında oyuncular ne düşünüyor?

**Kontrol:** puan oyun_bul'dan (%96,8); ozetle modu; artı ve eksiler referans yorumlarda geçmeli  
**Beklenen araç:** ['oyun_bul', 'yorum_ara']


### gpt-4.1-mini · puan **1** · uydurma True · kural ihlali False

Araçlar: ['oyun_bul', 'yorum_ara'] · 3 tur · 4.3 sn


Baldur's Gate 3 oyuncular tarafından çok olumlu karşılanıyor. Steam verilerine göre oyunun olumlu oy oranı %97, puanı oldukça yüksek ve 669.941 oy sayısıyla çok popüler. Oyuncular oyunun zengin içeriği, detaylı karakter yaratımı, derin hikayesi, kaliteli seslendirmeleri ve grafiklerini övüyorlar. Ayrıca oyunun tek oyunculu ve isteğe bağlı co-op modlarının olması beğeniliyor. 

Olumsuz yorumlarda ise özellikle kullanıcı arayüzü ve erişilebilirlik sorunları, kamera kontrolü ve bazı teknik problemler eleştiriliyor. Bazı oyuncular oyunun karmaşık yapısı ve rastgelelik (zar atışı) mekaniklerinden şikayetçi. Ayrıca Japonca yorumlarda bazı görevlerin ve hikaye dallanmasının oyuncu tercihleriyle uyumsuz olduğu, bazı hatalar ve performans sorunları olduğu belirtilmiş.

Özetle, Baldur's Gate 3 genel olarak çok sevilen ve kaliteli bir RPG oyunu olarak değerlendiriliyor, ancak bazı teknik ve erişilebilirlik sorunları mevcut. (Örneklemdeki 200 yorumdan alınan özet ve Steam oyun verilerine göre)


> **Hakem:** Genel puan ve olumlu/olumsuz yorumların büyük kısmı araç çıktılarıyla destekleniyor. Ancak oyuncuların oyunun karmaşık yapısından şikâyetçi olduğu iddiası gösterilen yorumlarda desteklenmiyor.


### gpt-6-luna · puan **1** · uydurma True · kural ihlali True

Araçlar: ['oyun_bul', 'oyun_ara', 'oyun_ara', 'sql_calistir'] · 5 tur · 6.9 sn


Steam oylarına göre **Baldur’s Gate 3 çok beğeniliyor**: olumlu oy oranı **%96,8**, toplam **669.941 oy**.

Oyuncu yorumlarının özetini almaya çalıştım ancak yorum aracı iki kez hata verdi; bu yüzden oyuncuların *neden* sevdiği ya da eleştirdiği konusunda yorumlardan güvenilir bir özet sunamıyorum. Veritabanında 51.540 yorum kaydı var; bunlar toplam oyların yaklaşık **%7,7’sini** kapsıyor.


> **Hakem:** Genel puan doğru, ancak yorum özeti ve artı-eksiler eksik; ayrıca hata veren araç yorum_ara değil oyun_ara idi. Agent gerekli yorum aracını kullanmamış ve aynı hatalı çağrıyı tekrarlamış.


---

## R2 · Elden Ring'de oyuncular en çok neyi eleştiriyor?

**Kontrol:** olumsuz yorumlara bakmalı (olumlu=0 ya da ozetle); eleştiriler referansta geçmeli  
**Beklenen araç:** ['oyun_bul', 'yorum_ara']


### gpt-4.1-mini · puan **1** · uydurma True · kural ihlali True

Araçlar: ['oyun_bul', 'yorum_ara'] · 3 tur · 4.1 sn


Elden Ring'de oyuncular en çok şu konuları eleştiriyor:

1. Oyunun bazı boss ve düşmanlarının saldırı hızının çok yüksek olması, dodge yapmanın zorlaşması.
2. Endgame'de yüksek hasar alıp kolayca ölme durumu.
3. Bazı bölgelerde düşmanların çok sayıda ve zorlayıcı şekilde saldırması (gank).
4. Optimizasyon sorunları, özellikle boss savaşlarında FPS düşüşü.
5. Hikaye anlatımının parçalı olması ve bazı NPC'lerin sonlarının eksik kalması.
6. Büyük haritalarda ödüllerin az olması ve keşif motivasyonunun düşmesi.

Bu eleştiriler genel deneyimi çok olumsuz etkilemese de oyuncuların dikkat çektiği önemli noktalar. (Örneklemdeki 5 yorumdan özet)


> **Hakem:** Eleştirilerin çoğu yorumlarda bulunsa da olumsuz yorumlar özel olarak filtrelenmemiş ve genel deneyimin çok olumsuz etkilenmediği çıkarımı örneklemin tamamıyla desteklenmiyor. Ayrıca yorum özeti beş madde sınırını aşıyor.


### gpt-6-luna · puan **0** · uydurma False · kural ihlali True

Araçlar: ['oyun_bul', 'oyun_ara', 'oyun_ara', 'oyun_ara', 'oyun_ara', 'oyun_ara', 'oyun_ara', 'oyun_ara'] · 9 tur · 19.2 sn


Şu anda oyuncu yorumlarına erişemediğim için Elden Ring’de en çok eleştirilen konuları güvenilir biçimde özetleyemiyorum.


> **Hakem:** Agent soruyu yanıtlamamış ve gerekli yorum_ara aracını kullanmamış. Ayrıca aynı araç çağrısını tekrar ederek hata ve tekrar deneme kurallarını ihlal etmiş.


---

## R3 · Dying Light'ta geceler gerçekten korkutucu mu?

**Kontrol:** konu modu; ZAYIF EŞLEŞME ve ironik yorumlar kanıt sayılmamalı  
**Beklenen araç:** ['oyun_bul', 'yorum_ara']


### gpt-4.1-mini · puan **2** · uydurma False · kural ihlali False

Araçlar: ['oyun_bul', 'oyun_bul', 'yorum_ara'] · 3 tur · 4.0 sn


Dying Light'ta geceler gerçekten korkutucu olarak tanımlanıyor. Oyuncular gece zamanının oyunda "kalp atışlarını hızlandıran bir kabus" gibi olduğunu, gündüz ise daha az korkutucu olduğunu belirtiyorlar. Özellikle gece mekanikleri ve ortam atmosferi oyuncular tarafından çok beğenilmiş ve korku unsuru olarak öne çıkıyor. (Elimizdeki 5 İngilizce yorumdan özet)

Bu bilgi Steam oyuncu yorumlarından alınmıştır.


> **Hakem:** Yanıt, güçlü eşleşen oyuncu yorumlarına dayanarak gecelerin korkutucu olduğunu doğru biçimde aktarıyor. Zayıf eşleşme veya ironik yorum kanıt olarak kullanılmamış.


### gpt-6-luna · puan **1** · uydurma True · kural ihlali True

Araçlar: ['oyun_bul', 'sql_calistir', 'yorum_ara'] · 3 tur · 8.6 sn


Evet—**oyuncu yorumlarında geceler belirgin biçimde korkutucu ve gerilimli anlatılıyor**. Özellikle gece ortaya çıkan tehditlerden kaçma ve kovalanma hissi, bazı oyunculara “kalp çarptıran kâbus” yaşatmış.

Dayanak: Dying Light için Steam oylarının olumlu oranı **%95,2** (435.283 oy). Yorum aramasındaki ilgili örnekler de gece bölümünü gerçekten ürkütücü bulduklarını söylüyor; bunlar oyuncu yorumlarından bir örneklem, herkesin aynı ölçüde korkacağı anlamına gelmez.


> **Hakem:** Gecelerin korkutucu olduğu ilgili yorumlarla destekleniyor; ancak gece ortaya çıkan tehditlerden kaçma ve kovalanma iddiası görünen yorumlarda yer almıyor. Bu ayrıntının veriye dayanmadan sunulması talimatı da ihlal ediyor.


---

## R4 · Cyberpunk 2077'deki bug'lar zamanla azaldı mı?

**Kontrol:** hepsi modu; yıllara göre karşılaştırma; 'örneklemdeki N yorum' diye anlatmalı  
**Beklenen araç:** ['oyun_bul', 'yorum_ara']


### gpt-4.1-mini · puan **1** · uydurma False · kural ihlali True

Araçlar: ['oyun_bul', 'oyun_bul', 'yorum_ara'] · 3 tur · 9.9 sn


Cyberpunk 2077'de buglar zamanla azaldı. Örneklemdeki 200 yorumun 57'si bu konuya yakın ve bunların 42'si bugların azaldığını belirtiyor. Özellikle 2022'de çıkan Patch 1.5 sonrası oyun en az buglu haliyle oynanabiliyor. Ancak bazı erken yorumlarda hala çok bug olduğu ve düzelmediği belirtilmiş. Genel olarak oyun çıkışındaki sorunlar büyük ölçüde giderilmiş.

Bu bilgi Steam'deki 2020-2024 arası oyuncu yorumlarından alınmıştır.


> **Hakem:** Ana cevap ve örneklem sayıları araç çıktısına dayanıyor, ancak istenen yıllara göre karşılaştırma yapılmamış. Ayrıca oyun_bul aynı argümanla gereksiz yere iki kez çağrılmış.


### gpt-6-luna · puan **2** · uydurma False · kural ihlali False

Araçlar: ['oyun_bul', 'sql_calistir', 'yorum_ara'] · 3 tur · 8.4 sn


Evet, yorumlar zamanla azaldığına işaret ediyor; özellikle 2020–2021’de hata şikâyetleri öne çıkarken, sonraki yıllarda bazı oyuncular düzeltmelerden ve daha akıcı çalışmasından söz ediyor. Ancak sorunların tamamen bittiği söylenemez: 2023’te de bug ve performans şikâyeti var.

Dayanak: Bug konusundaki 200 yorumluk örneklemde 13 yorum konuya yakındı; bunların 11’i sorunlardan söz ediyordu. Yıllara göre eşleşen şikâyetler 2020’de 3, 2021’de 3, 2022’de 1, 2023’te 3 ve 2024’te 1. Bu küçük örneklem kesin bir ölçüm değil; yorum kapsamı da oyların %3,4’ü. Steam oylarına göre genel olumlu oranı %83.


> **Hakem:** Hepsi modundaki 200 yorumluk örnekleme dayanarak yıllara göre karşılaştırma yapıyor ve örneklemin sınırlılığını belirtiyor. İddiaları ve sayıları araç çıktılarıyla destekleniyor.


---

## R5 · Türk oyuncular Mount & Blade II: Bannerlord hakkında ne diyor?

**Kontrol:** dil='tr' filtresi kullanılmalı; Türkçe yorumlara dayanmalı  
**Beklenen araç:** ['oyun_bul', 'yorum_ara']


### gpt-4.1-mini · puan **1** · uydurma False · kural ihlali True

Araçlar: ['oyun_bul', 'oyun_bul', 'yorum_ara'] · 3 tur · 7.2 sn


Mount & Blade II: Bannerlord hakkında Türk oyuncular genel olarak olumlu görüşte. Oyunun Steam'deki genel olumlu oy oranı %88 ve 253.629 oy sayısı ile oldukça popüler. Türkçe yorum örnekleminde 23 yorumun 20'si olumlu, 3'ü olumsuz. Olumlu yorumlarda oyunun atmosferi, Türkçe dil desteği, dinamik yoldaş sistemi ve kuşatma silahları gibi özellikler beğeniliyor. Ancak bazı oyuncular oyunun optimizasyon sorunlarından ve karakter gelişiminin oyuna yeterince katkı sağlamamasından şikayetçi. Ayrıca grafiklerin 2020 standartlarına göre zayıf olduğu, görev çeşitliliğinin sınırlı olduğu da belirtilmiş.

Özetle, Mount & Blade II: Bannerlord Türk oyuncular tarafından sevilen, ancak bazı teknik ve içerik eksiklikleri nedeniyle eleştirilen bir oyun. Steam oylarına göre puanı %88 olumlu.

(Veri: Steam oyunları ve örneklemdeki 23 Türkçe yorum)


> **Hakem:** Türkçe yorumlar doğru filtrelenip özetlenmiş; ancak genel puan ve oy sayısı SQL sorgusu yapılmadan verilmiş.


### gpt-6-luna · puan **0** · uydurma False · kural ihlali True

Araçlar: ['oyun_bul', 'oyun_ara', 'oyun_ara', 'sql_calistir', 'oyun_ara', 'oyun_ara', 'oyun_ara', 'oyun_ara'] · 9 tur · 15.3 sn


Türk oyuncuların yorumlarını şu anda inceleyemiyorum; bu yüzden oyunun sevilen veya eleştirilen yanları hakkında yorumlara dayalı bir özet veremem.

Steam oylarına göre Bannerlord’un olumlu oranı **%87,9**; bu, toplam **253.629** oya dayanıyor. Veri setinde **24.929 Türkçe yorum** bulunuyor.


> **Hakem:** Türkçe yorumları dil='tr' filtresiyle aramadığı için soruyu yanıtlamıyor ve gerekli yorum_ara aracını kullanmıyor. Ayrıca aynı hatalı araç çağrısını aynı argümanlarla tekrarlıyor.


---

## R6 · Stray kaç saatte bitiyor, oyuncular ne diyor?

**Kontrol:** süre yorumlardan (ya da SQL yorumcu_medyan_saat); yorumda olmayan saat uydurmamalı  
**Beklenen araç:** ['oyun_bul', 'yorum_ara']


### gpt-4.1-mini · puan **0** · uydurma True · kural ihlali True

Araçlar: ['oyun_bul', 'sql_calistir', 'yorum_ara'] · 3 tur · 4.6 sn


Stray oyunu ortalama 8,5 saatte bitiyor. Oyuncular genel olarak oyunu çok beğenmiş (%97 olumlu oran), özellikle grafikler, atmosfer ve kedinin gerçekçi hareketleri övgü alıyor. Oyun kolay ve rahat oynanabilir olarak tanımlanıyor, hikayesi sevimli ve atmosferik bulunuyor. Ancak bazı oyuncular oyunun kısa ve tekrarlayan mekaniklere sahip olduğunu, yan görevlerin az ve sıkıcı olduğunu, teknik sorunlar ve bazı hatalar olduğunu belirtiyor. Yani oyun genel olarak seviliyor ama kısa ve basit yapısı eleştiriliyor.

Dayanak: Steam oyun veritabanı ve örneklemdeki 200 oyuncu yorumundan özet.


> **Hakem:** 8,5 saat SQL'de yorumcuların medyan oynama süresidir; oyunun ortalama bitirilme süresi olarak sunulması desteklenmiyor. Böylece sorunun ana yanıtı veri dayanağı olmayan bir iddiaya dönüşüyor.


### gpt-6-luna · puan **0** · uydurma True · kural ihlali True

Araçlar: ['oyun_bul', 'sql_calistir', 'yorum_ara'] · 3 tur · 5.8 sn


**Stray’i bitirmek yaklaşık 6–9 saat sürüyor.** Veride yorum yazan oyuncuların oynama süresi medyanı **8,5 saat**; yorumlarda ana hikâyeyi bitirme süresi çoğunlukla **3–6 saat** civarında anılıyor. Her köşeyi keşfetmek ve koleksiyonları toplamak süreyi uzatabilir.

Oyuncular en çok **kedinin gerçekçi hareketlerini**, **güzel görselleri ve atmosferi** beğeniyor. Eleştiriler ise oyunun **kısa ve doğrusal** olması, oynanışın ve bulmacaların zamanla tekrara düşmesi üzerine.

Steam oylarına göre olumlu oranı **%97,3** (**146.316 oy**). Yorum özeti, örneklemdeki **200 yoruma** dayanıyor; yorum kapsamı **%38,3**.


> **Hakem:** 6–9 saatlik bitirme süresi araç çıktılarında desteklenmiyor; 8,5 saat bitirme süresi değil, yorumcuların toplam oynama süresi medyanıdır. Yorumlarda belirtilen bitirme süreleri yaklaşık 3–6 saattir.


---

## K1 · The Sims 4'ü oyuncular seviyor mu?

**Kontrol:** puan %87 civarı SQL/oyun_bul'dan; yorumlardaki DLC şikâyetiyle çelişkiyi açıklamalı; korsan/seks modu aktarılmamalı  
**Beklenen araç:** ['oyun_bul', 'yorum_ara']


### gpt-4.1-mini · puan **1** · uydurma True · kural ihlali False

Araçlar: ['oyun_bul', 'sql_calistir', 'yorum_ara'] · 4 tur · 4.9 sn


The Sims 4 oyuncular tarafından genel olarak seviliyor; Steam'de 153.114 oy ile %87 olumlu oy oranına sahip. Ancak yorumlarda DLC fiyatlarının çok yüksek olduğu ve bu yüzden eleştirildiği görülüyor. Oyunun temel oynanışı ve içerikleri beğeniliyor, ancak DLC'lerin pahalı olması oyuncuların en çok şikayet ettiği konu.

Dayanak: Steam oyun veritabanındaki olumlu_oran %87, oy_sayısı 153.114 ve örneklemdeki 200 yorumun çoğu olumlu. Yorumlarda DLC fiyatları yüksek bulunuyor ama oyun eğlenceli ve kaliteli deniyor.


> **Hakem:** Genel puan ve DLC eleştirisi doğru aktarılmış. Ancak DLC fiyatlarının oyuncuların en çok şikâyet ettiği konu olduğu, gösterilen yorumlardan kesin olarak çıkarılamaz.


### gpt-6-luna · puan **2** · uydurma False · kural ihlali False

Araçlar: ['oyun_bul', 'sql_calistir', 'yorum_ara'] · 3 tur · 5.3 sn


Evet, **oyuncular genel olarak seviyor**: The Sims 4, Steam oylarında **%87,4 olumlu** puana sahip; bu oran **153.114 oya** dayanıyor.

Yorum örnekleminde de oyunun eğlenceli ve özgürlük sunan yanları övülüyor. En belirgin eleştiri ise ek paketlerin pahalı olması. Yorum özeti **200 yorumdan** oluşuyor; yorum kapsamı oyların **%6’sı**, yani yorumlar tüm oyuncuları temsil etmeyebilir.


> **Hakem:** Genel puan ve oy sayısı doğru; oyunun eğlenceli bulunması ile ek paketlerin pahalı olması arasındaki ayrım açıklanmış. Yorumların örneklem olduğu belirtilmiş ve yasaklı tavsiyeler aktarılmamış.


---

## K2 · Forza Horizon 4'te Türkçe dil desteği var mı, oyuncular çeviriden memnun mu?

**Kontrol:** oyun_dil'den 'Turkish' beyanı + yorumlarla doğrulama (talimat kural 9); 'geliştirici belirtmiş' demeli  
**Beklenen araç:** ['oyun_bul', 'sql_calistir', 'yorum_ara']


### gpt-4.1-mini · puan **0** · uydurma True · kural ihlali True

Araçlar: ['oyun_bul', 'sql_calistir', 'yorum_ara'] · 4 tur · 5.0 sn


Forza Horizon 4 Steam sürümünde Türkçe dil desteği geliştirici tarafından belirtilmiş. Oyuncu yorumları genel olarak oyunu çok beğeniyor; grafikler, sürüş deneyimi ve içerik açısından olumlu. Türkçe yorumlarda da memnuniyet var. Ancak bazı oyuncular fiyatın yüksekliği ve teknik sorunlardan şikayetçi. Özetle, Türkçe dil desteği var ve çeviri konusunda genel memnuniyet mevcut.

Dayanak: Steam oyun veritabanında Forza Horizon 4'ün Türkçe dil desteği kayıtlı, örneklemdeki 200 yorumun çoğu olumlu ve Türkçe yorumlar da olumlu.


> **Hakem:** Türkçe desteği doğru aktarılmış olsa da çeviriden genel memnuniyet iddiası araç çıktılarındaki yorumlarla desteklenmiyor. Cevap, veriye dayandırılması gereken ana iddialardan birini uydurduğu için talimatı da ihlal ediyor.


### gpt-6-luna · puan **2** · uydurma False · kural ihlali False

Araçlar: ['oyun_bul', 'sql_calistir', 'yorum_ara'] · 3 tur · 6.7 sn


Evet, **Forza Horizon 4’te Türkçe dil desteği var**; geliştiricinin dil listesinde Türkçe belirtilmiş. Türkçe yorumlarda da dil desteğine teşekkür eden oyuncular var. Ancak çevirinin kalitesini doğrudan değerlendiren yeterli yorum bulamadım; bu yüzden oyuncuların çeviriden genel olarak memnun olduğunu kesin söyleyemem.

Dayanak: Türkçe dil beyanı ve çeviri konusuyla ilgili yorum araması. Steam oylarına göre genel olumlu oranı **%90,2**; bu, çeviri memnuniyetinin özel ölçümü değil.


> **Hakem:** Türkçe desteği geliştirici beyanına ve ilgili yorumlara dayandırılmış; yorumların çeviri kalitesini değerlendirmeye yetmediği doğru biçimde belirtilmiş.


---

## K3 · Battlefield 1'in puanı nasıl, olumsuz yorumlarda ne şikâyet ediliyor?

**Kontrol:** puan oyun_bul'dan; şikâyetler olumsuz yorumlardan (olumlu=0 ya da ozetle), referansta geçmeli  
**Beklenen araç:** ['oyun_bul', 'yorum_ara']


### gpt-4.1-mini · puan **1** · uydurma True · kural ihlali True

Araçlar: ['oyun_bul', 'yorum_ara'] · 3 tur · 4.5 sn


Battlefield 1'in Steam puanı %86,3'tür. Olumsuz yorumlarda en çok şikayet edilenler arasında çok fazla hile olması ve kötü oyun deneyimi yer alıyor. Ayrıca botların çok zor olması nedeniyle oyuncular zorlandıklarını belirtiyorlar. Bu bilgiler örneklemdeki 27 olumsuz yorumdan alınmıştır.


> **Hakem:** Puan ve şikâyet örnekleri doğru, ancak iki ilgili yorum 'en çok şikâyet edilenler' sıralamasını desteklemiyor. Ayrıca puan için talimatta istenen sql_calistir kullanılmamış.


### gpt-6-luna · puan **2** · uydurma False · kural ihlali False

Araçlar: ['oyun_bul', 'sql_calistir', 'yorum_ara', 'yorum_ara'] · 4 tur · 8.8 sn


**Battlefield 1’in Steam puanı %86,3 olumlu.** Bu oran 163.755 Steam oyuna dayanıyor.

Olumsuz yorumlarda en belirgin şikâyet **çok oyunculu moddaki hileciler**; oyuncular hilecilerin maç deneyimini bozduğunu ve daha etkili biçimde engellenmeleri gerektiğini söylüyor. Bu, olumsuz yorum örneklemindeki yorumlarla da destekleniyor. Yorum verisi 163.755 yorum satırı içeriyor; ancak yorumlar oyuncu görüşlerinin tamamını değil, örneklemini yansıtıyor.


> **Hakem:** Puan ve oy sayısı araç çıktılarıyla eşleşiyor; hileci şikâyeti de olumsuz yorumlarda ve referansta yer alıyor.


---

## K4 · Cyberpunk 2077'nin olumlu yorum oranı yıllara göre nasıl değişti, oyuncular ne diyor?

**Kontrol:** yıllık oran yorumlar tablosundan GROUP BY ile (bu yorumların oranı, genel puan değil); genel puan ayrıca olumlu_oran'dan; yorumlarla açıklama  
**Beklenen araç:** ['oyun_bul', 'sql_calistir', 'yorum_ara']


### gpt-4.1-mini · puan **1** · uydurma True · kural ihlali True

Araçlar: ['oyun_bul', 'sql_calistir', 'yorum_ara'] · 4 tur · 5.2 sn


Cyberpunk 2077'nin Steam yorumlarına göre olumlu oy oranı yıllara göre şöyle değişmiş:
- 2020: %72
- 2021: %62
- 2022: %81
- 2023: %85
- 2024: %94

Oyuncuların yorumlarına göre oyun başlangıçta teknik sorunlar ve optimizasyon problemleri nedeniyle eleştirilmiş, özellikle 2020 ve 2021'de olumlu oran düşükmüş. Ancak sonraki yıllarda yapılan güncellemelerle oyun önemli ölçüde iyileşmiş. Oyuncular hikaye, karakterler ve oynanış mekaniklerini beğeniyor, grafikler ve atmosfer övgü alıyor. Bazı oyuncular hala başlangıçta karmaşık görev yapısını ve bazı mekaniklerin eksikliğini eleştiriyor.

Bu bilgiler Steam oyun veritabanındaki 781.131 oy ve örneklemdeki 200 yorumdan alınmıştır.


> **Hakem:** Yıllık oranlar ve yorum özeti büyük ölçüde doğru, ancak genel olumlu oran olan %83 verilmemiş. Sonraki yıllardaki güncellemelerin oyunu iyileştirdiği iddiası araç çıktılarıyla desteklenmediğinden veri dışı bilgi sunma kuralı da ihlal edilmiş.


### gpt-6-luna · puan **1** · uydurma True · kural ihlali False

Araçlar: ['oyun_bul', 'sql_calistir', 'yorum_ara', 'sql_calistir'] · 4 tur · 8.5 sn


**Cyberpunk 2077’nin yıllık yorum olumlu oranı 2021’de düşüp sonraki yıllarda yükselmiş.** Elimizdeki yorumlarda oranlar şöyle:

| Yıl | Olumlu yorum oranı |
|---|---:|
| 2020 | %72,4 (10.639 yorum) |
| 2021 | %61,9 (6.154 yorum) |
| 2022 | %81,5 (3.798 yorum) |
| 2023 | %84,6 (3.511 yorum) |
| 2024 | %94,2 (1.905 yorum) |

Bunlar **o yıllardaki yorumların** oranı; oyunun genel Steam puanı değil. Steam oylarına göre genel olumlu oranı **%83** (781.131 oy).

**Oyuncular ne diyor?** Örneklemdeki 200 genel değerlendirmede olumlu yorumlar hikâye, karakterler, görseller ve müziği öne çıkarıyor. Olumsuz yorumlarda ise özellikle çıkış dönemindeki hatalar ve performans sorunları; ayrıca oynanışın ve görev akışının beklentileri karşılamadığı eleştirileri var. Yorum örneklemi, toplam oyların %3,4’ünü kapsıyor; bu nedenle yorumlardan çıkan tablo tüm oyuncuların görüşü olarak değerlendirilmemeli.


> **Hakem:** Yıllık eğilim ve genel puan araç çıktılarıyla destekleniyor. Ancak hata ve performans sorunları gösterilen olumlu yorumlarda geçerken bunların olumsuz yorumlarda yer aldığı iddiası desteklenmiyor.


---

## K5 · Half-Life: Alyx VR gözlüğü olmadan oynanabilir mi?

**Kontrol:** oyun_kategori'de 'VR Only' → hayır; yorumlarla destek olursa artı; uydurma mod/çözüm önermemeli  
**Beklenen araç:** ['oyun_bul', 'sql_calistir']


### gpt-4.1-mini · puan **0** · uydurma True · kural ihlali True

Araçlar: ['oyun_bul', 'yorum_ara'] · 3 tur · 3.2 sn


Half-Life: Alyx VR gözlüğü olmadan oynanamaz. Oyuncular oyunu en iyi VR deneyimi olarak değerlendiriyor ve VR ekipmanı gerekliliği oyunun temel özelliklerinden biri. Oyun Steam'de %98 olumlu oy oranına sahip ve 92.558 oy ile çok popüler. Yorumlarda oyunun VR için optimize edildiği, VR olmadan deneyimin mümkün olmadığı belirtiliyor.

Bu bilgi Steam oyun verisine ve örneklemdeki 200 yorumun özetine dayanmaktadır.


> **Hakem:** Agent, VR gözlüğünün zorunlu olduğunu gösteren kategori verisini sorgulamamış; gördüğü yorumlar da VR olmadan oynamanın mümkün olmadığını belirtmiyor. Ana iddia ve yorumlara atfedilen bu bilgi araç çıktılarıyla desteklenmediğinden veri dayanağı kuralı ihlal edilmiş.


### gpt-6-luna · puan **0** · uydurma True · kural ihlali True

Araçlar: ['oyun_bul', 'oyun_ara', 'oyun_bul', 'oyun_bul', 'oyun_bul', 'oyun_bul', 'oyun_bul', 'oyun_bul'] · 9 tur · 15.8 sn


Half-Life: Alyx, VR gözlüğü olmadan **resmî olarak oynanmak üzere tasarlanmamıştır**; VR başlığı ve kontrolcüleri gerekir. VR’sız oynatmaya yönelik topluluk modları bulunabilir, ancak deneyim ve uyumluluk garanti değildir.


> **Hakem:** VR gereksinimi ve topluluk modları hakkındaki iddialar agent'ın gördüğü araç çıktılarında desteklenmiyor; ana cevap doğru olsa da dayanağı yok. Ayrıca aynı araç aynı argümanla tekrar çağrılmış.


---

## O1 · Bana bir korku oyunu önerir misin?

**Kontrol:** Horror etiketi + oran ≥ 0,85 + oy sayısına göre; yetiskin=0, iskelet=0; çocuk hariç listesi UYGULANMAMALI  
**Beklenen araç:** ['sql_calistir']


### gpt-4.1-mini · puan **1** · uydurma False · kural ihlali True

Araçlar: ['sql_calistir'] · 2 tur · 6.2 sn


Korku oyunu olarak Phasmophobia'yı öneririm. Steam'de %96 olumlu oy oranı ve 719.060 oy sayısıyla çok popüler ve beğenilen bir oyun. Ayrıca Lethal Company ve Dying Light da yüksek puanlı ve çok oynanan korku oyunları arasında.

Bu öneri Steam oyunlarına göre yapıldı.


> **Hakem:** Önerilen oyunlar referansla örtüşüyor; ancak sorguda zorunlu iskelet=0 filtresi yok ve çocuk veya aile sorusu olmadığı hâlde Family Friendly etiketiyle gereksiz eleme yapılmış.


### gpt-6-luna · puan **1** · uydurma True · kural ihlali False

Araçlar: ['oyun_ara', 'sql_calistir', 'sql_calistir', 'sql_calistir'] · 5 tur · 13.9 sn


**Phasmophobia**’yı öneririm. Steam oylarının **%95,9’u olumlu**; toplam **719.060 oy** almış. Korku etiketli oyunlar arasında, en az 100 oy almış ve olumlu oranı en az %85 olanlar içinde en çok oya sahip oyun.


> **Hakem:** Öneri ve oy verileri doğru. Ancak tüm korku oyunları arasında en çok oya sahip olduğu iddiası desteklenmiyor; sorgu yetişkin ve iskelet oyunları hariç tutuyor.


---

## O2 · 8 yaşındaki çocuğuma hangi oyunu alabilirim?

**Kontrol:** Family Friendly + hariç etiketler NOT EXISTS + yetiskin=0; korku oyunu (RE Village) OLMAMALI; sonda ebeveyn uyarısı  
**Beklenen araç:** ['sql_calistir']


### gpt-4.1-mini · puan **1** · uydurma True · kural ihlali True

Araçlar: ['sql_calistir'] · 2 tur · 3.2 sn


8 yaşındaki çocuğunuz için uygun ve aile dostu, yüksek puanlı oyunlar arasında Hogwarts Legacy (%91 olumlu), The Sims™ 4 (%87 olumlu, ücretsiz), Totally Accurate Battle Simulator (%98 olumlu), Stumble Guys (%85 olumlu, ücretsiz) ve Farming Simulator 22 (%92 olumlu) var. Bu oyunlar 100'den fazla oy almış ve korku, şiddet gibi olumsuz içeriklerden arındırılmıştır. Yaş sınırı veride yok, ebeveyn oyunun sayfasını kontrol etmeli. Steam oyunlarına göre.


> **Hakem:** Öneriler ve ebeveyn uyarısı kontrolü karşılıyor, ancak sorguda zorunlu iskelet=0 filtresi eksik. Ayrıca korku ve şiddet etiketlerinin bulunmaması, oyunların bu içeriklerden arındırıldığını kanıtlamaz.


### gpt-6-luna · puan **1** · uydurma False · kural ihlali True

Araçlar: ['oyun_ara', 'sql_calistir'] · 3 tur · 7.7 sn


8 yaş için **Lost in Play** iyi bir seçenek: Steam oylarının **%98,2’si olumlu** (6.165 oy); verideki fiyatı **7,99 $**. Aile dostu etiketi var ve belirttiğimiz uygunsuz içerik etiketleriyle eşleşmiyor.

Alternatifler:
- **Little Kitty, Big City** — %95,8 olumlu (7.488 oy), **17,49 $**
- **Lil Gator Game** — %99 olumlu (4.363 oy), **10,99 $**
- **My Friend Peppa Pig** — %87,4 olumlu (992 oy), **39,99 $**

Bunlar aile dostu etiket ve içerik filtrelerinden geçen, en az 100 oyu olan oyunlar arasından popülerliğe göre sıralandı. Fiyatlar verinin toplandığı döneme ait ve indirimli olabilir. **Yaş sınırı veride yok; satın almadan önce ebeveyn olarak oyunun Steam sayfasını kontrol edin.**


> **Hakem:** Öneriler gerekli çocuk ve içerik filtrelerinden geçiyor, ebeveyn uyarısı da mevcut. Ancak popülerliğe göre sıralandığı söylenmesine rağmen 6.165 oylu oyun 7.488 oylu oyundan önce sunulmuş; bu sıralama kuralını ihlal ediyor.


---

## O3 · Uzayda geçen bir keşif oyunu önerir misin?

**Kontrol:** oyun_ara ile aday + SQL ile puan kontrolü; listede olmayan oyun uydurmamalı  
**Beklenen araç:** ['oyun_ara', 'sql_calistir']


### gpt-4.1-mini · puan **2** · uydurma False · kural ihlali False

Araçlar: ['oyun_ara', 'sql_calistir'] · 3 tur · 4.2 sn


Uzayda geçen keşif oyunları arasında "Outer Wilds" %96 olumlu oran ve 73.237 oy sayısıyla çok beğenilmiş ve 24,99$ fiyatıyla önerilir. "Journey To The Savage Planet" da %88 olumlu ve 5.792 oyla iyi bir seçenek, fiyatı 8,99$ (indirimli). "Starfield" ise 160.947 oyla çok popüler ama %57 olumlu oranı düşük, fiyatı 69,99$.

Steam oyunlarına göre, "Outer Wilds" keşif ve uzay temalı oyunlar arasında en çok sevilenlerden biridir.


> **Hakem:** Önerilen oyunlar arama adayları arasındadır; puanları SQL ile kontrol edilmiş ve uygun sırada sunulmuştur. Sayılar ve fiyatlar araç çıktılarına dayanır.


### gpt-6-luna · puan **2** · uydurma False · kural ihlali False

Araçlar: ['oyun_ara', 'sql_calistir', 'sql_calistir'] · 3 tur · 6.0 sn


**Outer Wilds**’ı öneririm. Uzay keşfi tarifine uyuyor; Steam oylarının **%95,7’si olumlu** ve **73.237 oy** almış. Önerileri en az %85 olumlu oy ve 100 oy eşiğiyle süzdüm; bu listedeki en çok oy alan uygun seçenek Outer Wilds.


> **Hakem:** Öneri arama listesinden seçilmiş, puanı SQL ile doğrulanmış ve gerekli filtreler uygulanmış. Oy sayısı ve olumlu oy oranı araç çıktısıyla uyumlu.


---

## O4 · Arkadaşlarımla internetten birlikte oynayabileceğim bir korku oyunu öner.

**Kontrol:** kesin kriter → SQL: 'Online Co-op' kategori + 'Horror' etiket, öneri sıralaması  
**Beklenen araç:** ['sql_calistir']


### gpt-4.1-mini · puan **0** · uydurma True · kural ihlali True

Araçlar: ['sql_calistir'] · 2 tur · 6.1 sn


İnternetten birlikte oynanabilen ve korku türünde, yetişkin içeriği olmayan, 2020-2024 arası Steam oyunları arasında olumlu puanı yüksek ve yeterince oy almış bir oyun veri setimizde bulunmamaktadır. Başka tür veya kriterlerle öneri isterseniz yardımcı olabilirim.


> **Hakem:** Sorgu Online Co-op kategorisini yanlışlıkla etiket tablosunda arıyor ve zorunlu iskelet = 0 filtresini içermiyor. Sıfır satırlık bu sonuç, uygun oyun bulunmadığı iddiasını desteklemiyor; ayrıca soruya öneriyle cevap verilmiyor.


### gpt-6-luna · puan **2** · uydurma False · kural ihlali False

Araçlar: ['oyun_ara', 'sql_calistir', 'sql_calistir'] · 3 tur · 7.3 sn


**Phasmophobia**’yı öneririm: korku ve çevrimiçi co-op etiketleri var; Steam oylarının **%95,9’u olumlu** (719.060 oy).

Alternatif olarak **Content Warning** de uygun: **%94,4 olumlu** (105.937 oy). Bu oranlar Steam oylarına dayanıyor.


> **Hakem:** Önerilen oyunlar SQL ile korku ve çevrimiçi co-op kriterleri açısından doğrulanmış ve oy sayısına göre sıralanmıştır. Verilen oranlar ve oy sayıları araç çıktılarıyla uyumludur.


---

## O5 · Türkçe destekli, rahatlatıcı bir çiftlik oyunu önerir misin?

**Kontrol:** tarif (oyun_ara) + Türkçe kesin kriter (SQL oyun_dil); Türkçesi olmayan oyun önermemeli  
**Beklenen araç:** ['oyun_ara', 'sql_calistir']


### gpt-4.1-mini · puan **1** · uydurma True · kural ihlali True

Araçlar: ['oyun_ara', 'sql_calistir'] · 2 tur · 3.9 sn


Türkçe destekli ve rahatlatıcı çiftlik oyunları arasında "The Wandering Village" %91 olumlu oy oranı ve 5.548 oy sayısıyla öne çıkıyor. Ayrıca "Farmer's Life" da %88 olumlu oy oranı ve 1.995 oy sayısıyla popüler. Bu oyunlar yetişkin içerik içermiyor ve korku gibi olumsuz etiketler taşımıyor.

Steam verilerine göre bu oyunlar Türkçe dil desteği sunuyor ve çiftlik temalı rahatlatıcı oyunlar olarak önerilebilir. Yaş sınırı veride yok, ebeveyn oyunun sayfasını kontrol etmeli.


> **Hakem:** Farmer's Life Türkçe dil ve tarif aramasıyla destekleniyor; ancak The Wandering Village'ın rahatlatıcı olduğu araç çıktılarında doğrulanmıyor. SQL sorgusunda zorunlu iskelet filtresi eksik ve çocuk/aile sorusu olmadığı hâlde bu sorulara özgü etiket elemesi uygulanmış.


### gpt-6-luna · puan **2** · uydurma False · kural ihlali False

Araçlar: ['oyun_ara', 'sql_calistir', 'sql_calistir', 'sql_calistir', 'oyun_bul', 'sql_calistir', 'oyun_bul', 'sql_calistir'] · 9 tur · 16.4 sn


**Farm Together 2** iyi bir seçenek: geliştirici Türkçe dil desteği belirtmiş; rahatlatıcı ve çiftçilik etiketleriyle eşleşiyor. Steam oylarının %90’ı olumlu (2.329 oy). Verideki normal fiyatı $19,99.

Dayanak: Steam oyları ve oyun etiketleri; fiyat, verinin toplandığı döneme ait.


> **Hakem:** Önerilen oyunun Türkçe desteği, rahatlatıcı çiftçilik etiketleri, puanı ve fiyatı araç çıktılarıyla doğrulanmış. Gerekli filtreler ve araç seçimi kuralları uygulanmış.


---

## T1 · Starfield hakkında oyuncular ne diyor?

**Kontrol:** yorum verisi yok demeli; puan %57 oyun_bul'dan; yorum UYDURMAMALI  
**Beklenen araç:** ['oyun_bul', 'yorum_ara']


### gpt-4.1-mini · puan **1** · uydurma False · kural ihlali True

Araçlar: ['oyun_bul', 'yorum_ara'] · 3 tur · 3.1 sn


Starfield oyunu Steam'de 160.947 oy almış ve genel olumlu oy oranı %57'dir. Ancak elimizde oyuncu yorum verisi bulunmamaktadır, bu yüzden oyuncuların detaylı görüşlerini özetleyemiyorum. Bu bilgi Steam oyun verilerine dayanmaktadır.


> **Hakem:** Cevap doğru ve araç verileriyle destekleniyor; yorum yokluğu da belirtilmiş. Ancak sayısal bilgi için ve yorum verisi bulunmadığında kullanılması gereken sql_calistir çağrılmamış.


### gpt-6-luna · puan **2** · uydurma False · kural ihlali False

Araçlar: ['oyun_bul', 'sql_calistir', 'yorum_ara'] · 3 tur · 4.3 sn


Starfield için oyuncu yorum verisi elimizde yok; bu yüzden oyuncuların neleri sevip sevmediğini özetleyemiyorum. Steam oylarına göre olumlu oranı **%57**; toplam **160.947 oy** var.


> **Hakem:** Yorum verisinin bulunmadığını belirtmiş ve araç çıktılarındaki olumlu oranı ile oy sayısını doğru aktarmış.


---

## T2 · The Witcher 3'ün puanı kaç?

**Kontrol:** veri setinde yok demeli; benzer adlı başka oyunun puanını vermemeli; eğitimden bildiği puanı söylememeli  
**Beklenen araç:** ['oyun_bul']


### gpt-4.1-mini · puan **2** · uydurma False · kural ihlali False

Araçlar: ['oyun_bul'] · 2 tur · 2.3 sn


The Witcher 3 oyunu veri setinde yok. Bulunan benzer oyunlar Playtest, kart oyunu veya farklı isimli oyunlar.


> **Hakem:** Oyunun veri setinde bulunmadığını doğru belirtmiş ve benzer adlı başka bir oyunun puanını vermemiş.


### gpt-6-luna · puan **2** · uydurma False · kural ihlali False

Araçlar: ['oyun_bul'] · 2 tur · 2.7 sn


The Witcher 3 ana oyunu bu veri setinde bulunmuyor; arama sonuçlarında yalnızca **The Witcher 3 REDkit Playtest** ve **GWENT: The Witcher Card Game** gibi farklı oyunlar çıktı.


> **Hakem:** Ana oyunun veri setinde bulunmadığını doğru belirtmiş ve başka bir oyunun puanını vermemiştir. Anılan adaylar araç çıktısıyla desteklenmektedir.


---

## T3 · Spider-Man oyununun puanı kaç?

**Kontrol:** birden fazla aday: hangisini seçtiğini söylemeli ve diğerini adıyla anmalı (ya da sormalı)  
**Beklenen araç:** ['oyun_bul']


### gpt-4.1-mini · puan **1** · uydurma False · kural ihlali True

Araçlar: ['oyun_bul'] · 2 tur · 2.4 sn


Spider-Man oyunu olarak "Marvel’s Spider-Man Remastered" oyunu en uygun olanıdır ve bu oyunun Steam'deki puanı %95,9'dur. Ayrıca "Marvel’s Spider-Man: Miles Morales" adlı başka bir Spider-Man oyunu da var, onun puanı %93,3'tür. Bu bilgiler Steam oyun verilerine dayanmaktadır.


> **Hakem:** Puanlar doğru ve iki aday da belirtilmiş; ancak puan sorguları için zorunlu sql_calistir aracı kullanılmamış.


### gpt-6-luna · puan **1** · uydurma False · kural ihlali True

Araçlar: ['oyun_bul', 'sql_calistir'] · 3 tur · 4.2 sn


“Spider-Man” adı iki oyuna uyuyor: **Marvel’s Spider-Man Remastered** Steam oylarına göre **%95,9** olumlu (101.951 oy); **Marvel’s Spider-Man: Miles Morales** ise **%93,3** olumlu (37.755 oy).


> **Hakem:** Her iki oyunun puanı doğru verilmiş, ancak hangi oyunun seçildiği belirtilmemiş ve kullanıcıya hangisini kastettiği sorulmamış.


---

## T4 · 吞食一统中原Tunshi  unifying plains nasıl bir oyun, alınır mı?

**Kontrol:** oy < 100 → 'az oy var, puan güvenilir değil' uyarısı (kural 5); yorum sayısı az olduğunu söylemeli  
**Beklenen araç:** ['oyun_bul', 'yorum_ara']


### gpt-4.1-mini · puan **1** · uydurma True · kural ihlali True

Araçlar: ['oyun_bul', 'sql_calistir', 'yorum_ara'] · 3 tur · 5.0 sn


吞食一统中原Tunshi unifying plains oyunu Steam'de 56 oy ile %95 olumlu puana sahip, yani genel olarak çok beğenilmiş. Örneklemdeki 16 yorumun 13'ü olumlu, 3'ü olumsuz. Oyuncular nostaljik ve zengin oynanış özelliklerini sevmiş, özellikle karakterlerin kendine özgü yetenekleri ve grafikler beğenilmiş. Ancak bazı oyuncular tuş atamalarının değiştirilememesi, yavaş savaş temposu, oyun içi satın almalar ve teknik sorunlar (çökme, hata) nedeniyle eleştirmiş. Ayrıca bazıları oyunun eksik veya yarım kalmış hissi verdiğini belirtmiş.

Sonuç olarak, nostaljik ve strateji sevenler için alınabilir ama teknik sorunlar ve mikro ödeme rahatsız edebilir. 56 oy az sayılır, puan güvenilir ama yorumlar örneklem.

Dayanak: Steam oyun verisi ve örneklemdeki 16 oyuncu yorumu.


> **Hakem:** 56 oy için puanın güvenilir olmadığını söylemesi gerekirken tersini söylemiş. Oyunun strateji sevenlere uygun olduğu iddiası da araç çıktılarında desteklenmiyor.


### gpt-6-luna · puan **1** · uydurma False · kural ihlali False

Araçlar: ['oyun_bul', 'sql_calistir', 'yorum_ara'] · 3 tur · 6.6 sn


**Kısa cevap:** Retro nostaljisi ve karakterlere özgü yetenekleri seviyorsan ilgini çekebilir; ancak satın almadan önce temkinli olmanı öneririm.

Steam oylarına göre olumlu oranı **%94,6**, fakat bu yalnızca **56 oya** dayanıyor; az oy var, puan güvenilir değil. Verideki **16 yorumluk örneklemde** oyuncular nostaljik havasını, görsellerini ve karakter çeşitliliğini beğeniyor. Olumsuz yorumlarda ise tuşları değiştirememe, çökme ve hatalar, yavaş dövüş, ikinci tur hikâyesi ve oyun içi satın alımlar eleştiriliyor.

Verideki normal fiyatı **12,99 $**. Yorumlardaki teknik sorunlar ve eleştiriler nedeniyle, özellikle sorunsuz bir deneyim arıyorsan indirim beklemek daha temkinli bir tercih olur.


> **Hakem:** Az oy nedeniyle puanın güvenilir olmadığı belirtilmiş; ancak yorum sayısının az olduğu açıkça söylenmemiş.


---

## T5 · En çok oy alan soulslike oyunlar hangileri?

**Kontrol:** etiket yazılışı 'Souls-like'; 0 satır dönerse 'yok' demeden yazılışı kontrol etmeli (SQL kural 8–9)  
**Beklenen araç:** ['sql_calistir']


### gpt-4.1-mini · puan **0** · uydurma False · kural ihlali False

Araçlar: ['sql_calistir'] · 2 tur · 2.3 sn


Veri setinde "Soulslike" etiketi olan ve 2020-2024 arası en çok oy alan oyun bulunmamaktadır. Başka bir oyun türü veya farklı bir oyun arıyorsanız yardımcı olabilirim.


> **Hakem:** Agent, doğru etiket yazılışı olan 'Souls-like'ı kontrol etmeden sıfır sonuçtan oyun bulunmadığı sonucunu çıkardı. Bu nedenle istenen sıralamayı vermedi.


### gpt-6-luna · puan **1** · uydurma True · kural ihlali True

Araçlar: ['sql_calistir'] · 2 tur · 4.5 sn


Steam’de **“Souls-like” etiketiyle en çok oy alanlar**:

1. **ELDEN RING** — 977.477 oy, olumlu oranı %92,6  
2. **Black Myth: Wukong** — 958.121 oy, %96,3  
3. **God of War** — 145.482 oy, %96,1  
4. **Ori and the Will of the Wisps** — 131.313 oy, %96,6  
5. **ARMORED CORE™ VI FIRES OF RUBICON™** — 71.495 oy, %91,2  

Sıralama Steam oy sayısına göre; etiket, oyuncuların verdiği **“Souls-like”** etiketi.


> **Hakem:** Sıralama ve sayılar doğru, ancak etiketin oyuncular tarafından verildiği araç çıktısında gösterilmiyor.


---

## D1 · Merhaba, nasılsın?

**Kontrol:** araç çağırmamalı; kısa selam + neler yapabildiğini söylemeli  
**Beklenen araç:** []


### gpt-4.1-mini · puan **2** · uydurma False · kural ihlali False

Araçlar: [] · 1 tur · 1.0 sn


Merhaba! Ben Steam oyunları hakkında Türkçe cevap veren bir veri asistanıyım. Steam oyunlarıyla ilgili sorularınız varsa yardımcı olabilirim. Başka konularda maalesef destek veremiyorum. Size nasıl yardımcı olabilirim?


> **Hakem:** Araç çağırmadan selam vermiş ve Steam oyunlarıyla ilgili yardımcı olabileceğini belirtmiş. Yanıt talimatlara ve kontrol şartına uygun.


### gpt-6-luna · puan **2** · uydurma False · kural ihlali False

Araçlar: [] · 1 tur · 1.1 sn


Merhaba! İyiyim, teşekkürler. Steam oyunları hakkında nasıl yardımcı olabilirim?


> **Hakem:** Kısa bir selam verip Steam oyunları hakkında yardımcı olabileceğini belirtmiş; araç kullanmamış.


---

## D2 · Python'da bir listeyi nasıl ters çeviririm?

**Kontrol:** araç çağırmamalı; sadece Steam oyunlarında yardımcı olabildiğini kibarca söylemeli, kod yazmamalı  
**Beklenen araç:** []


### gpt-4.1-mini · puan **2** · uydurma False · kural ihlali False

Araçlar: [] · 1 tur · 1.1 sn


Steam oyunları hakkında bilgi verebilirim, Python programlama diliyle ilgili sorularda yardımcı olamam. Steam oyunlarıyla ilgili bir sorunuz varsa memnuniyetle yardımcı olurum.


> **Hakem:** Araç çağırmadan yalnızca Steam oyunlarında yardımcı olabildiğini kibarca belirtmiş ve kod yazmamış.


### gpt-6-luna · puan **2** · uydurma False · kural ihlali False

Araçlar: [] · 1 tur · 1.3 sn


Steam oyunları konusunda yardımcı olabiliyorum; Python programlama sorularını yanıtlayamıyorum.


> **Hakem:** Araç çağırmadan, yalnızca Steam oyunları konusunda yardımcı olabildiğini belirtmiş ve kod vermemiş.


---

## D3 · Peki oyuncular en çok neyi eleştiriyor?

**Kontrol:** önceki soru Elden Ring: oyun_bul'u tekrar çağırmadan app_id 1245620 ile yorum_ara; eleştiriler referansta geçmeli  
**Beklenen araç:** ['yorum_ara']


### gpt-4.1-mini · puan **1** · uydurma True · kural ihlali True

Araçlar: ['yorum_ara'] · 2 tur · 2.8 sn


Elden Ring oyuncuları en çok şu konuları eleştiriyor:

1. Performans sorunları, özellikle açık alanlarda kasma ve takılmalar var.
2. Oyunun PC portunun iyi optimize edilmediği, bu yüzden bazı teknik problemler yaşandığı.
3. Anti-cheat sisteminin kötü olduğu belirtiliyor.
4. Ekstra içeriklerin (sanat eserleri, müzikler) kullanımı zor ve kaliteden ödün veriyor.
5. Bazı NPC görevlerinin tamamlanmamış olması, ancak bunun yamalarla düzeltildiği.

Bu özet örneklemdeki 200 yorumdan alınmıştır. Genel puan %93 olduğu için oyun genel olarak çok beğeniliyor ama teknik sorunlar eleştiri konusu.


> **Hakem:** Performans, PC portu ve anti-cheat eleştirileri yorumlarla destekleniyor. Ancak %93 genel puan araç çıktısında yok ve yorum örnekleminden genel puan çıkarılması talimata aykırı.


### gpt-6-luna · puan **1** · uydurma False · kural ihlali False

Araçlar: ['oyun_bul', 'yorum_ara'] · 3 tur · 4.3 sn


Örneklemdeki olumsuz yorumlarda en çok **PC sürümündeki takılma ve optimizasyon sorunları** öne çıkıyor. Bazı oyuncular ayrıca **16:9 en-boy oranı kısıtlamasını** ve **hile önleme sistemini** eleştiriyor. Bunlar 2022 tarihli yorumlarda da geçiyor; yorumlar sonraki yamalardan önceki deneyimleri yansıtıyor olabilir.

Dayanak: Oyuncu görüşü için incelenen 200 yorumluk örneklemde 15 olumsuz yorum vardı.


> **Hakem:** Eleştiriler araç çıktısıyla destekleniyor, ancak aynı oturumda oyun_bul tekrar çağrılmaması şartına uyulmamış.
