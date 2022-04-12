
# Readme

En aquest repositori es troba el projecte de Web scraping (PRA1) de l'assignatura Tipologia i cicle de vida de les dades.

### Autors:
Guillem Campo Fons

Aleix Yébenes Creus

## Fitxers

Els fitxers que es troben en aquest repositori són els següents:

* readme.md: Descripció del repositori.
* M2.951_20212_Practica1.PDF: Enunciat de la pràctica.
* PRA1_Campo_Yebenes.PDF: Memòria de la pràctica.
* /src/webScraping_final.py: Fixter font del codi per executar el procés de scraping.
* /src/webScraping_final.ipynb: Codi font en format Jupiter notebook.


## Dataset generat

El dataset generat mitjançant l'execució del codi el dia 12/04/2022 a les 15:27 s'ha publicat a Zenodo amb el següent DOI: 10.5281/zenodo.6453166

El dataset té els següents camps:

* ID: Índex del vol dins del dataset
* Origin: nom de l’aeroport d’origen
* Origin ID: Codi (3 lletres) de l’aeroport d’origen
* Arrival: hora d’arribada programada
* Flights: codi(s) del vol (múltiples en cas de codi compartit)
* Airline: aerolínia/es que opera el vol
* Terminal: número de terminal on aterra l’avió
* Status: estat del vol 
* Date: data programada

En total té 575 registres.
