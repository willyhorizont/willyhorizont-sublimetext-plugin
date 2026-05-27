import sublime
import sublime_plugin

class VscodeDuplicateSelectedDownCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        selections = list(self.view.sel())

        for region in reversed(selections):
            if region.empty():
                line = self.view.line(region)
                print(line)
                text = "\n" + self.view.substr(line)
                self.view.insert(edit, line.end(), text)
            else:
                text = self.view.substr(region)
                self.view.insert(edit, region.end(), text)
