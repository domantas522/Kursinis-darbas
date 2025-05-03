# Išmanių namų valdymo sistema

## 1. Įžanga

### Kas yra ši programa?

Tai yra išmanių namų valdymo sistema, parašyta Python programavimo kalba. Ji leidžia vartotojui valdyti įvairius įrenginius, tokius kaip televizoriai, šviesos, kondicionieriai, durys ir kameros. Sistema leidžia įjungti/išjungti įrenginius, keisti jų parametrus, išsaugoti būseną faile ir atkurti ją paleidžiant programą iš naujo.

### Kaip paleisti programą?

1. Įsitikinkite, kad jūsų kompiuteryje įdiegta Python (rekomenduojama versija 3.8 ar naujesnė).
2. Išsaugokite programos kodą į `.py` failą, pvz., `smart_home.py`.
3. Paleiskite terminalą (komandinę eilutę) ir įveskite:

```bash
python smart_home.py
```

### Kaip naudotis programa?

Paleidus programą terminale, pateikiamas meniu su pasirinkimais. Naudotojas gali pasirinkti veiksmą įvesdamas skaičių:

- Įjungti/išjungti visus įrenginius
- Peržiūrėti įrenginių būseną
- Pridėti arba ištrinti įrenginį
- Aktyvuoti „Išvykimo režimą“
- Keisti įrenginių parametrus
- Įrašyti būseną į failą/išeiti

---

## 2. Pagrindinė dalis / Analizė

### Kaip programa įgyvendina funkcinius reikalavimus?

Programa įgyvendina šiuos funkcinius reikalavimus:

- **Įrenginių valdymas:** Naudojant `Device` abstrakčią klasę ir jos paveldėtas klases (TV, Light, AirConditioner, Door, Camera), kiekvienas įrenginys turi savo individualias funkcijas.
- **Pridėjimas/šalinimas:** Klasė `Valdymas` leidžia pridėti ir ištrinti įrenginius iš sąrašo.
- **Išvykimo režimas:** Funkcija `leavehome()` automatiškai išjungia šviesas, TV ir kondicionierius, užrakina duris ir įjungia kameras.
- **Failų įrašymas ir nuskaitymas:** Įrenginių būsena įrašoma JSON faile ir atstatoma automatiškai programos paleidimo metu.
- **Parametrų keitimas:** Galima keisti TV kanalą ir garsą, šviesos ryškumą, oro kondicionieriaus temperatūrą, kameros rezoliuciją bei durų užrakto būseną.

---

# Programos funkcinių reikalavimų įgyvendinimas

Ši programa buvo sukurta siekiant įgyvendinti šiuos funkcinius reikalavimus, naudojant įvairius objektinio programavimo principus ir dizaino šablonus:

## ✅ Polymorphism
Programoje **Polymorphism** (polimorfizmas) įgyvendintas naudojant abstrakčią `Device` klasę ir jos paveldėtas klases, tokias kaip `TV`, `Light`, `AirConditioner`, `Door`, ir `Camera`. Kiekviena klasė turi savo unikalią metodiką, tačiau visi įrenginiai gali naudoti bendrą metodą `turn_on()` ir `turn_off()`, kad įjungtų ir išjungtų įrenginius. Taip pat metodas `device_info()` yra naudojamas polimorfiškai, leidžiantis kiekvienam įrenginiui pateikti savo informaciją.

## ✅ Abstraction
**Abstraction** (abstrakcija) buvo pasiekta naudojant abstrakčią `Device` klasę, kuri apibrėžia bendrus įrenginių metodus, bet neapibrėžia jų įgyvendinimo. Tai leidžia slėpti detales ir suteikti bendrą sąsają visiems įrenginiams, tokiems kaip TV, šviesa, oro kondicionierius ir kt.

## ✅ Inheritance
**Inheritance** (paveldėjimas) buvo naudojamas kuriant specifines įrenginių klases, kurios paveldi bendrą funkcionalumą iš `Device` klasės. Kiekviena įrenginio klasė, tokia kaip `TV`, `Light`, `AirConditioner`, paveldi bendras funkcijas, tokias kaip `turn_on()`, `turn_off()`, ir `device_info()`, tačiau prideda savo unikalius metodus, pavyzdžiui, `set_channel()` ar `set_brightness()`.

