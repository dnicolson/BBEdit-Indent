import sublime, sublime_plugin

class BbeditIndentCommand(sublime_plugin.TextCommand):
    def run(self, edit, action):
        view = self.view

        settings = view.settings()
        tab_size = int(settings.get('tab_size', 4))
        use_spaces = settings.get('translate_tabs_to_spaces')

        # iterate over selections
        for sel in view.sel():
            points = []

            # iterate over lines
            for line in view.lines(sel):

                # get point at the start of the line
                pt = line.begin()
                char = view.substr(pt)

                # loop through line whitespace
                while char == ' ' or char == '\t':
                    pt += 1
                    char = view.substr(pt)

                # ignore blank lines
                if view.rowcol(pt + 1)[0] != view.rowcol(line.begin())[0]:
                    continue

                points.append(pt)

            pt_count = 0
            for pt in points:
                if action == 'indent':
                    view.insert(edit, pt + pt_count, ' ')
                    # check if last inserted characters can be converted to a tab
                    selected_text = view.substr(sublime.Region(pt + pt_count - (tab_size - 1), pt + pt_count + 1))
                    if not use_spaces and selected_text == ' ' * tab_size:
                        view.replace(edit, sublime.Region(pt + pt_count - (tab_size - 1), pt + pt_count + 1), '\t')
                        pt_count -= tab_size - 1
                    pt_count += 1
                elif action == 'unindent':
                    start = pt - pt_count - 1
                    end = pt - pt_count

                    # continue if point is at the left most position
                    if view.rowcol(end)[1] == 0:
                        continue

                    # remove spaces if available
                    if view.rowcol(start)[0] == view.rowcol(end)[0]:

                        # replace tab with spaces
                        if view.substr(start) == '\t':
                            view.replace(edit, sublime.Region(start, end), ' ' * (tab_size - 1))
                            pt_count -= tab_size - 2
                        else:
                            view.erase(edit, sublime.Region(start, end))
                            pt_count += 1

                    # remove one space if available
                    elif view.rowcol(start)[0] == view.rowcol(start + 1)[0]:
                        view.erase(edit, sublime.Region(start, start + 1))
                        pt_count += 1
