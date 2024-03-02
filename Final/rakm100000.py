import sys
import typing
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QWidget, QLabel, QCheckBox
from PyQt5.uic import loadUiType
import urllib.request
from pyqtgraph.Qt import QtCore,QtGui
import numpy as np
import pyqtgraph as pg 
import pandas as pd
import os
from PyQt5.QtWidgets import QMessageBox
from os import path
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPen
FORM_CLASS, _ = loadUiType(path.join(path.dirname(__file__), "test1.ui"))

class Signal:
    def __init__(self, name, x_data, y_data, color=pg.mkColor('b'), label=None, visible=True):
        self.name = name
        self.x_data = x_data
        self.y_data = y_data
        self.color = color
        self.label = label if label else name
        self.visible = visible
        self.curve_plot1 = None
        self.curve_plot2 = None
        self.data_line = None

class MainApp(QMainWindow, FORM_CLASS):
    def __init__(self, parent=None):
        super(MainApp, self).__init__(parent)
        self.setupUi(self)
        self.x1 = []  # Replace with your data
        self.y1 = []  # Replace with your data
        self.speed = 1  # Adjust as needed
        self.j1 = 0
        self.i1 = 0
        self.k = 0
        self.Listx1 = []
        self.Listy1 = []
        self.data_line1 = None
        self.hide1 = False  # Add this line to define self.h
        self.is_paused = False  # Initialize is_paused attribute
        self.play_pause_button = self.play_pause_v1
        self.play_pause_button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))  
        self.play_pause_button.clicked.connect(self.toggle_play_pause)
        self.replay_button = self.replay_v1
        self.replay_button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.replay_button.clicked.connect(self.replay_signal)
        self.zoom_in_v1.clicked.connect(lambda: self.zoom_in())
        self.zoom_in_v1.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.zoom_out_v1.clicked.connect(lambda: self.zoom_out())
        self.zoom_out_v1.setCursor(QCursor(QtCore.Qt.PointingHandCursor))

        self.pushButton_move_to_v1.clicked.connect(lambda: self.move_signal(0, 1))
        self.pushButton_move_to_v2.clicked.connect(lambda: self.move_signal(1, 0))

        self.plot_widgets = [self.graphicsView_v1, self.graphicsView_v2]
        self.comboboxes = [self.Signals_v1,self.Signals_v2]
        self.comboboxes[0].currentIndexChanged.connect(lambda index: self.signal_selected(index, 0))
        self.comboboxes[1].currentIndexChanged.connect(lambda index: self.signal_selected(index, 1))

        self.hide_checkboxes = [self.hide_checkbox_signal_v1, self.hide_checkbox_signal_v2]
        # self.hide_checkbox_signal_v1.stateChanged.connect(lambda state, viewer=0: self.toggle_signal_visibility(state, viewer))
        # self.hide_checkbox_signal_v2.stateChanged.connect(lambda state, viewer=1: self.toggle_signal_visibility(state, viewer))

        self.open_viewer_1.triggered.connect(lambda: self.load(0,0))
        self.open_viewer_2.triggered.connect(lambda: self.load(1,1))
        self.current_signal_v1 = None
        self.current_signal_v2 = None
        # Create attributes to track the currently selected signal for each viewer
        
        self.signals = []
        
        # self.hide_checkbox_signal_v1.setChecked(False)
        # self.hide_checkbox_signal_v2.setChecked(False)
        # self.hide_checkbox_signal_v1.stateChanged.connect(lambda state: self.toggle_signal_visibility(state, 0))        
        # self.hide_checkbox_signal_v2.stateChanged.connect(lambda state: self.toggle_signal_visibility(state, 1))
        # self.hide_checkbox_signal_v1.stateChanged.connect(lambda state, viewer=0: self.toggle_signal_visibility(state, viewer))
        # self.hide_checkbox_signal_v2.stateChanged.connect(lambda state, viewer=1: self.toggle_signal_visibility(state, viewer))
        # self.signal_visibility = {0: True, 1: True}
        self.pushButton_color_v1.clicked.connect(lambda: self.change_color(self.plot_widgets[0]))
        self.pushButton_color_v2.clicked.connect(lambda: self.change_color(self.plot_widgets[1]))        
        self.lineEdit_signal_v1.editingFinished.connect(self.change_label_v1)
        self.lineEdit_signal_v2.editingFinished.connect(self.change_label_v2)
        self.timer = pg.QtCore.QTimer(self)
        self.timer.timeout.connect(self.play_signal)
        self.is_playing = False
        self.play_speed = 100  # Update interval in milliseconds
        self.current_frame = 0
        self.num_frames = 0
        # self.plot = self.graphicsView_v1
        self.selected_viewer = None
        self.selected_signal = None

        # for checkbox in self.hide_checkboxes:
        #     checkbox.stateChanged.connect(self.toggle_signal_visibility)
        # Connect the stateChanged signal for each hide_checkbox_signal to the corresponding viewer

        for i,checkbox in enumerate(self.hide_checkboxes):
            checkbox.stateChanged.connect(lambda state,viewer=i : self.toggle_signal_visibility(viewer))


        for widget in self.plot_widgets:
            self.init_plot(widget)

    def init_plot(self,  plot_widget):
        plot_widget.clear()
        self.plot = plot_widget.getPlotItem()

    # def init_checkboxes(self):
    #     for checkbox in self.hide_checkboxes:
    #         checkbox.setChecked(True)

    def load(self,viewer,combobox):
        # You can continue using the "Add Signal" button to add more signals
        path_info = QFileDialog.getOpenFileName(
            None, "Select a signal...", os.getenv('HOME'), filter="CSV files (*.csv);;All files (*)")
        path = path_info[0]
        if path:
            data_of_signal = pd.read_csv(path)
            x_data = data_of_signal.values[:, 0]
            y_data = data_of_signal.values[:, 1]
            signal_name = path.split('/')[-1].split('.')[0]
            new_signal = Signal(signal_name, x_data, y_data)
            self.signals.append(new_signal)
            self.add_signal_to_combobox(new_signal,combobox)
            # self.current_signal = new_signal
            self.selected_viewer = self.plot_widgets[viewer]
            if viewer == 0:
                # self.current_signal_v1 = new_signal
                self.current_signal_v1 = self.selected_signal
            elif viewer == 1:
                self.current_signal_v2 = new_signal
            self.play_signal()

    def add_signal_to_combobox(self, signal,combobox):
        self.comboboxes[combobox].addItem(signal.label)
    
    def change_color(self, viewer):
        current_signal = self.current_signal_v1 if viewer ==self.graphicsView_v1 else self.current_signal_v2
        if current_signal:
            color = QColorDialog.getColor()
            if color.isValid():
                current_signal.color = color
                if current_signal.data_line:
                    current_signal.data_line.setPen(pg.mkPen(color))
    
    def change_label_v1(self):
        if self.current_signal_v1:
            new_label = self.lineEdit_signal_v1.text()
            if new_label:
                self.current_signal_v1.label = new_label
                self.Signals_v1.setItemText(self.Signals_v1.currentIndex(), new_label)
            self.lineEdit_signal_v1.setText("")  # Clear the line edit
    
    def change_label_v2(self):
        if self.current_signal_v2:
            new_label = self.lineEdit_signal_v2.text()
            if new_label:
                self.current_signal_v2.label = new_label
                self.Signals_v2.setItemText(self.Signals_v2.currentIndex(), new_label)
            self.lineEdit_signal_v2.setText("")  # Clear the line edit

    def toggle_signal_visibility(self, viewer):
        current_signal = self.current_signal_v1 if viewer == 0 else self.current_signal_v2
        if current_signal and current_signal.data_line: 
            if  (self.hide_checkboxes[viewer].isChecked()):
                current_signal.data_line.setVisible(False)
            else:
                current_signal.data_line.setVisible(True)
            self.update_plot(viewer)

            # # After updating the visibility, update the plot to reflect the changes
            # self.update_plot(self.plot_widgets[viewer])

    # def signal_selected(self, index, viewer):
    #     current_signal = self.current_signal_v1 if viewer==0 else self.current_signal_v2
    #     if 0 <= index < len(self.signals):
    #         current_signal= self.signals[index]
    #         label_widget = self.lineEdit_signal_v1 if viewer == 0 else self.lineEdit_signal_v2
    #         checkbox = self.hide_checkboxes[viewer]
    #         # label_widget.setText(current_signal.label)
    #         # checkbox.setChecked(not self.signal_visibility[viewer])
    def signal_selected(self, index, viewer):
        if 0 <= index < len(self.signals):
            selected_signal = self.signals[index]

            if viewer == 0:
                self.current_signal_v1 = selected_signal
                self.lineEdit_signal_v1.setText(selected_signal.label)  # Set the label text
                # self.hide_checkboxes[0].setChecked(selected_signal.visible)  # Set checkbox state
            elif viewer == 1:
                self.current_signal_v2 = selected_signal
                self.lineEdit_signal_v2.setText(selected_signal.label)  # Set the label text
                # self.hide_checkboxes[1].setChecked(selected_signal.visible)  # Set checkbox state
            else:
                return  # Invalid viewer
    def update_plot(self, viewer):
        if self.signals:
            if self.current_frame < self.num_frames:
                self.update_signal_data(viewer)

        for signal in self.signals:
            if signal.visible:
                if signal.data_line is None:
                    signal.data_line = viewer.plot(pen=signal.color)

                x_data = signal.x_data[:self.current_frame]
                y_data = signal.y_data[:self.current_frame]

                signal.data_line.setData(x_data, y_data)

        self.current_frame += 1

    def update_signal_data(self,viewer):
        # if self.current_signal:
        current_signal = self.current_signal_v1 if viewer ==0 else self.current_signal_v2
        if current_signal:
            x_data = current_signal.x_data[:self.current_frame]
            y_data = current_signal.y_data[:self.current_frame]
            self.num_frames = len(x_data)

    def toggle_play_pause(self):
        if not self.is_playing:
            self.is_playing = True
            self.play_pause_button.setText("Pause")
            self.play_signal()
        else:
            self.is_playing = False
            self.play_pause_button.setText("Play")

    def play_signal(self):
        if not self.signals:
            return

        if not self.is_playing:
            self.is_playing = True
            self.num_frames = max(len(signal.x_data) for signal in self.signals)
            self.current_frame = 0

            if not self.is_paused:
                self.timer.start(self.play_speed)

        self.update_plot(self.selected_viewer)  # Pass the viewer as an argument

    def replay_signal(self):
        self.play_signal()
        self.replay_button.setText("Replay")

    # def signal_selected(self, text):
    #     for signal in self.signals:
    #         if signal.label == text:
    #             self.current_signal = signal
    #             self.show_hide_checkbox.setChecked(self.current_signal.visible)
    #             self.label_lineedit.setText(self.current_signal.label)
    #             self.color_button.setStyleSheet(f'background-color: {self.current_signal.color.name()}')
    #             break



    def zoom_in(self):
        self.plot.vb.scaleBy((0.5, 0.5))

    def zoom_out(self):
        self.plot.vb.scaleBy((2, 2))
    def move_signal(self, source_viewer, target_viewer):
        if source_viewer == 0:
            source_combobox = self.Signals_v1
            source_viewer_widget = self.graphicsView_v1
            source_current_signal = self.current_signal_v1
        elif source_viewer == 1:
            source_combobox = self.Signals_v2
            source_viewer_widget = self.graphicsView_v2
            source_current_signal = self.current_signal_v2
        else:
            return  # Invalid source viewer

        if target_viewer == 0:
            target_combobox = self.Signals_v1
            target_viewer_widget = self.graphicsView_v1
            target_current_signal = self.current_signal_v1
        elif target_viewer == 1:
            target_combobox = self.Signals_v2
            target_viewer_widget = self.graphicsView_v2
            target_current_signal = self.current_signal_v2
        else:
            return  # Invalid target viewer

        selected_signal_index = source_combobox.currentIndex()
        if selected_signal_index >= 0:
            selected_signal_name = source_combobox.currentText()
            selected_signal = None

            for signal in self.signals:
                if signal.label == selected_signal_name:
                    selected_signal = signal
                    break

            if selected_signal:
                # Update the source viewer's data_line visibility
                if source_current_signal:
                    source_current_signal.data_line.setVisible(False)

                # Remove the signal from the source viewer and combobox
                source_viewer_widget.removeItem(selected_signal.data_line)
                source_combobox.removeItem(selected_signal_index)

                # Add the signal to the target viewer and combobox
                selected_signal.data_line = target_viewer_widget.plot(pen=selected_signal.color)
                target_combobox.addItem(selected_signal.label)
                target_combobox.setCurrentText(selected_signal.label)

                # Update the current_signal for both viewers
                if target_viewer == 0:
                    self.current_signal_v1 = selected_signal
                    self.current_signal_v2 = target_current_signal
                elif target_viewer == 1:
                    self.current_signal_v2 = selected_signal
                    self.current_signal_v1 = target_current_signal
def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
