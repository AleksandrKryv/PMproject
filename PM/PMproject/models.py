from __future__ import unicode_literals
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractUser
from sorl.thumbnail import *
from django.contrib.contenttypes.fields import *
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import F, Sum


class PMuser(AbstractUser):
    USERNAME_FIELD = 'username'
    GENDER_CHOICES = (
        ("M", "Male"),
        ("F", "Female"),
        ("O", "Other")
    )
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        default="?",
        null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    country = CountryField(null=True, blank=True)
    city = models.CharField('city or locality', null=True, max_length=100)
    phone_number = PhoneNumberField(null=True, unique=True)
    preferences = models.TextField(max_length=255, blank=True)
    photo = models.ForeignKey('Photo', null=True, on_delete=None)
    likes = models.IntegerField(blank=True, default=0)

    def __str__(self):
        return str(self.username)

    def number(self):
        formnum = str(self.phone_number)
        prefix = str(formnum[0:4])
        operat = str(formnum[4:6])
        number = str(formnum[6:])
        formatnum = str("%s  " "  %s  " "  %s" % (prefix,
                                                  operat,
                                                  number))
        return formatnum


class Photo(models.Model):
    photo_name = models.CharField(max_length=120, blank=True, null=True)
    description = models.TextField(max_length=250, blank=True, null=True)
    image = ImageField(upload_to='media', default='')
    Photograph = models.ManyToManyField('Photograph', blank=True, null=True)
    Model = models.ManyToManyField('Model', blank=True, null=True)
    comments = GenericRelation('Comment', blank=True, null=True)
    likes = models.IntegerField(blank=True, default=0)

    def photographs(self):
        return ", ".join([str(ph.user) for ph in self.Photograph.all()])

    def models(self):
        return ", ".join([str(ph.user) for ph in self.Model.all()])

    def __str__(self):
        return str(self.photo_name)

    def thumb(self):
        return u'<img src="%s" />' % (get_thumbnail(self.image, "100x100", crop='center', quality=95).url,)

    thumb.short_description = 'Photos'
    thumb.allow_tags = True


class Model(models.Model):
    user = models.OneToOneField('PMuser')
    about = models.TextField(max_length=255, blank=True)
    height_choices = (
        ("S", "Short"),
        ("A", "Average"),
        ("T", "Tall")
    )
    height = models.CharField(
        max_length=1,
        choices=height_choices,
        default="?")
    hairlength_choices = (
        ("S", "Short"),
        ("A", "Average"),
        ("L", "Long")
    )
    hair_length = models.CharField(
        max_length=1,
        choices=hairlength_choices,
        default="?")
    haircolor_choices = (
        ("B", "Black"),
        ("Bl", "Blond"),
        ("Br", "Brown"),
        ("Gi", "Ginger"),
        ("R", "Red"),
        ("Gr", "Green"),
        ("W", "White"),
        ("Ye", "Yellow"),
        ("Pu", "Purple"),
        ("Gra", "Gray"),
        ("Blu", "Blue"),
        ("Mi", "Mixed"),
        ("Ot", "Other")
    )
    hair_color = models.CharField(
        max_length=5,
        choices=haircolor_choices,
        default="?")
    eyecolor_choice = (
        ("Bl", "Blue"),
        ("G", "Green"),
        ("Br", "Brown"),
        ("Gr", "Gray"),
        ("P", "Purple")
    )
    eye_color = models.CharField(
        max_length=2,
        choices=eyecolor_choice,
        default="?")
    bodytype_choices = (
        ("S", "Slim"),
        ("A", "Average"),
        ("T", "Thick")
    )
    body_type = models.CharField(
        max_length=1,
        choices=bodytype_choices,
        default="?")
    skintone_choice = (
        ("L", "Light"),
        ("B", "Black"),
        ("D", "Dark"),
        ("O", "Olive")
    )
    skin_tone = models.CharField(
        max_length=1,
        choices=skintone_choice,
        default="?")

    experience_choice = (
        ("N", "About a year or less"),
        ("A", "About a 5 years"),
        ("P", "About a 10 years or more")
    )
    experience = models.CharField(
        max_length=1,
        choices=experience_choice,
        default="?"
    )

    level_choice = (
        ("N", "Newbie"),
        ("A", "Amateur"),
        ("P", "Professional"),
    )
    level = models.CharField(
        max_length=1,
        choices=level_choice,
        default="?"
    )
    likes = models.IntegerField(null=True, blank=True)
    condition_choices = (
        ('T', 'TFP'),
        ('P', 'Payment')
    )
    conditions = models.CharField(
        max_length=1,
        choices=condition_choices,
        default="?"
    )

    def __str__(self):
        return str(self.user)


class Photograph(models.Model):
    user = models.OneToOneField('PMuser')
    about = models.TextField(max_length=255, blank=True)
    experience_choice = (
        ("N", "About a year or less"),
        ("A", "About a 5 years"),
        ("P", "About a 10 years or more")
    )
    experience = models.CharField(
        max_length=1,
        choices=experience_choice,
        default="?"
    )

    level_choice = (
        ("N", "Newbie"),
        ("A", "Amateur"),
        ("P", "Professional"),
    )
    level = models.CharField(
        max_length=1,
        choices=level_choice,
        default="?"
    )
    likes = models.IntegerField(null=True, blank=True)
    condition_choices = (
        ('T', 'TFP'),
        ('P', 'Payment')
    )
    conditions = models.CharField(
        max_length=1,
        choices=condition_choices,
        default="?"
    )

    def __str__(self):
        return str(self.user)


class Comment(models.Model):
    user = models.OneToOneField('PMuser', null=True)
    text = models.TextField(max_length=300)
    date = models.DateTimeField(auto_now_add=True)

    limit = models.Q(app_label='PMproject', model='Photo') | \
            models.Q(app_label='PMproject', model='Photograph') | \
            models.Q(app_label='PMproject', model='Model')
    content_type = models.ForeignKey(ContentType, null=True, limit_choices_to=limit)
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return self.text


class Portfolio(models.Model):
    user = models.OneToOneField('PMuser')
    description = models.TextField(max_length=250, null=True, blank=True)
    photo = models.ManyToManyField('Photo', null=True, blank=True)
    likes = models.PositiveIntegerField(blank=True, default=0)

    @property
    def random_img(self):

        return self.photo.order_by("?").first()

    def __str__(self):
        return str(self.user)


class Album(models.Model):
    album_name = models.CharField(max_length=50, null=True)
    description = models.TextField(max_length=250, null=True, blank=True)
    user = models.ForeignKey('PMuser')
    photo = models.ManyToManyField('Photo', null=True, blank=True)
    likes = models.PositiveIntegerField(blank=True, default=0)

    @property
    def random_img(self):
        return self.photo.order_by("?").first()

    def __str__(self):
        return str(self.user)


class Like(models.Model):
    user = models.ForeignKey('PMuser')
    photo = models.ForeignKey('Photo')

    def __str__(self):
        return str(self.photo)
