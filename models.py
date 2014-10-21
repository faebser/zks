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
from unidecode import unidecode
import datetime
from requests import get as request
from django.utils.http import urlencode
from django.db.models.signals import pre_save
from django.dispatch import receiver


def replace_all(text, removables):
    for i, j in removables.iteritems():
        text = text.replace(i, j)
    return text


class ArticleTags(models.Model):
    name = models.CharField(max_length=256, verbose_name=u'Name')
    url = models.CharField(max_length=1024, verbose_name=u'Url', editable=False)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.url = unidecode(self.name.lower().replace(' ', '_'))
        print self.url
        super(ArticleTags, self).save()

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
    amountSmall = models.IntegerField(verbose_name=u'Anzahl zweispaltig', default=4)
    amountThreeCol = models.IntegerField(verbose_name=u'Anzahl dreispaltig', default=6)


class Blockquote(CMSPlugin):
    quote = HTMLField(verbose_name=u'Zitat')
    author = models.CharField(max_length=1024, verbose_name=u'Autor')

    class Meta:
        verbose_name = u'Zitat'

    def __unicode__(self):
        return self.author + ': ' + Truncator(strip_tags(self.quote)).words(5, truncate='...')


class Iframe(CMSPlugin):
    url = models.CharField(max_length=1024, verbose_name=u'Embed Url', default=u'')
    #css = models.CharField(max_length=512, editable=False, default=u'video')
    oembed_url = None
    iframe = models.CharField(max_length=20148, editable=False, default='Fehler im Iframe')

    def save(self, no_signals=False, *args, **kwargs):
        print 'saving!'
        super(Iframe, self).save(no_signals=False, *args, **kwargs)

    def __unicode__(self):
        return self.url

    class Meta:
        verbose_name = u"Einbetten"
        abstract = True


class YouTubeIframe(Iframe):
    oembed_url = 'http://www.youtube.com/oembed'
    css = u'youtube'

    class Meta:
        verbose_name = u'Youtube Media'


class MixcloudIframe(Iframe):
    oembed_url = 'http://www.mixcloud.com/oembed/'
    css = u'mixcloud'

    class Meta:
        verbose_name = u'Mixcloud Media'


class SoundCloudIframe(Iframe):
    oembed_url = 'https://soundcloud.com/oembed'
    css = u'soundcloud'

    class Meta:
        verbose_name = u'Soundcloud Media'


class Slider(CMSPlugin):

    class Meta:
        verbose_name = u'Slider'


class SliderItem(CMSPlugin):
    picture = models.ImageField(verbose_name=u'Bild', upload_to=CMSPlugin.get_media_path)
    caption = models.CharField(max_length=512, blank=True, null=True)

    class Meta:
        verbose_name = u'Slider Item'


@receiver(pre_save, sender=Iframe)
@receiver(pre_save, sender=YouTubeIframe)
@receiver(pre_save, sender=MixcloudIframe)
@receiver(pre_save, sender=SoundCloudIframe)
def makeAPICall(sender, instance, **kwargs):
    # see https://github.com/panzi/oembedendpoints/blob/master/endpoints.json for enpoints
    # http://oembed.com/ for doc
    print "stuff bla"
    try:
        obj = Iframe.objects.get(pk=instance.pk)
    except Iframe.DoesNotExist:
        instance.iframe = query_oembed(instance.oembed_url, instance.url)  # object is new
    else:
        if not obj.url == instance.url:  # Field has changed
            instance.iframe = query_oembed(instance.oembed_url, instance.url)
    pass


def query_oembed(oembed_url, query_url):
    """
    see https://github.com/panzi/oembedendpoints/blob/master/endpoints.json for endpoints
    http://oembed.com/ for doc

    querys the ombed endpoint and returns a string containing a iframe ready to be put in a template

    :param string oembed_url: Ombed Endpoint
    :param string query_dict:
    :return: string Iframe for Template
    """
    oembed_options = {
        "format": "json",
        'maxwidth': 710
    }
    oembed_options.update({
        'url': query_url
    })
    print 'omebed_url is ' + oembed_url + '?' + urlencode(oembed_options)
    if oembed_url is not None or oembed_url != 'default':
        r = request(oembed_url + '?' + urlencode(oembed_options))
        print r
        return r.json()['html']
    else:
        return None
