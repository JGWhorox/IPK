# IPK - Počítačové komunikácie a siete
### Projekt 1: HTTP resolver doménových mien
### Autor: Johann Gawron (xgawro00@stud.fit.vutbr.cz)

## Popis projektu
Úlohou bolo vytvoriť server, ktorý resolvuje domény na IP adresy a naopak. 
Cieľom bolo zoznámiť sa s **programovaním klientských a serverových aplikácií** s použitím socketov

## Špecifikácia
Implementácia serveru, ktorý bude komunikovať použitím protokolu HTTP a bude 
zaisťovať preklad doménových mien. Pre preklad server využíva lokálny resolver stanice, 
na ktorej beží - OS API (v prípade pythonu gethostbyaddr a gethostbyname).
Server podporuje nasledujúce operácie:

### GET
Vezme jeden parameter v podobe URL požiadavku a preloží ho, napríklad:

GET /resolve?name=apple.com&type=A HTTP/1.1

parametry sú:
	- name = doménové meno alebo IP adresa
	- type = typ požadovanej odpovedi (A alebo PTR)

### POST
Obsahuje zoznam požiadavkov vo svojom tele, každý na samostatnom riadku.
S využitím curl môže vyzerať naprílad takto:

curl --data-binary @queries.txt -X POST http://localhost:5353/dns-query

kde queries.txt obsahuje riadky s nasledujúcim formátom:

**DOTAZ:TYP**

kde:
	- DOTAZ =  doménové meno alebo IP adresa
	- TYP = typ požadovanej odpovedi (A alebo PTR)
	
napríklad:

www.fit.vutbr.cz:A
www.google.com:A
www.seznam.cz:A
147.229.14.131:PTR
ihned.cz:A

## Popis implementácie
Projekt je vypracovaný v jazyku python verzie 3.8 no je testovaný aj na 3.6.9. Obsahuje implementáciu 
požadovaných funkcií a základné kontroly vstupov a requestov.
Spúšťa sa pomocou príkazu **python3 server.py PORT** kde treba dosadiť port na server, 
ktorý bude následne použitý na posielanie požiadavkov na daný server.

Po prijatí požiadavku sa z neho vytiahnu podstatné údaje, resolvnú sa podľa zadaných 
parametrov a ukladajú sa do bufferu. Pokiaľ pri spracovaní nedôjde k žiadnej chybe budú na konci 
odoslané hneď po hlavičke **HTTP/$(version) 200 OK.**. Ak nastala chyba bude podľa špecifikácie navrátená chyba.


