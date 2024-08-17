from aqt import mw
from aqt.qt import QAction
from anki.hooks import addHook
from aqt.editor import Editor
from PyQt6.QtGui import QKeySequence
from .display_window import MyCustomWindow
import os

def open_custom_window(editor):
    selected_text = editor.web.selectedText()
    if selected_text:
        dialog = MyCustomWindow(selected_text, 1, editor.parentWindow)  # mw
        dialog.show()
    else:
        dialog = MyCustomWindow(selected_text, 0, editor.parentWindow)  # mw
        dialog.show()

def addYourei(buttons, editor):
    def on_action_triggered():
        open_custom_window(editor)

    editor._links['open_custom_window'] = open_custom_window

    action = QAction("youreimenu", editor.parentWindow)
    action.setShortcut(QKeySequence("Ctrl+Y"))
    action.triggered.connect(on_action_triggered)
    editor.parentWindow.addAction(action)

    icon_path = os.path.join(os.path.dirname(__file__), 'favicon.ico')

    return buttons + [editor._addButton(
        icon_path,  # Replace with the path to your icon if you have one
        "open_custom_window",  # Link name
        "Load Example Sentences"  # Tooltip
    )]

addHook("setupEditorButtons", addYourei)