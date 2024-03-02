import sys
import typing
import reportlab
from reportlab.platypus import SimpleDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus.flowables import Image
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
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
        self.data_line = None
        self.max_y = max(self.y_data)
        self.min_y = min(self.y_data)
        self.max_x = max(self.x_data)
        self.min_x = min(self.x_data)



class MainApp(QMainWindow, FORM_CLASS):
    def __init__(self, parent=None):
        super(MainApp, self).__init__(parent)
        self.setupUi(self)
        self.is_paused = False  # Initialize is_paused attribute
        self.play_pause_button1 = self.play_pause_v1
        self.play_pause_button2 = self.play_pause_v2
        self.plot_widgets = [self.graphicsView_v1, self.graphicsView_v2]
        self.replay_button1 = self.replay_v1
        self.replay_button2 = self.replay_v2
        self.current_signal_v1 = None
        self.current_signal_v2 = None
        self.signals =[]
        self.signals1 = []
        self.signals2 = []
        self.image_filenames = []
        self.is_playing1 = False
        self.is_playing2 = False
        self.play_speed = 5  # Update interval in milliseconds
        self.current_frame1 = 0
        self.current_frame2 = 0
        self.num_frames1 = 0
        self.num_frames2 = 0
        self.selected_viewer = None
        self.selected_signal = None
        self.plot_widgets[1].addLegend() 
        self.plot_widgets[0].addLegend()
        self.timer1 = pg.QtCore.QTimer(self) 
        self.timer2 = pg.QtCore.QTimer(self) 
        self.timer_delay1 = 20 #initiate time delay
        self.timer_delay2 = 20 #initiate time delay
        self.link = False 
        self.timer1.setInterval(self.timer_delay1)
        self.timer2.setInterval(self.timer_delay2)
        self.comboboxes = [self.Signals_v1,self.Signals_v2]
        self.comboboxes[0].currentIndexChanged.connect(lambda index: self.signal_selected(index, 0))
        self.comboboxes[1].currentIndexChanged.connect(lambda index: self.signal_selected(index, 1))
        self.hide_checkboxes = [self.hide_checkbox_signal_v1, self.hide_checkbox_signal_v2]
        
        #PointingHandCursor
        self.replay_button1.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.replay_button2.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.zoom_in_v1.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.zoom_in_v2.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.zoom_out_v1.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.zoom_out_v2.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.play_pause_button1.setCursor(QCursor(QtCore.Qt.PointingHandCursor)) 
        self.play_pause_button2.setCursor(QCursor(QtCore.Qt.PointingHandCursor)) 
        self.add_to_rep_v1.setCursor(QCursor(QtCore.Qt.PointingHandCursor)) 
        self.add_to_rep_v2.setCursor(QCursor(QtCore.Qt.PointingHandCursor)) 
        self.speed_up_1.setCursor(QCursor(QtCore.Qt.PointingHandCursor)) 
        self.speed_up_2.setCursor(QCursor(QtCore.Qt.PointingHandCursor)) 
        self.speed_down_1.setCursor(QCursor(QtCore.Qt.PointingHandCursor)) 
        self.speed_down_2.setCursor(QCursor(QtCore.Qt.PointingHandCursor)) 


        self.zoom_out_v1.clicked.connect(lambda: self.zoom_out(self.graphicsView_v1))
        self.zoom_in_v1.clicked.connect(lambda: self.zoom_in(self.graphicsView_v1))
        self.zoom_out_v2.clicked.connect(lambda: self.zoom_out(self.graphicsView_v2))
        self.zoom_in_v2.clicked.connect(lambda: self.zoom_in(self.graphicsView_v2))

        self.replay_button1.clicked.connect(lambda: self.replay_signal(0))
        self.replay_button2.clicked.connect(lambda: self.replay_signal(1))

        self.play_pause_button1.clicked.connect(lambda:self.toggle_play_pause(0))
        self.play_pause_button2.clicked.connect(lambda:self.toggle_play_pause(1))

        self.clear_viewer_1.triggered.connect(lambda:self.clear_graph(self.plot_widgets[0]))
        self.clear_viewer_2.triggered.connect(lambda:self.clear_graph(self.plot_widgets[1]))

        self.open_viewer_1.triggered.connect(lambda: self.load(0,0))
        self.open_viewer_2.triggered.connect(lambda: self.load(1,1))

        self.pushButton_color_v1.clicked.connect(lambda: self.change_color(self.plot_widgets[0]))
        self.pushButton_color_v2.clicked.connect(lambda: self.change_color(self.plot_widgets[1]))             

        self.lineEdit_signal_v1.editingFinished.connect(self.change_label_v1)
        self.lineEdit_signal_v2.editingFinished.connect(self.change_label_v2)

        self.pushButton_move_to_v1.clicked.connect(lambda: self.move_signal(0, 1))
        self.pushButton_move_to_v2.clicked.connect(lambda: self.move_signal(1, 0))


        # Speed up/down
        self.speed_up_1.clicked.connect(lambda:self.speed_up(0))
        self.speed_up_2.clicked.connect(lambda:self.speed_up(1))
        self.speed_down_1.clicked.connect(lambda:self.Speed_down(0))
        self.speed_down_2.clicked.connect(lambda:self.Speed_down(1))

        self.actionLink.triggered.connect(lambda: self.link_unlink(True)) 
        self.actionUnLink.triggered.connect(lambda: self.link_unlink(False)) 

        self.timer1.timeout.connect(lambda: self.play_signal(0))
        self.timer2.timeout.connect(lambda: self.play_signal(1))

        # Generate PDF
        generate_pdf_action = self.actionGenerate_PDF_2
        generate_pdf_action.triggered.connect(self.generate_pdf)
        self.menuzoom_in = self.findChild(QMenu, "menuzoom_in")
        self.menuzoom_in.addAction(generate_pdf_action)
        self.add_to_rep_v1.clicked.connect(lambda : self.take_snapshot(0))
        self.add_to_rep_v2.clicked.connect(lambda : self.take_snapshot(1))

        for i,checkbox in enumerate(self.hide_checkboxes):
            checkbox.stateChanged.connect(lambda state,viewer=i : self.toggle_signal_visibility(viewer))


        for widget in self.plot_widgets:
            self.init_plot(widget)

    def init_plot(self,  plot_widget):
        plot_widget.clear()
        self.plot = plot_widget.getPlotItem()



