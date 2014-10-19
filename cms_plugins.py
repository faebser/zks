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
from models import ArticleCategory, ArticleTags, ArticleIntro, ExternalLink, ExternalLinkBox, InternalLink, \
    InternalLinkBox, Ad, Box, BlogListWithPagination, YouTubeIframe, MixcloudIframe, Blockquote


class PluginSettings():
    templatePath = path.join("plugins")
    module = u'ZKS'

ps = PluginSettings()


class ArticleIntroPlugin(CMSPluginBase):
    model = ArticleIntro
    module = ps.module
    render_template = path.join(ps.templatePath, 'article_header.html')
    name = _(u'Blog Intro')

plugin_pool.register_plugin(ArticleIntroPlugin)


class BlogListWithPaginationPlugin(CMSPluginBase):
    cache = False
    model = BlogListWithPagination
    module = ps.module
    render_template = path.join(ps.templatePath, 'article_list_onecol.html')
    name = _(u'Blog Liste')

    def render(self, context, instance, placeholder):
        context['instance'] = instance
        context['placeholder'] = placeholder
        parameter = context['request'].GET.get('pagination', None)
        total_amount = instance.amount + instance.amountSmall
        objects = None
        get_parameter = None

        # see https://plus.google.com/118309212962987618554/posts/Nc8xQPN9yFy
        # to exclude plugins from list
        objects = ArticleIntro.objects.all().exclude(placeholder__page__publisher_is_draft=False).order_by('date')
        objects = objects.exclude(placeholder__page=None)
        try:
            onecol, twocol, threecol, get_parameter = pagination(objects, parameter, instance.amount, instance.amountSmall, instance.amountThreeCol)
        except ObjectDoesNotExist:
            onecol = None
            twocol = None
            threecol = None

        context.update({
            'onecol': onecol,
            'twocol': twocol,
            'threcol': threecol,
            'pagination': get_parameter
        })

        return context

plugin_pool.register_plugin(BlogListWithPaginationPlugin)


class YoutubeIframePlugin(CMSPluginBase):
    model = YouTubeIframe
    module = ps.module
    render_template = path.join(ps.templatePath, 'iframe.html')
    name = _(u'Youtube Video')


def render(self, context, instance, placeholder):
        context['instance'] = instance
        context['placeholder'] = placeholder

#plugin_pool.register_plugin(YoutubeIframePlugin)


class MixcloudIframePlugin(CMSPluginBase):
    model = MixcloudIframe
    module = ps.module
    render_template = path.join(ps.templatePath, 'iframe.html')
    name = _(u'Mixcloud')

#plugin_pool.register_plugin(MixcloudIframePlugin)


class IframePlugin(CMSPluginBase):
    model = Iframe
    module = ps.module
    render_template = path.join(ps.templatePath, 'iframe.html')
    name = _(u'Media Embed')

plugin_pool.register_plugin(IframePlugin)


class BlockquotePlugin(CMSPluginBase):
    model = Blockquote
    module = ps.module
    render_template = path.join(ps.templatePath, 'blockquote.html')
    name = _(u'Zitat')

plugin_pool.register_plugin(BlockquotePlugin)

'''class DefaultPlugin(TextPlugin):
    name = _(u"Text")
    module = ps.module
    model = SfbDefaultText
    render_template = path.join(ps.templatePath, "text.html")

    def render(self, context, instance, placeholder):
        context['instance'] = instance
        return context
        '''