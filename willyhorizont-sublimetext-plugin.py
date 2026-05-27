import sublime
import sublime_plugin


def create_logger(show_log=False):
    if not show_log:
        return lambda _: None
    return print


def clear_console():
    settings = sublime.load_settings("Preferences.sublime-settings")
    scrollback = settings.get("console_max_history_lines")
    settings.set("console_max_history_lines", 1)
    print("")
    settings.set("console_max_history_lines", scrollback)


def vscode_duplicate_selected_up(self, edit):
    selections = list(self.view.sel())

    for region in reversed(selections):
        if region.empty():
            line = self.view.line(region)
            text = self.view.substr(line) + "\n"
            self.view.insert(edit, line.begin(), text)
        else:
            text = self.view.substr(region)
            self.view.insert(edit, region.begin(), text)


def vscode_duplicate_selected_down(self, edit):
    selections = list(self.view.sel())

    for region in reversed(selections):
        if region.empty():
            line = self.view.line(region)
            text = "\n" + self.view.substr(line)
            self.view.insert(edit, line.end(), text)
        else:
            text = self.view.substr(region)
            self.view.insert(edit, region.end(), text)


def vscode_ctrl_shift_up_or_down(self, edit, forward=True, show_log=False):
    log = create_logger(show_log)
    self.view.window().run_command("willyhorizont_utils", {"action": "clear_console"})

    settings = self.view.settings()
    target_prev_col = settings.get("target_prev_col")
    log(f"target_prev_col={target_prev_col}")

    current_selections = list(self.view.sel())

    if not current_selections:
        return

    log(f"current_selections={current_selections}")
    log(f"current_selections[-1]={current_selections[-1]}")
    log(f"current_selections[0]={current_selections[0]}")

    current_selections_text = "".join([self.view.substr(region) for region in current_selections])
    log(f"current_selections_text=\"\"\"{current_selections_text}\"\"\"")
    current_selections_text_length = len(current_selections_text)
    log(f"current_selections_text_length={current_selections_text_length}")

    current_selection = current_selections[-1] if forward else current_selections[0]
    log(f"current_selection={current_selection}")
    log(f"current_selection.a={current_selection.a}")
    log(f"current_selection.b={current_selection.b}")

    current_row, current_col = self.view.rowcol(current_selection.b)
    current_row += 1
    current_col += 1
    log(f"current_row={current_row}")
    log(f"current_col={current_col}")

    target_row = (current_row + (1 if forward else -1))
    log(f"target_row={target_row}")
    target_col = current_col
    log(f"target_col={target_col}")

    target_text_point = self.view.text_point((target_row - 1), 0)
    log(f"target_text_point={target_text_point}")
    target_line = self.view.line(target_text_point)
    log(f"target_line={target_line}")
    target_line_text = self.view.substr(target_line)
    log(f"target_line_tex=\"\"\"{target_line_text}\"\"\"")
    target_line_length = target_line.size()
    log(f"target_line_length={target_line_length}")

    new_target_text_point = 0
    log(f"new_target_text_point_init={new_target_text_point}, target_col={target_col}")
    if (target_col > target_line_length):
        new_target_text_point = (target_text_point + target_line_length)
        log(f"new_target_text_point_if={new_target_text_point}")
        if (target_line_length > 0):
            settings.set("target_prev_col", target_col)
            log(f"target_prev_col set to {target_col}")
    else:
        new_target_text_point = (target_text_point + (target_col - 1))
        if target_prev_col:
            target_text_point = self.view.text_point((target_row - 1), target_prev_col)
            new_target_text_point = (target_text_point - 1)
        log(f"new_target_text_point_else={new_target_text_point}, target_col={target_col}")
        settings.set("target_prev_col", None)
        log(f"target_prev_col set to {None}")
    log(f"new_target_text_point_final={new_target_text_point}")

    target_text_point = new_target_text_point
    log(f"target_text_point={target_text_point}")
    target_region = sublime.Region(target_text_point, (target_text_point + (target_line_length - (target_col - 1))))
    log(f"target_region={target_region}")
    target_region_text = self.view.substr(target_region)
    log(f"target_region_text=\"\"\"{target_region_text}\"\"\"")
    target_region_length = target_region.size()
    log(f"target_region_length={target_region_length}")

    new_region_text_point = new_target_text_point
    log(f"new_region_text_point={new_region_text_point}")
    new_region = sublime.Region(current_selection.a, new_target_text_point)
    log(f"new_region={new_region}")
    new_region_text = self.view.substr(new_region)
    log(f"new_region_text=\"\"\"{new_region_text}\"\"\"")
    new_region_length = new_region.size()
    log(f"new_region_length={new_region_length}")

    if forward:
        current_selections[-1] = new_region
    else:
        current_selections[0] = new_region
    
    self.view.sel().clear()
    self.view.sel().add_all(current_selections)
    self.view.show(new_region)


class WillyhorizontKeyboardShortcutCommand(sublime_plugin.TextCommand):
    def run(self, edit, *args, action="default", **kwargs):
        """
        usage example:
        { "keys": ["shift+alt+up"], "command": "willyhorizont_keyboard_shortcut", "args": {"action": "vscode_duplicate_selected_up"}  },
        """
        if action == "vscode_duplicate_selected_up":
            vscode_duplicate_selected_up(self, edit)
            return
        if action == "vscode_duplicate_selected_down":
            vscode_duplicate_selected_down(self, edit)
            return
        if action == "vscode_ctrl_shift_up_or_down":
            vscode_ctrl_shift_up_or_down(self, edit, forward=kwargs.get("forward"))
            return
        if action == "do_nothing":
            return


class WillyhorizontUtilsCommand(sublime_plugin.ApplicationCommand):
    def run(self, *args, action="default", **kwargs):
        """
        usage example:
        self.view.window().run_command("willyhorizont_utils", {"action": "clear_console"})
        """
        if action == "clear_console":
            clear_console()
            return
        if action == "do_nothing":
            return

