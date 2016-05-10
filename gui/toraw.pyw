#!/usr/bin/env python
"""
    gui/toraw
    ~~~~~~~~~~~~~~~~~~~~

    Graphical user interface for converting movies to raw files

    :author: Joerg Schnitzbauer, 2015
    :copyright: Copyright (c) 2015 Jungmann Lab, Max Planck Institute of Biochemistry
"""

import sys
import os
import os.path
from PyQt4 import QtCore, QtGui
import traceback


_this_file = os.path.abspath(__file__)
_this_directory = os.path.dirname(_this_file)
_parent_directory = os.path.dirname(_this_directory)
sys.path.insert(0, _parent_directory)    # We want to use the local picasso instead the system-wide
from picasso import io


class TextEdit(QtGui.QTextEdit):

    def __init__(self, parent=None):
        super().__init__(parent)
        # self.setAcceptDrops(True)

    def canInsertFromMimeData(self, source):
        if source.hasUrls():
            return True
        return False

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        paths = [url.toLocalFile() for url in urls]
        valid_paths = []
        for path in paths:
            base, extension = os.path.splitext(path)
            if extension.lower() in ['.tif', '.tiff']:
                valid_paths.append(path)
            for root, dirs, files in os.walk(path):
                for name in files:
                    candidate = os.path.join(root, name)
                    base, extension = os.path.splitext(candidate)
                    if extension.lower() in ['.tif', '.tiff']:
                        valid_paths.append(candidate)
        self.set_paths(valid_paths)

    def set_paths(self, paths):
        for path in paths:
            self.append(path)


class Window(QtGui.QWidget):

    def __init__(self):
        super().__init__()
        # Init GUI
        self.setWindowTitle('Picasso: ToRaw')
        self.resize(768, 512)
        this_directory = os.path.dirname(os.path.realpath(__file__))
        icon_path = os.path.join(this_directory, 'toraw.ico')
        icon = QtGui.QIcon(icon_path)
        self.setWindowIcon(icon)
        vbox = QtGui.QVBoxLayout()
        self.setLayout(vbox)
        vbox.addWidget(QtGui.QLabel('Files:'))
        self.path_edit = TextEdit()
        vbox.addWidget(self.path_edit)
        hbox = QtGui.QHBoxLayout()
        vbox.addLayout(hbox)
        self.browse_button = QtGui.QPushButton('Browse')
        self.browse_button.clicked.connect(self.browse)
        hbox.addWidget(self.browse_button)
        hbox.addStretch(1)
        to_raw_button = QtGui.QPushButton('To raw')
        to_raw_button.clicked.connect(self.to_raw)
        hbox.addWidget(to_raw_button)

    def browse(self):
        paths = QtGui.QFileDialog.getOpenFileNames(self, 'Open files to convert', filter='*.tif; **.tiff')
        self.path_edit.set_paths(paths)

    def to_raw(self):
        text = self.path_edit.toPlainText()
        paths = text.splitlines()
        movie_groups = io.get_movie_groups(paths)
        n_movies = len(movie_groups)
        if n_movies == 1:
            text = 'Converting 1 movie...'
        else:
            text = 'Converting {} movies...'.format(n_movies)
        self.progress_dialog = QtGui.QProgressDialog(text, 'Cancel', 0, n_movies, self)
        progress_bar = QtGui.QProgressBar(self.progress_dialog)
        progress_bar.setTextVisible(False)
        self.progress_dialog.setBar(progress_bar)
        self.progress_dialog.setMaximum(n_movies)
        self.progress_dialog.setWindowTitle('Picasso: ToRaw')
        self.progress_dialog.setWindowModality(QtCore.Qt.WindowModal)
        self.progress_dialog.canceled.connect(self.cancel)
        self.progress_dialog.closeEvent = self.cancel
        self.worker = Worker(movie_groups)
        self.worker.progressMade.connect(self.update_progress)
        self.worker.finished.connect(self.on_finished)
        self.worker.start()
        self.progress_dialog.show()

    def cancel(self, event=None):
        self.worker.terminate()

    def update_progress(self, n_done):
        self.progress_dialog.setValue(n_done)

    def on_finished(self, done):
        self.progress_dialog.close()
        QtGui.QMessageBox.information(self, 'Picasso: ToRaw', 'Conversion complete.')


class Worker(QtCore.QThread):

    progressMade = QtCore.pyqtSignal(int)
    finished = QtCore.pyqtSignal(int)
    interrupted = QtCore.pyqtSignal()

    def __init__(self, movie_groups):
        super().__init__()
        self.movie_groups = movie_groups

    def run(self):
        for i, (basename, paths) in enumerate(self.movie_groups.items()):
            io.to_raw_combined(basename, paths)
            self.progressMade.emit(i+1)
        self.finished.emit(i)


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = Window()
    window.show()

    def excepthook(type, value, tback):
        message = ''.join(traceback.format_exception(type, value, tback))
        errorbox = QtGui.QMessageBox.critical(window, 'An error occured', message)
        errorbox.exec_()
        sys.__excepthook__(type, value, tback)
    sys.excepthook = excepthook

    sys.exit(app.exec_())
