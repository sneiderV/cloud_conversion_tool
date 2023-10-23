
# Cloud conversion tool 📀 📹📽️

Cloud Conversion Tool App es una aplicación web que ofrece a los usuarios la posibilidad de subir y transformar diversos formatos multimedia de archivos, así como llevar a cabo procesos de compresión de manera gratuita.  

Los formatos de conversión que maneja la aplicación son:
- MP4 
- WEBM 
- AVI 
- MPEG 
- WMV

Funcionamiento de la Aplicación
El funcionamiento general de la aplicación se basa en la creación de una cuenta en el portal web y el acceso al administrador de archivos. Una vez se ha creado la cuenta, los usuarios pueden cargar archivos y solicitar la conversión 
de formato de estos para su posterior descarga. La aplicación web permite a los usuarios convertir archivos multimedia en línea de un formato a otro, seleccionando el formato de destino.

## 🏗️ Componentes del Sistema Cloud Conversion Tool App

| Componente  | Descripcion |
| :---------: | ----------- |
| `conversion_app` | Aplicacion receptora de tareas para convertir archivos. |
| `worker` | Procesador de tareas asincrono de los archivos del usuario pentiendes por atender. |
| `Redis` | Servidor de encolamiento. |
| `Postgres` | Motor de base de datos. |

La interacción de los componentes se presenta en el siguiente modelo, si desea revisar más documentación sobre la arquitectura de software lo invitamos a revisar la [wiki](https://github.com/sneiderV/cloud_conversion_tool/wiki) del proyecto

<img width="500" alt="Modelo de despliegue" src="https://github.com/sneiderV/cloud_conversion_tool/assets/20799651/ad400dd2-5950-4511-8399-b687ee68acb1">

## ▶️ Ejecutando los componentes

1. Descargar o clonar el repositorio
2. Abrir una terminal de comandos y dirigir el apuntamiento a la carpeta del proyecto
   
    `cd cloud_conversion_tool`
   
4. Crear un nuevo ambiente virtual `python3 -m venv nuevo_ambiente`, activarlo `source nuevo_ambiente/bin/activate`.

5. Instalar dependencias `pip install flask` , `pip install flask-restful`, `pip install flask-marshmallow`

6. Configurar variables de entorno `export FLASK_APP=app.py`, `export FLASK_DEBUG=1`, `export FLASK_ENV=development`

7. Localizar el archivo que tiene por nombre `docker-compose.yml` y ejecutar el comando `docker-compose up` y esperar mientras se descargan las imagenes de los recursos y se construyen los contenedores.

   <img width="300" alt="image" src="https://github.com/sneiderV/cloud_conversion_tool/assets/20799651/a8bc8aca-27a5-416b-a2db-0003a5eea03b">

 
8. Visualizar la creación y ejecución activa de 4 contenedores.
   
   <img width="1326" alt="image" src="https://github.com/sneiderV/cloud_conversion_tool/assets/20799651/2722c756-1fc5-4401-a884-8650fb12b6e6">
   <img width="566" alt="image" src="https://github.com/sneiderV/cloud_conversion_tool/assets/105640955/23d345ee-fa35-4bb6-b9a7-4a5a348b87d9">


9. En el folder `/collections` se encuentrar dos archivos `.json` que puede importar directamente en la aplicación Postman.

   También, tiene a disposición la [documentación](https://documenter.getpostman.com/view/30660012/2s9YRCVqp2) de la Api en el siguiente [link](https://documenter.getpostman.com/view/30660012/2s9YRCVqp2).

   <img width="300" alt="image" src="https://github.com/sneiderV/cloud_conversion_tool/assets/20799651/23e2cb9f-cd75-4cb2-94cd-971a6db2effd">

   Colección importada en Postman:
   
   <img width="209" alt="image" src="https://github.com/sneiderV/cloud_conversion_tool/assets/20799651/b0daf9f2-f996-4ee0-b7e3-8b26a7f08e60">

   Recomendamos el siguiente orden de ejecución, para probar el sistema:
   
   | Paso  | Descripcion | Nombre Request |
   | :---: | :---------: | :--------------:|
   | 1 | Crear el usuario. | `signup` |
   | 2 | Realizar login. | `login` |
   | 3 | Crear tarea. | `task` |
   | 4 | Listar tareas del usuario. | `tasks` |
   | 5 | Buscar tarea por id del usuario. | `task by id` |
   | 6 | Eliminar tarea. | `delete` |
   

______

>  Disponibilizamos [un servicio de registro](https://github.com/sneiderV/cloud_conversion_tool/issues/new/choose) de 🐞 `Bugs` o ✨ `Features` del cual estaremos dispuestos a atender.

<img width="1700" alt="image" src="https://github.com/sneiderV/cloud_conversion_tool/assets/20799651/2543836c-5ae2-4bb7-996b-824f098266e1">

## 📽️ Demostración de la aplicación

* [Demostración de la aplicación aquí](https://www.canva.com/design/DAFx3poFmkc/CdUHNyewScI0eBimbfxxjg/edit?utm_content=DAFx3poFmkc&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton)

## 🧪 Plan de pruebas

* [Plan de pruebas](https://github.com/sneiderV/cloud_conversion_tool/files/13064912/Escenario.y.Pruebas.de.Estres.API.REST.y.Batch.pdf)
