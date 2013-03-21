import sublime, sublime_plugin
import subprocess, os

class RGrepCommand(sublime_plugin.WindowCommand):
    def run(self):
        self.window.show_input_panel('grep -rnH', '', self.recursive_grep, None, None)

    def output_and_status(commands):
        process = subprocess.Popen(commands, stdout=subprocess.PIPE)
        stdout, stderr = process.communicate()
        status = process.wait()
        return [stdout, status]

    def recursive_grep(self, query):
        base_dir, status = output_and_status(['pwd'])

        if status != 0:
            sublime.message_dialog(base_dir)
            return
        os.chdir(base_dir)

        matches, status = output_and_status(['grep', '-rnH', query])
        if status != 0:
            sublime.message_dialog(matches)
            return

        matches = matches.decode('utf8', 'ignore').split("\n")

        def split(l):
            file_name, line, match = l.split(":", 2)
            return [match.strip(), ":".join([file_name, line])]

        items = map(split, matches)

        def on_done(index):
            if index < 0:
                return

            line = matches[index]
            file_name, line_no, match = line.split(":", 2)
            file_name = os.path.join(base_dir, file_name)
            self.window.open_file(file_name + ':' + line_no, sublime.ENCODED_POSITION)

        self.window.show_quick_panel(items, on_done)
