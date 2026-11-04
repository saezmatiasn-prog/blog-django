import shutil
import tempfile
from io import BytesIO

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from PIL import Image

from .models import Perfil

MEDIA_TEMPORAL = tempfile.mkdtemp()


@override_settings(MEDIA_ROOT=MEDIA_TEMPORAL)
class CuentasTests(TestCase):
    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(MEDIA_TEMPORAL, ignore_errors=True)

    def test_registro_crea_usuario_con_perfil_e_inicia_sesion(self):
        respuesta = self.client.post(
            reverse("accounts:registro"),
            {
                "username": "nuevo",
                "email": "nuevo@example.com",
                "password1": "ClaveDePrueba123",
                "password2": "ClaveDePrueba123",
            },
        )
        self.assertRedirects(respuesta, reverse("posts:post_list"))
        usuario = User.objects.get(username="nuevo")
        self.assertTrue(Perfil.objects.filter(usuario=usuario).exists())
        self.assertEqual(int(self.client.session["_auth_user_id"]), usuario.pk)

    def test_login_y_logout(self):
        User.objects.create_user("lector", password="ClaveDePrueba123")
        respuesta = self.client.post(
            reverse("accounts:login"),
            {"username": "lector", "password": "ClaveDePrueba123"},
        )
        self.assertRedirects(respuesta, reverse("posts:post_list"))
        self.assertIn("_auth_user_id", self.client.session)

        respuesta = self.client.post(reverse("accounts:logout"))
        self.assertRedirects(respuesta, reverse("posts:post_list"))
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_menu_distingue_anonimo_de_autenticado(self):
        respuesta = self.client.get(reverse("posts:post_list"))
        self.assertContains(respuesta, "Iniciar sesión")
        self.assertNotContains(respuesta, "Cerrar sesión")

        self.client.force_login(User.objects.create_user("lector", password="ClaveDePrueba123"))
        respuesta = self.client.get(reverse("posts:post_list"))
        self.assertContains(respuesta, "Cerrar sesión")
        self.assertContains(respuesta, "Nuevo post")

    def test_perfil_requiere_sesion(self):
        for nombre in ("accounts:perfil", "accounts:editar_perfil"):
            with self.subTest(vista=nombre):
                ruta = reverse(nombre)
                respuesta = self.client.get(ruta)
                self.assertRedirects(respuesta, f"{reverse('accounts:login')}?next={ruta}")

    def test_editar_perfil_con_imagen(self):
        usuario = User.objects.create_user("lector", password="ClaveDePrueba123")
        self.client.force_login(usuario)

        buffer = BytesIO()
        Image.new("RGB", (50, 50), "orange").save(buffer, "PNG")
        avatar = SimpleUploadedFile("avatar.png", buffer.getvalue(), content_type="image/png")

        respuesta = self.client.post(
            reverse("accounts:editar_perfil"),
            {
                "first_name": "Ana",
                "last_name": "García",
                "email": "ana@example.com",
                "bio": "Me gusta escribir.",
                "avatar": avatar,
            },
        )
        self.assertRedirects(respuesta, reverse("accounts:perfil"))
        usuario.refresh_from_db()
        self.assertEqual(usuario.first_name, "Ana")
        self.assertEqual(usuario.perfil.bio, "Me gusta escribir.")
        self.assertTrue(usuario.perfil.avatar.name.startswith("avatares/"))