###################################
    ##FUNCTIONS##
###################################

    def load(self,viewer,combobox):
        path_info = QFileDialog.getOpenFileName(
            None, "Select a signal...", os.getenv('HOME'), filter="CSV files (.csv);;All files ()")
        path = path_info[0]
        if path:
            # Read the data from the selected CSV file and set x,y_axis
            data_of_signal = pd.read_csv(path)
            x_data = data_of_signal.values[:, 0]
            y_data = data_of_signal.values[:, 1]
            signal_name = path.split('/')[-1].split('.')[0]
            new_signal = Signal(signal_name, x_data, y_data)
            # Add the new signal to the list have all signals
            self.signals.append(new_signal)
            # Add the new signal to the specified combobox
            self.add_signal_to_combobox(new_signal,combobox)
            self.selected_viewer = self.plot_widgets[viewer]
            # Set the current signal for the specified viewer
            if viewer == 0:
                self.signals1.append(new_signal) # add signal to list of viewer 1
                self.current_signal_v1 = new_signal
            elif viewer == 1:
                self.signals2.append(new_signal) # add signal to list of viewer 2
                self.current_signal_v2 = new_signal
            self.play_signal(viewer)


    def add_signal_to_combobox(self, signal,combobox):
        self.comboboxes[combobox].addItem(signal.label)

    def play_signal(self,viewer):
        if viewer == 0:
            if not self.is_playing1:
            # If viewer 1 is not currently playing
                self.is_playing1 = True
            # Calculate the number of frames of viewer 1 based on the maximum signal length
                self.num_frames1 = max(len(signal.x_data) for signal in self.signals1)
                self.current_frame1 = 0
                # if not self.is_paused:
                # If not paused, start the timer for viewer 1
                self.timer1.start(self.play_speed)
        else :    
            if not self.is_playing2:
                self.is_playing2 = True
            # Calculate the number of frames of viewer 2 based on the maximum signal length
                self.num_frames2 = max(len(signal.x_data) for signal in self.signals2)
                self.current_frame2 = 0
                self.timer2.start(self.play_speed)            
        self.update_plot(viewer )

    def update_plot(self, viewer_index):
        if viewer_index == 0:
            if self.signals1:
                # If viewer 1 has signals and there are more frames to display:
                # Update signal data for viewer 1 (increments current_frame1)
                if self.current_frame1 < self.num_frames1 : 
                    self.update_signal_data(viewer_index)

            for signal in self.signals1:
                if signal.visible:
                    if signal.data_line is None:
                    # If the signal's data_line (plot) doesn't exist, create one
                        signal.data_line = self.plot_widgets[viewer_index].plot(pen=signal.color,name=signal.name)
                    # Update the data displayed on the signal's data_line
                    signal.data_line.setData(signal.x_data, signal.y_data)
        else :
            if self.signals2:
                if self.current_frame2 < self.num_frames2 :
                    self.update_signal_data(viewer_index)

            for signal in self.signals2:
                if signal.visible:
                    if signal.data_line is None:
                        signal.data_line = self.plot_widgets[viewer_index].plot(pen=signal.color)
                    # Update the data displayed on the signal's data_line
                    signal.data_line.setData(signal.x_data, signal.y_data)


    def update_signal_data(self, viewer_index):
        if viewer_index==0:
            if self.current_frame1 < self.num_frames1:
                # Calculate the minimum and maximum x values for viewer 1
                x_min = min(signal.x_data[self.current_frame1] for signal in self.signals1)
                x_max = max(signal.x_data[self.current_frame1] for signal in self.signals1)
                # Set the X range for the viewer 1 plot
                self.plot_widgets[viewer_index].setXRange(x_min, x_max)
            self.current_frame1 += 1
        else:
            if self.current_frame2 < self.num_frames2:
                # Calculate the minimum and maximum x values for viewer 2
                x_min = min(signal.x_data[self.current_frame2] for signal in self.signals2)
                x_max = max(signal.x_data[self.current_frame2] for signal in self.signals2)
                # Set the X range for the viewer 2 plot
                self.plot_widgets[viewer_index].setXRange(x_min, x_max)
            self.current_frame2 += 1


