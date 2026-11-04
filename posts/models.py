from django.conf import settings
from django.db import models
from django.urls import reverse


class Post(models.Model):
    titulo = models.CharField("título", max_length=200)
    contenido = models.TextField("contenido")
    imagen = models.ImageField("imagen", upload_to="posts/", blank=True)
    autor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="posts",
        verbose_name="autor",
    )
    fecha_creacion = models.DateTimeField("fecha de creación", auto_now_add=True)
    fecha_actualizacion = models.DateTimeField("última actualización", auto_now=True)

    class Meta:
        ordering = ["-fecha_creacion"]
        verbose_name = "post"
        verbose_name_plural = "posts"

    def __str__(self):
        return self.titulo

    def get_absolute_url(self):
        return reverse("posts:post_detail", kwargs={"pk": self.pk})
