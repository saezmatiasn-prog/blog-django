# Blog Web con Django

Blog web desarrollado con Django como proyecto final del curso de Python. Permite que cualquier visitante lea las publicaciones y que los usuarios registrados escriban, editen y eliminen sus propios posts con imágenes, además de gestionar su perfil.

## Tecnologías

- **Python** 3.10 o superior
- **Django** 5.2 (LTS)
- **SQLite** como base de datos
- **Pillow** para el manejo de imágenes
- **python-decouple** para las variables de entorno
- **Bootstrap** 5.3 (desde CDN) para el diseño

## Funcionalidades

**Publicaciones**
- Listado de posts con paginación y detalle de cada post.
- Crear, editar y eliminar posts desde la interfaz web (no solo desde el admin).
- Imagen opcional en cada post. Si un post no tiene imagen, se muestra una imagen por defecto.
- Solo el autor de un post puede editarlo o eliminarlo.
- Búsqueda por título o contenido, con aviso cuando no hay resultados.

**Usuarios**
- Registro, inicio de sesión y cierre de sesión.
- Perfil con nombre, correo, biografía e imagen de perfil, y la lista de posts propios.
- Edición del perfil y de la imagen de perfil.
- El menú cambia según si el visitante es anónimo o tiene la sesión iniciada.

**Seguridad**
- Crear, editar y eliminar posts, ver el perfil y editarlo requieren sesión iniciada. La protección está en las vistas (`LoginRequiredMixin` y `@login_required`), no solo en los botones.
- Un visitante anónimo puede ver el listado y el detalle de los posts.
- La clave secreta y la configuración sensible se leen de un archivo `.env` que no se sube al repositorio.

## Rutas principales

| Ruta | Descripción | Acceso |
|------|-------------|--------|
| `/` | Listado de posts (acepta `?q=` para buscar) | Público |
| `/posts/<id>/` | Detalle de un post | Público |
| `/posts/nuevo/` | Crear post | Requiere sesión |
| `/posts/<id>/editar/` | Editar post | Requiere sesión (solo el autor) |
| `/posts/<id>/eliminar/` | Eliminar post | Requiere sesión (solo el autor) |
| `/cuentas/registro/` | Crear cuenta | Público |
| `/cuentas/login/` | Iniciar sesión | Público |
| `/cuentas/logout/` | Cerrar sesión | Requiere sesión |
| `/cuentas/perfil/` | Ver mi perfil | Requiere sesión |
| `/cuentas/perfil/editar/` | Editar mi perfil | Requiere sesión |
| `/admin/` | Panel de administración | Superusuario |

Si un usuario anónimo intenta entrar a una ruta protegida, se lo redirige a la página de inicio de sesión.

## Estructura del proyecto

```
blog-django/
├── config/              # Configuración del proyecto (settings, urls)
├── posts/               # App de publicaciones: modelo, vistas CRUD, búsqueda, tests
├── accounts/            # App de usuarios: registro, login, perfil, tests
├── templates/           # Template base, página 403 y fragmentos reutilizables
├── static/              # CSS e imágenes por defecto
├── manage.py
├── requirements.txt
├── .env.example         # Modelo del archivo .env
└── .gitignore
```

## Instalación y ejecución

### Requisitos previos

- Python 3.10 o superior
- Git

En Windows el comando suele ser `python`; en macOS y Linux, `python3`.

### 1. Clonar el repositorio

```bash
git clone https://github.com/saezmatiasn-prog/blog-django.git
cd blog-django
```

### 2. Crear y activar el entorno virtual

**Windows**

```bash
python -m venv venv
venv\Scripts\activate
```

> En PowerShell, si aparece un error de permisos al activar, ejecutá una vez `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` y volvé a intentar.

**macOS / Linux**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar las dependencias

```bash
pip install -r requirements.txt
```

### 4. Crear el archivo `.env`

El proyecto lee la configuración sensible desde un archivo `.env`. Copiá el archivo de ejemplo:

**Windows**

```bash
copy .env.example .env
```

**macOS / Linux**

```bash
cp .env.example .env
```

Para uso local, el archivo funciona tal como viene. Si querés generar una clave secreta propia, ejecutá el siguiente comando y pegá el resultado en `SECRET_KEY` dentro de `.env`:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 5. Aplicar las migraciones

```bash
python manage.py migrate
```

Esto crea la base de datos `db.sqlite3` con todas las tablas.

### 6. Crear un superusuario (opcional, para el panel de administración)

```bash
python manage.py createsuperuser
```

Ingresá un nombre de usuario, un correo y una contraseña. Con ese usuario podés entrar a `http://127.0.0.1:8000/admin/`.

### 7. Iniciar el servidor

```bash
python manage.py runserver
```

Abrí `http://127.0.0.1:8000/` en el navegador.

## Probar el proyecto desde cero

El repositorio **no incluye** la base de datos (`db.sqlite3`) ni las imágenes subidas (`media/`), así que el blog empieza vacío. Después de seguir los pasos de instalación:

1. Entrá a `http://127.0.0.1:8000/` sin iniciar sesión: vas a ver el listado vacío y el menú con **Iniciar sesión** y **Registrarse**.
2. Probá entrar a `http://127.0.0.1:8000/posts/nuevo/`: te redirige al login porque la ruta está protegida.
3. Hacé clic en **Registrarse** y creá una cuenta. Al terminar, la sesión queda iniciada.
4. Hacé clic en **Nuevo post**, completá título y contenido, elegí una imagen y publicá.
5. Creá otro post sin imagen: en el listado se muestra la imagen por defecto.
6. Desde el detalle de un post propio, probá **Editar** y **Eliminar**.
7. Usá el buscador de la barra superior con una palabra del título o del contenido, y también con una palabra que no exista para ver el aviso de "sin resultados".
8. Abrí el menú con tu nombre de usuario, entrá a **Editar perfil** y subí una imagen de perfil.
9. Cerrá sesión y verificá que el listado y el detalle sigan siendo visibles.

Las imágenes que subas se guardan en la carpeta `media/`, que se crea automáticamente.

## Tests automáticos

El proyecto incluye tests para el CRUD de posts, la carga de imágenes, la búsqueda, el registro, el login y logout, el perfil y la protección de rutas:

```bash
python manage.py test
```

## Variables de entorno

| Variable | Descripción | Valor para desarrollo |
|----------|-------------|-----------------------|
| `SECRET_KEY` | Clave secreta de Django | Cualquier texto largo y aleatorio |
| `DEBUG` | Modo de depuración. En `True` Django sirve las imágenes de `media/` | `True` |
| `ALLOWED_HOSTS` | Hosts permitidos, separados por coma | `localhost,127.0.0.1` |

El archivo `.env` real nunca se sube al repositorio (está en `.gitignore`). Solo se incluye `.env.example`, sin valores privados.

## Archivos que no se suben al repositorio

El `.gitignore` excluye `venv/`, `.env`, `__pycache__/`, `*.pyc`, `db.sqlite3`, `media/`, `staticfiles/` y la configuración local de editores y del sistema operativo.

## Autor

**Matías Nicolás Saez**
GitHub: [@saezmatiasn-prog](https://github.com/saezmatiasn-prog)
