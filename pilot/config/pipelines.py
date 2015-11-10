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
}

PIPELINE_JS = {
    'main': {
        'source_filenames': ('base/resize.js', 'base/main.js',),
        'output_filename': 'js/main.js',
    },
}