#SELECTING SIGNAL
    def signal_selected(self, index, viewer):
            if viewer == 0:
                if 0 <= index < len(self.signals1):
                    selected_signal =  self.signals1[index] 
                    self.current_signal_v1 = selected_signal
                    self.lineEdit_signal_v1.setText(selected_signal.label)  # Set the label text
                    self.selected_viewer = self.plot_widgets[0]  # Set the selected viewer to viewer 1
            elif viewer == 1:
                if 0 <= index < len(self.signals2):
                    selected_signal =  self.signals2[index]
                    self.current_signal_v2 = selected_signal
                    self.lineEdit_signal_v2.setText(selected_signal.label)  # Set the label text
                    self.selected_viewer = self.plot_widgets[1]  # Set the selected viewer to viewer 2
        
#ZOOMING
    def zoom_in(self,viewer):
        if self.link: 
            self.graphicsView_v1.getViewBox().scaleBy((0.5, 0.5))
            self.graphicsView_v2.getViewBox().scaleBy((0.5, 0.5))
        else : viewer.getViewBox().scaleBy((0.5, 0.5))

    def zoom_out(self,viewer):
        if self.link: 
            self.graphicsView_v1.getViewBox().scaleBy((2, 2))
            self.graphicsView_v2.getViewBox().scaleBy((2, 2))
        else : viewer.getViewBox().scaleBy((2, 2))


#CHANGE COLOUR ---> problem (last selected)      
    def change_color(self, viewer):
        current_signal = self.current_signal_v1 if viewer ==self.graphicsView_v1 else self.current_signal_v2
        if current_signal:
            color = QColorDialog.getColor()
            if color.isValid():
                current_signal.color = color
                if current_signal.data_line:
                    current_signal.data_line.setPen(pg.mkPen(color))
    

