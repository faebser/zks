# -*- coding: utf-8 -*-
__author__ = 'faebser'

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from django.utils.translation import ugettext_lazy as _
from djangocms_text_ckeditor.cms_plugins import TextPlugin
from django.core.urlresolvers import reverse
from models import *
from os import path
from author_and_tags.views import pagination
from models import ArticleCategory, ArticleTags, ArticleIntro, ExternalLink, ExternalLinkBox, InternalLink, \
    InternalLinkBox, Ad, Box, BlogListWithPagination


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
    render_template = path.join(ps.templatePath, 'article_list.html')
    name = _(u'Blog Liste')

    def render(self, context, instance, placeholder):
        context['instance'] = instance
        context['placeholder'] = placeholder
        parameter = context['request'].GET.get('pagination', None)
        objects = None
        get_parameter = None

        # see https://plus.google.com/118309212962987618554/posts/Nc8xQPN9yFy
        # to exclude plugins from list
        objects = ArticleIntro.objects.all().exclude(placeholder__page__publisher_is_draft=False).order_by('date')
        objects, get_parameter = pagination(objects, parameter, instance.amount)
        context.update({
            'articles': objects,
            'pagination': get_parameter
        })

        return context


plugin_pool.register_plugin(BlogListWithPaginationPlugin)

'''class DefaultPlugin(TextPlugin):
    name = _(u"Text")
    module = ps.module
    model = SfbDefaultText
    render_template = path.join(ps.templatePath, "text.html")

    def render(self, context, instance, placeholder):
        context['instance'] = instance
        return context
        '''