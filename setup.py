from distutils.core import setup,Extension

module1=Extension( 
    'antichessAI',
    include_dirs=['/usr/local/include'],
    sources=['antichessAImodule.cpp']
)

setup(
    name='antichessAI',
    version='1.0',
    ext_modules=[module1]
)