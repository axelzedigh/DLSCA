################################################################################
#
# Creator: Martin Brisfors, 2019
#
# A GUI tool for executing some of the code we have developed throughout our
# work so far.
#
################################################################################

import sys
import os
import PyQt5.QtWidgets as QtWidgets
from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5.QtCore import QDateTime, Qt, QTimer
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
import subprocess
import re


class WidgetGallery(QDialog):
    def __init__(self, parent=None):

        screen = app.primaryScreen()
        self.screenSize = screen.size()
        self.screenMode = 0
        if self.screenSize.width() > 1200:
            self.screenMode = 1
        if self.screenSize.width() > 1900:
            self.screenMode = 2
        if self.screenSize.width() > 2500:
            self.screenMode = 3
        if self.screenSize.width() > 3800:
            self.screenMode = 4
        super(WidgetGallery, self).__init__(parent)

        self.originalPalette = QApplication.palette()
        self.selectedString = (
            # String used to generate list of args for scripts
            "selected files:"
        )
        if self.screenMode < 3:
            # Application default resolution
            self.resize(600, 500)
        if self.screenMode >= 3:
            self.resize(250 + (self.screenMode * 250), 500)
        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tabs.blockSignals(True)
        self.createT1()
        self.createT2()
        self.createT3()
        self.tabs.addTab(self.T1, "Training")
        self.tabs.addTab(self.T2, "Testing")
        self.tabs.addTab(self.T3, "Utils")

        # Currently contains nothing, but it is the tof of the layout above tabs
        topLayout = QHBoxLayout()
        topLayout.addStretch(1)

        # Layout of the main program. Basically just the tabs.
        mainLayout = QVBoxLayout()
        mainLayout.addLayout(topLayout)
        mainLayout.addWidget(self.tabs)
        mainLayout.addStretch(1)

        # Window layout and header
        self.setLayout(mainLayout)

        # This is used to prevent an error during startup
        self.tabs.blockSignals(False)
        self.setWindowTitle("Deep Learning SCA Tool")

        # Input argument handling
        if "-d" in sys.argv:
            subprocess.call(["python", "scripts/diagnostics.py"])

        if "-h" in sys.argv:
            print(
                "\nUSAGE:\n"
                "python main.py flag0 arg0 arg1 arg2 ...\n\n\n"
                "FLAGS:\n"
                "-t\tstart in test tab\n\n"
                "-u\tstart in utility tab\n\n"
                "-d\trun diagnostics\n\n"
                "-h\tprint usage\n\n\n"
                "EXAMPLES:\n"
                "python main.py myFile\t\tload myFile\n\n"
                "python main.py ourModels/MLP/*\tload all MLP models\n\n"
                "python main.py -u history/*"
                "\tload all history files in util tab"
            )
            sys.exit()

        if len(sys.argv) > 2:
            if sys.argv[1] == "-t":
                self.tabs.setCurrentIndex(1)
                temp = self.selectedString
                for i in sys.argv[2:]:
                    temp = temp + "\n" + i
                self.updateSelected(temp)
            elif sys.argv[1] == "-u":
                self.tabs.setCurrentIndex(2)
                temp = self.selectedString
                for i in sys.argv[2:]:
                    temp = temp + "\n" + i
                self.updateSelected(temp)

        if len(sys.argv) > 1:
            if sys.argv[1] not in ["-u", "-t"]:
                self.tabs.setCurrentIndex(1)
                temp = self.selectedString
                for i in sys.argv[1:]:
                    temp = temp + "\n" + i
                self.updateSelected(temp)

    # Naming convention atm:
    # T = tab, #X = index starting from 1, L = left side
    # So if something is createT1L it means create the left side of tab1...
    def createT1L(self):
        self.tab1 = QWidget()
        t1lLayout = QVBoxLayout(self)

        # Name
        t1ModelName = QWidget()
        hori = QHBoxLayout()
        vert = QVBoxLayout()
        modelName = QLineEdit("MyModel")
        modelNameh = QPushButton("?")
        vert.addWidget(QLabel("Name:"))
        hori.addWidget(modelName, 40)
        hori.addWidget(modelNameh, 1)
        vert.addLayout(hori)
        t1ModelName.setLayout(vert)
        t1lLayout.addWidget(t1ModelName)

        # Interval
        t1interval = QWidget()
        hori = QHBoxLayout()
        vert = QVBoxLayout()
        vert.addWidget(QLabel("Training interval:"))
        traceInterval = QLineEdit("57:153")
        traceIntervalh = QPushButton("?")
        hori.addWidget(traceInterval, 40)
        hori.addWidget(traceIntervalh, 1)
        vert.addLayout(hori)
        t1interval.setLayout(vert)
        t1lLayout.addWidget(t1interval)

        # Which keybyte
        t1Keybyte = QWidget()
        hori = QHBoxLayout()
        vert = QVBoxLayout()
        vert.addWidget(QLabel("Keybyte to test"))
        keybytePos = QComboBox()
        keybytePos.addItem("0")
        keybytePos.addItem("1")
        keybytePos.addItem("2")
        keybytePos.addItem("3")
        keybytePos.addItem("4")
        keybytePos.addItem("5")
        keybytePos.addItem("6")
        keybytePos.addItem("7")
        keybytePos.addItem("8")
        keybytePos.addItem("9")
        keybytePos.addItem("A")
        keybytePos.addItem("B")
        keybytePos.addItem("C")
        keybytePos.addItem("D")
        keybytePos.addItem("E")
        keybytePos.addItem("F")
        keybyteh = QPushButton("?")
        hori.addWidget(keybytePos, 40)
        hori.addWidget(keybyteh, 1)
        vert.addLayout(hori)
        t1Keybyte.setLayout(vert)
        t1lLayout.addWidget(t1Keybyte)

        # Num of nodes
        t1Nodes = QWidget()
        hori = QHBoxLayout()
        vert = QVBoxLayout()
        vert.addWidget(QLabel("Number of nodes:"))
        numNodes = QLineEdit("200")
        numNodesh = QPushButton("?")
        hori.addWidget(numNodes, 40)
        hori.addWidget(numNodesh, 1)
        vert.addLayout(hori)
        t1Nodes.setLayout(vert)
        t1lLayout.addWidget(t1Nodes)

        # Num of layers
        t1Layers = QWidget()
        hori = QHBoxLayout()
        vert = QVBoxLayout()
        vert.addWidget(QLabel("Number of layers:"))
        numLayers = QLineEdit("6")
        numLayersh = QPushButton("?")
        hori.addWidget(numLayers, 40)
        hori.addWidget(numLayersh, 1)
        vert.addLayout(hori)
        t1Layers.setLayout(vert)
        t1lLayout.addWidget(t1Layers)

        # Learning rate
        t1LearningRate = QWidget()
        hori = QHBoxLayout()
        vert = QVBoxLayout()
        vert.addWidget(QLabel("Learning rate:"))
        learningRate = QLineEdit("0.00008")
        learningRateh = QPushButton("?")
        hori.addWidget(learningRate, 40)
        hori.addWidget(learningRateh, 1)
        vert.addLayout(hori)
        t1LearningRate.setLayout(vert)
        t1lLayout.addWidget(t1LearningRate)

        # Num of epochs
        t1Epochs = QWidget()
        hori = QHBoxLayout()
        vert = QVBoxLayout()
        vert.addWidget(QLabel("Number of epochs:"))
        numEpochs = QLineEdit("200")
        numEpochsh = QPushButton("?")
        hori.addWidget(numEpochs, 40)
        hori.addWidget(numEpochsh, 1)
        vert.addLayout(hori)
        t1Epochs.setLayout(vert)
        t1lLayout.addWidget(t1Epochs)

        # Batch size
        t1BatchSize = QWidget()
        hori = QHBoxLayout()
        vert = QVBoxLayout()
        vert.addWidget(QLabel("Batch size:"))
        batchSize = QLineEdit("100")
        batchSizeh = QPushButton("?")
        hori.addWidget(batchSize, 40)
        hori.addWidget(batchSizeh, 1)
        vert.addLayout(hori)
        t1BatchSize.setLayout(vert)
        t1lLayout.addWidget(t1BatchSize)

        t1Button = QWidget()
        t1ButtonLayout = QHBoxLayout()
        trainingButton = QPushButton("Create training file")
        trainingButtonh = QPushButton("?")
        t1ButtonLayout.addWidget(trainingButton, 40)
        t1ButtonLayout.addWidget(trainingButtonh, 1)
        t1Button.setLayout(t1ButtonLayout)
        t1lLayout.addWidget(t1Button)

        self.tab1.setLayout(t1lLayout)

        def createTraining():
            name = modelName.text()
            nodes = numNodes.text()
            layers = numLayers.text()
            lr = learningRate.text()
            epochs = numEpochs.text()
            batches = batchSize.text()
            keybytepos = str(keybytePos.currentIndex())

            interval = traceInterval.text()
            traceStart = re.search("(\d+):(\d+)", interval).group(1)
            traceEnd = re.search("(\d+):(\d+)", interval).group(2)

            alert = QMessageBox()
            alert.setText("Choose trace file")
            alert.exec_()
            tracefile = self.openTracesDialog()
            if not tracefile:
                return
            alert.setText("Choose file containing labels")
            alert.exec_()
            labels = self.openTracesDialog()
            if not labels:
                return
            subprocess.call(
                [
                    "python",
                    "scripts/trainingCreator.py",
                    name,
                    nodes,
                    layers,
                    lr,
                    epochs,
                    batches,
                    traceStart,
                    traceEnd,
                    tracefile,
                    labels,
                    keybytepos,
                ]
            )
            print(
                "Training file created! You can find it in the base directory. \nContents of: "
                + os.getcwd()
                + ":"
            )
            for entry in os.listdir(os.getcwd()):
                if entry == name + "_training.py":
                    print(entry + " <----- Your training file")
                else:
                    print(entry)
            alert.setText("Done!")
            alert.exec_()

        # Helpbutton prints

        def nameInfo():
            info = "Write the name you want to give the model."
            self.updateInfo(info, self.tabs.currentIndex())

        def intervalInfo():
            info = "Set the time interval in the trace that you want the " \
                   "model to train on."
            self.updateInfo(info, self.tabs.currentIndex())

        def nodesInfo():
            info = "Set the number of nodes in each dense layer (We had 200)."
            self.updateInfo(info, self.tabs.currentIndex())

        def layersInfo():
            info = "Set the total number of layers " \
                   "(Including input and output layer) (We had 6)."
            self.updateInfo(info, self.tabs.currentIndex())

        def learningRateInfo():
            info = "Set the learning rate for the RMSPRop optimizer " \
                   "(Default is 0.01, we had best results with 0.00008)."
            self.updateInfo(info, self.tabs.currentIndex())

        def epochsInfo():
            info = "Set the number of epochs for the training process " \
                   "(We had 200)."
            self.updateInfo(info, self.tabs.currentIndex())

        def batchSizeInfo():
            info = "Set the size of each training batch (We had 100)."
            self.updateInfo(info, self.tabs.currentIndex())

        def buttonInfo():
            info = "Click here to create a new training script with the " \
                   "set parameters in the src directory."
            self.updateInfo(info, self.tabs.currentIndex())

        modelNameh.clicked.connect(nameInfo)
        traceIntervalh.clicked.connect(intervalInfo)
        numNodesh.clicked.connect(nodesInfo)
        numLayersh.clicked.connect(layersInfo)
        learningRateh.clicked.connect(learningRateInfo)
        numEpochsh.clicked.connect(epochsInfo)
        batchSizeh.clicked.connect(batchSizeInfo)
        trainingButtonh.clicked.connect(buttonInfo)
        trainingButton.clicked.connect(createTraining)

    # Not sure if there's a better way to do this since I want elements to be aligned.
    # The block separation in this code represents GUI modules.
    # Naming convention: t = tab, #X = index starting from 1, l = left side
    # Naming convention: b = button, s = script, h = help
    # Each widget has its own layout variable where if possible it has the same prefix
    def createT2L(self):
        self.tab2 = QWidget()
        t2lLayout = QVBoxLayout(self)

        t2b1Widget = QWidget()
        hori = QHBoxLayout()
        vert = QVBoxLayout()
        vert.addWidget(QLabel("File browser"))
        tab2Button1 = QPushButton("Files")
        tab2Button1h = QPushButton("?")
        hori.addWidget(tab2Button1, 40)
        hori.addWidget(tab2Button1h, 1)
        vert.addLayout(hori)
        t2b1Widget.setLayout(vert)
        t2lLayout.addWidget(t2b1Widget)

        self.tab2TextWidget = QWidget()
        hori = QHBoxLayout()
        vert = QVBoxLayout()
        vert.addWidget(QLabel("Selected files"))
        self.tab2.textEdit = QTextEdit()
        self.tab2.textEdit.setPlainText(self.selectedString)
        tab2Texth = QPushButton("?")
        hori.addWidget(self.tab2.textEdit, 40)
        hori.addWidget(tab2Texth, 1)
        vert.addLayout(hori)
        self.tab2TextWidget.setLayout(vert)
        t2lLayout.addWidget(self.tab2TextWidget)

        t2dropdownWidget = QWidget()
        hori = QHBoxLayout()
        vert = QVBoxLayout()
        vert.addWidget(QLabel("Test selector"))
        t2dropdown = QComboBox()
        t2dropdown.addItem("Average Rank Test")
        t2dropdown.addItem("First Trace Success Test")
        t2dropdown.addItem("Whole Key Test")
        t2dropdownh = QPushButton("?")
        hori.addWidget(t2dropdown, 40)
        hori.addWidget(t2dropdownh, 1)
        vert.addLayout(hori)
        t2dropdownWidget.setLayout(vert)
        t2lLayout.addWidget(t2dropdownWidget)

        # SHARED GROUP
        t2sharedGroup = QWidget()
        t2sharedLayout = QVBoxLayout()

        t2interval = QWidget()
        hori = QHBoxLayout()
        vert = QVBoxLayout()
        vert.addWidget(QLabel("First keybyte interval"))
        traceInterval = QLineEdit("57:153")
        traceIntervalh = QPushButton("?")
        hori.addWidget(traceInterval, 40)
        hori.addWidget(traceIntervalh, 1)
        vert.addLayout(hori)
        t2interval.setLayout(vert)
        t2sharedLayout.addWidget(t2interval)

        t2keybyte = QWidget()
        hori = QHBoxLayout()
        vert = QVBoxLayout()
        vert.addWidget(QLabel("Keybyte to test"))
        keybytePos = QComboBox()
        keybytePos.addItem("0")
        keybytePos.addItem("1")
        keybytePos.addItem("2")
        keybytePos.addItem("3")
        keybytePos.addItem("4")
        keybytePos.addItem("5")
        keybytePos.addItem("6")
        keybytePos.addItem("7")
        keybytePos.addItem("8")
        keybytePos.addItem("9")
        keybytePos.addItem("A")
        keybytePos.addItem("B")
        keybytePos.addItem("C")
        keybytePos.addItem("D")
        keybytePos.addItem("E")
        keybytePos.addItem("F")
        keybytePosh = QPushButton("?")
        hori.addWidget(keybytePos, 40)
        hori.addWidget(keybytePosh, 1)
        vert.addLayout(hori)
        t2keybyte.setLayout(vert)
        t2sharedLayout.addWidget(t2keybyte)

        t2iter = QWidget()
        hori = QHBoxLayout()
        vert = QVBoxLayout()
        labels = QHBoxLayout()
        labels.addWidget(QLabel("Number of traces"))
        labels.addWidget(QLabel("Iterations"))
        vert.addLayout(labels)
        numtraces = QLineEdit("50")
        numiter = QLineEdit("100")
        numiterh = QPushButton("?")
        hori.addWidget(numtraces, 40)
        hori.addWidget(numiter, 40)
        hori.addWidget(numiterh, 1)
        vert.addLayout(hori)
        t2iter.setLayout(vert)
        t2sharedLayout.addWidget(t2iter)

        t2sharedGroup.setLayout(t2sharedLayout)
        t2lLayout.addWidget(t2sharedGroup)

        # SELECTION GROUP 1
        t2Group1 = QWidget()
        t2Group1Layout = QVBoxLayout()
        t2art = QWidget()
        t2artLayout = QHBoxLayout()
        art = QPushButton("run average rank test")
        arth = QPushButton("?")
        t2artLayout.addWidget(art, 40)
        t2artLayout.addWidget(arth, 1)
        t2art.setLayout(t2artLayout)
        t2Group1Layout.addWidget(t2art)

        t2Group1.setLayout(t2Group1Layout)
        t2lLayout.addWidget(t2Group1)

        # SELECTION GROUP 2
        t2Group2 = QWidget()
        t2ftstLayout = QHBoxLayout()
        tab2ftst = QPushButton("run first trace success test")
        tab2ftsth = QPushButton("?")
        t2ftstLayout.addWidget(tab2ftst, 40)
        t2ftstLayout.addWidget(tab2ftsth, 1)
        t2Group2.setLayout(t2ftstLayout)
        t2Group2.hide()
        t2lLayout.addWidget(t2Group2)

        # SELECTION GROUP 3
        t2Group3 = QWidget()
        t2fkLayout = QHBoxLayout()
        tab2fk = QPushButton("run whole key test")
        tab2fkh = QPushButton("?")
        t2fkLayout.addWidget(tab2fk, 40)
        t2fkLayout.addWidget(tab2fkh, 1)
        t2Group3.setLayout(t2fkLayout)
        t2Group3.hide()
        t2lLayout.addWidget(t2Group3)

        self.tab2.setLayout(t2lLayout)

        # A lot of local functions will be used as well as some
        # "global" (bound to super) functions.
        # The following is a list of functions that will be used on
        # buttons presses or text changes
        # Naming convention: info = update right hand side info column.
        def filebrowserinfo():
            info = "Browse for files to add to the list in the text editor. " \
                   "Trained models are of type .h5 while history files and " \
                   "raw results data are .npz or .npy."
            self.updateInfo(info, self.tabs.currentIndex())

        def selectedinfo():
            info = "This is an editable list of files currently selected. " \
                   "You can edit it by just deleting text. This flexibility " \
                   "comes at the price of fault tolerance. Never remove the " \
                   "first line and never enter non-file non-empty strings " \
                   "on a line. Make sure you enter the correct files for " \
                   "your purposes."
            self.updateInfo(info, self.tabs.currentIndex())

        def dropdowninfo():
            info = "Use the dropdown menu to select which script to run " \
                   "on the selected files. It is up to you as the user " \
                   "to not make a mistake..."
            self.updateInfo(info, self.tabs.currentIndex())

        def artinfo():
            info = "Run the average rank test for all selected models. " \
                   "Graphs of results are saved in results/pdf and " \
                   "numerical results are saved in results/npy. Due to " \
                   "how the test works you must use a fixed key for this test."
            self.updateInfo(info, self.tabs.currentIndex())

        def ftstinfo():
            info = "Run the first trace success test for all selected models." \
                   " Graphs of results are saved in results/pdf and numerical" \
                   " results are saved in results/npy."
            self.updateInfo(info, self.tabs.currentIndex())

        def fullkeyinfo():
            info = "Runs the full key recovery test. WARNING! This test " \
                   "is EXTREMELY time consuming. Also it currently does " \
                   "not plot the info for you automatically. Due to how " \
                   "the test works you must use a fixed key for this test."
            self.updateInfo(info, self.tabs.currentIndex())

        def intervalinfo():
            info = "Set the interval for the first keybyte position " \
                   "to correspond to your model's input size. Subsequent " \
                   "keybytes will be calculated from this."
            self.updateInfo(info, self.tabs.currentIndex())

        def keybyteinfo():
            info = "select which keybyte position to attack using " \
                   "selected models. Best success is typically attacking " \
                   "the same position as trained on. This creates an " \
                   "offset between the base interval e.g. [57:153] and " \
                   "the attacked interval e.g. [249:345]"
            self.updateInfo(info, self.tabs.currentIndex())

        def iterinfo():
            info = "set the number of traces to plot and the number of " \
                   "test iterations to run for your average results. " \
                   "Default numbers provided that are suitable for " \
                   "quick testing of example model."
            self.updateInfo(info, self.tabs.currentIndex())

        def textchanget2():
            temp = self.tab2.textEdit.toPlainText()
            self.updateSelected(temp, ignore=1, current=self.tabs.currentIndex())

        def clickedt2b1():
            self.openFileNamesDialog()

        def clickedConfirm():
            print(self.selectedString)

        def avgrank():
            traces = numtraces.text()
            iterations = numiter.text()
            interval = traceInterval.text()
            tracestart = re.search("(\d+):(\d+)", interval).group(1)
            traceend = re.search("(\d+):(\d+)", interval).group(2)
            keybytepos = keybytePos.currentIndex()
            alert = QMessageBox()
            alert.setText("choose trace file. Fixed key")
            alert.exec_()
            tracefile = self.openTracesDialog()
            if not tracefile:
                return
            alert.setText("choose plaintext file")
            alert.exec_()
            ptfile = self.openTracesDialog()
            if not ptfile:
                return
            alert.setText("choose keylist file. Fixed key.")
            alert.exec_()
            keyfile = self.openTracesDialog()
            if not keyfile:
                return
            models = self.splitter(self.selectedString)
            subprocess.call(
                [
                    "python",
                    "scripts/average_rank_test.py",
                    str(traces),
                    str(iterations),
                    str(tracestart),
                    str(traceend),
                    str(keybytepos),
                    tracefile,
                    ptfile,
                    keyfile,
                ]
                + models[1:]
            )

        def ftst():
            traces = numtraces.text()
            iterations = numiter.text()
            interval = traceInterval.text()
            tracestart = re.search("(\d+):(\d+)", interval).group(1)
            traceend = re.search("(\d+):(\d+)", interval).group(2)
            keybytepos = keybytePos.currentIndex()
            alert = QMessageBox()
            alert.setText("choose trace file")
            alert.exec_()
            tracefile = self.openTracesDialog()
            if not tracefile:
                return
            alert.setText("choose plaintext file")
            alert.exec_()
            ptfile = self.openTracesDialog()
            if not ptfile:
                return
            alert.setText("choose keylist file")
            alert.exec_()
            keyfile = self.openTracesDialog()
            if not keyfile:
                return
            models = self.splitter(self.selectedString)
            subprocess.call(
                [
                    "python",
                    "scripts/first_trace_success_test.py",
                    str(traces),
                    str(iterations),
                    str(tracestart),
                    str(traceend),
                    str(keybytepos),
                    tracefile,
                    ptfile,
                    keyfile,
                ]
                + models[1:]
            )

        def fullkey():
            traces = numtraces.text()
            iterations = numiter.text()
            interval = traceInterval.text()
            tracestart = re.search("(\d+):(\d+)", interval).group(1)
            traceend = re.search("(\d+):(\d+)", interval).group(2)
            keybytepos = keybytePos.currentIndex()
            alert = QMessageBox()
            alert.setText("WARNING! This test takes a very long time")
            alert.exec_()
            alert.setText("choose trace file. Fixed key.")
            alert.exec_()
            tracefile = self.openTracesDialog()
            if not tracefile:
                return
            alert.setText("choose plaintext file")
            alert.exec_()
            ptfile = self.openTracesDialog()
            if not ptfile:
                return
            alert.setText("choose keylist file. Fixed key.")
            alert.exec_()
            keyfile = self.openTracesDialog()
            if not keyfile:
                return

            models = self.splitter(self.selectedString)
            subprocess.call(
                [
                    "python",
                    "scripts/whole_key_test.py",
                    str(traces),
                    str(iterations),
                    str(tracestart),
                    str(traceend),
                    tracefile,
                    ptfile,
                    keyfile,
                ]
                + models[1:]
            )

        def selection(i):
            if i == 0:
                t2Group1.show()
                t2Group2.hide()
                t2Group3.hide()
                t2iter.show()
                t2keybyte.show()

            if i == 1:
                t2Group1.hide()
                t2Group2.show()
                t2Group3.hide()
                t2iter.hide()
                t2keybyte.show()

            if i == 2:
                t2Group1.hide()
                t2Group2.hide()
                t2Group3.show()
                t2iter.show()
                t2keybyte.hide()

        # Actually bind the scripts to the buttons and textedits.
        # This needs to be defined after the
        # functions they will be used which is why they are hidden down here
        tab2Button1.clicked.connect(clickedt2b1)
        tab2Button1h.clicked.connect(filebrowserinfo)
        tab2Texth.clicked.connect(selectedinfo)
        t2dropdownh.clicked.connect(dropdowninfo)
        tab2ftst.clicked.connect(ftst)
        tab2ftsth.clicked.connect(ftstinfo)
        traceIntervalh.clicked.connect(intervalinfo)
        keybytePosh.clicked.connect(keybyteinfo)
        numiterh.clicked.connect(iterinfo)
        art.clicked.connect(avgrank)
        arth.clicked.connect(artinfo)
        tab2fk.clicked.connect(fullkey)
        tab2fkh.clicked.connect(fullkeyinfo)
        self.tab2.textEdit.textChanged.connect(textchanget2)
        t2dropdown.currentIndexChanged.connect(selection)

    def createT3L(self):
        self.tab3 = QWidget()
        t3lLayout = QVBoxLayout(self)

        # File browser
        t3b1Widget = QWidget()
        hori = QHBoxLayout()
        vert = QVBoxLayout()
        vert.addWidget(QLabel("File browser"))
        tab3Button1 = QPushButton("Files")
        tab3Button1h = QPushButton("?")
        hori.addWidget(tab3Button1, 40)
        hori.addWidget(tab3Button1h, 1)
        vert.addLayout(hori)
        t3b1Widget.setLayout(vert)
        t3lLayout.addWidget(t3b1Widget)

        # Selected files window
        self.tab3TextWidget = QWidget()
        hori = QHBoxLayout()
        vert = QVBoxLayout()
        vert.addWidget(QLabel("Selected files"))
        self.tab3.textEdit = QTextEdit()
        self.tab3.textEdit.setPlainText(self.selectedString)
        tab3Texth = QPushButton("?")
        hori.addWidget(self.tab3.textEdit, 40)
        hori.addWidget(tab3Texth, 1)
        vert.addLayout(hori)
        self.tab3TextWidget.setLayout(vert)
        t3lLayout.addWidget(self.tab3TextWidget)

        t3dropdownWidget = QWidget()
        hori = QHBoxLayout()
        vert = QVBoxLayout()
        vert.addWidget(QLabel("Script selector"))
        t3dropdown = QComboBox()
        t3dropdown.addItem("Unzip .tar.zip traces")
        t3dropdown.addItem("Model Input Shape")
        t3dropdown.addItem("Model Summary")
        t3dropdown.addItem("Plot History Files")
        t3dropdown.addItem("Plot a trace")
        t3dropdownh = QPushButton("?")
        hori.addWidget(t3dropdown, 40)
        hori.addWidget(t3dropdownh, 1)
        vert.addLayout(hori)
        t3dropdownWidget.setLayout(vert)
        t3lLayout.addWidget(t3dropdownWidget)

        # SELECTION GROUP 1
        t3Group1 = QWidget()
        unzipperLayout = QHBoxLayout()
        unzipper = QPushButton("Unzip")
        unzipperh = QPushButton("?")
        unzipperLayout.addWidget(unzipper, 40)
        unzipperLayout.addWidget(unzipperh, 1)
        t3Group1.setLayout(unzipperLayout)
        t3lLayout.addWidget(t3Group1)

        # SELECTION GROUP 2
        t3Group2 = QWidget()
        inputShapeLayout = QHBoxLayout()
        inShape = QPushButton("Print Model Input Shapes")
        inShapeh = QPushButton("?")
        inputShapeLayout.addWidget(inShape, 40)
        inputShapeLayout.addWidget(inShapeh, 1)
        t3Group2.setLayout(inputShapeLayout)
        t3Group2.hide()
        t3lLayout.addWidget(t3Group2)

        # SELECTION GROUP 3
        t3Group3 = QWidget()
        summaryLayout = QHBoxLayout()
        modelSummary = QPushButton("Print Model Summary")
        modelSummaryh = QPushButton("?")
        summaryLayout.addWidget(modelSummary, 40)
        summaryLayout.addWidget(modelSummaryh, 1)
        t3Group3.setLayout(summaryLayout)
        t3Group3.hide()
        t3lLayout.addWidget(t3Group3)

        # SELECTION GROUP 4
        t3Group4 = QWidget()
        historyLayout = QHBoxLayout()
        plotHistory = QPushButton("Plot History Files")
        plotHistoryh = QPushButton("?")
        historyLayout.addWidget(plotHistory, 40)
        historyLayout.addWidget(plotHistoryh, 1)
        t3Group4.setLayout(historyLayout)
        t3Group4.hide()
        t3lLayout.addWidget(t3Group4)

        # SELECTION GROUP 5
        t3Group5 = QWidget()
        traceLayout = QHBoxLayout()
        plotTrace = QPushButton("Plot Trace")
        plotTraceh = QPushButton("?")
        traceLayout.addWidget(plotTrace, 40)
        traceLayout.addWidget(plotTraceh, 1)
        t3Group5.setLayout(traceLayout)
        t3Group5.hide()
        t3lLayout.addWidget(t3Group5)

        self.tab3.setLayout(t3lLayout)

        def textchanget3():
            temp = self.tab3.textEdit.toPlainText()
            self.updateSelected(
                temp, ignore=2, current=self.tabs.currentIndex()
            )

        def clickedt3b1():
            self.openFileNamesDialog()

        def filebrowserinfo():
            info = "Browse for files to add to the list in the text editor." \
                   " Trained models are of type .h5 while history files and" \
                   " raw results data are .npz or .npy."
            self.updateInfo(info, self.tabs.currentIndex())

        def selectedinfo():
            info = "This is an editable list of files currently selected." \
                   " You can edit it by just deleting text." \
                   " This flexibility comes at the price of fault tolerance." \
                   " Never remove the first line and never enter non-file" \
                   " non-empty strings on a line. Make sure you enter the" \
                   " correct files for your purposes."
            self.updateInfo(info, self.tabs.currentIndex())

        def dropdowninfo():
            info = "Use the dropdown menu to select which script to run on " \
                   "the selected files. It is up to you as the user to not " \
                   "make a mistake..."
            self.updateInfo(info, self.tabs.currentIndex())

        def unzipperinfo():
            info = "If given .tar.zip files containing traces and other " \
                   "files in the format of YYYY.MM.DD-HH.MM.SS_traces.npy " \
                   "it will automatically create and combine the traces " \
                   "and Sbox labels"
            self.updateInfo(info, self.tabs.currentIndex())

        def inshapeinfo():
            info = "A script for printing the input shape of all models " \
                   "selected."
            self.updateInfo(info, self.tabs.currentIndex())

        def summaryinfo():
            info = "A script for printing the model summary of all models " \
                   "selected."
            self.updateInfo(info, self.tabs.currentIndex())

        def historyinfo():
            info = "A script for plotting all selected history files from " \
                   "trained models. These should be .npz files."
            self.updateInfo(info, self.tabs.currentIndex())

        def traceinfo():
            info = "A script for plotting a randomly selected trace from " \
                   "each selected trace file. Make sure to only select " \
                   "trace files for this."
            self.updateInfo(info, self.tabs.currentIndex())

        def summary():
            args = self.splitter(self.selectedString)
            subprocess.call(["python", "scripts/model_summary.py"] + args[1:])

        def inputshape():
            args = self.splitter(self.selectedString)
            subprocess.call(["python", "scripts/input_shape.py"] + args[1:])

        def historyplotter():
            args = self.splitter(self.selectedString)
            subprocess.call(["python", "scripts/plot_history.py"] + args[1:])

        def traceplot():
            args = self.splitter(self.selectedString)
            subprocess.call(["python", "scripts/trace_plotter.py"] + args[1:])

        def unzip():
            args = self.splitter(self.selectedString)
            subprocess.call(["python", "scripts/unzipper.py"] + args[1:])

        def selection(i):
            if i == 0:
                t3Group1.show()
                t3Group2.hide()
                t3Group3.hide()
                t3Group4.hide()
                t3Group5.hide()

            if i == 1:
                t3Group1.hide()
                t3Group2.show()
                t3Group3.hide()
                t3Group4.hide()
                t3Group5.hide()

            if i == 2:
                t3Group1.hide()
                t3Group2.hide()
                t3Group3.show()
                t3Group4.hide()
                t3Group5.hide()

            if i == 3:
                t3Group1.hide()
                t3Group2.hide()
                t3Group3.hide()
                t3Group4.show()
                t3Group5.hide()

            if i == 4:
                t3Group1.hide()
                t3Group2.hide()
                t3Group3.hide()
                t3Group4.hide()
                t3Group5.show()

        # For some reason this code does not work.
        # Left in here just in case a solution is found
        # because it would make it easier to introduce
        # new elements into the program
        # One would have to comment out (or remove) the
        # above if clauses
        #            for j in range(t3dropdown.count()):
        #                x = "t3Group"+str(j+1)
        #                print(str(i+1) in x[-1:])
        #                print(x)
        #                if str(i+1) in x[-1:]:
        #                     exec("%s.show()" % (x))
        #                else:
        #                     exec("%s.hide()" % (x))
        #            print("")

        tab3Button1.clicked.connect(clickedt3b1)
        tab3Button1h.clicked.connect(filebrowserinfo)
        plotHistory.clicked.connect(historyplotter)
        t3dropdownh.clicked.connect(dropdowninfo)
        unzipper.clicked.connect(unzip)
        unzipperh.clicked.connect(unzipperinfo)
        inShape.clicked.connect(inputshape)
        inShapeh.clicked.connect(inshapeinfo)
        modelSummary.clicked.connect(summary)
        modelSummaryh.clicked.connect(summaryinfo)
        plotHistoryh.clicked.connect(historyinfo)
        plotTrace.clicked.connect(traceplot)
        plotTraceh.clicked.connect(traceinfo)
        tab3Texth.clicked.connect(selectedinfo)
        self.tab3.textEdit.textChanged.connect(textchanget3)
        t3dropdown.currentIndexChanged.connect(selection)

    # The following three definitions are for right hand side of tabs,
    # used for displaying info.
    def createT1R(self):
        self.T1R = QWidget()
        self.T1R.setMinimumWidth(self.screenMode * 75)
        t1rLayout = QVBoxLayout(self)
        self.tab1info = QLabel()
        self.tab1info.setWordWrap(True)
        self.tab1info.setText("press the ? buttons to get more info")
        t1rLayout.addWidget(self.tab1info)
        self.T1R.setLayout(t1rLayout)

    def createT2R(self):
        self.T2R = QWidget()
        self.T2R.setMinimumWidth(self.screenMode * 75)
        t2rLayout = QVBoxLayout(self)
        self.tab2info = QLabel()
        self.tab2info.setWordWrap(True)
        self.tab2info.setText("press the ? buttons to get more info")
        t2rLayout.addWidget(self.tab2info)
        self.T2R.setLayout(t2rLayout)

    def createT3R(self):
        self.T3R = QWidget()
        self.T3R.setMinimumWidth(self.screenMode * 75)
        t3rLayout = QVBoxLayout(self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        self.T3R.setSizePolicy(sizePolicy)
        self.tab3info = QLabel()
        self.tab3info.setWordWrap(True)
        self.tab3info.setText("press the ? buttons to get more info")
        t3rLayout.addWidget(self.tab3info)
        self.T3R.setLayout(t3rLayout)

    # The actual tabs. Naming convention will have to be changed
    # to be consistent later.
    # These are basically just containers holding the two halves of each tab.
    def createT1(self):
        self.T1 = QGroupBox()
        t1Layout = QHBoxLayout()
        self.createT1L()
        self.createT1R()
        if self.screenMode < 4:
            self.T1R.setMaximumWidth(100)
        else:
            self.T1R.setMaximumWidth(300)
        t1Layout.addWidget(self.tab1)
        t1Layout.addWidget(self.T1R)
        self.T1.setLayout(t1Layout)

    def createT2(self):
        self.T2 = QGroupBox()
        t2Layout = QHBoxLayout()
        self.createT2L()
        self.createT2R()
        if self.screenMode < 4:
            self.T2R.setMaximumWidth(100)
        else:
            self.T2R.setMaximumWidth(300)
        t2Layout.addWidget(self.tab2)
        t2Layout.addWidget(self.T2R)
        self.T2.setLayout(t2Layout)

    def createT3(self):
        self.T3 = QGroupBox()
        t3Layout = QHBoxLayout()
        self.createT3L()
        self.createT3R()
        if self.screenMode < 4:
            self.T3R.setMaximumWidth(100)
        else:
            self.T3R.setMaximumWidth(300)
        t3Layout.addWidget(self.tab3)
        t3Layout.addWidget(self.T3R)
        self.T3.setLayout(t3Layout)

    # File browser used to load files if you didn't use the terminal for that.
    def openFileNamesDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "File Browser",
            "",
            "All Files (*);;Model Files (*.h5);;Numpy Arrays (*.npy);;Numpy Zipfiles (*.npz)",
            options=options,
        )
        if files:
            temp = self.selectedString
            for i in files:
                temp = temp + "\n" + i
            self.updateSelected(temp)

    def openTracesDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(
            self, "Trace Browser", "", "Numpy Arrays (*.npy)", options=options
        )
        if fileName:
            return fileName
        else:
            return False

    # Updates and synchronizes the loaded file lists on t2 and t3.
    # The conditionals prevent infinite recursion.
    def updateSelected(self, newSelected, ignore=0, current=0):
        self.selectedString = newSelected
        if ignore is not 1:
            if current is not 1:
                self.tab2.textEdit.setPlainText(self.selectedString)
        if ignore is not 2:
            if current is not 2:
                self.tab3.textEdit.setPlainText(self.selectedString)

    # Update the right hand side info bar with whatever query the user clicked.
    def updateInfo(self, info, tabnumber):
        if tabnumber == 0:
            self.tab1info.setText(info)

        if tabnumber == 1:
            self.tab2info.setText(info)

        if tabnumber == 2:
            self.tab3info.setText(info)

    # I don't think this is used anymore? Probably old debugging thing.
    # Will be removed if it turns out it is useless.
    def tabSwitch(self):
        print(str(self.tabs.currentIndex()))
        if self.tabs.currentIndex() is not 0:
            if self.tabs.currentIndex() == 1:
                temp = self.tab2.textEdit.toPlainText()
                self.updateSelected(temp)
            if self.tabs.currentIndex() == 2:
                temp = self.tab3.textEdit.toPlainText()
                self.updateSelected(temp)
        self.updateSelected(self.selectedString)

    # Script for splitting the string stored in the text edit into a
    # list strings
    # to send as args for the linked scripts
    def splitter(self, s):
        return [line.strip() for line in s.splitlines() if line.strip()]


if __name__ == "__main__":
    #    appctxt = ApplicationContext()
    app = QApplication(sys.argv)
    gallery = WidgetGallery()
    gallery.show()
    sys.exit(app.exec_())
