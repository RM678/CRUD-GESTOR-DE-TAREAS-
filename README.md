# CRUD-GESTOR-DE-TAREAS-
CRUD desarrollado con API REST Framework,  Python y Django

La base de datos utilzia 2 colecciones, la colección usuarios, donde almacena el nombre, email y contraseña de un usuario, y la colección tareas que registra los datos de las tareas (nombre, descripción, fecha de inicio, fecha final)

Para el funcionamiento de este programa, tenemos que existe una relación 1:N entre usuarios y tareas, ya que un usuario puede agregar muchas tareas, pero una tarea solo puede ser agregada por un usuario. Esto podemos visualizarlo si nos vamos al documento donde están las URLs usadas en la API, ya que por la serializacion utilizada para la misma, para poder registrar cualquier tarea se verifica que el usuario exista (que el correo esté registrado) igual para eliminar, editar e incluso para visualizar (ya que cada usuario solo puede visualizar sus propias tareas)

Tambien tenemos que el campo 'descripción' de tareas no es requerido en su totalidad, sino un campo opcional, por lo que no es necesario enviarlo, de hecho, si dicho campo se deja vacio simplemente se registrarán los demás datos a excepcion de ese, sin afectar el funcionamiento de la API. por lo que tenemos que cada tarea puede o no tener una descripción.
