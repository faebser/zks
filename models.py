# -*- coding: utf-8 -*-
__author__ = 'faebser'

from django.db import models
from cms.models import Page
from django.contrib.auth.models import User
from cms.models.pluginmodel import CMSPlugin  # normal cms-plugin
from djangocms_text_ckeditor.fields import HTMLField  # html field
from django.utils.translation import ugettext_lazy as _
from django.utils.text import Truncator
from django.utils.html import strip_tags
import datetime


def replace_all(text, removables):
    for i, j in removables.iteritems():
        text = text.replace(i, j)
    return text


class ArticleTags(models.Model):
    name = models.CharField(max_length=256, verbose_name=u'Name')
    url = models.CharField(max_length=1024, verbose_name=u'Url', default=' ', editable=False)

    class Meta:
        verbose_name = u'Blog Tag'

    def __unicode__(self):
        return self.name


class ArticleCategory(models.Model):
    name = models.CharField(max_length=256, verbose_name=u'Name')


class ArticleIntro(CMSPlugin):
    title = models.CharField(max_length=256, verbose_name=u'Titel')
    author = models.ManyToManyField(User, verbose_name=u'Autor', limit_choices_to={'is_active': True, 'is_staff': True})
    date = models.DateField(verbose_name=u'Datum', default=datetime.datetime.now())
    lead = HTMLField(verbose_name=u'Lead')
    tags = models.ManyToManyField(ArticleTags, verbose_name=u'Schlagworte')
    picBig = models.ImageField(upload_to=CMSPlugin.get_media_path, verbose_name=u'unteres Bild', blank=True, null=True)
    picTop = models.ImageField(upload_to=CMSPlugin.get_media_path, verbose_name=u'Bild oben, im Kasten', blank=True, null=True)
    isPublic = models.BooleanField(editable=False, default=False)

    class Meta:
        verbose_name = u'Article'

    def __unicode__(self):
        return unicode(self.isPublic) + " " + unicode(self.date) + " " + Truncator(strip_tags(self.lead)).words(5, truncate='...')

    def copy_relations(self, old_instance):
        self.author = old_instance.author.all()
        self.tags = old_instance.tags.all()


class ExternalLinkBox(CMSPlugin):

    def __unicode__(self):
        return u'externe Links'


class InternalLinkBox(CMSPlugin):

    def __unicode__(self):
        return u'interne Links'


class InternalLink(CMSPlugin):
    name = models.CharField(max_length=256, verbose_name=u"Text für Link")
    href = models.ForeignKey(Page, verbose_name=u"interne Seite")
    target = models.CharField(verbose_name=u'Öffnen in', blank=True, default=("_blank", u"gleichem Fenster"), max_length=100, choices=((
        ("", _("gleichem Fenster")),
        ("_blank", _("neuem Fenster")),
    )))

    def __unicode__(self):
        return self.name


class ExternalLink(CMSPlugin):
    name = models.CharField(max_length=256, verbose_name=u"Text für Link")
    href = models.URLField(verbose_name=u"externer Link")
    target = models.CharField(verbose_name=u'Öffnen in', blank=True, default=("_blank", u"gleichem Fenster"), max_length=100, choices=((
        ("", _("gleichem Fenster")),
        ("_blank", _("neuem Fenster")),
    )))

    def __unicode__(self):
        return self.name


class Ad(CMSPlugin):
    image = models.ImageField(verbose_name=u'Bild', upload_to=CMSPlugin.get_media_path)
    title = models.CharField(max_length=512, verbose_name=u'Titel')
    href = models.URLField(verbose_name=u'Link')
    target = models.CharField(verbose_name=u'Öffnen in', blank=True, default=("_blank", u"gleichem Fenster"), max_length=100, choices=((
        ("", _("gleichem Fenster")),
        ("_blank", _("neuem Fenster")),
    )))

    class Meta:
        verbose_name = u'Werbung'

    def __unicode__(self):
        return self.title


class Box(CMSPlugin):
    title = models.CharField(max_length=512, verbose_name=u'Titel')


class BlogListWithPagination(CMSPlugin):
    amount = models.IntegerField(verbose_name=u'Anzahl', default=5)

