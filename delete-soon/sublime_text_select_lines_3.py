import sublime
import sublime_plugin

class SublimeTextSelectLinesCommand(sublime_plugin.TextCommand):
    def run(self, edit, forward=True):
        # print("\n" * 5)
        print("\n" * 100)

        settings = self.view.settings()
        # settings.set("target_prev_col", 0)
        # target_prev_col = settings.get("target_prev_col", 0)

        current_selections = list(self.view.sel())

        if not current_selections:
            return

        print(f"current_selections={current_selections}")
        print(f"current_selections[-1]={current_selections[-1]}")
        print(f"current_selections[0]={current_selections[0]}")

        current_selections_text = "".join([self.view.substr(region) for region in current_selections])
        print(f"current_selections_text: \"\"\"{current_selections_text}\"\"\"")
        current_selections_text_length = len(current_selections_text)
        print(f"current_selections_text_length={current_selections_text_length}")

        current_selection = current_selections[-1] if forward else current_selections[0]
        print(f"current_selection={current_selection}")
        print(f"current_selection.a={current_selection.a}")
        print(f"current_selection.b={current_selection.b}")

        current_row, current_col = self.view.rowcol(current_selection.b)
        current_row += 1
        current_col += 1
        print(f"current_row={current_row}")
        print(f"current_col={current_col}")

        target_row = current_row + (1 if forward else -1)
        print(f"target_row={target_row}")
        target_col = current_col
        print(f"target_col={target_col}")

        target_text_point = self.view.text_point((target_row - 1), 0)
        print(f"target_text_point={target_text_point}")
        target_line = self.view.line(target_text_point)
        print(f"target_line={target_line}")
        target_line_text = self.view.substr(target_line)
        print(f"target_line_text: \"\"\"{target_line_text}\"\"\"")
        target_line_length = target_line.size()
        print(f"target_line_length={target_line_length}")

        new_target_col = (target_text_point + (target_col - 1))
        print(f"new_target_col={new_target_col}")

        target_text_point = new_target_col
        print(f"target_text_point={target_text_point}")
        target_region = sublime.Region(target_text_point, (target_text_point + (target_line_length - (target_col - 1))))
        print(f"target_region={target_region}")
        target_region_text = self.view.substr(target_region)
        print(f"target_region_text: \"\"\"{target_region_text}\"\"\"")
        target_region_length = target_region.size()
        print(f"target_region_length={target_region_length}")

        for region in reversed(current_selections):
            self.view.sel().add(region)
        self.view.sel().add(target_region)

        current_selections = list(self.view.sel())

        current_selections_text = "".join([self.view.substr(region) for region in current_selections])
        print(f"current_selections_text: \"\"\"{current_selections_text}\"\"\"")
        current_selections_text_length = len(current_selections_text)
        print(f"current_selections_text_length={current_selections_text_length}")

        current_selection = current_selections[-1] if forward else current_selections[0]
        print(f"current_selection={current_selection}")
        print(f"current_selection.a={current_selection.a}")
        print(f"current_selection.b={current_selection.b}")

        # current_selections.insert(0, target_region)
        # self.view.sel().add(target_region)

        # self.view.sel().clear()

        # self.view.sel().add(target_region)

        # for region in current_selections:
        #     self.view.sel().add(region)

        new_region_text_point = 342
        print(f"new_region_text_point={new_region_text_point}")
        new_region = sublime.Region(394, 342)
        print(f"new_region={new_region}")
        new_region_text = self.view.substr(new_region)
        print(f"new_region_text: \"\"\"{new_region_text}\"\"\"")
        new_region_length = new_region.size()
        print(f"new_region_length={new_region_length}")

        # self.view.sel().add(region)