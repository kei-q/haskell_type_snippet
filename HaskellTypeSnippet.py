import sublime, sublime_plugin
import re

# これは何？
# ==========
# Haskellの型宣言書くのをサポートするplugin
#
# example
# ==========
# solve siis<Tab>
# で次のように展開される
# 同じalphabetを入力したところはsnippetで同時に編集される
# solve :: type1 -> type2 -> type2 -> type1
# solve = undefined
#
# あとはsublime textのsnippet機能と同様に書く。
#
# settings
# =============
# keybindingsに以下を追加
#    { "keys": ["shift+tab"], "command": "haskell_type_snippet", "context":
#        [
#            { "key": "selector", "operator": "equal", "operand": "source.haskell", "match_all": true },
#        ]
#    },
#


class HaskellTypeSnippetCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    view = self.view
    region = view.sel()[0]
    line = view.substr(view.line(region))
    pats = re.split(r"\s+", line)

    if len(pats) == 2:
      # pats[1]を位置文字ずつ分割
      keys = re.findall(r".", pats[1])

      # 引数高知素
      i = 1
      dict = {}
      types = []
      for key in keys:
        if key not in dict:
          dict[key] = i
          i += 1
        s = str(dict[key])
        types += ["${" + s + ":type" + s + "}"]

      # replace
      undef = "${" + str(i) + ":undefined}"
      ret = "{0} :: {1}\n{0} = {2}".format(pats[0], " -> ".join(types), undef)
      view.replace(edit, view.line(region), "")
      view.run_command('insert_snippet', {"contents": ret})
