import shutil
import tempfile
from io import BytesIO

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from PIL import Image

from .models import Post

MEDIA_TEMPORAL = tempfile.mkdtemp()


def crear_imagen(nombre="foto.png"):
    buffer = BytesIO()
    Image.new("RGB", (60, 40), "steelblue").save(buffer, "PNG")
    return SimpleUploadedFile(nombre, buffer.getvalue(), content_type="image/png")


@override_settings(MEDIA_ROOT=MEDIA_TEMPORAL)
class PostViewsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.autor = User.objects.create_user("autor", password="ClaveDePrueba123")
        cls.otro = User.objects.create_user("otro", password="ClaveDePrueba123")
        cls.post = Post.objects.create(
            titulo="Primer post",
            contenido="Contenido de prueba sobre Django.",
            autor=cls.autor,
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(MEDIA_TEMPORAL, ignore_errors=True)

    def test_listado_y_detalle_visibles_para_anonimos(self):
        respuesta = self.client.get(reverse("posts:post_list"))
        self.assertContains(respuesta, "Primer post")
        respuesta = self.client.get(self.post.get_absolute_url())
        self.assertContains(respuesta, "Contenido de prueba")

    def test_post_sin_imagen_muestra_imagen_por_defecto(self):
        respuesta = self.client.get(reverse("posts:post_list"))
        self.assertContains(respuesta, "img/sin-imagen.svg")

    def test_rutas_protegidas_redirigen_al_login(self):
        rutas = [
            reverse("posts:post_create"),
            reverse("posts:post_update", args=[self.post.pk]),
            reverse("posts:post_delete", args=[self.post.pk]),
        ]
        for ruta in rutas:
            with self.subTest(ruta=ruta):
                respuesta = self.client.get(ruta)
                self.assertRedirects(respuesta, f"{reverse('accounts:login')}?next={ruta}")

    def test_crear_post_con_imagen(self):
        self.client.force_login(self.autor)
        respuesta = self.client.post(
            reverse("posts:post_create"),
            {"titulo": "Post con foto", "contenido": "Texto", "imagen": crear_imagen()},
        )
        post = Post.objects.get(titulo="Post con foto")
        self.assertRedirects(respuesta, post.get_absolute_url())
        self.assertEqual(post.autor, self.autor)
        self.assertTrue(post.imagen.name.startswith("posts/"))
        self.assertContains(self.client.get(post.get_absolute_url()), post.imagen.url)

    def test_crear_post_sin_imagen(self):
        self.client.force_login(self.autor)
        self.client.post(reverse("posts:post_create"), {"titulo": "Solo texto", "contenido": "Texto"})
        self.assertFalse(Post.objects.get(titulo="Solo texto").imagen)

    def test_autor_puede_editar_su_post(self):
        self.client.force_login(self.autor)
        self.client.post(
            reverse("posts:post_update", args=[self.post.pk]),
            {"titulo": "Título editado", "contenido": "Nuevo contenido"},
        )
        self.post.refresh_from_db()
        self.assertEqual(self.post.titulo, "Título editado")

    def test_autor_puede_eliminar_su_post(self):
        self.client.force_login(self.autor)
        respuesta = self.client.post(reverse("posts:post_delete", args=[self.post.pk]))
        self.assertRedirects(respuesta, reverse("posts:post_list"))
        self.assertFalse(Post.objects.filter(pk=self.post.pk).exists())

    def test_otro_usuario_no_puede_editar_ni_eliminar(self):
        self.client.force_login(self.otro)
        for nombre in ("posts:post_update", "posts:post_delete"):
            with self.subTest(vista=nombre):
                respuesta = self.client.post(reverse(nombre, args=[self.post.pk]), {"titulo": "x", "contenido": "x"})
                self.assertEqual(respuesta.status_code, 403)
        self.assertTrue(Post.objects.filter(pk=self.post.pk, titulo="Primer post").exists())

    def test_busqueda_por_titulo_y_contenido(self):
        Post.objects.create(titulo="Receta de empanadas", contenido="Masa casera", autor=self.autor)
        respuesta = self.client.get(reverse("posts:post_list"), {"q": "empanadas"})
        self.assertContains(respuesta, "Receta de empanadas")
        self.assertNotContains(respuesta, "Primer post")

        respuesta = self.client.get(reverse("posts:post_list"), {"q": "django"})
        self.assertContains(respuesta, "Primer post")

    def test_busqueda_sin_resultados_muestra_aviso(self):
        respuesta = self.client.get(reverse("posts:post_list"), {"q": "inexistente"})
        self.assertContains(respuesta, "No se encontraron posts")