#CHANGE LABEL
    def change_label_v1(self):
        if self.current_signal_v1:
            new_label = self.lineEdit_signal_v1.text() #take name from user input
            if new_label:
                self.current_signal_v1.label = new_label
                self.comboboxes[0].setItemText(self.comboboxes[0].currentIndex(), new_label) # set new name of signal in combobox instead of old one
            self.lineEdit_signal_v1.setText("")  # Clear the line edit to add another one if i want
    
    def change_label_v2(self):
        if self.current_signal_v2:
            new_label = self.lineEdit_signal_v2.text()
            if new_label:
                self.current_signal_v2.label = new_label
                self.comboboxes[1].setItemText(self.Signals_v2.currentIndex(), new_label)
            self.lineEdit_signal_v2.setText("")  # Clear the line edit


#HIDE AND SHOW ---> PROBLEM (TEST TO SEE)
    def toggle_signal_visibility(self, viewer):
        current_signal = self.current_signal_v1 if viewer == 0 else self.current_signal_v2
        if current_signal and current_signal.data_line: 
            if  (self.hide_checkboxes[viewer].isChecked()): #check box of hide is clicked so signal should be hidden 
                current_signal.data_line.setVisible(False)
            else:
                current_signal.data_line.setVisible(True)
            self.update_plot(viewer)


    def clear_graph(self , plot_widget ):
        if plot_widget == self.graphicsView_v1 :
            self.graphicsView_v1.clear()
            self.comboboxes[0].clear()
            self.timer1.stop()
            self.lineEdit_signal_v1.clear()
        else :
            self.graphicsView_v2.clear()
            self.comboboxes[1].clear()
            self.timer2.stop()
            self.lineEdit_signal_v2.clear()

#PLAY/PAUSE
    def toggle_play_pause(self, viewer):
        if self.link:
            if self.is_playing1:
                self.is_playing1 = False
                self.play_pause_button1.setText("Pause v1")
                self.timer1.stop()
                self.timer2.stop()
            else:
                self.is_playing1 = True
                self.play_pause_button1.setText("Play v1")
                self.timer1.start()
                self.timer2.start()
        else :
            if viewer == 0:
                if self.is_playing1:
                    self.is_playing1 = False
                    self.play_pause_button1.setText("Pause v1")
                    x_max = max(signal.x_data[self.current_frame1] for signal in self.signals1)
                    x_min = min(signal.x_data[self.current_frame1] for signal in self.signals1)
                    self.plot_widgets[0].setLimits(xMin=x_min ,xMax=x_max + 2)
                    y_max = max(max(signal.y_data) for signal in self.signals1)
                    y_min = min(min(signal.y_data) for signal in self.signals1)
                    self.plot_widgets[0].setLimits(yMin= y_min ,yMax= y_max )
                    self.timer1.stop()
                else:
                    self.is_playing1 = True
                    self.play_pause_button1.setText("Play v1")
                    self.plot_widgets[0].setLimits(xMin=None, xMax=None, yMin=None, yMax=None)
                    self.timer1.start()
            else:
                if self.is_playing2:
                    self.is_playing2 = False
                    self.play_pause_button2.setText("Pause v2")
                    x_max = max(signal.x_data[self.current_frame2] for signal in self.signals2)
                    x_mIN = min(signal.x_data[self.current_frame2] for signal in self.signals2)
                    self.plot_widgets[1].setLimits(xMin=x_mIN,xMax=x_max + 2)
                    y_max = max(max(signal.y_data) for signal in self.signals2)
                    y_min = min(min(signal.y_data) for signal in self.signals2)
                    self.plot_widgets[1].setLimits(yMin= y_min ,yMax= y_max )
                    self.timer1.stop()
                    self.timer2.stop()
                else:
                    self.is_playing2 = True
                    self.play_pause_button2.setText("Play v2")
                    self.plot_widgets[1].setLimits(xMin=None, xMax=None, yMin=None, yMax=None)
                    self.timer2.start()


