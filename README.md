# Renovación de la aplicación de Contactos para Presidencia

## TODO:
* Tabla M2M para los datos de agenda


## Anotaciones:
*  select nombre, apellidos, count(*) c from persona group by nombre, apellidos having c > 1;