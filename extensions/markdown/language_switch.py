import re
from os import path
from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor


class LanguageSwitchExtension(Extension):
    def extendMarkdown(self, md, md_globals):
        md.registerExtension(self)
        md.preprocessors.register(
            LanguageSwitchBlockPreprocessor(md), "language_switch_block", 999
        )


class LanguageSwitchBlockPreprocessor(Preprocessor):
    method_pattern = re.compile(r'{%\s?method\s?%}(?P<content>.*?){%\s?endmethod\s?%}', re.MULTILINE | re.DOTALL | re.VERBOSE | re.UNICODE)
    sample_pattern = re.compile(r'{%\s?sample\s+lang="(?P<lang>.*?)"\s?%}(?P<content>.*?){%\s?endsample\s?%}', re.MULTILINE | re.DOTALL | re.VERBOSE | re.UNICODE)
    filename_pattern = re.compile(r'data-filename="(.*?)"')
    block_wrap = '''<div class="method_block">
    <div class="header">
        <select>
            %s
        </select>
    </div>
    
    %s
    </div>'''
    sample_wrap = '<div class="code_sample code_sample_lang_%s hidden">%s\n%s</div>'
    def __init__(self, md):
        super().__init__(md)

    def run(self, lines):
        text = "\n".join(lines)
        
        while 1:
            m = self.method_pattern.search(text)
            if m:
                
                if m.group("content"):
                    content = m.group('content')
                    langs, content = self.process_content(content)
                
                option_list = "".join('<option value="%s">%s</option>' % (lang, lang) for lang in langs)
                content = self.block_wrap % (option_list, content)
                # placeholder = self.md.htmlStash.store(content)
                text = "%s\n%s\n%s" % (text[:m.start()], content, text[m.end():])
            else:
                break

        return text.split("\n")

    def process_content(self, text):
        langs = []
        while 1:
            m = self.sample_pattern.search(text)
            
            if m:
                content = m.group('content')
                lang = m.group('lang')
                langs.append(lang)

                filenames = self.filename_pattern.findall(content)
                filename_list = " ".join('<a href="#" data-target="%s">%s</a>' % (file, path.basename(file)) for file in filenames)
                header = '<div class="header">%s</div>' % filename_list
                content = self.sample_wrap % (lang, header, content)
                # placeholder = self.md.htmlStash.store(content)
                text = '''\n%s\n%s\n%s''' % (text[: m.start()], content, text[m.end():])
            else:
                break
        return (langs, text)
        
def makeExtension(**kwargs):
    return LanguageSwitchExtension(**kwargs)


