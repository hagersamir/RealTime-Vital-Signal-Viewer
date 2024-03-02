[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-24ddc0f5d75046c5622901739e7c5dd533143b0c8e959d652212380cedb1ea36.svg)](https://classroom.github.com/a/3GlyUq-o)

# SBME_DSP_SignalViewer
## **Introduction** :-
This PyQt-powered application serves as a **real-time vital sign monitoring system**. It features a polished user interface that offers an intuitive platform for visualizing and analyzing vital signals. This tool empowers users to effortlessly navigate through a diverse array of signals, extracting pertinent information from each, and even provides the flexibility to fine-tune them to precise specifications, delivering a tailored and insightful outcome.
## Features :-
- **Real-Time Playback:** Seamlessly play and display signals in real-time for immediate insights.
- **Playback Controls:** Enjoy comprehensive playback controls, including play, pause, and zoom functionalities, enhancing signal examination.
- **Customization Options:** Personalize signal names and colors to optimize visualization and analysis.
- **Signal Management:** Effortlessly move signals between viewers and selectively hide them for focused examination.
- **Statistical Reports:** Generate comprehensive reports with statistical measures for in-depth signal analysis.
- **Viewer Synchronization:** Link viewers for synchronized playback and simultaneous analysis, ensuring coherence in observations.
- **Snapshot Capture:** Capture snapshots of signal views for documentation or easy sharing.
- **Dynamic Speed Control:** Adjust signal playback speed to suit your specific requirements, facilitating precise examination.
## Screenshots:
### Open Signal in Viewport 1:
![Screenshot (40)](https://github.com/hagersamir/RealTime-Vital-Signal-Viewer/assets/105936147/d291306f-63ce-464e-831d-e9a27c4a154f)
### Display Signal in Viewport 1:
![Screenshot (41)](https://github.com/hagersamir/RealTime-Vital-Signal-Viewer/assets/105936147/526631f1-0877-423d-967b-822809dc7635)
### Choosing another color of displayed signal:
![Screenshot (42)](https://github.com/hagersamir/RealTime-Vital-Signal-Viewer/assets/105936147/5010f5fd-1b4d-4406-8515-9e728374da63)
### Changing color of displayed signal:
![Screenshot (43)](https://github.com/hagersamir/RealTime-Vital-Signal-Viewer/assets/105936147/3a2943d9-60ae-436e-89c8-1a09fabc0029)
### Hide the displayed signal:
![Screenshot (44)](https://github.com/hagersamir/RealTime-Vital-Signal-Viewer/assets/105936147/d0362485-e873-4a2e-8cd7-eff52bf21646)
### displayed signal in both viewers :
![Screenshot (45)](https://github.com/hagersamir/RealTime-Vital-Signal-Viewer/assets/105936147/4dab8c43-ac2e-4ecd-b26e-7ddad3fcd0d6)
### Move displayed signal in viewer 1 to viewer 2:
![Screenshot (46)](https://github.com/hagersamir/RealTime-Vital-Signal-Viewer/assets/105936147/6baee8d6-24f4-4699-beda-b76a0a38f212)
### Linking the 2 viewports to work together :
![Screenshot (47)](https://github.com/hagersamir/RealTime-Vital-Signal-Viewer/assets/105936147/a09a0e92-aa9f-4c3f-99a6-580d36829378)
### 2 viewports linked together:
![Screenshot (48)](https://github.com/hagersamir/RealTime-Vital-Signal-Viewer/assets/105936147/93a21e8c-a7b5-49b7-aec1-9e3f288c3136)

## Installation
1. Clone the repository
```sh
   git clone https://github.com/malaknasser812/SBME_DSP_SignalViewer.git
 ```
2. Install project dependencies
```sh
   pip install typing
   pip install os
   pip install PyQt5
   pip install reportlab
   pip install pandas
   pip install numpy
   pip install pyqtgraph
 ```
3. Run the application
```sh
   python main.py
```
## Libraries
- PyQt5
- pyqtgraph
- reportlab
- platypus
- numpy
- pandas
## Usage
- Playing Signals :-
  
  Open the file tab at the left hand corner it displays drop-down menu for viewer one and viewer two, choose what you want and then you can browse to choose a signal.
  
- Changing Signal Properties :-

  you can change the name of the signal on the line-edit with the word label beside it, you can also change color by pushing a button that displays various and 
  different color palettes to choose from.

 - Moving Signals To Another Viewer :-

   You can move the signal from viewer one to viewer two by clicking a button named Move To V2 and vice versa.

- Playback Controls :-

  You can pause, replay from the specified buttons or zoom in and out by clicking the buttons that have the plus and minus icons, and even speed up or down the velocity of the signal.

- Taking Snapshots :-

  You can take a screenshot of the signal, or more than one signal by clicking on the snapshot icon and save it as an image on your computer.

- Generating Reports :-

  A pdf report is generated when you click on the Generate report tab that displays a table of the statistical measures of each signal, its label and all the snapshots you captured.

- Linking Viewers :-

  Linking the two viewers together for synchronized playback and analysis of the signals, using the controls will enable you to handle the two signals simultaneously.

## Our Team

- Camellia Marwan
- Hager Samir
- Farah Ossama
- Malak Nasser


  

