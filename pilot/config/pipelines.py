PIPELINE_CSS_COMPRESSOR = 'pipeline.compressors.cssmin.CSSMinCompressor'
PIPELINE_COMPILERS = ('pipeline.compilers.sass.SASSCompiler',)


PIPELINE_CSS = {
    'main': {
        'source_filenames': ('base/main.scss',),
        'output_filename': 'css/main.css',
        'extra_context': {
            'media': 'screen,projection',
        },
    },
    'dashboards_play': {
        'source_filenames': ('dashboards/play.scss',),
        'output_filename': 'css/play.css',
        'extra_context': {
            'media': 'screen,projection',
        },
    },
    'error': {
        'source_filenames': ('base/error.scss',),
        'output_filename': 'css/error.css',
        'extra_context': {
            'media': 'screen,projection',
        },
    },
}

PIPELINE_JS = {
    'main': {
        'source_filenames': ('base/resize.js', 'base/main.js', 'base/modal.js',),
        'output_filename': 'js/main.js',
    },
    'visualizations_show': {
        'source_filenames': ('visualizations/schedule.js',),
        'output_filename': 'js/main.js',
    },
}