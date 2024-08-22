from aqt.qt import *
from .load_yourei import get_sentence
from aqt import mw
from aqt.editor import Editor
import time
from PyQt6.QtCore import pyqtSlot, Qt
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QTextEdit, QPushButton, QInputDialog, QListWidget, \
    QListWidgetItem
from PyQt6.QtGui import QFont
from bs4 import BeautifulSoup

class HTMLListWidgetItem(QWidget):
    def __init__(self, html_content, parent=None):
        super().__init__(parent)

        # Create a horizontal layout
        layout = QHBoxLayout()

        # Set margins and spacing (values in pixels)
        layout.setContentsMargins(1, 0, 1, 0)  # Adjust this to control the padding (left, top, right, bottom)
        layout.setSpacing(0)  # Adjust this to control spacing between widgets

        # Add a QLabel that supports HTML and store it as an instance attribute
        self.label = QLabel()
        self.label.setText(html_content)
        self.label.setTextFormat(Qt.TextFormat.RichText)
        self.label.setFont(QFont("Meiryo", 14))  # Use a common Japanese font, 14 is the font size
        self.label.setWordWrap(True)  # Allow text to wrap if it's too long
        layout.addWidget(self.label)

        # Set the layout for the custom widget
        self.setLayout(layout)

        # Install an event filter to detect hover events
        self.installEventFilter(self)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.Enter:
            # Change background color on hover
            self.setStyleSheet("background-color: lightblue;")
        elif event.type() == QEvent.Type.Leave:
            # Reset background color when not hovering
            self.setStyleSheet("")
        return super().eventFilter(obj, event)

class MyCustomWindow(QDialog):
    def __init__(self, selected_text, loadstate=0, parent=None, geometry=None):
        super().__init__(parent)
        self.setWindowTitle("Example Sentences")
        self.resize(700, 400)

        self.setWindowFlags(Qt.WindowType.Window)

        if geometry:
            self.setGeometry(geometry)

        layout = QVBoxLayout()

        label = QLabel("Example Sentences")
        label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(label)

        # Add a dropdown to select fields
        self.field_dropdown = QComboBox()
        layout.addWidget(self.field_dropdown)

        # Populate the dropdown with fields from the current note type
        self.populate_field_dropdown()

        self.sentence_list = QListWidget()
        layout.addWidget(self.sentence_list)

        font = QFont("Meiryo", 14)
        self.sentence_list.setFont(font)

        if selected_text is None or selected_text == '':
            button = QPushButton("No term selected")
            button.clicked.connect(self.on_button_clicked_search)
            layout.addWidget(button)
        else:
            button = QPushButton(f"Load sentences for {selected_text}")
            button.clicked.connect(lambda: self.on_button_clicked(selected_text))
            layout.addWidget(button)

            buttonr = QPushButton("Search new word")
            buttonr.clicked.connect(self.on_button_clicked_search)
            layout.addWidget(buttonr)

        self.setLayout(layout)

        self.sentence_list.itemDoubleClicked.connect(self.insert_and_close)

        if loadstate == 1:
            self.on_button_clicked(selected_text)

    def populate_field_dropdown(self):
        # Get the current editor's note
        editor = self.parent().editor

        # Add the fields of the current note type to the dropdown
        if editor.note:
            field_names = mw.col.models.fieldNames(editor.note.model())
            self.field_dropdown.addItems(field_names)
        else:
            # If no note is available, handle the situation (e.g., show a message or disable the dropdown)
            self.field_dropdown.addItem("No fields available")
            self.field_dropdown.setEnabled(False)

    def on_button_clicked_search(self):
        # Save current geometry
        current_geometry = self.geometry()

        # Open a dialog box to enter a term
        text, ok = QInputDialog.getText(self, 'No term selected', 'Enter a term:')
        if ok and text:
            # Reload the window with the new selected text
            self.close()
            new_window = MyCustomWindow(text, 1, self.parent(), current_geometry)
            new_window.show()

    def on_button_clicked(self, term):
        # Clear any existing items
        self.sentence_list.clear()

        # Get sentences from the function
        sentences = get_sentence(term)
        if not sentences:
            sentences = ['No sentences found for the selected term.']

        # Add sentences to the list widget
        for sentence in sentences:
            html_content = f'{sentence}'
            item_widget = HTMLListWidgetItem(html_content)

            # Create a QListWidgetItem and set the custom widget
            item = QListWidgetItem()
            item.setSizeHint(item_widget.sizeHint())  # Set the size hint based on the widget
            self.sentence_list.addItem(item)
            self.sentence_list.setItemWidget(item, item_widget)

        # Connect item click event to sentence insertion
        self.sentence_list.itemClicked.connect(self.insert_sentence_into_field)

    def insert_and_close(self, item):
        self.insert_sentence_into_field(item)
        self.close()

    def insert_sentence_into_field(self, item):
        # Get the custom widget associated with the clicked item
        widget = self.sentence_list.itemWidget(item)

        # Extract the plain text from the widget
        html_sentence = widget.label.text()
        soup = BeautifulSoup(html_sentence, "html.parser")
        sentence = soup.get_text()

        # Get the selected field name from the dropdown
        field_name = self.field_dropdown.currentText()

        # Access the editor from the parent window
        editor = self.parent().editor

        if editor and editor.note:
            # Assuming you want to insert the sentence into a field called 'Sentence'

            if field_name in editor.note:
                editor.note[field_name] = sentence
                # Notify the editor that the note has been modified
                editor.loadNote()