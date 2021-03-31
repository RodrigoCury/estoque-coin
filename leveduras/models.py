from datetime import date
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse
from django.core.validators import FileExtensionValidator, MaxValueValidator


class Todo(models.Model):
    activity = models.CharField(max_length=50,
                                null=False,
                                blank=False,
                                verbose_name="O que fazer?")
    complete = models.BooleanField(default=False)
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)

    def __str__(self):
        return self.activity

    class Meta:
        verbose_name = "ToDo"
        verbose_name_plural = "ToDos"
        ordering = ('id',)


class Brand(models.Model):
    name = models.CharField(max_length=100, verbose_name="Marca",
                            unique=True, blank=False, null=False)
    slug = models.SlugField(max_length=100, verbose_name="Slug",
                            unique=True, blank=False, null=False)

    @property
    def sort(self):
        return Brand.objects.all().order_by('name')

    def get_absolute_url(self):
        return reverse('brand_detail', args=[self.slug])

    def get_absolute_url_delete(self):
        return reverse("brand_delete", args=[self.slug])

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    class Meta:
        verbose_name = "Marca"
        verbose_name_plural = "Marcas"
        ordering = ("name",)


class FermentativeProfile(models.Model):
    name = models.CharField(max_length=100,
                            verbose_name="Perfil Fermentativo",
                            unique=True,
                            blank=False,
                            null=False)
    slug = models.SlugField(verbose_name="slug",
                            unique=True)

    @property
    def sort(self):
        return Brand.objects.all().order_by('name')

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    class Meta:
        verbose_name = "Perfil Fermentativo"
        verbose_name_plural = "Perfis Fermentativos"
        ordering = ("name",)

    def get_absolute_url(self):
        return reverse('profile_detail', args=[self.slug])

    def get_absolute_url_delete(self):
        return reverse("profile_delete", args=[self.slug])


class Yeast(models.Model):
    name = models.CharField(max_length=100,
                            verbose_name="Nome",
                            unique=True,
                            blank=False, null=False,
                            )
    slug = models.SlugField(verbose_name="Slug",
                            unique=True,
                            blank=False,
                            null=False
                            )
    brand = models.ForeignKey(
        Brand,
        verbose_name="Marca",
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        User,
        verbose_name="Usuário",
        on_delete=models.CASCADE
    )
    fermentative_profile = models.ForeignKey(
        FermentativeProfile,
        on_delete=models.CASCADE,
        verbose_name="Perfil Fermentativo")
    created_at = models.DateField(default=date.today,
                                  verbose_name="Adicionado ao banco")
    last_reinnoculation = models.DateField(editable=True,
                                           verbose_name='Última repicagem')
    next_reinnoculation_limit_date = models.DateField(
        verbose_name='Próxima repicagem')
    reinnoculation_count = models.PositiveIntegerField(
        verbose_name="Quantidade de repiques")
    attenuation = models.PositiveIntegerField(
        verbose_name="Atenuação",
        validators=[MaxValueValidator(100)])
    FLOCCULATION_CHOICES = [
        ("Alta", "Alta"),
        ("Média", "Média"),
        ("Baixa", "Baixa"),
        ("N/D", "N/D"),
    ]
    flocculation = models.CharField(verbose_name="Floculação",
                                    max_length=5,
                                    choices=FLOCCULATION_CHOICES,
                                    default='N/D')
    POF_AMG_CHOICES = [
        ("+", "+"),
        ("-", "-")
    ]
    datasheet = models.FileField(
        verbose_name="PDF",
        upload_to="datasheets",
        null=True,
        blank=True,
        validators=[FileExtensionValidator(['pdf'])],
    )
    polyphenol = models.CharField(verbose_name="PoF",
                                  max_length=1,
                                  choices=POF_AMG_CHOICES,
                                  default=POF_AMG_CHOICES[0][0])
    amyloglucosidase = models.CharField(verbose_name="AMG",
                                        max_length=1,
                                        choices=POF_AMG_CHOICES,
                                        default=POF_AMG_CHOICES[0][0])

    def get_absolute_url(self):
        return reverse('yeast_detail', args=[self.slug])

    def get_absolute_url_update(self):
        return reverse('yeast_edit', args=[self.slug])

    def get_absolute_url_delete(self):
        return reverse("yeast_delete", args=[self.slug])

    class Meta:
        verbose_name = "Levedura"
        verbose_name_plural = "Leveduras"
        ordering = ("name",)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


# Log de actividades

def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='Usuário Deletado')[0]


class ActivityLog(models.Model):
    user = models.ForeignKey(User,
                             verbose_name='Usuário',
                             on_delete=models.SET(get_sentinel_user),
                             default=User.objects.first().id)
    activity = models.CharField(max_length=50,
                                blank=False,
                                null=False,
                                verbose_name="Atividade")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Atividade"
        verbose_name_plural = "Atividades"
        ordering = ('-created_at',)

    def __str__(self):
        return self.activity
