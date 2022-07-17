from ast import Store
from email.mime import image
from tabnanny import verbose
from unicodedata import category, name
from django import views
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey
from django.utils.text import slugify
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save

# Create your models here.


class Category(MPTTModel):
    name = models.CharField(verbose_name=_("Category Name"), help_text="This is required field",
                            unique=True, max_length=300)
    slug = models.SlugField(verbose_name=_("Category slug"), null=True, blank=True, help_text=_(
        "This field is filled automatically, you can leave this field blank"), unique=True, max_length=300)
    parent = TreeForeignKey('self', on_delete=models.CASCADE,
                            related_name='children', null=True, blank=True)
    active = models.BooleanField(default=False)

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def get_absolute_url(self):
        return reverse("store:category_list", args=[self.slug])

    def __str__(self):
        if self.active == True:
            return self.name
        else:
            return self.name + ' - [ Inactive]'


@receiver(pre_save, sender=Category)
def category_pre_save(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.name)


# @receiver(post_save, sender=Category)
# def category_post_save(sender, instance, created, *args, **kwargs):
#     if not instance.slug:
#         instance.slug = slugify(instance.name)
#     if instance.id and instance.notify_users:
#       print("notify users")
#       instance.notify_users_timestamp = timezone.now()


class Post(models.Model):
    category = models.ForeignKey(Category, on_delete=models.RESTRICT)
    title = models.CharField(help_text=_('Required field'), max_length=300)
    slug = models.SlugField(verbose_name=_("Post slug"), null=True, blank=True, help_text=_(
        "This field is filled automatically, you can leave this field blank"), unique=True, max_length=300)
    content = models.TextField(verbose_name=_('Description'), blank=False)
    image = models.ImageField(verbose_name=_(
        'Featured image'), help_text=_('Featured image size: 1200X600 px'), upload_to='blogs/', default='default.jpg')
    alt_text = models.CharField(verbose_name=_(
        'Image alternative text'), max_length=300, null=True, blank=True)
    author = models.CharField(max_length=50)
    views = models.IntegerField(default=0, editable=False)
    active = models.BooleanField(default=False)
    notify_users = models.BooleanField(default=False)
    notify_users_timestamp = models.DateTimeField(
        blank=True, null=True, auto_now_add=False)
    created_at = models.DateTimeField(verbose_name=_(
        "Created at"), auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(
        verbose_name=_('Updated at'), auto_now=True)

    class Meta:
        ordering = ("-created_at",)
        verbose_name = _("Post")
        verbose_name_plural = _("Posts")

    def get_absolute_url(self):
        return reverse("store:blog_detail", args=[self.slug])

    def __str__(self):
        if self.active == True:
            return self.title
        else:
            return self.title + ' - [Inactive, Requested by: ' + self.author + ' ]'


@receiver(pre_save, sender=Post)
def post_pre_save(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.title)


# class PostImage(models.Model):
#     post = models.ForeignKey(
#         Post, on_delete=models.CASCADE, related_name='Featured image')
#     image = models.ImageField(verbose_name=_(
#         'Post image'), help_text=_('Post image size: 1200X600 px'), upload_to='static/images/blogs/', default='static/images/default.jpg')
#     alt_text = models.CharField(verbose_name=_(
#         'Alternative Text'), max_length=300, null=True, blank=True)
#     is_feature = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True, editable=False)
#     updated_at = models.DateTimeField(auto_now=True)

#     class Meta:
#         verbose_name = _('Post Image')
#         verbose_name_plural = _('Post Images')
