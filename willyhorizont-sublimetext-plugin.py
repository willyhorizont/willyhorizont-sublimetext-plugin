import sublime
import sublime_plugin
import sys
from platform import python_version


def create_logger(show_log=False):
    if not show_log:
        return lambda _: None
    return print


def print_python_version():
    print("# python version")
    print("sys.version:")
    print(sys.version)
    print("sys.version_info:")
    print(sys.version_info)
    print("python_version():")
    print(python_version())


def toggle_log_commands():
    settings = sublime.load_settings("WillyhorizontUtils.sublime-settings")
    current_state = settings.get("log_commands_enabled", False)
    new_state = not current_state
    settings.set("log_commands_enabled", new_state)
    sublime.save_settings("WillyhorizontUtils.sublime-settings")
    sublime.log_commands(new_state)


def toggle_log_input():
    settings = sublime.load_settings("WillyhorizontUtils.sublime-settings")
    current_state = settings.get("log_input_enabled", False)
    new_state = not current_state
    settings.set("log_input_enabled", new_state)
    sublime.save_settings("WillyhorizontUtils.sublime-settings")
    sublime.log_input(new_state)


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


def vscode_ctrl_shift_up_or_down(self, edit, forward=True, show_log=True):
    log = create_logger(show_log)
    self.view.window().run_command("willyhorizont_utils", {"action": "clear_console"})

    settings = self.view.settings()
    col = settings.get("col")
    log(f"col = {col}")

    current_selections = list(self.view.sel())

    if not current_selections:
        return

    # log(f"current_selections = {current_selections}")
    # log(f"current_selections[-1] = {current_selections[-1]}")
    # log(f"current_selections[0] = {current_selections[0]}")

    current_selection = current_selections[-1] if forward else current_selections[0]
    log(f"current_selection = {current_selection}")
    # log(f"current_selection.a = {current_selection.a}")
    # log(f"current_selection.b = {current_selection.b}")

    current_selection_text = "".join([self.view.substr(region) for region in current_selections])
    # log(f"current_selection_text = \"\"\"{current_selection_text}\"\"\"")
    current_selection_length = len(current_selection_text)
    log(f"current_selection_length = {current_selection_length}")

    current_row, current_col = self.view.rowcol(current_selection.b)
    current_row += 1
    current_col += 1
    log(f"current_row = {current_row}, current_col = {current_col}")

    target_row = (current_row + (1 if forward else -1))
    target_col = current_col
    if not col:
        settings.set("col", target_col)
        log(f"col={target_col}, message=\"just setting\"")
    else:
        log(f"col={col}, message=\"not setting\"")
    log(f"target_row = {target_row}, target_col = {target_col}")

    target_row_line_text_point = self.view.text_point((target_row - 1), 0)
    log(f"target_row_line_text_point = {target_row_line_text_point}")
    target_row_line = self.view.line(target_row_line_text_point)
    log(f"target_row_line = {target_row_line}")
    # target_row_line_text = self.view.substr(target_row_line)
    # log(f"target_row_line_text = \"\"\"{target_row_line_text}\"\"\"")
    target_row_line_length = target_row_line.size()
    log(f"target_row_line_length = {target_row_line_length}")

    target_col = (expected_or_stored_col if ((expected_or_stored_col := settings.get("col", target_col)) <= target_row_line_length) else target_row_line_length)
    log(f"target_col = {target_col}")

    target_text_point = (target_row_line_text_point + (target_col - 1))
    log(f"target_text_point = {target_text_point}")

    # target_line_region = sublime.Region(target_text_point, (target_text_point + (target_row_line_length - (target_col - 1))))
    # log(f"target_line_region = {target_line_region}")
    # target_line_region_text = self.view.substr(target_line_region)
    # log(f"target_line_region_text = \"\"\"{target_line_region_text}\"\"\"")
    # target_line_region_length = target_line_region.size()
    # log(f"target_line_region_length = {target_line_region_length}")

    new_region = sublime.Region(current_selection.a, target_text_point)
    log(f"new_region = {new_region}")
    # new_region_text = self.view.substr(new_region)
    # log(f"new_region_text = \"\"\"{new_region_text}\"\"\"")
    # new_region_length = new_region.size()
    # log(f"new_region_length = {new_region_length}")

    if forward:
        current_selections[-1] = new_region
    else:
        current_selections[0] = new_region
    
    self.view.sel().clear()
    self.view.sel().add_all(current_selections)
    self.view.show(new_region)


def unset_state_column(view):
    if not view.settings().has("col"):
        return
    view.settings().erase("col")
    print("state \"col\" erased.")


class WillyhorizontStateResetListener(sublime_plugin.EventListener):
    def on_deactivated(self, view):
        unset_state_column(view)
    def on_text_command(self, view, command_name, args):
        if (command_name == "move"):
            if (args.get("by") == "characters"):
                unset_state_column(view)
                return None
            if args.get("by") == "lines":
                unset_state_column(view)
                return None
        if command_name == "drag_select":
            unset_state_column(view)
            return None
        # if command_name in ["undo", "soft_undo", "single_selection"]:
        #     unset_state_column(view)
        return None


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
        if action == "print_python_version":
            print_python_version()
            return
        if action == "toggle_log_commands":
            toggle_log_commands()
            return
        if action == "toggle_log_input":
            toggle_log_input()
            return
        if action == "do_nothing":
            return
    def is_checked(self, action="default", **kwargs):
        if action == "toggle_log_commands":
            settings = sublime.load_settings("WillyhorizontUtils.sublime-settings")
            return settings.get("log_commands_enabled", False)
        if action == "toggle_log_input":
            settings = sublime.load_settings("WillyhorizontUtils.sublime-settings")
            return settings.get("log_input_enabled", False)
        return False

