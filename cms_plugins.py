# -*- coding: utf-8 -*-
__author__ = 'faebser'

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from django.utils.translation import ugettext_lazy as _
from djangocms_text_ckeditor.cms_plugins import TextPlugin
from django.core.urlresolvers import reverse
from models import *
from os import path
from models import ArticleCategory, ArticleTags, ArticleIntro, ExternalLink, ExternalLinkBox, InternalLink, \
    InternalLinkBox, Ad, Box


class PluginSettings():
    templatePath = path.join("plugins")
    module = u'ZKS'

ps = PluginSettings()


class ArticleIntroPlugin(CMSPluginBase):
    model = ArticleIntro
    module = ps.module
    render_template = path.join(ps.templatePath, 'article_intro.html')
    name = _(u'Blog Intro')

plugin_pool.register_plugin(ArticleIntroPlugin)

'''class DefaultPlugin(TextPlugin):
    name = _(u"Text")
    module = ps.module
    model = SfbDefaultText
    render_template = path.join(ps.templatePath, "text.html")

    def render(self, context, instance, placeholder):
        context['instance'] = instance
        return context
        '''