#REPLAY

    def replay_signal(self, viewer):
        if self.link :
            self.is_playing1 = True
            self.current_frame1 = 0
            self.play_pause_button1.setText("Play v1")
            self.timer1.start(self.play_speed)
            self.current_frame2 = 0
            self.play_pause_button2.setText("Play v2")
            self.timer2.start(self.play_speed)
        if viewer == 0:
            self.is_playing1 = True
            self.current_frame1 = 0
            self.play_pause_button1.setText("Play v1")
            self.timer1.start(self.play_speed)
        elif viewer == 1:
            self.is_playing2 = True
            self.current_frame2 = 0
            self.play_pause_button2.setText("Play v2")
            self.timer2.start(self.play_speed)

#MOVE TO OTHER GRAPH 
    
    def move_signal(self, source_viewer, target_viewer):
        if source_viewer == 0:
            source_combobox = self.comboboxes[0]
            source_viewer_widget = self.plot_widgets[0]
            source_current_signal = self.current_signal_v1
            source_line_edit = self.lineEdit_signal_v1
            source_signals = self.signals1
            source_frame = self.current_frame1
        elif source_viewer == 1:
            source_combobox = self.comboboxes[1]
            source_viewer_widget = self.plot_widgets[1]
            source_current_signal = self.current_signal_v2
            source_line_edit = self.lineEdit_signal_v2
            source_signals = self.signals2
            source_frame = self.current_frame2
        else:
            return  # Invalid source viewer

        if target_viewer == 0:
            target_combobox = self.comboboxes[0]
            target_viewer_widget = self.plot_widgets[0]
            target_current_signal = self.current_signal_v1
            target_line_edit = self.lineEdit_signal_v1
            target_signals = self.signals1
            target_frame = self.current_frame1
        elif target_viewer == 1:
            target_combobox = self.comboboxes[1]
            target_viewer_widget = self.plot_widgets[1]
            target_current_signal = self.current_signal_v2
            target_line_edit = self.lineEdit_signal_v2
            target_signals = self.signals2
            target_frame = self.current_frame2
        else:
            return  # Invalid target viewer

        selected_signal_index = source_combobox.currentIndex()
        if selected_signal_index >= 0:
            selected_signal_name = source_combobox.currentText()
            selected_signal = None

            for signal in source_signals:
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
                source_line_edit.setText("")  # Clear the LineEdit for source viewer
                source_signals.remove(selected_signal)

                # Add the signal to the target viewer and combobox
                selected_signal.data_line = target_viewer_widget.plot(pen=selected_signal.color)
                target_combobox.addItem(selected_signal.label)
                target_combobox.setCurrentText(selected_signal.label)
                target_signals.append(selected_signal)

                # Update the current_signal for both viewers
                if target_viewer == 0:
                    self.current_signal_v1 = selected_signal
                    self.current_signal_v2 = target_current_signal
                    target_line_edit.setText(selected_signal.label)
                    # target_frame = len(selected_signal.x_data)  # Update target viewer frame
                elif target_viewer == 1:
                    self.current_signal_v2 = selected_signal
                    self.current_signal_v1 = target_current_signal
                    target_line_edit.setText(selected_signal.label)
                    # target_frame = len(selected_signal.x_data)  # Update target viewer frame
                # Check if the target viewer has no signals and start playing if it doesn't
                if target_signals ==1:
                    self.play_signal(target_viewer)

                # Check if viewer 1 has only one signal, and if so, stop playing
                if source_viewer == 0 and len(source_signals) == 1:
                    self.is_playing1 = False

        # Update the plots
        self.update_plot(source_viewer)
        self.update_plot(target_viewer)
        

#SPEEDING UP AND DOWN
    def speed_up(self, viewer):
        speed_up_factor = 2
        if self.link: 
            self.timer_delay1 = max(1, int(self.timer_delay1 / speed_up_factor))  
            self.timer1.setInterval(self.timer_delay1) 
            self.timer_delay2 = max(1, int(self.timer_delay2 / speed_up_factor))  
            self.timer2.setInterval(self.timer_delay2)
        elif viewer == 0:
            self.timer_delay1 = max(1, int(self.timer_delay1 / 3))  
            self.timer1.setInterval(self.timer_delay1)

        else:
            self.timer_delay2 = max(1, int(self.timer_delay2 / speed_up_factor))  
            self.timer2.setInterval(self.timer_delay2)

    def Speed_down(self, viewer):
        # Define a constant factor for slowing down
        slow_down_factor = 2
        if self.link:
            self.timer_delay1 = int(self.timer_delay1 * slow_down_factor)  # Multiply by the factor
            self.timer1.setInterval(self.timer_delay1)

            self.timer_delay2 = int(self.timer_delay2 * slow_down_factor)  # Multiply by the factor
            self.timer2.setInterval(self.timer_delay2)

        if viewer == 0:
            self.timer_delay1 = int(self.timer_delay1 * slow_down_factor)  # Multiply by the factor
            self.timer1.setInterval(self.timer_delay1)


        else:
            self.timer_delay2 = int(self.timer_delay2 * slow_down_factor)  # Multiply by the factor
            self.timer2.setInterval(self.timer_delay2)


