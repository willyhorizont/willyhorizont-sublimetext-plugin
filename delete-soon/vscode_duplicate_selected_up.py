import sublime
import sublime_plugin

class VscodeDuplicateSelectedUpCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        selections = list(self.view.sel())

        for region in reversed(selections):
            if region.empty():
                line = self.view.line(region)
                text = self.view.substr(line) + "\n"
                self.view.insert(edit, line.begin(), text)
            else:
                text = self.view.substr(region)
                self.view.insert(edit, region.begin(), text)