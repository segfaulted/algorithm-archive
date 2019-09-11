from setuptools import setup

setup(
    name='extenions',
    verison='1.0',
    py_modules=['language_switch'],
    entry_points = {
        'markdown.extensions': [
            'language_switch = extensions.markdown.language_switch:LanguageSwitchExtension' 
        ],
        'mkdocs.plugins': [
            'codeimport = extensions.mkdocs.code_import:CodeImportPlugin'
        ]
    }
)