#LINKING TWO GRAPHS
    def link_unlink(self,flag):
        if flag:
            self.link = True
            self.play_pause_v2.setVisible(False)
            self.replay_v2.setVisible(False)
            self.zoom_in_v2.setVisible(False)
            self.zoom_out_v2.setVisible(False)
            self.speed_up_2.setVisible(False)
            self.speed_down_2.setVisible(False)
        else:
            self.link = False
            self.play_pause_v2.setVisible(True)
            self.replay_v2.setVisible(True)
            self.zoom_in_v2.setVisible(True)
            self.zoom_out_v2.setVisible(True)
            self.speed_up_2.setVisible(True)
            self.speed_down_2.setVisible(True)

# take a snapshot of the graph with the uploaded signals
    def take_snapshot(self, viewer):
        # Capture a screenshot of the specified viewer  
        pixmap = self.graphicsView_v1.grab() if viewer == 0 else self.graphicsView_v2.grab()

        # Determine the index for the snapshot image and define its name
        snapshot_index = len([f for f in os.listdir('.') if f.startswith('snapshot_')]) + 1
        image_filename = f"snapshot_{snapshot_index}.png"
        pixmap.save(image_filename)
        self.image_filenames.append(image_filename)

# Generating a pdf report
    def generate_pdf(self):
        # Define the PDF filename
        pdf_filename = "output.pdf"
        doc = SimpleDocTemplate(pdf_filename, pagesize=letter)

        # Initialize an empty list that contains the report content
        layout = []
        title_style = getSampleStyleSheet()["Title"]

        # Loop to get each signal statistics in the list of signals
        for signal in self.signals:
            stat_data = self.setStats(signal.y_data, signal.x_data)

            # Define the table data for the statistics
            table_data = [["Statistic", "Value"],
            ["Min Y", str(stat_data[0])],
            ["Min X", str(stat_data[1])],
            ["Max Y", str(stat_data[2])],
            ["Max X", str(stat_data[3])],
            ["Duration", str(stat_data[4])],
            ["Mean", str(stat_data[5])],
            ["Standard Deviation", str(stat_data[6])]]

            # Set a title for the table
            title_text = f"Signal : {signal.label}"
            title = Paragraph(title_text, title_style)

            # Create a table and define its style
            table = Table(table_data, colWidths=[200, 200], rowHeights=30)
            table.setStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ])
            layout.append(title)
            layout.append(Spacer(1,20))
            layout.append(table)

        # Loop through each image filename and add images to the report
        for image_filename in self.image_filenames:
            img = Image(image_filename, width=400, height=200)
            layout.append(Spacer(1, 20))
            layout.append(img)

        # Build the document and open it using the default PDF viewer  
        doc.build(layout)
        os.startfile("output.pdf")


# Calculate statistics measures for a given signal
    def setStats(self, y1, x1):
        # Calculate the minimum and maximum values of the y-data
        ymin = np.min(y1)
        ymax = np.max(y1)

        # Find the corresponding x-values for the min y1 and max y1
        xmin = x1[np.argmin(y1)]
        xmax = x1[np.argmax(y1)]

        # Calculate the duration of the signal
        duration = x1[-1]

        # Calculate the mean and standard deviation of the y-data
        mean = np.mean(y1)
        std = np.std(y1)

        # Store the calculated statistics in a list
        statData = [ymin, xmin, ymax, xmax, duration, mean, std]
        return statData

def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
