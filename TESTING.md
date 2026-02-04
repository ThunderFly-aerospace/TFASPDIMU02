## Testovací procedura desky TFASPDIMU02

Deska obsahuje více senzorů. Všechny z nich je potřeba po výrobě otestovat. Následující postup popisuje, jak testování jednotlivých senzorů provádět. Pro toto testování je vhodné použít [pymlab skript](sw/pymlab/test_suite.py). 

### I2C komunikace
Komunikace po I2C se otestuje tím, že všechny z následující testy lze provést bez chyby. Pokud některý z testů selže je potřeba zkontrolovat správnost zapojení a ověřit jestli jsou všechny senzory viditelné na sběrnici například nástrojem `i2cdetect`. 

### SDP3x senzor
U airspeed senzoru se ověřuje, jestli při fouknutí do jedné z jeho trubiček se vytváří rozdíl tlaku. Toto měření je jen velmi orientační a zjišťuje funkčnost senzoru. Přesnější test je proveden ve finální aplikaci, kdy je senzor je vložen do odpovídajícího obalu. Tam se pak testuje i jeho dobré utěsnění. 

```
(.venv) TFASPDIMU02/sw/pymlab$ python3 test_suite.py 9 0
{'port': 9, 'device': 'hid'}
ID: 0x3010384 - sensor: SDP33 1500Pa
Magnetometer not calibrated.

0000; 2026-02-04T10:50:02.387614+00:00; Dp: +0.00 [Pa]; T: 29.467 [degC]; MAG_HDG: +56.41; SPD_W_DP: +0.00 [km/h]
0000; 2026-02-04T10:50:02.521622+00:00; Dp: +0.00 [Pa]; T: 29.611 [degC]; MAG_HDG: +55.76; SPD_W_DP: +0.00 [km/h]
0000; 2026-02-04T10:50:02.655617+00:00; Dp: +0.05 [Pa]; T: 29.563 [degC]; MAG_HDG: +55.50; SPD_W_DP: -0.08 [km/h]
0000; 2026-02-04T10:50:02.789611+00:00; Dp: +0.00 [Pa]; T: 29.563 [degC]; MAG_HDG: +55.18; SPD_W_DP: +0.00 [km/h]
0000; 2026-02-04T10:50:02.923609+00:00; Dp: +0.00 [Pa]; T: 29.372 [degC]; MAG_HDG: +55.25; SPD_W_DP: +0.00 [km/h]
0000; 2026-02-04T10:50:03.057605+00:00; Dp: +0.00 [Pa]; T: 29.563 [degC]; MAG_HDG: +55.04; SPD_W_DP: +0.00 [km/h]
0000; 2026-02-04T10:50:03.191574+00:00; Dp: -43.10 [Pa]; T: 29.563 [degC]; MAG_HDG: +54.88; SPD_W_DP: +2.36 [km/h]
0000; 2026-02-04T10:50:03.325599+00:00; Dp: -77.60 [Pa]; T: 29.467 [degC]; MAG_HDG: +54.78; SPD_W_DP: +3.17 [km/h]
0000; 2026-02-04T10:50:03.459580+00:00; Dp: -74.50 [Pa]; T: 29.611 [degC]; MAG_HDG: +54.74; SPD_W_DP: +3.11 [km/h]
0000; 2026-02-04T10:50:03.593552+00:00; Dp: -100.25 [Pa]; T: 29.419 [degC]; MAG_HDG: +54.65; SPD_W_DP: +3.60 [km/h]
0000; 2026-02-04T10:50:03.727543+00:00; Dp: -91.85 [Pa]; T: 29.563 [degC]; MAG_HDG: +54.57; SPD_W_DP: +3.45 [km/h]
0000; 2026-02-04T10:50:03.861543+00:00; Dp: -136.35 [Pa]; T: 29.467 [degC]; MAG_HDG: +54.48; SPD_W_DP: +4.20 [km/h]
0000; 2026-02-04T10:50:03.995534+00:00; Dp: -140.55 [Pa]; T: 29.611 [degC]; MAG_HDG: +55.69; SPD_W_DP: +4.27 [km/h]
0000; 2026-02-04T10:50:04.129526+00:00; Dp: -132.70 [Pa]; T: 29.611 [degC]; MAG_HDG: +56.82; SPD_W_DP: +4.15 [km/h]
```

### IMU jednotka
U imu jednotky se ověřují hodnoty, které jsou měřeny. 

```TODO: Není jasné jakým skriptem jsou následující testy provedeny```

#### Akcelorometr
Funkčnost akcelorometru se ověřuje tím, že indikované hodnoty náklonů pitch/roll jsou spávné. Je vhodné si senzor vzít na rovnou plochu. Při položení na tuto plochu by měl indikovat nulový náklon pitch/roll. 

Otáčením podle delší osy by se měly měnit hodnoty v ose roll. Při měření je vhodné si pomoct trojúhelníkovým pravítkem, podle kterého se PCB opře. V této poloze by senzor měl ukazovat hodnoty okolo 90deg. Vzhledem k tomu, že při tomto měření není senzor kalibrovaný, tak maximální hodnota může být nižší. Neměla by však být nižší než 85 deg. Běžně se s funkčním senzorem (bez kalibrace) dají změřit úhly okolo 89.8 deg. Stejný postup je potřeba zopakovat pro osu pitch (kolmo na podélnou osu senzoru). 

#### Magnetometr
U magnetometru je potřeba ověřit, že určený azimut odpovídá realitě, při pomalém kompletním otáčení se hodnota očekávatelně mění. Zde si lze pomoct buď úhloměrem nebo vytištěnou kružnicí na papíře s naznačenými úhly. Je také vhodné věřit opakovatelnost tohoto měření způsobem, že si na začátku zapamatujete určitou orientaci a měřený úhel. Na konci procedury tyto zapamatované hodnoty a aktuálni hodnoty sedí.

#### Gyroskop
U gyroskopu je možné ověřit, že v klidovém stavu ukazuje nulu. A pří pokusu o otočení v jedné ose tyto hodnoty zvětší a zase se vrátí na nulu. 
