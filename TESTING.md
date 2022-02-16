Testovací procedura desky TF-ASPDIMU

Deska obsahuje více senzorů. Všechny z nich je potřeba po výrobě otestovat. Následující postp popisuje, jak testování jednotlivých senzorů provádět. Pro toto testování je vhodné použít pymlab skript. 

### I2C komunikace
Komunikace po I2C se otestuje tím, že všechny z následujících testů lze provést. Pokud některý z testů nelze provést je potřeba zkontrolovat správnost zapojení a jestli jsou všechny senzory dostupné na sběrnici například nástrojem `i2cdetect`. 


### SDP3x senzor
U airspeed senzoru se ověřuje, jestli při fouknutí do jedné z jeho trubiček se vytváří rozdíl tlaku. Toto měření je jen velmi orientační a zjišťuje funkčnost senzoru. Přesnější test je proveden ve finální aplikaci, kdy je senzor je vložen do odpovídajícího obalu. Tam se pak testuje i jeho dobré utěsnění. 

### IMU jednotka
U imu jednotky se ověřují hodnoty, které jsou měřeny. 

#### Akcelorometr
Funkčnost akcelorometru se ověřuje tím, že indikované hodnoty náklonů pitch/roll jsou spávné. Je vhodné si senzor vzít na rovnou plochu. Při položení na tuto plochu by měl indikovat nulový náklon pitch/roll. 

Otáčením podle delší osy by se měly měnit hodnoty v ose roll. Při měření je vhodné si pomoct trojúhelníkovým pravítkem, podle kterého se PCB opře. V této poloze by senzor měl ukazovat hodnoty okolo 90deg. Vzhledem k tomu, že při tomto měření není senzor kalibrovaný, tak maximální hodnota může být nižší. Neměla by však být nižší než 85 deg. Běžně se s funkčním senzorem (bez kalibrace) dají změřit úhly okolo 89.8 deg. 
Stejný postup je potřeba zopakovat pro osu pitch (kolmo na podélnou osu senzoru). 

#### Magnetometr
U magnetometru je potřeba ověřit, že určený azimut odpovídá realitě, při pomalém kompletním otáčení se hodnota očekávatelně mění. Zde si lze pomoct buď úhloměrem nebo vytištěnou kružnicí na papíře s naznačenými úhly. 
Je také vhodné věřit opakovatelnost tohoto měření způsobem, že si na začátku zapamatujete určitou orientaci a měřený úhel. Na konci procedury tyto zapamatované hodnoty a aktuálni hodnoty sedí.

#### Gyroskop
U gyroskopu je možné ověřit, že v klidovém stavu ukazuje nulu. A pří pokusu o otočení v jedné ose tyto hodnoty zvětší a zase se vrátí na nulu. 
