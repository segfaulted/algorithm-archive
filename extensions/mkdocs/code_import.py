import re
from os import path
import io
import logging
from mkdocs.plugins import BasePlugin

log = logging.getLogger(__name__)


class CodeImportPlugin(BasePlugin):
    import_pattern = re.compile(
        r"\[import(:(?P<start>[0-9]+)-(?P<end>[0-9]+))?,\slang(:|=)\"(?P<lang>[a-zA-Z0-9\-_]*)\"\]\((?P<file>[a-zA-Z0-9\.\+\_\-/]*?)\)",
        re.DOTALL | re.UNICODE,
    )

    def on_page_markdown(self, markdown, page, config, **kwargs):
        while 1:
            m = self.import_pattern.search(markdown)
            if m:
                file = m.group("file")
                lang = m.group("lang")
                code = ""
                try:
                    dir = path.dirname(page.file.abs_src_path)
                    with io.open(
                        path.join(dir, file), "r", encoding="utf-8-sig", errors="strict"
                    ) as f:
                        code = f.readlines()

                except IOError:
                    log.error("File not found: {}".format(path.join(dir, file)))
                    raise
                except ValueError:
                    log.error(
                        "Encoding error reading file: {}".format(path.join(dir, file))
                    )
                    raise
                hl_lines = ''
                if m.group("start"):
                    start = int(m.group("start"))
                    end = int(m.group("end")) - 1
                    
                    #hl_lines = 'hl_lines="%s"' % ' '.join(str(x) for x in range(start, end))
                    code = code[start:end]
                    remove = None

                    for line in code:
                        spaces = len(line) - len(line.lstrip(' \t'))
                        if remove is None and len(line) > 0 and spaces > 0:
                            remove = spaces
                        elif remove is not None and len(line) > 0 and spaces < remove:
                            spaces = remove
                    
                    for idx, line in enumerate(code):
                        code[idx] = line[remove:]

                markdown = '''%s
<div class="code_import" data-filename="%s">
``` %s %s
%s
```
</div>
%s''' % (
                    markdown[: m.start()],
                    file,
                    lang,
                    hl_lines,
                    "".join(code),
                    markdown[m.end() :],
                )
            else:
                break

        return markdown
