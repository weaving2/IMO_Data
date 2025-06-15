# Dato mata relato.

EL objetivo del programa es medir el rendimiento de un pais en el P1/4 de la IMO, se dividen los problemas por las cuatro areas(ACGN) y luego se saca la nota promedio(por equipo) en cada area. Para paises que suelen resolver los P1/4 esta metrica usualmente resulta en ~38-40 sus promedios.

## ¿Qué hace el programa?
1. El script `gethtml.py` descarga los htmls con la informacion de cada pais el cual el usuario introduzca por pantalla. [Info de un pais en particular](https://www.imo-official.org/country_individual_r.aspx?code=FRA) en este ejemplo el link es de Francia, pero basta cambiar el ISO 3166-1 alpha-3 al final de la URL.
2. El script `practice.py` extrae los datos del html(se asume que se encuentran en una carpeta llamada countries) y los guarda en un dataframe, se añade la información acerca de la rama de cada problema, pero la rama de los problemas el autor las designa manualmente en un diccionario inicial.