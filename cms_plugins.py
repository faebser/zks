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
    templatePath = path.join("plugins", "zks")
    templatePathShop = path.join('plugins', 'zks')
    module = u'ZKS'

ps = PluginSettings()

