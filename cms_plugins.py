# -*- coding: utf-8 -*-
__author__ = 'faebser'

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _
from djangocms_text_ckeditor.cms_plugins import TextPlugin
from django.core.urlresolvers import reverse
from models import *
from os import path
from author_and_tags.views import pagination
from models import (
    ArticleCategory, ArticleTags, ArticleIntro,
    ExternalLink, ExternalLinkBox, InternalLink,
    InternalLinkBox, Ad, Box, BlogListWithPagination,
    YouTubeIframe, MixcloudIframe, Blockquote, SoundCloudIframe,
    Slider, SliderItem
)


class PluginSettings():
    templatePath = path.join("plugins")
    module = u'ZKS'

ps = PluginSettings()


class ArticleIntroPlugin(CMSPluginBase):
    model = ArticleIntro
    module = ps.module
    render_template = path.join(ps.templatePath, 'article_header.html')
    name = _(u'Blog Intro')

    def render(self, context, instance, placeholder):
        context['instance'] = instance
        context['placeholder'] = placeholder
        context['isOnList'] = False

        return context

plugin_pool.register_plugin(ArticleIntroPlugin)


class BlogListWithPaginationPlugin(CMSPluginBase):
    cache = False
    model = BlogListWithPagination
    module = ps.module
    render_template = path.join(ps.templatePath, 'articles_list.html')
    name = _(u'Blog Liste')

    def render(self, context, instance, placeholder):
        context['instance'] = instance
        context['placeholder'] = placeholder
        parameter = context['request'].GET.get('pagination', None)
        total_amount = instance.amount + instance.amountSmall
        objects = None
        get_parameter = None
        context['isOnList'] = True

        # see https://plus.google.com/118309212962987618554/posts/Nc8xQPN9yFy
        # to exclude plugins from list
        objects = ArticleIntro.objects.all().exclude(placeholder__page__publisher_is_draft=False).order_by('date')
        objects = objects.exclude(placeholder__page=None)
        try:
            articles, get_parameter = pagination(objects, parameter, instance.amount, instance.amountSmall, instance.amountThreeCol)
        except ObjectDoesNotExist:
            articles = None

        context.update({
            'articles': articles,
            'pagination': get_parameter
        })

        return context

plugin_pool.register_plugin(BlogListWithPaginationPlugin)


class YoutubeIframePlugin(CMSPluginBase):
    model = YouTubeIframe
    module = ps.module
    render_template = path.join(ps.templatePath, 'iframe.html')
    name = _(u'Youtube')


plugin_pool.register_plugin(YoutubeIframePlugin)


class MixcloudIframePlugin(CMSPluginBase):
    model = MixcloudIframe
    module = ps.module
    render_template = path.join(ps.templatePath, 'iframe.html')
    name = _(u'Mixcloud')

plugin_pool.register_plugin(MixcloudIframePlugin)


class SoundcloudIframePlugin(CMSPluginBase):
    model = SoundCloudIframe
    module = ps.module
    render_template = path.join(ps.templatePath, 'iframe.html')
    name = _(u'Soundcloud')

plugin_pool.register_plugin(SoundcloudIframePlugin)


class IframePlugin(CMSPluginBase):
    model = Iframe
    module = ps.module
    render_template = path.join(ps.templatePath, 'iframe.html')
    name = _(u'Media Embed')

#plugin_pool.register_plugin(IframePlugin)


class BlockquotePlugin(CMSPluginBase):
    model = Blockquote
    module = ps.module
    render_template = path.join(ps.templatePath, 'blockquote.html')
    name = _(u'Zitat')

plugin_pool.register_plugin(BlockquotePlugin)


class InterviewText(TextPlugin):
    module = ps.module
    render_template = path.join(ps.templatePath, 'interview.html')
    name = _(u'Interview')

plugin_pool.register_plugin(InterviewText)


class ZksText(TextPlugin):
    module = ps.module
    render_template = path.join(ps.templatePath, 'text.html')
    name = _(u'Text')

plugin_pool.register_plugin(ZksText)


class SliderPlugin(CMSPluginBase):
    module = ps.module
    model = Slider
    name = _(u'Slider')
    render_template = path.join(ps.templatePath, 'slider.html')
    allow_children = True
    child_classes = ["SliderItemPlugin"]

plugin_pool.register_plugin(SliderPlugin)


class SliderItemPlugin(CMSPluginBase):
    module = ps.module
    model = SliderItem
    name = _(u'Bild')
    render_template = path.join(ps.templatePath, 'slider-item.html')

plugin_pool.register_plugin(SliderItemPlugin)


class InternalLinkBoxPlugin(CMSPluginBase):
    module = ps.module
    model = InternalLinkBox
    name = _(u'Interesting (Link-Box)')
    child_classes = ['InternalLinkPlugin']
    allow_children = True
    render_template = path.join(ps.templatePath, 'internal_link_box.html')

plugin_pool.register_plugin(InternalLinkBoxPlugin)


class ExternalLinkBoxPlugin(CMSPluginBase):
    module = ps.module
    model = ExternalLinkBox
    name = _(u'Link zum Artikel (Link-Box)')
    render_template = path.join(ps.templatePath, 'external_link_box.html')
    allow_children = True
    child_classes = ['ExternalLinkPlugin']

plugin_pool.register_plugin(ExternalLinkBoxPlugin)


class ExternalLinkPlugin(CMSPluginBase):
    module = ps.module
    model = ExternalLink
    name = _(u'externer Link')
    render_template = path.join(ps.templatePath, 'link.html')

plugin_pool.register_plugin(ExternalLinkPlugin)


class InternalLinkPlugin(CMSPluginBase):
    module = ps.module
    model = InternalLink
    name = _(u'Interner Link')
    render_template = path.join(ps.templatePath, 'link.html')

plugin_pool.register_plugin(InternalLinkPlugin)

'''class DefaultPlugin(TextPlugin):
    name = _(u"Text")
    module = ps.module
    model = SfbDefaultText
    render_template = path.join(ps.templatePath, "text.html")

    def render(self, context, instance, placeholder):
        context['instance'] = instance
        return context
        '''