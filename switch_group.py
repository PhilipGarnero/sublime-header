import sublime, sublime_plugin

class SwitchGroupCommand(sublime_plugin.WindowCommand):
    def run(self):
        i = self.window.num_groups()
        j = self.window.active_group()
        j = (j + 1) % i
        self.window.run_command("focus_group", { "group": j })