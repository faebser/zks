import os
gettext = lambda s: s


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Application definition


CMS_LANGUAGES = {
    ## Customize this
    'default': {
        'public': True,
        'hide_untranslated': False,
        'redirect_on_fallback': True,
    },
    1: [
        {
            'public': True,
            'code': 'de',
            'hide_untranslated': False,
            'name': gettext('de'),
            'redirect_on_fallback': True,
        },
        {
            'public': True,
            'code': 'en',
            'hide_untranslated': False,
            'name': gettext('en'),
            'redirect_on_fallback': True,
        },
    ],
}

CMS_TEMPLATES = (
    ## Customize this
    ('fullwidth.html', 'Fullwidth'),
    ('sidebar_left.html', 'Sidebar Left'),
    ('sidebar_right.html', 'Sidebar Right'),
    ('index.html', 'zks home'),
    ('article_detail.html', 'zks blog detail')
)

LANGUAGES = (
    ## Customize this
    ('de', gettext('de')),
    ('en', gettext('en')),
)


CMS_PERMISSION = True

CMS_PLACEHOLDER_CONF = {
    'blog': {
        'plugins': ['BlogListWithPaginationPlugin'],
        'name': u'Blog Liste',
        'limits': {
            'global': 1
        }
    },
    'intro': {
        'plugins': ['ArticleIntroPlugin'],
        'name': u'Blog Intro'
    },
    'content': {
        'name': u'Inhalt',
        'plugins': ['YoutubeIframePlugin', 'MixcloudIframePlugin', 'SoundcloudIframePlugin', 'BlockquotePlugin',
                    'InterviewText', 'ZksText', 'SliderPlugin', 'SliderItemPlugin']
    },
    'internal-links': {
        'name': u'Interne Links',
        'plugins': ['InternalLinkBoxPlugin'],
        'limits': {
            'global': 1
        }
    },
    'external-links': {
        'name': u'Externe Links',
        'plugins': ['ExternalLinkBoxPlugin'],
        'limits': {
            'global': 1
        }
    },
    'ads': {
        'name': u'Werbung',
        'plugins': ['']
    },
    'footnotes': {
        'name': u'Fussnoten',
        'plugins': ['']
    }
}


