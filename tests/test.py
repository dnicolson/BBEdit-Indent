import sublime, sublime_plugin
import sys, os
import unittest

version = sublime.version()

class BbeditIndentWriteBuffer(sublime_plugin.TextCommand):
    def run(self, edit, text=''):
        self.view.replace(edit, sublime.Region(0, self.view.size()), text)

class TestBbeditIndentCommand(unittest.TestCase):
    def setUp(self):
        self.view = sublime.active_window().new_file()
        settings = sublime.load_settings("Preferences.sublime-settings")
        settings.set("close_windows_when_empty", False)

    def tearDown(self):
        if self.view:
            self.view.set_scratch(True)
            self.view.window().focus_view(self.view)
            self.view.window().run_command("close_file")

    def write_text(self, text):
        self.view.run_command('bbedit_indent_write_buffer', {'text': text})

    def get_text(self):
        return self.view.substr(sublime.Region(0, self.view.size()))

    def select_all(self):
        self.view.sel().clear()
        self.view.sel().add(sublime.Region(0, self.view.size()))

    def fixture(self, name):
        fixtures_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fixtures')
        return open(os.path.join(fixtures_path, name), 'r').read()

    def test_indent(self):
        fixture_before = self.fixture('test-1.txt')
        fixture_after = self.fixture('test-1-indent.txt')
        self.write_text(fixture_before)
        self.select_all()
        self.view.run_command('bbedit_indent', {'action': 'indent'})
        text = self.get_text()
        self.assertEqual(fixture_after, text)

    def test_unindent(self):
        fixture_before = self.fixture('test-1.txt')
        fixture_after = self.fixture('test-1-unindent.txt')
        self.write_text(fixture_before)
        self.select_all()
        self.view.run_command('bbedit_indent', {'action': 'unindent'})
        text = self.get_text()
        self.assertEqual(fixture_after, text)

bbedit_indent = sys.modules["BBEdit-Indent.bbedit_indent"]