## ✅ Encapsulation
**Encapsulation** (apsaugoti duomenys) pasiekiama per uždarų (`_`) atributų naudojimą ir metodų teikimą norint kontroliuoti, kaip prie jų prieinama. Pavyzdžiui, kiekvienas įrenginys turi privačius atributus (pvz., `_status`, `_brightness`, `_temperature`), kuriems galima pasiekti tik per viešus metodus (pvz., `turn_on()`, `turn_off()`, `set_brightness()`), užtikrinant duomenų apsaugą ir valdymą.

## ✅ Factory Pattern
**Factory Pattern** (Fabrikos šablonas) buvo taikomas per `DeviceFactory` klasę, kuri yra atsakinga už įrenginių kūrimą pagal tipą. Šis dizaino šablonas leidžia centralizuotai registruoti įrenginius ir lengvai sukurti įrenginius, pasitelkiant bendrą sąsają. Šis šablonas atskiria objekto kūrimą nuo kliento kodo, todėl programos plėtimas yra lengvesnis.

## ✅ Registry Pattern
**Registry Pattern** (Registracijos šablonas) buvo įdiegtas per `DeviceFactory` klasės atributą `_device_registry`, kuris laikomas įrenginių tipų registrą. Kiekvienas įrenginys registruojamas pagal savo tipą, ir vėliau gali būti sukurtas naudojant šį registrą. Tai leidžia efektyviai valdyti įrenginių tipus ir užtikrina, kad sukuriami tik registruoti įrenginiai.

## ✅ File I/O
**File I/O** (Failų įvestis/ išvestis) buvo naudojama įrenginių būsenai išsaugoti į failą ir ją atkurti. Programoje yra funkcijos `save_devices_to_file()` ir `load_devices_from_file()`, kurios atsakingos už įrenginių būsenų įrašymą į `JSON` failą ir jų atstatymą programos paleidimo metu. Tai leidžia išlaikyti įrenginių būseną tarp programos sesijų.

## ✅ SOLID principai (ypač SRP)
Programoje taikomi **SOLID principai**, tačiau ypatingą dėmesį skiriame **Single Responsibility Principle (SRP)** – principui, kad klasė turi turėti tik vieną atsakomybę. Kiekviena klasė turi tik savo funkcionalumą: `Device` klasė atsakinga už bendrą įrenginių funkcionalumą, o jos pavaldinės klasės (`TV`, `Light`, `AirConditioner` ir kt.) yra atsakingos už specifinius įrenginių parametrus. Taip pat `Valdymas` klasė yra atsakinga už įrenginių valdymą (pridėjimą, ištrynimą, įjungimą, išjungimą ir pan.), o `DeviceFactory` už įrenginių kūrimą, todėl kiekviena klasė atitinka tik vieną atsakomybę.

---

## Rezultatai ir santrauka

### Rezultatai

Programa leidžia realiu laiku atlikti visus reikiamus įrenginių valdymo veiksmus. Įrenginiai gali būti įjungti/išjungti, jų parametrai koreguojami, o visa sistema leidžia dirbti su skirtingais įrenginių tipais vieningai.

### Išvados

Sukurta sistema yra lanksti, lengvai plečiama ir naudojasi objektiškai orientuotu programavimu bei SOLID principais. Kiekvienas įrenginio tipas turi aiškią atsakomybę, o bendras valdymas vykdomas per centralizuotą „Valdymas“ klasę.


- Programa sėkmingai veikia ir leidžia valdyti įrenginius bei išsaugoti jų būseną failuose.
- Naudojant SOLID principus, sistema tapo lengviau plečiama ir keičiasi.
- Iššūkiai buvo susiję su tai, kaip užtikrinti, kad visi įrenginiai veiktų pagal bendrą sąsają ir būtų lengvai modifikuojami.
- Reikėjo užtikrinti, kad įrenginių būsenos būtų teisingai išsaugomos ir atstatomos iš failų.


### Kaip būtų galima išplėsti programą?

Galimi išplėtimai:

- Pridėti papildomų įrenginių (pvz., šildytuvas, signalizacija).
- Integruoti tinklo protokolą (pvz., MQTT) ir leisti valdyti įrenginius per internetą.
- Realizuoti vartotojų paskyrų sistemą su skirtingomis prieigos teisėmis.
- Įtraukti įrenginių būsenų istorijos sekimą.

