import sys

# from PyQt6.QtWidgets import QApplication,QGridLayout,QComboBox,QInputDialog,QGraphicsLineItem,QGraphicsTextItem,QRadioButton,QGraphicsScene,QHeaderView,QAbstractItemView, QGraphicsView,QScrollArea, QGraphicsView, QTableWidgetItem,QFrame, QWidget,QToolBar, QSpacerItem,QMainWindow, QFileDialog, QLabel, QMenu, QPushButton, QVBoxLayout, QStatusBar, QHBoxLayout, QLineEdit, QMessageBox
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *

# from PyQt6.QtGui import QBrush,QIcon,QPen, QFont, QCursor, QAction, QShortcut, QKeySequence, QColor, QPalette, QPainter, QMouseEvent, QPixmap
# from PyQt6.QtCore import QTimer, Qt, QPoint, QUrl, QSize, QPoint,QEvent, pyqtSignal, pyqtSlot
from PyQt6.QtCore import *
from PyQt6.QtCharts import *
from PyQt6.QtPrintSupport import *
from PyQt6 import uic
from ui_aboutGMAA import Ui_AboutGMAA
from ui_guiGMAA import Ui_MainWindow
from ui_LogIn import Ui_LogIn
from ui_nodeInformation import Ui_MainWindow
from ui_alternativeConsequences import Ui_MainWindow
from ui_modifyAltCon import Ui_ModifyAltCon
from ui_componentsUtilitiesView import Ui_componentsUtilitiesView
from ui_viewingTWeights import Ui_ViewingTotalWeights
from ui_linearUtilityFunction import Ui_linearUtilityFunction
from ui_utilitiesDiscreteAttributes import Ui_UtilitiesDiscreteAttributes
from AlternativeClassification_ui import Ui_MainWindow
import networkx as nx  # With this library we can save and import any proyect thanks to XML
import xml.etree.ElementTree as ET  # XML serialisation library to convert the data structure to an XML file
import os
import math
import re
import ast  # Abstract Syntax Trees
import traceback

# global variables

PrimaryObjective = False
Branch = 0
Leaf = 0
identifier_labels = 0
currentRow = 0
currentColumn = 0
attributes = []
attributesnames = []
alternatives = []
labels = []

# this is the root for the 'xml' file

root = ET.Element("QLabels")

# # This class is embodied in 'WindowPrincipalGMAA(QMainWindow)' and we set
# up a layout of QGridLayout() that allows to structure the labels and lines by
# rows and columns in order to make a correct implementation and fit the spaces
# well


class MyWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setContentsMargins(200, 200, 200, 200)


# This is the main window of the application where the QMenu, the QToolBar,
# QScrollArea, MyWidget(QWidget), etc. are located


class VentanaPrincipalGMAA(QMainWindow):

    # signals
    # textChanged = pyqtSignal(str)

    def __init__(self):
        super(VentanaPrincipalGMAA, self).__init__()
        uic.loadUi("guiGMAA.ui", self)
        # carga el icono desde un archivo de imagen
        icono = QIcon("iconoUPM.ico")
        super(VentanaPrincipalGMAA, self).setWindowIcon(
            icono
        )  # establece el icono de la ventana
        super(VentanaPrincipalGMAA, self).setWindowTitle(
            "GMAA (Generic Multi-Attribute Analysis)"
        )
        super(VentanaPrincipalGMAA, self).statusBar().showMessage("Current WorkSpace: ")

        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.central_widget = MyWidget(self)
        self.setCentralWidget(self.central_widget)
        self.layout = QGridLayout()

        self.central_widget.setLayout(self.layout)
        self.scroll_area.setWidget(self.central_widget)

        self.scroll_area.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOn
        )
        self.scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOn
        )

        self.setCentralWidget(self.scroll_area)

        # self.botonDesactivar = self.findChild(QPushButton, "botonDesactivar")

        # Initial Options

        # self.InitLabel1 = InitialOptionLabels("New Project")
        # self.InitLabel1.setObjectName("New Project")
        # self.InitLabel1.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)
        # self.InitLabel2 = InitialOptionLabels("Open Project")
        # self.InitLabel2.setObjectName("Open Project")

        self.UPMLogoInit = QLabel()
        pixmap = QPixmap("images/Fondo_GMAA.png")
        # pixmap = QPixmap("images/LOGOTIPO leyenda color PNG.png")
        scaled_pixmap = pixmap.scaled(
            QSize(1000, 1000), Qt.AspectRatioMode.KeepAspectRatio
        )
        self.UPMLogoInit.setPixmap(scaled_pixmap)
        self.layout.addWidget(self.UPMLogoInit, 0, 0)

        # self.InitLabel2.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter)
        # self.UPMLogoInit = QLabel()
        # pixmap = QPixmap("images/Fondo_GMAA.png")
        # # pixmap = QPixmap("images/LOGOTIPO leyenda color PNG.png")
        # scaled_pixmap = pixmap.scaled(self.UPMLogoInit.size(), Qt.AspectRatioMode.KeepAspectRatio)
        # self.UPMLogoInit.setPixmap(scaled_pixmap)
        # self.layout.addWidget(self.UPMLogoInit,0,0)
        # self.layout.addWidget(self.InitLabel1,1,0)
        # self.layout.addWidget(self.InitLabel2,2,0)
        self.layout.setAlignment(
            Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter
        )
        self.setStyleSheet("background-color: #13376A")
        self.menubar.setStyleSheet("background-color: #F0F0F0")
        self.menuWindow.setStyleSheet("background-color: #F0F0F0")
        self.toolBarWGMAA.setStyleSheet("background-color: #F0F0F0")
        self.statusBar.setStyleSheet("background-color: #F0F0F0")

        # Labels created
        self.labels = []

        # Lines created
        self.lineB = []
        self.lines = []

        # Saves the previous value in the Save QInputDialog
        self.previous_value = None

        # pressed New Workspace button variable
        self.pressedNW = False

        # Context Menu Creation
        self.context_menuPO = QMenu(self)

        # Enable context menu in the main widget
        # self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        # self.customContextMenuRequested.connect(self.show_context_menuPO)

        # Initial Menu Buttons
        # self.InitLabel1.clicked.connect(self.remove_initial)
        # self.InitLabel2.clicked.connect(self.open_workspace2)

        # Action to create the PrimaryObjective Label
        self.actionCPO = QAction("Create a Primary Objective", self)
        # create_PO function to create the PO first Label
        self.actionCPO.triggered.connect(self.new_workspace)

        # # Action to create the Brach/Leaf Labels
        # self.actionCBL = QAction("Create Branches/Leaf", self)
        # self.actionCBL.triggered.connect(self.create_BL)

        # Action to delete the Primary Objective Label
        self.actionDPO = QAction("Delete Primary Objective", self)
        self.actionDPO.triggered.connect(self.delete_PO)

        # Adding actions to de the Context Menu Created
        self.context_menuPO.addAction(self.actionCPO)

        # connect Menu signals
        self.actionCredits.triggered.connect(self.fn_help)
        self.actionLogOut.triggered.connect(self.fn_login)
        self.actionNew_Workspace.triggered.connect(self.new_workspace)
        self.actionOpen_Workspace.triggered.connect(self.open_workspace)
        self.actionSave_WorkSpace.triggered.connect(self.save_proInput)
        self.actionSave_WorkSpace_As.triggered.connect(self.save_proInput)
        self.actionClose_WorkSpace.triggered.connect(self.close_workspace)

        # connect View Alternative signals
        self.actionView_Total_Weights.triggered.connect(self.open_VTW)
        self.actionView_Component_Utilities.triggered.connect(self.open_VCU)
        self.actionView_Alt_Consequences.triggered.connect(self.open_AltCon)

        # connect Toolbar signals
        self.actionNewWorkspace.triggered.connect(self.new_workspace)
        self.actionExistingWorkspace.triggered.connect(self.open_workspace)
        self.actionSaveWorkspace.triggered.connect(self.save_proInput)
        # -----------------------
        self.actionViewComponentUtilities.triggered.connect(self.open_VCU)
        self.actionAltConsequences.triggered.connect(self.open_AltCon)
        self.actionViewTotalWeights.triggered.connect(self.open_VTW)
        self.actionPrinter.triggered.connect(self.open_AltClas)

        # -----------------------
        self.actionLightBulb.triggered.connect(self.fn_help)
        # self.actionPrinter.triggered.connect(self.print_workspace)

        # Inhabilitamos todos los botones hasta que no se cree o importe un WorkSpace

        self.actionSaveWorkspace.setObjectName("actionSaveWorkspace")
        self.actionViewComponentUtilities.setEnabled(False)
        self.actionAltConsequences.setEnabled(False)
        self.actionViewTotalWeights.setEnabled(False)
        self.actionAltClassification.setEnabled(False)
        self.actionWeightStabilityIntervals.setEnabled(False)
        self.actionDPOptimality.setEnabled(False)
        self.actionSimulatorTechniques.setEnabled(False)
        self.actionPrinter.setEnabled(False)
        if len(self.labels) == 0:
            self.actionSaveWorkspace.setEnabled(False)
            self.actionSave_WorkSpace.setEnabled(False)
            self.actionSave_WorkSpace_As.setEnabled(False)
        else:
            self.actionSaveWorkspace.setEnabled(True)
            self.actionSave_WorkSpace.setEnabled(True)
            self.actionSave_WorkSpace_As.setEnabled(True)

        # self.textEdit.textChanged.connect(self.fn_toolbarSave) # Si se escribe texto el icono printer se habilita

        # Exit Button
        self.actionExit.triggered.connect(self.close_window)

    def fn_help(self):
        vHelp = VentanaHelp(self)
        vHelp.show()

    # opens log in window

    def fn_login(self):
        vLogin = VentanaLogIn(self)
        vLogin.show()

    # removes the previously inserted widget to display different types
    # of options in the direct assignment method in the line chart.

    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.setParent(None)
            else:
                self.clear_layout(item.layout())

    # allows to know which nodes are the final ones and
    # collects them in the global variables attributes and attributesnames.

    def getFinalAttributes(self, finalNodes):
        global attributes
        global attributesnames
        attributes.clear()
        attributesnames.clear()

        for node in finalNodes:
            if not node.connections:
                node.finalNode = True
                attributes.append(node)
                attributesnames.append(node.text())

    # shows the initial screen once the buttons to create a new
    # project or open an existing one are pressed.

    def remove_initial(self):
        self.UPMLogoInit.deleteLater()
        # self.InitLabel1.deleteLater()
        # self.InitLabel2.deleteLater()
        self.setStyleSheet("background-color: ")
        self.menubar.setStyleSheet("background-color: ")
        self.menuWindow.setStyleSheet("background-color: ")
        self.toolBarWGMAA.setStyleSheet("background-color: ")
        self.statusBar.setStyleSheet("background-color: ")
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.central_widget = MyWidget(self)
        self.setCentralWidget(self.central_widget)
        self.layout = QGridLayout()
        self.central_widget.setLayout(self.layout)
        self.scroll_area.setWidget(self.central_widget)

        self.scroll_area.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOn
        )
        self.scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOn
        )

        self.setCentralWidget(self.scroll_area)

    # directly displays a new workspace where the user's 'Overall
    # Objective' appears and is prepared for the user to use the following dynamic
    # functions of the application.

    def new_workspace(self):
        global PrimaryObjective
        global currentColumn
        global currentRow
        global Branch
        global identifier_labels
        global Leaf

        # Enable context menu in the main widget
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menuPO)

        try:
            if self.pressedNW:
                reply = QMessageBox.question(
                    self,
                    "Save Changes?",
                    "Do you want to save changes before creating a new workspace?",
                    QMessageBox.StandardButton.Yes
                    | QMessageBox.StandardButton.No
                    | QMessageBox.StandardButton.Cancel,
                )
                if reply == QMessageBox.StandardButton.Cancel:
                    pass
                elif reply == QMessageBox.StandardButton.Yes:
                    self.save_proInput()
                    for label in self.labels:
                        label.deleteLater()
                    self.labels.clear()
                    PrimaryObjective = False
                    Branch = 0
                    Leaf = 0  # if the delete button of the PO Label is triggered the num of Leaf is 0
                    identifier_labels = 0
                    currentRow = 0
                    currentColumn = 0
                    self.setStyleSheet("background-color: ")
                    self.menubar.setStyleSheet("background-color: ")
                    self.menuWindow.setStyleSheet("background-color: ")
                    self.toolBarWGMAA.setStyleSheet("background-color: ")
                    self.statusBar.setStyleSheet("background-color: ")
                    self.scroll_area = QScrollArea(self)
                    self.scroll_area.setWidgetResizable(True)
                    self.central_widget = MyWidget(self)
                    self.setCentralWidget(self.central_widget)
                    self.layout = QGridLayout()
                    self.central_widget.setLayout(self.layout)
                    self.scroll_area.setWidget(self.central_widget)
                    self.scroll_area.setVerticalScrollBarPolicy(
                        Qt.ScrollBarPolicy.ScrollBarAlwaysOn
                    )
                    self.scroll_area.setHorizontalScrollBarPolicy(
                        Qt.ScrollBarPolicy.ScrollBarAlwaysOn
                    )
                    self.setCentralWidget(self.scroll_area)

                    labelPO = LabelNode(
                        identifier=identifier_labels,
                        text="Ov. Objective",
                        label_name=f"Ov.Objective/PO Label{identifier_labels}",
                        posArray=0,
                        cRow=2,
                        cColumn=0,
                    )
                    identifier_labels += 1
                    self.labels.append(
                        labelPO
                    )  # adds PO Label to the list of mainwindow labels

                    print(f"P: nº labels in self.labels: {len(self.labels)}")
                    self.actionSaveWorkspace.setEnabled(True)
                    self.actionSave_WorkSpace.setEnabled(True)
                    self.actionSave_WorkSpace_As.setEnabled(True)
                    # print("P: "+str(self.labels[identifier_labels-1].label_name))
                    Leaf = Leaf + 1
                    labelPO.setVisible(True)
                    labelPO.setFixedSize(120, 40)
                    self.layout.addWidget(labelPO, 2, 0)
                    currentColumn += 1

                    # self.setCentralWidget(labelPO)
                    # labelPO.move(200, 100)
                    # labelPO.double_clicked.connect(lambda: self.open_NodeInfo(labelPO.identifier))
                    labelPO.double_clicked.connect(self.open_NodeInfo)

                # XML with ElementTree so that we can save it

                elif reply == QMessageBox.StandardButton.No:
                    for label in self.labels:
                        label.deleteLater()
                    self.labels.clear()
                    PrimaryObjective = False
                    Branch = 0
                    Leaf = 0  # if the delete button of the PO Label is triggered the num of Leaf is 0
                    identifier_labels = 0
                    currentRow = 0
                    currentColumn = 0
                    self.setStyleSheet("background-color: ")
                    self.menubar.setStyleSheet("background-color: ")
                    self.menuWindow.setStyleSheet("background-color: ")
                    self.toolBarWGMAA.setStyleSheet("background-color: ")
                    self.statusBar.setStyleSheet("background-color: ")
                    self.scroll_area = QScrollArea(self)
                    self.scroll_area.setWidgetResizable(True)
                    self.central_widget = MyWidget(self)
                    self.setCentralWidget(self.central_widget)
                    self.layout = QGridLayout()
                    self.central_widget.setLayout(self.layout)
                    self.scroll_area.setWidget(self.central_widget)
                    self.scroll_area.setVerticalScrollBarPolicy(
                        Qt.ScrollBarPolicy.ScrollBarAlwaysOn
                    )
                    self.scroll_area.setHorizontalScrollBarPolicy(
                        Qt.ScrollBarPolicy.ScrollBarAlwaysOn
                    )
                    self.setCentralWidget(self.scroll_area)

                    labelPO = LabelNode(
                        identifier=identifier_labels,
                        text="Ov. Objective",
                        label_name=f"Ov.Objective/PO Label{identifier_labels}",
                        posArray=0,
                        cRow=2,
                        cColumn=0,
                    )
                    identifier_labels += 1
                    self.labels.append(
                        labelPO
                    )  # adds PO Label to the list of mainwindow labels

                    print(f"P: nº labels in self.labels: {len(self.labels)}")
                    self.actionSaveWorkspace.setEnabled(True)
                    self.actionSave_WorkSpace.setEnabled(True)
                    self.actionSave_WorkSpace_As.setEnabled(True)
                    # print("P: "+str(self.labels[identifier_labels-1].label_name))
                    Leaf = Leaf + 1
                    labelPO.setVisible(True)
                    labelPO.setFixedSize(120, 40)
                    self.layout.addWidget(labelPO, 2, 0)
                    currentColumn += 1

                    # self.setCentralWidget(labelPO)
                    # labelPO.move(200, 100)
                    # labelPO.double_clicked.connect(lambda: self.open_NodeInfo(labelPO.identifier))
                    labelPO.double_clicked.connect(self.open_NodeInfo)

                # XML with ElementTree so that we can save it

            if not self.labels and not self.pressedNW:
                self.pressedNW = True
                for label in self.findChildren(QLabel):
                    if label.pixmap():
                        label.deleteLater()
                        self.setStyleSheet("background-color: ")
                        self.menubar.setStyleSheet("background-color: ")
                        self.menuWindow.setStyleSheet("background-color: ")
                        self.toolBarWGMAA.setStyleSheet("background-color: ")
                        self.statusBar.setStyleSheet("background-color: ")
                        self.scroll_area = QScrollArea(self)
                        self.scroll_area.setWidgetResizable(True)
                        self.central_widget = MyWidget(self)
                        self.setCentralWidget(self.central_widget)
                        self.layout = QGridLayout()
                        self.central_widget.setLayout(self.layout)
                        self.scroll_area.setWidget(self.central_widget)
                        self.scroll_area.setVerticalScrollBarPolicy(
                            Qt.ScrollBarPolicy.ScrollBarAlwaysOn
                        )
                        self.scroll_area.setHorizontalScrollBarPolicy(
                            Qt.ScrollBarPolicy.ScrollBarAlwaysOn
                        )
                        self.setCentralWidget(self.scroll_area)

                labelPO = LabelNode(
                    identifier=identifier_labels,
                    text="Ov. Objective",
                    label_name=f"Ov.Objective/PO Label{identifier_labels}",
                    posArray=0,
                    cRow=2,
                    cColumn=0,
                )
                identifier_labels += 1
                self.labels.append(
                    labelPO
                )  # adds PO Label to the list of mainwindow labels

                print(f"P: nº labels in self.labels: {len(self.labels)}")
                self.actionSaveWorkspace.setEnabled(True)
                self.actionSave_WorkSpace.setEnabled(True)
                self.actionSave_WorkSpace_As.setEnabled(True)
                # print("P: "+str(self.labels[identifier_labels-1].label_name))
                Leaf = Leaf + 1
                labelPO.setVisible(True)
                labelPO.setFixedSize(120, 40)
                self.layout.addWidget(labelPO, 2, 0)
                currentColumn += 1

                # self.setCentralWidget(labelPO)
                # labelPO.move(200, 100)
                # labelPO.double_clicked.connect(lambda: self.open_NodeInfo(labelPO.identifier))
                labelPO.double_clicked.connect(self.open_NodeInfo)

                # XML with ElementTree so that we can save it

        except:
            pass

    # once an existing project has been loaded, prepares all lines for
    # positioning in the layout.
    def place_lines(self):

        for line in self.lineB:
            try:
                line.deleteLater()
                self.lineB.pop(line)
            except:
                pass

        for line in self.lines:
            try:
                line.deleteLater()
                self.lines.pop(line)

            except:
                pass
            # self.layout.removeWidget(line)
        if not self.labels:
            return

        labelPO = self.labels[0]
        if labelPO is not None and labelPO.connections:
            connection_listPO = labelPO.connections
            for k in range(len(connection_listPO)):
                if k == 0:
                    line = DLineFrameB()
                    self.layout.addWidget(line, 0, 1, 3, 1)
                    line.lower()
                    self.lineB.append(line)

                else:
                    numero = k * 20
                    connection = connection_listPO[k]
                    line = DLineFrame(
                        dRow=labelPO.cRow,
                        dColumn=connection.cColumn - 1,
                        dNum=numero - 1,
                    )
                    line.dRow = labelPO.cRow
                    line.dColumn = connection.cColumn - 1
                    line.dNum = numero - 1
                    self.layout.addWidget(line, line.dRow, line.dColumn, line.dNum, 2)
                    line.lower()
                    self.lines.append(line)

        for i in range(1, len(self.labels)):
            label = self.labels[i]
            if label.connections:
                for k, connection in enumerate(label.connections):
                    if (k == 0) and (label.cRow == connection.cRow):
                        line = HLineFrame()
                        self.layout.addWidget(
                            line, label.cRow, connection.cColumn - 1, 1, 2
                        )
                        line.lower()
                        self.lines.append(line)
                    else:
                        numero = connection.cRow - label.cRow
                        line = DLineFrame(
                            dRow=label.cRow,
                            dColumn=connection.cColumn - 1,
                            dNum=numero - 1,
                        )
                        line.dRow = label.cRow
                        line.dColumn = connection.cColumn - 1
                        line.dNum = numero - 1
                        self.layout.addWidget(
                            line, line.dRow, line.dColumn, line.dNum + 2, 2
                        )
                        line.lower()
                        self.lines.append(line)
                self.layout.update()

    # checks what node generation it is in, i.e. how far it has moved
    # from the original node.
    def count_parent(self, node):
        if node.padre is None:
            # Si el padre es None, hemos llegado al nodo raíz
            return 0
        else:
            # Si no es None, hay un padre y contamos también ese nodo
            return 1 + self.count_parent(node.padre)

    # opens an existing xml project
    def open_workspace(self):
        global identifier_labels
        global alternatives
        global attributes
        global attributesnames

        file_name, _ = QFileDialog.getOpenFileName(
            self, "Selecciona un archivo XML", "", "Archivos XML (*.xml)"
        )
        if file_name:
            # Process the XML file here
            print(f"P: Archivo seleccionado: {file_name}")
            try:
                self.UPMLogoInit.deleteLater()
                # self.InitLabel1.deleteLater()
                # self.InitLabel2.deleteLater()
            except RuntimeError as e:
                traceback.print_exc()
                pass
            self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
            self.customContextMenuRequested.connect(self.show_context_menuPO)
            self.setStyleSheet("background-color: ")
            self.menubar.setStyleSheet("background-color: ")
            self.menuWindow.setStyleSheet("background-color: ")
            self.toolBarWGMAA.setStyleSheet("background-color: ")
            self.statusBar.setStyleSheet("background-color: ")
            self.scroll_area = QScrollArea(self)
            self.scroll_area.setWidgetResizable(True)
            self.central_widget = MyWidget(self)
            self.setCentralWidget(self.central_widget)
            self.layout = QGridLayout()
            self.central_widget.setLayout(self.layout)
            self.scroll_area.setWidget(self.central_widget)

            self.scroll_area.setVerticalScrollBarPolicy(
                Qt.ScrollBarPolicy.ScrollBarAlwaysOn
            )
            self.scroll_area.setHorizontalScrollBarPolicy(
                Qt.ScrollBarPolicy.ScrollBarAlwaysOn
            )

            self.setCentralWidget(self.scroll_area)

            self.labels.clear()

            tree = ET.parse(file_name)
            root = tree.getroot()
            for child in root:
                if child.tag == "Node":
                    cUnitType = child.get("unitType")
                    if cUnitType == "":
                        label = LabelNode(
                            identifier=int(child.get("id")),
                            text=child.get("text"),
                            cRow=int(child.get("cRow")),
                            cColumn=int(child.get("cColumn")),
                            posArray=int(child.get("posArray")),
                            label_name=child.get("label_name"),
                        )
                        label.connections = child.get("connections")
                        label.nodeDescription = child.get("nodeDescription")
                        label.padre = child.get("padre")
                        label.weightI = float(child.get("weightI"))
                        label.weightS = float(child.get("weightS"))
                        self.labels.append(label)
                        self.layout.addWidget(label, label.cRow, label.cColumn)
                    elif cUnitType == "Continuous":
                        label = LabelNode(
                            identifier=int(child.get("id")),
                            text=child.get("text"),
                            cRow=int(child.get("cRow")),
                            cColumn=int(child.get("cColumn")),
                            posArray=int(child.get("posArray")),
                            label_name=child.get("label_name"),
                        )
                        label.connections = child.get("connections")
                        label.nodeDescription = child.get("nodeDescription")
                        label.unitType = cUnitType
                        label.unitDescription = child.get("unitDescription")
                        label.unitName = child.get("unitName")
                        label.weightI = float(child.get("weightI"))
                        label.weightS = float(child.get("weightS"))
                        label.minRange = int(child.get("minRange"))
                        label.maxRange = int(child.get("maxRange"))
                        label.mostPrefered = child.get("mostPrefered")
                        label.padre = child.get("padre")
                        iPoints = int(child.get("interPoints"))
                        label.interPoints = iPoints
                        if iPoints > 0:
                            for i in range(1, iPoints + 1):
                                variable_name1 = "IP{}1".format(i)
                                valuev1 = float(child.get(variable_name1))
                                variable_name2 = "IP{}2".format(i)
                                valuev2 = float(child.get(variable_name2))
                                variable_name3 = "IPAV{}".format(i)
                                valuev3 = float(child.get(variable_name3))
                                setattr(label, variable_name1, valuev1)
                                setattr(label, variable_name2, valuev2)
                                setattr(label, variable_name3, valuev3)

                        self.labels.append(label)
                        self.layout.addWidget(label, label.cRow, label.cColumn)

                    elif cUnitType == "Discrete":
                        label = LabelNode(
                            identifier=int(child.get("id")),
                            text=child.get("text"),
                            cRow=int(child.get("cRow")),
                            cColumn=int(child.get("cColumn")),
                            posArray=int(child.get("posArray")),
                            label_name=child.get("label_name"),
                        )
                        label.unitType = cUnitType
                        label.nodeDescription = child.get("nodeDescription")
                        label.unitDescription = child.get("unitDescription")
                        label.weightI = float(child.get("weightI"))
                        label.weightS = float(child.get("weightS"))
                        label.padre = child.get("padre")
                        my_var = child.get("optionsList")
                        label.optionsList = ast.literal_eval(my_var)
                        for i in range(1, len(label.optionsList) + 1):
                            variable_name1 = "UP{}1".format(i)
                            valuev1 = float(child.get(variable_name1))
                            variable_name2 = "UP{}2".format(i)
                            valuev2 = float(child.get(variable_name2))
                            setattr(label, variable_name1, valuev1)
                            setattr(label, variable_name2, valuev2)

                        self.labels.append(label)
                        self.layout.addWidget(label, label.cRow, label.cColumn)
                        # print(my_arr)  # ['Option1', 'Option2', 'Option3']

            # alternatives = []
            alternatives.clear()

            # Loop through the Alternative elements
            for alt_element in root.findall("Alternative"):
                name = alt_element.get("name")
                desc = alt_element.get("desc")
                attr = []

                # Loop through the attribute elements
                for attr_element in alt_element.findall("*"):
                    if attr_element.tag == "ContinuousAttribute":
                        value1 = float(attr_element.get("value1"))
                        value2 = float(attr_element.get("value2"))
                        cAtt = ContinuousAttribute(value1, value2)
                        cAtt.name = attr_element.get("name")
                        attr.append(cAtt)

                    elif attr_element.tag == "DiscreteAttribute":
                        attributenames = attr_element.get("attributenames").split(",")
                        selected = attr_element.get("selected")
                        dAtt = DiscreteAttribute(attributenames)
                        dAtt.selected = selected
                        dAtt.name = attr_element.get("name")
                        attr.append(dAtt)

                # Create the Alternative object with the attributes and add it to the list
                alternatives.append(Alternative(name, desc, attr))

            # We establish the connections again

            for label in self.labels:
                # label_nodes = "[LabelNode(Label2), LabelNode(Label1)]"
                label.double_clicked.connect(self.open_NodeInfo)
                if label.connections:
                    label_names = re.findall(
                        r"LabelNode\((.*?)\)", str(label.connections)
                    )  # Exit: ["Label2", "Label1"]
                    label.connections = []
                    for labelC in self.labels:
                        if labelC.text() in label_names:
                            label.connections.append(labelC)

                identifier_labels = len(self.labels)
                # print(f"P: Importar conections: {label.connections}")

            labelPO = self.labels[0]
            labelPO.padre = None
            print(f"Labels: {self.labels}")
            for i in range(1, len(self.labels)):
                label = self.labels[i]
                # print(f"P: label.padre = {label.padre}")
                match = re.search(r"\((.*?)\)", str(label.padre))
                if match:
                    result = match.group(1)
                    for labelC in self.labels:
                        if result == labelC.text():
                            label.padre = labelC

            attributes.clear()
            attributesnames.clear()
            for label in self.labels:
                if label.finalNode:
                    attributes.append(label)
                    attributesnames.append(label.text())

            self.changeStyleSheetGlobal()
            self.place_lines()
            self.getFinalAttributes(self.labels)

            self.actionSaveWorkspace.setEnabled(True)
            self.actionViewTotalWeights.setEnabled(True)
            self.actionViewComponentUtilities.setEnabled(True)
            self.actionAltConsequences.setEnabled(True)
            self.actionAltClassification.setEnabled(True)
            self.actionPrinter.setEnabled(True)

            file_name = os.path.basename(file_name)
            super(VentanaPrincipalGMAA, self).statusBar().showMessage(
                f"Current WorkSpace: {file_name}"
            )

    def open_workspace2(self):
        global identifier_labels

        file_name, _ = QFileDialog.getOpenFileName(
            self, "Selecciona un archivo XML", "", "Archivos XML (*.xml)"
        )
        if file_name:
            # Process the XML file here
            print(f"P: Archivo seleccionado: {file_name}")
            self.UPMLogoInit.deleteLater()
            # self.InitLabel1.deleteLater()
            # self.InitLabel2.deleteLater()
            self.setStyleSheet("background-color: ")
            self.menubar.setStyleSheet("background-color: ")
            self.menuWindow.setStyleSheet("background-color: ")
            self.toolBarWGMAA.setStyleSheet("background-color: ")
            self.statusBar.setStyleSheet("background-color: ")
            self.scroll_area = QScrollArea(self)
            self.scroll_area.setWidgetResizable(True)
            self.central_widget = MyWidget(self)
            self.setCentralWidget(self.central_widget)
            self.layout = QGridLayout()
            self.central_widget.setLayout(self.layout)
            self.scroll_area.setWidget(self.central_widget)

            self.scroll_area.setVerticalScrollBarPolicy(
                Qt.ScrollBarPolicy.ScrollBarAlwaysOn
            )
            self.scroll_area.setHorizontalScrollBarPolicy(
                Qt.ScrollBarPolicy.ScrollBarAlwaysOn
            )

            self.setCentralWidget(self.scroll_area)

            tree = ET.parse(file_name)
            root = tree.getroot()
            for child in root:
                if child.tag == "Node":
                    label = LabelNode(
                        identifier=int(child.get("id")),
                        text=child.get("text"),
                        cRow=int(child.get("cRow")),
                        cColumn=int(child.get("cColumn")),
                        posArray=int(child.get("posArray")),
                        label_name=child.get("label_name"),
                    )
                    label.connections = child.get("connections")
                    self.labels.append(label)
                    self.layout.addWidget(label, label.cRow, label.cColumn)
                # elif child.tag == 'dlineframeb':
                #     dlineframeb = DLineFrameB()
                #     self.lineB.append(dlineframeb)
                #     self.layout.addWidget(dlineframeb, 0, 1,3,1)
                # elif child.tag == 'dlineframe':
                #     dRowNumber = int(child.get('row'))
                #     dColumnNumber = int(child.get('column'))
                #     dNumNumber = int(child.get('num'))
                #     dlineframe = DLineFrame(dRow=dRowNumber,dColumn=dColumnNumber,dNum=dNumNumber)
                #     self.lines.append(dlineframe)
                #     self.layout.addWidget(dlineframe, dRowNumber, dColumnNumber,dNumNumber,2)
                #     dlineframe.lower()

            # We establish the connections again

            for label in self.labels:
                # label_nodes = "[LabelNode(Label2), LabelNode(Label1)]"
                label.double_clicked.connect(self.open_NodeInfo)

                if label.connections:
                    label_names = re.findall(
                        r"LabelNode\((.*?)\)", str(label.connections)
                    )  # Exit: ["Label2", "Label1"]
                    label.connections = []
                    for labelC in self.labels:
                        if labelC.text() in label_names:
                            label.connections.append(labelC)

                identifier_labels = len(self.labels)
                # print(f"P: Importar conections: {label.connections}")

            self.changeStyleSheetGlobal()
            self.place_lines()
            self.actionSaveWorkspace.setEnabled(True)

            file_name = os.path.basename(file_name)
            super(VentanaPrincipalGMAA, self).statusBar().showMessage(
                f"Current WorkSpace: {file_name}"
            )

    # changes the colour of the Label (node label) as they
    # are created in order to identify which is the final and intermediate node.
    def changeStyleSheetGlobal(self):
        for label in self.labels:
            if not label.connections:
                label.finalNode = True
                label.setStyleSheet(
                    "background-color: #AAA8A8; border-radius: 6px; border: 1px solid #7CEE69;"
                )
            else:
                label.finalNode = False
                label.setStyleSheet(
                    "background-color: #AAA8A8; border-radius: 6px; border: 1px solid #1F1F1F;"
                )

    # displays a QFileDialog that allows you to locate the project you
    # want to save.

    def save_proInput(self):
        # the default_value and self.previous_value variables are used to identify
        # the value of the previously saved file so that the user does not forget it.
        default_value = self.previous_value if self.previous_value is not None else ""
        file_name, ok = QFileDialog.getSaveFileName(
            self, "Save Project", default_value, "XML files (*.xml)"
        )
        valueF = file_name
        # file_name = file_name  # adds the XML extension
        if (
            ok
        ):  # ok is a boolean that indicates whether the user pressed any optional button.
            self.previous_value = valueF
            self.save_project(file_name)

    # processes the request shown with the 'save_proInput' function
    # and saves each Label in an XML file with its own characteristics (Row, Column,
    # etc.). We can save it correctly in an XML file thanks to the import of a
    # serialisation module to convert the label data structure in the program to this
    # type of file. We use 'import xml.etree.ElementTree as ET' and initialise with 'root
    # = ET.Element("QLabels")'.

    def save_project(self, file_path):
        global alternatives
        root = ET.Element("Project_GMAA")
        # Loop through the elements of the label array
        for label in self.labels:
            element = ET.Element("Node")
            element.set("text", label.text())
            element.set("cRow", str(label.cRow))
            element.set("cColumn", str(label.cColumn))
            element.set("id", str(label.identifier))
            element.set("label_name", label.label_name)
            element.set("posArray", str(label.posArray))
            element.set("connections", str(label.connections))
            element.set("nodeDescription", label.nodeDescription)
            element.set("padre", str(label.padre))
            element.set("weightI", str(label.weightI))
            element.set("weightS", str(label.weightS))

            if label.unitType == "Continuous":
                element.set("unitType", "Continuous")
                element.set("unitDescription", label.unitDescription)
                element.set("unitName", label.unitName)
                element.set("minRange", str(label.minRange))
                element.set("maxRange", str(label.maxRange))
                element.set("mostPrefered", label.mostPrefered)
                element.set("interPoints", str(label.interPoints))
                if label.interPoints > 0:
                    for i in range(1, label.interPoints + 1):
                        variable_name1 = "IP{}1".format(i)
                        variable_name2 = "IP{}2".format(i)
                        variable_name3 = "IPAV{}".format(i)
                        element.set(variable_name1, str(getattr(label, variable_name1)))
                        element.set(variable_name2, str(getattr(label, variable_name2)))
                        element.set(variable_name3, str(getattr(label, variable_name3)))

            elif label.unitType == "Discrete":
                element.set("unitType", "Discrete")
                element.set("unitDescription", label.unitDescription)
                # element.set("optionDiscrete",label.optionDiscrete)
                element.set("optionsList", str(label.optionsList))
                for i in range(1, len(label.optionsList) + 1):
                    variable_name1 = "UP{}1".format(i)
                    variable_name2 = "UP{}2".format(i)
                    element.set(variable_name1, str(getattr(label, variable_name1)))
                    element.set(variable_name2, str(getattr(label, variable_name2)))
            else:
                element.set("unitType", "")

            root.append(element)

        # we create the element for the Alternatives
        # Loop through the Alternative objects
        for alt in alternatives:
            alt_element = ET.Element("Alternative")
            alt_element.set("name", alt.name)
            alt_element.set("desc", alt.desc)

            # Create an element for each attribute in the attr list
            for attr in alt.attr:
                if isinstance(attr, ContinuousAttribute):
                    attr_element = ET.Element("ContinuousAttribute")
                    attr_element.set("value1", str(attr.value1))
                    attr_element.set("value2", str(attr.value2))
                    attr_element.set("name", attr.name)

                elif isinstance(attr, DiscreteAttribute):
                    attr_element = ET.Element("DiscreteAttribute")
                    attr_element.set("attributenames", ",".join(attr.attributenames))
                    attr_element.set("selected", attr.selected)
                    attr_element.set("name", attr.name)

                else:
                    continue

                # Add the attribute element to the Alternative element
                alt_element.append(attr_element)
            # Add the Alternative element to the root element
            root.append(alt_element)

        tree = ET.ElementTree(root)
        tree.write(file_path)

    # connections = []
    # for label1 in self.labels:
    #     for label2 in self.labels:
    #         if label1 is not label2 and label1.text() == label2.text():
    #             if label1 not in connections:
    #                 connections.append(label1)
    #             if label2 not in connections:
    #                 connections.append(label2)

    # What this function does is to ask you what you want to do when you save your workspace

    def close_workspace(self, event):
        global PrimaryObjective
        global currentColumn
        global currentRow
        global Branch
        global identifier_labels
        global Leaf
        global attributes
        global attributesnames
        global alternatives

        if self.labels:
            reply = QMessageBox.question(
                self,
                "Save Changes?",
                "Do you want to save changes before closing?",
                QMessageBox.StandardButton.Yes
                | QMessageBox.StandardButton.No
                | QMessageBox.StandardButton.Cancel,
            )
            if reply == QMessageBox.StandardButton.Cancel:
                pass
            elif reply == QMessageBox.StandardButton.Yes:
                self.save_proInput()
            else:
                PrimaryObjective = False
                print(self.labels)
                for label in self.labels:
                    if label:
                        label.deleteLater()
                self.labels.clear()
                self.lineB.clear()
                self.lines.clear()
                attributes.clear()
                attributesnames.clear()
                alternatives.clear()
                identifier_labels = 0
                PrimaryObjective = False
                Branch = 0
                Leaf = 0  # if the delete button of the PO Label is triggered the num of Leaf is 0
                identifier_labels = 0
                currentRow = 0
                currentColumn = 0
                self.actionSaveWorkspace.setEnabled(False)
                self.actionViewComponentUtilities.setEnabled(False)
                self.actionSave_WorkSpace.setEnabled(False)
                self.actionAltConsequences.setEnabled(False)
                self.actionViewTotalWeights.setEnabled(False)
                self.actionAltClassification.setEnabled(False)
                self.actionSave_WorkSpace_As.setEnabled(False)
                self.new_workspace()  # newly incorporated, I have to take a look at it
                self.place_lines()

        else:
            pass

    # Function that shows the Context Menu created before
    def show_context_menuPO(self, point):
        # Show the Context Menu depending on the value of PrimaryObjective
        if self.labels:
            self.context_menuPO.removeAction(self.actionCPO)
            # Adding the Action of creating branches and leaves
            # self.context_menuPO.addAction(self.actionCBL)
            # Adding the Action of creating branches and leaves
            # self.context_menuPO.addSeparator()
            self.context_menuPO.addAction(self.actionDPO)
        elif not self.labels:
            self.context_menuPO.addAction(self.actionCPO)
            # self.context_menuPO.removeAction(self.actionCBL)
            self.context_menuPO.removeAction(self.actionDPO)
        self.context_menuPO.exec(self.mapToGlobal(point))

    # shows a new screen with the node information (Label). This
    # new screen is the initialisation of a class called WindowNodeInfo(QMainWindow).
    def open_NodeInfo(self):
        global attributes
        global attributesnames
        global alternatives
        sender = (
            self.sender()
        )  # Collects all the information of the label that has emitted the double-click signal
        self.vNodeInfo = VentanaNodeInfo()
        # self.vNodeInfo = VentanaNodeInfo(self)
        print(f"sender.nodeDescription {sender.nodeDescription}")
        if not sender.finalNode:
            widget = self.vNodeInfo.findChild(
                QWidget, "LeafAttribute"
            )  # Search for the QWidget by name
            widget1 = self.vNodeInfo.findChild(QWidget, "ViewingCUtilities")
            widget2 = self.vNodeInfo.findChild(QWidget, "ViewingAltCons")
            widget3 = self.vNodeInfo.findChild(QWidget, "QPreferences")
            if (widget and widget2 and widget3 and widget1) is not None:
                widget.deleteLater()  # Deletes QWidget
                widget1.deleteLater()
                widget2.deleteLater()
                widget3.deleteLater()
        else:
            widget = self.vNodeInfo.findChild(
                QWidget, "ViewingWeights"
            )  # Search for the QWidget by name
            widget2 = self.vNodeInfo.findChild(
                QWidget, "WeightElicitation"
            )  # Search for the QWidget by name
            if (widget) is not None:
                widget.deleteLater()  # Deletes QWidget
                widget2.deleteLater()  # Deletes QWidget

        if sender.unitType == "Continuous":

            self.vNodeInfo.radioButtonDAC.setChecked(True)
            self.vNodeInfo.radioButtonDAD.setEnabled(False)
            self.vNodeInfo.radioButtonDAC.setEnabled(True)
            self.vNodeInfo.radioButtonCEM.setEnabled(True)

        elif sender.unitType == "Discrete":

            self.vNodeInfo.radioButtonDAD.setChecked(True)
            self.vNodeInfo.radioButtonDAD.setEnabled(True)
            self.vNodeInfo.radioButtonDAC.setEnabled(False)
            self.vNodeInfo.radioButtonCEM.setEnabled(False)

        else:

            self.vNodeInfo.radioButtonDAD.setEnabled(False)
            self.vNodeInfo.radioButtonDAC.setEnabled(False)
            self.vNodeInfo.radioButtonCEM.setEnabled(False)

        # HAY QUE PONERLOOO
        # if sender.nodeDescription:
        #     # self.vNodeInfo.textDescription.setPlainText(sender.nodeDescription)
        # else:
        #     self.vNodeInfo.textDescription.setPlaceholderText("Enter your node description here...")

        # self.vNodeInfo.textDescription.setPlainText(f"Número de hijos: {len(sender.connections)}.\nConexiones: {sender.connections}. \nUnit type: {sender.unitType}\nTable Discrete: {sender.optionsList}\nFinal Nodes: {attributes}\nAlternatives: {alternatives}\nAttributes: {attributes}\nAttributesNames: {attributesnames}") # Test to check posArray from the labels
        print(f"P: Labels: {self.labels}")
        self.vNodeInfo.textDescription.setPlainText(
            f"Padre: {sender.padre}\nGeneración: {sender.count_parents(sender)}\ncRow: {sender.cRow}\ncColumn: {sender.cColumn}\nweightI: {sender.weightI}\nweightIS: {sender.weightS}\nFinal Nodes: {attributes}\nAlternatives: {alternatives}\nAttributes: {attributes}\nAttributesNames: {attributesnames}"
        )

        self.vNodeInfo.textDescription.setPlainText(
            f"Padre: {sender.padre}\nsender.UP21 0.5: {sender.UP21}\ncRow: {sender.cRow}\ncColumn: {sender.cColumn}\nweightI: {sender.weightI}\nweightIS: {sender.weightS}\nFinal Nodes: {attributes}\nAlternatives: {alternatives}\nAttributes: {attributes}\nAttributesNames: {attributesnames}"
        )
        # self.vNodeInfo.textUnits.setPlaceholderText("Enter your node units...")
        # self.vNodeInfo.textMinRange.setPlaceholderText("ej. 1")
        # self.vNodeInfo.textMaxRange.setPlaceholderText("ej. 5")
        self.vNodeInfo.textName.setPlainText(sender.label_name)
        self.vNodeInfo.textLabel.setPlainText(sender.text())
        self.vNodeInfo.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)

        # button Viewing Alternative Consequences
        button_group = QButtonGroup()
        button_group.addButton(self.vNodeInfo.radioButtonDAD)
        button_group.addButton(self.vNodeInfo.radioButtonDAC)
        button_group.setExclusive(True)

        if self.vNodeInfo.radioButtonDAC.isChecked():
            self.vNodeInfo.buttonNext.clicked.connect(lambda: self.open_LUF(sender))
        if self.vNodeInfo.radioButtonDAD.isChecked():
            self.vNodeInfo.buttonNext.clicked.connect(lambda: self.open_UDV(sender))

        self.vNodeInfo.pushButtonVAC.clicked.connect(lambda: self.modifyAltCon(sender))

        # button signals
        # self.vNodeInfo.radioBAverageVAC.toggled.connect(lambda: self.ave_alt(sender))
        # self.vNodeInfo.radioBMaximumVAC.toggled.connect(lambda: self.max_alt(sender))
        # self.vNodeInfo.radioBMinimumVAC.toggled.connect(lambda: self.min_alt(sender))

        # several options if the string is empty, continuous or discrete
        if not sender.unitType:
            self.vNodeInfo.textDescCont.setPlaceholderText(
                "Enter your node description here..."
            )
            self.vNodeInfo.textUnitsCont.setPlaceholderText("Enter your node units...")
            self.vNodeInfo.textMinRangeCont.setPlaceholderText("ej. 1")
            self.vNodeInfo.textMaxRangeCont.setPlaceholderText("ej. 5")
            self.vNodeInfo.textDescDisc.setPlaceholderText(
                "Enter your node description here..."
            )
            if not sender.optionsList:
                self.vNodeInfo.spinBoxDiscrete.setValue(2)

        elif sender.unitType == "Continuous":
            self.vNodeInfo.radioBCont.setChecked(True)
            self.vNodeInfo.textName.setPlainText(sender.label_name)
            self.vNodeInfo.textLabel.setPlainText(sender.text())
            self.vNodeInfo.textUnitsCont.setPlainText(sender.unitName)
            self.vNodeInfo.textDescCont.setPlainText(sender.unitDescription)
            self.vNodeInfo.textMinRangeCont.setPlainText(str(sender.minRange))
            self.vNodeInfo.textMaxRangeCont.setPlainText(str(sender.maxRange))
            if sender.mostPrefered == "Sup":
                self.vNodeInfo.radioBMPS.setChecked(True)
            else:
                self.vNodeInfo.radioBMPI.setChecked(True)

        elif sender.unitType == "Discrete":
            self.vNodeInfo.textDescDisc.setPlainText(sender.unitDescription)
            self.vNodeInfo.radioBDisc.setChecked(True)
            self.vNodeInfo.spinBoxDiscrete.setValue(len(sender.optionsList))
            # we create the table
            # Adding elements to the table
            num_rows = len(sender.optionsList)
            widthTable = self.vNodeInfo.tableDiscrete.width()
            self.vNodeInfo.tableDiscrete.setRowCount(num_rows)
            self.vNodeInfo.tableDiscrete.setColumnCount(1)
            self.vNodeInfo.tableDiscrete.setColumnWidth(0, widthTable)
            self.vNodeInfo.tableDiscrete.setHorizontalHeaderLabels(["Attributes"])
            # self.vNodeInfo.tableDiscrete.setColumnWidth(0, 190)

            for i in range(num_rows):
                # Add text in the first column
                item = QTableWidgetItem(sender.optionsList[i])
                self.vNodeInfo.tableDiscrete.setItem(i, 0, item)

                # Add option in second column
                # radio_button = QRadioButton()
                # radio_button.setObjectName(str(i))
                # if item.text() == sender.optionDiscrete:
                #     radio_button.setChecked(True)
                # self.vNodeInfo.tableDiscrete.setCellWidget(i, 1, radio_button)
                # widget = self.vNodeInfo.tableDiscrete.cellWidget(i, 1)
                # if isinstance(widget, QRadioButton):
                #     widget.setStyleSheet('margin-left: 10px;')

        self.vNodeInfo.textLabel.setPlainText(sender.text())

        # create VAC Table

        # establish the alternative for the attribute table

        attributeName = sender.text()
        textMinRange = float(sender.minRange)
        textMaxRange = float(sender.maxRange)
        print(f"P: textMinRange: " + str(textMinRange))
        print(f"P: textMaxRange: " + str(textMaxRange))
        index = None

        for i, attr in enumerate(attributes):
            if attr.unitType == "Continuous":
                print(
                    "P: attr.minRange: "
                    + str(float(attr.minRange))
                    + ", attr.minRange: "
                    + str(float(attr.maxRange))
                )
                if (str(float(attr.minRange)) == str(textMinRange)) and (
                    str(float(attr.maxRange)) == str(textMaxRange)
                    and (attributeName == attr.text())
                ):
                    index = i
                    break
                else:
                    index = None
            elif attr.unitType == "Discrete":
                items = []
                for j in range(self.vNodeInfo.tableDiscrete.rowCount()):
                    item = self.vNodeInfo.tableDiscrete.item(j, 0)
                    if item is not None:
                        items.append(item.text())
                if (attr.optionsList == items) and (attributeName == attr.text()):
                    index = i
                    break
                else:
                    index = None

        if sender.unitType == "Continuous":
            num_columns = (len(alternatives) + 1) * 2
            widthTable = self.vNodeInfo.tableWidgetVAC.width() // 12
            self.vNodeInfo.tableWidgetVAC.setRowCount(3)
            self.vNodeInfo.tableWidgetVAC.setColumnCount(num_columns)

            # self.vNodeInfo.tableWidgetAC.setSpan(0, 0, 1, 2) # ocupies two columns
            self.vNodeInfo.tableWidgetVAC.verticalHeader().setVisible(False)
            self.vNodeInfo.tableWidgetVAC.horizontalHeader().setVisible(False)

            for i in range(num_columns):
                self.vNodeInfo.tableWidgetVAC.setColumnWidth(i, widthTable)

            header_item = QTableWidgetItem("Intervals:")
            font = QFont()
            font.setBold(True)
            self.vNodeInfo.tableWidgetVAC.setSpan(0, 0, 1, 2)
            item = QTableWidgetItem("Alternatives:")
            item.setTextAlignment(
                Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
            )
            self.vNodeInfo.tableWidgetVAC.setItem(0, 0, item)
            self.vNodeInfo.tableWidgetVAC.setSpan(1, 0, 1, 2)
            header_item.setTextAlignment(
                Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
            )
            self.vNodeInfo.tableWidgetVAC.setItem(1, 0, header_item)
            item = QTableWidgetItem(attributeName)
            item.setFont(font)

            # item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.vNodeInfo.tableWidgetVAC.setSpan(2, 0, 1, 2)
            self.vNodeInfo.tableWidgetVAC.setItem(2, 0, item)
            column = 0
            for i, altern in enumerate(alternatives):
                self.vNodeInfo.tableWidgetVAC.setSpan(0, column + 2, 1, 2)
                header_item = QTableWidgetItem(altern.name)
                font = QFont()
                font.setBold(True)
                brush = QBrush(QColor(0, 0, 0, 25))
                header_item.setBackground(brush)  # Establecer el fondo con el QBrush

                header_item.setFont(font)
                header_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.vNodeInfo.tableWidgetVAC.setItem(0, column + 2, header_item)
                font = QFont()
                font.setBold(True)
                header_item.setFont(font)
                item = QTableWidgetItem("min")
                # item2 = QTableWidgetItem("ave")
                item3 = QTableWidgetItem("max")
                item.setFont(font)
                item.setBackground(brush)  # Establecer el fondo con el QBrush

                # item2.setFont(font)
                item3.setFont(font)
                item3.setBackground(brush)  # Establecer el fondo con el QBrush

                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.vNodeInfo.tableWidgetVAC.setItem(1, column + 2, item)
                # item2.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                # self.vNodeInfo.tableWidgetVAC.setItem(1, column+4, item3)
                item3.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.vNodeInfo.tableWidgetVAC.setItem(1, column + 3, item3)
                column += 2

            if not (index == None):
                column = 0
                for alternative in alternatives:
                    elementCD = alternative.attr[index]
                    if isinstance(elementCD, ContinuousAttribute):
                        value1 = elementCD.value1
                        value2 = elementCD.value2
                        # value3 = float(elementCD.value1 + elementCD.value2) / 2

                        item = QTableWidgetItem(str(value1))
                        item2 = QTableWidgetItem(str(value2))
                        # item3 = QTableWidgetItem(str(value3))
                        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                        self.vNodeInfo.tableWidgetVAC.setItem(2, column + 2, item)
                        # item3.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                        # self.vNodeInfo.tableWidgetVAC.setItem(2, column+4, item3)
                        item2.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                        self.vNodeInfo.tableWidgetVAC.setItem(2, column + 3, item2)
                    column += 2
            else:
                pass
        elif sender.unitType == "Discrete":
            num_columns = (len(alternatives) + 1) * 2
            widthTable = self.vNodeInfo.tableWidgetVAC.width() // 12
            self.vNodeInfo.tableWidgetVAC.setRowCount(2)
            self.vNodeInfo.tableWidgetVAC.setColumnCount(num_columns)

            # self.vNodeInfo.tableWidgetAC.setSpan(0, 0, 1, 2) # ocupies two columns
            self.vNodeInfo.tableWidgetVAC.verticalHeader().setVisible(False)
            self.vNodeInfo.tableWidgetVAC.horizontalHeader().setVisible(False)

            for i in range(num_columns):
                self.vNodeInfo.tableWidgetVAC.setColumnWidth(i, widthTable)

            font = QFont()
            font.setBold(True)
            self.vNodeInfo.tableWidgetVAC.setSpan(0, 0, 1, 2)
            item = QTableWidgetItem("Alternatives:")
            item.setTextAlignment(
                Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
            )
            self.vNodeInfo.tableWidgetVAC.setItem(0, 0, item)
            self.vNodeInfo.tableWidgetVAC.setSpan(1, 0, 1, 2)
            item = QTableWidgetItem(attributeName)
            item.setFont(font)

            # item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.vNodeInfo.tableWidgetVAC.setSpan(1, 0, 1, 2)
            self.vNodeInfo.tableWidgetVAC.setItem(1, 0, item)
            column = 0
            for i, altern in enumerate(alternatives):
                self.vNodeInfo.tableWidgetVAC.setSpan(0, column + 2, 1, 2)
                header_item = QTableWidgetItem(altern.name)
                brush = QBrush(
                    QColor(0, 0, 0, 25)
                )  # Color negro con transparencia baja (25)
                header_item.setBackground(brush)
                font = QFont()
                font.setBold(True)
                header_item.setFont(font)
                header_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.vNodeInfo.tableWidgetVAC.setItem(0, column + 2, header_item)
                # font = QFont()
                # font.setBold(True)
                # header_item.setFont(font)
                # item = QTableWidgetItem("min")
                # item.setBackground(brush)
                # # item2 = QTableWidgetItem("ave")
                # item3 = QTableWidgetItem("max")
                # item3.setBackground(brush)
                # item.setFont(font)
                # # item2.setFont(font)
                # item3.setFont(font)
                # item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                # self.vNodeInfo.tableWidgetVAC.setItem(1, column+2, item)
                # # item2.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                # # self.vNodeInfo.tableWidgetVAC.setItem(1, column+4, item3)
                # item3.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                # self.vNodeInfo.tableWidgetVAC.setItem(1, column+3, item3)
                column += 2

            if not (index == None):
                column = 0
                for alternative in alternatives:
                    elementCD = alternative.attr[index]
                    if isinstance(elementCD, DiscreteAttribute):
                        self.vNodeInfo.tableWidgetVAC.setSpan(1, column + 2, 1, 2)
                        # combo_box = QComboBox()
                        # combo_box.addItems(elementCD.attributenames)
                        selected_option = elementCD.selected
                        # index1 = elementCD.attributenames.index(selected_option)
                        # combo_box.setCurrentIndex(index1)
                        selected_item = QTableWidgetItem(selected_option)
                        selected_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

                        self.vNodeInfo.tableWidgetVAC.setItem(
                            1, column + 2, selected_item
                        )
                        # self.vNodeInfo.tableWidgetVAC.setCellWidget(0, column+2, combo_box)
                    column += 2
            else:
                pass

        if not sender.finalNode:
            data = []
            valmins = []
            valmaxs = []
            for internod in sender.connections:
                if isinstance(internod, QLabel):
                    valmins.append(float(internod.weightI))
                    valmaxs.append(float(internod.weightS))

            for valmin, valmax in zip(valmins, valmaxs):
                data.append((valmin, valmax))

            chart_widget = BarChartWidget()
            chart_widget.set_data(data)
            # chart_widget.set_connections(sender.connections)
            self.hlayoutVW = self.vNodeInfo.hLayoutGV
            self.hlayoutVW.addWidget(chart_widget)

            # here we are going to create the table for the direct assignment of weights

            self.vNodeInfo.buttonView.clicked.connect(
                lambda: self.view_table(
                    self.vNodeInfo, self.vNodeInfo.tableWidgetWE, sender
                )
            )
            self.vNodeInfo.buttonNorm.clicked.connect(
                lambda: self.norm_table(self.vNodeInfo.tableWidgetWE, sender)
            )

            self.vNodeInfo.tableWidgetWE.setContentsMargins(0, 0, 0, 0)
            # self.vNodeInfo.tableWidgetWE.setStyleSheet("background-color: #F0F0F0;")
            self.vNodeInfo.tableWidgetWE.setFrameShape(QFrame.Shape.NoFrame)
            self.vNodeInfo.tableWidgetWE.setLineWidth(0)
            self.vNodeInfo.tableWidgetWE.setShowGrid(False)

            num_rows = len(sender.connections)
            num_columns = 5
            widthTable = self.vNodeInfo.tableWidgetWE.width() // 5
            print(f"P: widthTable {widthTable}")
            self.vNodeInfo.tableWidgetWE.setRowCount(num_rows)
            self.vNodeInfo.tableWidgetWE.setColumnCount(num_columns)
            self.vNodeInfo.tableWidgetWE.setColumnWidth(0, widthTable)
            # font = QFont()
            # font.setBold(True)
            # header_item.setFont(font)
            # item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignCenter)
            # self.vNodeInfo.tableWidgetWE.setSpan(0, 0, 1, 2) # ocupies two columns
            self.vNodeInfo.tableWidgetWE.verticalHeader().setVisible(False)
            self.vNodeInfo.tableWidgetWE.horizontalHeader().setVisible(False)

            for i in range(num_columns):
                if i == 4 or i == 2:
                    self.vNodeInfo.tableWidgetWE.setColumnWidth(i, 45)
                else:
                    self.vNodeInfo.tableWidgetWE.setColumnWidth(i, widthTable)

            for i, conn in enumerate(sender.connections):
                item = QTableWidgetItem(conn.text())
                item2 = QTableWidgetItem("Lower Bound")
                item3 = "{:.3f}".format(float(conn.weightI))
                item3 = QTableWidgetItem(str(item3))
                item4 = QTableWidgetItem("Upper Bound")
                item5 = "{:.3f}".format(float(conn.weightS))
                item5 = QTableWidgetItem(str(item5))
                font = QFont()
                font.setBold(True)
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                item2.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                item3.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                item2.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                item4.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                item5.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                item.setFont(font)

                # brush = QBrush(QColor(0, 0, 0, 25))  # Color negro con transparencia baja (25)
                # item.setBackground(brush)
                item.setFlags(Qt.ItemFlag.ItemIsEnabled)
                self.vNodeInfo.tableWidgetWE.setItem(i, 0, item)
                item2.setFlags(Qt.ItemFlag.ItemIsEnabled)
                self.vNodeInfo.tableWidgetWE.setItem(i, 1, item2)
                self.vNodeInfo.tableWidgetWE.setItem(i, 2, item3)
                item4.setFlags(Qt.ItemFlag.ItemIsEnabled)
                self.vNodeInfo.tableWidgetWE.setItem(i, 3, item4)
                self.vNodeInfo.tableWidgetWE.setItem(i, 4, item5)

        else:
            if sender.unitType == "Continuous":
                # window = QMainWindow()
                background_color = QColor("#EFEAE6")
                brush = QBrush(background_color)

                widget = QWidget()
                self.clear_layout(self.vNodeInfo.hLayoutVCU)
                # self.vNodeInfo.clear_layout(self.hLayoutVCU)
                # window.setCentralWidget(widget)
                self.layoutVCU = self.vNodeInfo.hLayoutVCU
                self.layoutVCU.addWidget(widget)

                series = QLineSeries()
                series1 = QLineSeries()
                series2 = QLineSeries()
                if sender.mostPrefered == "Sup":
                    series.append(float(sender.minRange), 0)  # Punto inicial
                    series1.append(float(sender.minRange), 0)  # Punto inicial
                    series2.append(float(sender.minRange), 0)  # Punto inicial
                    self.vNodeInfo.AttMP.setText(
                        f"Index ({int(sender.minRange)}: Worst, {int(sender.maxRange)} Ideal)"
                    )
                    if sender.interPoints == 5:
                        series.append(float(sender.IPAV1), float(sender.IP11))
                        series.append(float(sender.IPAV2), float(sender.IP21))
                        series.append(float(sender.IPAV3), float(sender.IP31))
                        series.append(float(sender.IPAV4), float(sender.IP41))
                        series.append(float(sender.IPAV5), float(sender.IP51))
                        series1.append(float(sender.IPAV1), float(sender.IP12))
                        series1.append(float(sender.IPAV2), float(sender.IP22))
                        series1.append(float(sender.IPAV3), float(sender.IP32))
                        series1.append(float(sender.IPAV4), float(sender.IP42))
                        series1.append(float(sender.IPAV5), float(sender.IP52))
                        averagevar = float(
                            (float(sender.IP11) + float(sender.IP12)) / 2
                        )
                        series2.append(float(sender.IPAV1), averagevar)
                        averagevar = float(
                            (float(sender.IP21) + float(sender.IP22)) / 2
                        )
                        series2.append(float(sender.IPAV2), averagevar)
                        averagevar = float(
                            (float(sender.IP31) + float(sender.IP32)) / 2
                        )
                        series2.append(float(sender.IPAV3), averagevar)
                        averagevar = float(
                            (float(sender.IP41) + float(sender.IP42)) / 2
                        )
                        series2.append(float(sender.IPAV4), averagevar)
                        averagevar = float(
                            (float(sender.IP51) + float(sender.IP52)) / 2
                        )
                        series2.append(float(sender.IPAV5), averagevar)
                        # series.append(3.5, 0.6)  # Punto intermedio
                        # series.append(3.5, 0.2)  # Punto intermedio
                        series.append(float(sender.maxRange), 1)  # Punto final
                        series1.append(float(sender.maxRange), 1)  # Punto final
                        series2.append(float(sender.maxRange), 1)  # Punto final

                        chart = QChart()
                        chart.addSeries(series)
                        chart.addSeries(series1)
                        chart.addSeries(series2)

                    elif sender.interPoints == 4:
                        series.append(float(sender.IPAV1), float(sender.IP11))
                        series.append(float(sender.IPAV2), float(sender.IP21))
                        series.append(float(sender.IPAV3), float(sender.IP31))
                        series.append(float(sender.IPAV4), float(sender.IP41))
                        series1.append(float(sender.IPAV1), float(sender.IP12))
                        series1.append(float(sender.IPAV2), float(sender.IP22))
                        series1.append(float(sender.IPAV3), float(sender.IP32))
                        series1.append(float(sender.IPAV4), float(sender.IP42))
                        averagevar = float(
                            (float(sender.IP11) + float(sender.IP12)) / 2
                        )
                        series2.append(float(sender.IPAV1), averagevar)
                        averagevar = float(
                            (float(sender.IP21) + float(sender.IP22)) / 2
                        )
                        series2.append(float(sender.IPAV2), averagevar)
                        averagevar = float(
                            (float(sender.IP31) + float(sender.IP32)) / 2
                        )
                        series2.append(float(sender.IPAV3), averagevar)
                        averagevar = float(
                            (float(sender.IP41) + float(sender.IP42)) / 2
                        )
                        series2.append(float(sender.IPAV4), averagevar)
                        series.append(float(sender.maxRange), 1)  # Punto final
                        series1.append(float(sender.maxRange), 1)  # Punto final
                        series2.append(float(sender.maxRange), 1)  # Punto final

                        series.append(float(sender.maxRange), 1)  # Punto final
                        series1.append(float(sender.maxRange), 1)  # Punto final
                        series2.append(float(sender.maxRange), 1)  # Punto final

                        chart = QChart()
                        chart.addSeries(series)
                        chart.addSeries(series1)
                        chart.addSeries(series2)

                    elif sender.interPoints == 3:
                        series.append(float(sender.IPAV1), float(sender.IP11))
                        series.append(float(sender.IPAV2), float(sender.IP21))
                        series.append(float(sender.IPAV3), float(sender.IP31))
                        series1.append(float(sender.IPAV1), float(sender.IP12))
                        series1.append(float(sender.IPAV2), float(sender.IP22))
                        series1.append(float(sender.IPAV3), float(sender.IP32))
                        averagevar = float(
                            (float(sender.IP11) + float(sender.IP12)) / 2
                        )
                        series2.append(float(sender.IPAV1), averagevar)
                        averagevar = float(
                            (float(sender.IP21) + float(sender.IP22)) / 2
                        )
                        series2.append(float(sender.IPAV2), averagevar)
                        averagevar = float(
                            (float(sender.IP31) + float(sender.IP32)) / 2
                        )
                        series2.append(float(sender.IPAV3), averagevar)

                        series.append(float(sender.maxRange), 1)  # Punto final
                        series1.append(float(sender.maxRange), 1)  # Punto final
                        series2.append(float(sender.maxRange), 1)  # Punto final

                        chart = QChart()
                        chart.addSeries(series)
                        chart.addSeries(series1)
                        chart.addSeries(series2)

                    elif sender.interPoints == 2:
                        series.append(float(sender.IPAV1), float(sender.IP11))
                        series.append(float(sender.IPAV2), float(sender.IP21))
                        series1.append(float(sender.IPAV1), float(sender.IP12))
                        series1.append(float(sender.IPAV2), float(sender.IP22))
                        averagevar = float(
                            (float(sender.IP11) + float(sender.IP12)) / 2
                        )
                        series2.append(float(sender.IPAV1), averagevar)
                        averagevar = float(
                            (float(sender.IP21) + float(sender.IP22)) / 2
                        )
                        series2.append(float(sender.IPAV2), averagevar)

                        series.append(float(sender.maxRange), 1)  # Punto final
                        series1.append(float(sender.maxRange), 1)  # Punto final
                        series2.append(float(sender.maxRange), 1)  # Punto final

                        chart = QChart()
                        chart.addSeries(series)
                        chart.addSeries(series1)
                        chart.addSeries(series2)

                    elif sender.interPoints == 1:
                        series.append(float(sender.IPAV1), float(sender.IP11))
                        series1.append(float(sender.IPAV1), float(sender.IP12))
                        averagevar = float(
                            (float(sender.IP11) + float(sender.IP12)) / 2
                        )
                        series2.append(float(sender.IPAV1), averagevar)

                        series.append(float(sender.maxRange), 1)  # Punto final
                        series1.append(float(sender.maxRange), 1)  # Punto final
                        series2.append(float(sender.maxRange), 1)  # Punto final

                        chart = QChart()
                        chart.addSeries(series)
                        chart.addSeries(series1)
                        chart.addSeries(series2)
                    else:
                        series.append(float(sender.maxRange), 1)
                        chart = QChart()
                        chart.addSeries(series)
                else:
                    self.vNodeInfo.AttMP.setText(
                        f"Index ({int(sender.minRange)}: Ideal, {int(sender.maxRange)} Worst)"
                    )
                    series.append(float(sender.minRange), 1)  # Punto inicial
                    series1.append(float(sender.minRange), 1)  # Punto inicial
                    series2.append(float(sender.minRange), 1)  # Punto inicial
                    if sender.interPoints == 5:
                        series.append(float(sender.IPAV1), float(sender.IP11))
                        series.append(float(sender.IPAV2), float(sender.IP21))
                        series.append(float(sender.IPAV3), float(sender.IP31))
                        series.append(float(sender.IPAV4), float(sender.IP41))
                        series.append(float(sender.IPAV5), float(sender.IP51))
                        series1.append(float(sender.IPAV1), float(sender.IP12))
                        series1.append(float(sender.IPAV2), float(sender.IP22))
                        series1.append(float(sender.IPAV3), float(sender.IP32))
                        series1.append(float(sender.IPAV4), float(sender.IP42))
                        series1.append(float(sender.IPAV5), float(sender.IP52))
                        averagevar = float(
                            (float(sender.IP11) + float(sender.IP12)) / 2
                        )
                        series2.append(float(sender.IPAV1), averagevar)
                        averagevar = float(
                            (float(sender.IP21) + float(sender.IP22)) / 2
                        )
                        series2.append(float(sender.IPAV2), averagevar)
                        averagevar = float(
                            (float(sender.IP31) + float(sender.IP32)) / 2
                        )
                        series2.append(float(sender.IPAV3), averagevar)
                        averagevar = float(
                            (float(sender.IP41) + float(sender.IP42)) / 2
                        )
                        series2.append(float(sender.IPAV4), averagevar)
                        averagevar = float(
                            (float(sender.IP51) + float(sender.IP52)) / 2
                        )
                        series2.append(float(sender.IPAV5), averagevar)
                        # series.append(3.5, 0.6)  # Punto intermedio
                        # series.append(3.5, 0.2)  # Punto intermedio
                        series.append(float(sender.maxRange), 0)  # Punto final
                        series1.append(float(sender.maxRange), 0)  # Punto final
                        series2.append(float(sender.maxRange), 0)  # Punto final

                        chart = QChart()
                        chart.addSeries(series)
                        chart.addSeries(series1)
                        chart.addSeries(series2)
                    elif sender.interPoints == 4:
                        series.append(float(sender.IPAV1), float(sender.IP11))
                        series.append(float(sender.IPAV2), float(sender.IP21))
                        series.append(float(sender.IPAV3), float(sender.IP31))
                        series.append(float(sender.IPAV4), float(sender.IP41))
                        series1.append(float(sender.IPAV1), float(sender.IP12))
                        series1.append(float(sender.IPAV2), float(sender.IP22))
                        series1.append(float(sender.IPAV3), float(sender.IP32))
                        series1.append(float(sender.IPAV4), float(sender.IP42))
                        averagevar = float(
                            (float(sender.IP11) + float(sender.IP12)) / 2
                        )
                        series2.append(float(sender.IPAV1), averagevar)
                        averagevar = float(
                            (float(sender.IP21) + float(sender.IP22)) / 2
                        )
                        series2.append(float(sender.IPAV2), averagevar)
                        averagevar = float(
                            (float(sender.IP31) + float(sender.IP32)) / 2
                        )
                        series2.append(float(sender.IPAV3), averagevar)
                        averagevar = float(
                            (float(sender.IP41) + float(sender.IP42)) / 2
                        )
                        series2.append(float(sender.IPAV4), averagevar)

                        # series.append(3.5, 0.6)  # Punto intermedio
                        # series.append(3.5, 0.2)  # Punto intermedio
                        series.append(float(sender.maxRange), 0)  # Punto final
                        series1.append(float(sender.maxRange), 0)  # Punto final
                        series2.append(float(sender.maxRange), 0)  # Punto final

                        chart = QChart()
                        chart.addSeries(series)
                        chart.addSeries(series1)
                        chart.addSeries(series2)

                    elif sender.interPoints == 3:
                        series.append(float(sender.IPAV1), float(sender.IP11))
                        series.append(float(sender.IPAV2), float(sender.IP21))
                        series.append(float(sender.IPAV3), float(sender.IP31))
                        series1.append(float(sender.IPAV1), float(sender.IP12))
                        series1.append(float(sender.IPAV2), float(sender.IP22))
                        series1.append(float(sender.IPAV3), float(sender.IP32))
                        averagevar = float(
                            (float(sender.IP11) + float(sender.IP12)) / 2
                        )
                        series2.append(float(sender.IPAV1), averagevar)
                        averagevar = float(
                            (float(sender.IP21) + float(sender.IP22)) / 2
                        )
                        series2.append(float(sender.IPAV2), averagevar)
                        averagevar = float(
                            (float(sender.IP31) + float(sender.IP32)) / 2
                        )
                        series2.append(float(sender.IPAV3), averagevar)

                        # series.append(3.5, 0.6)  # Punto intermedio
                        # series.append(3.5, 0.2)  # Punto intermedio
                        series.append(float(sender.maxRange), 0)  # Punto final
                        series1.append(float(sender.maxRange), 0)  # Punto final
                        series2.append(float(sender.maxRange), 0)  # Punto final

                        chart = QChart()
                        chart.addSeries(series)
                        chart.addSeries(series1)
                        chart.addSeries(series2)

                    elif sender.interPoints == 2:
                        series.append(float(sender.IPAV1), float(sender.IP11))
                        series.append(float(sender.IPAV2), float(sender.IP21))
                        series1.append(float(sender.IPAV1), float(sender.IP12))
                        series1.append(float(sender.IPAV2), float(sender.IP22))
                        averagevar = float(
                            (float(sender.IP11) + float(sender.IP12)) / 2
                        )
                        series2.append(float(sender.IPAV1), averagevar)
                        averagevar = float(
                            (float(sender.IP21) + float(sender.IP22)) / 2
                        )
                        series2.append(float(sender.IPAV2), averagevar)

                        # series.append(3.5, 0.6)  # Punto intermedio
                        # series.append(3.5, 0.2)  # Punto intermedio
                        series.append(float(sender.maxRange), 0)  # Punto final
                        series1.append(float(sender.maxRange), 0)  # Punto final
                        series2.append(float(sender.maxRange), 0)  # Punto final

                        chart = QChart()
                        chart.addSeries(series)
                        chart.addSeries(series1)
                        chart.addSeries(series2)
                    elif sender.interPoints == 1:
                        series.append(float(sender.IPAV1), float(sender.IP11))
                        series1.append(float(sender.IPAV1), float(sender.IP12))
                        averagevar = float(
                            (float(sender.IP11) + float(sender.IP12)) / 2
                        )
                        series2.append(float(sender.IPAV1), averagevar)

                        series.append(float(sender.maxRange), 0)  # Punto final
                        series1.append(float(sender.maxRange), 0)  # Punto final
                        series2.append(float(sender.maxRange), 0)  # Punto final

                        chart = QChart()
                        chart.addSeries(series)
                        chart.addSeries(series1)
                        chart.addSeries(series2)
                    else:
                        series.append(float(sender.maxRange), 0)  # Punto final
                        chart = QChart()
                        chart.addSeries(series)

                # chart.setTitle("Gráfico de Línea")
                chart.legend().setVisible(False)

                # Crear los ejes X e Y y establecer etiquetas en los puntos
                x_axis = QValueAxis()
                x_axis.setLabelFormat("%.1f")
                x_axis.setTickCount(2)  # Número de etiquetas en el eje X
                x_axis.setRange(float(sender.minRange), float(sender.maxRange))

                y_axis = QValueAxis()
                y_axis.setLabelFormat("%.1f")
                y_axis.setTickCount(4)  # Número de etiquetas en el eje Y
                y_axis.setRange(0, 1)

                chart.addAxis(x_axis, Qt.AlignmentFlag.AlignBottom)
                chart.addAxis(y_axis, Qt.AlignmentFlag.AlignLeft)

                series.attachAxis(x_axis)
                series.attachAxis(y_axis)

                chart.setBackgroundBrush(brush)
                chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)

                self.vNodeInfo.groupBoxNI.setVisible(True)

                # Crear la vista del gráfico
                # chart_view = QChartView()
                self.vNodeInfo.plainTextAVC.setReadOnly(True)

                chart_view = ChartView(
                    text_X=self.vNodeInfo.plainTextAVC,
                    text_Y=self.vNodeInfo.plainTextAU,
                    posX_1=float(sender.minRange),
                    posX_2=float(sender.maxRange),
                )
                chart_view.setChart(chart)
                chart_view.setFrameShape(QFrame.Shape.NoFrame)
                chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)
                chart_view.setBackgroundBrush(brush)

                self.layoutVCU.addWidget(chart_view)
                self.vNodeInfo.AttMP.raise_()

            elif sender.unitType == "Discrete":
                background_color = QColor("#F0F0F0")
                brush = QBrush(background_color)
                self.clear_layout(self.vNodeInfo.hLayoutVCU)
                self.clear_layout(self.vNodeInfo.vLayoutVCU)
                data = []
                valmins = []
                valmaxs = []
                for i in range(1, len(sender.optionsList) + 1):
                    variable_name1 = "UP{}1".format(i)
                    variable_name2 = "UP{}2".format(i)
                    valmins.append(float(getattr(sender, variable_name1)))
                    valmaxs.append(float(getattr(sender, variable_name2)))

                for valmin, valmax in zip(valmins, valmaxs):
                    data.append((valmin, valmax))

                self.vNodeInfo.groupBoxNI.setVisible(False)

                chart_widget = LineBarChartWidget()
                names_chart = NamesChart()
                names_chart.set_connections(sender.optionsList)
                chart_widget.set_data(data)
                # chart_widget.set_connections(selected_attr.optionsList)

                chart_widget = LineBarChartWidget()
                names_chart = NamesChart()
                chart_widget.set_data(data)
                names_chart.set_connections(sender.optionsList)
                self.clear_layout(self.vNodeInfo.hLayoutVCU)
                self.clear_layout(self.vNodeInfo.vLayoutVCU)
                self.vNodeInfo.hLayoutVCU.addWidget(chart_widget)
                self.vNodeInfo.vLayoutVCU.addWidget(names_chart)

            else:
                pass

        def copy_text():
            global attributes
            global attributesnames
            global alternatives
            attributesnames.clear()
            if len(self.vNodeInfo.textLabel.toPlainText()) > 15:
                self.vNodeInfo.setWindowFlags(
                    self.windowFlags() & ~Qt.WindowType.WindowStaysOnTopHint
                )
                self.vNodeInfo.show()
                QMessageBox.warning(
                    self,
                    "Warning",
                    f"The text cannot exceed 15 characters. There are {len(self.vNodeInfo.textLabel.toPlainText())} characters.",
                )
                self.vNodeInfo.setWindowFlags(
                    self.windowFlags() | Qt.WindowType.WindowStaysOnTopHint
                )
                self.vNodeInfo.show()
                return
            textNameNI = self.vNodeInfo.textName.toPlainText()
            textDescNI = self.vNodeInfo.textDescription.toPlainText()
            textLabelNI = self.vNodeInfo.textLabel.toPlainText()[:15]
            sender.setText(textLabelNI)
            sender.label_name = textNameNI
            sender.nodeDescription = textDescNI
            if sender.finalNode:
                if self.vNodeInfo.radioBCont.isChecked():
                    text = self.vNodeInfo.textMinRangeCont.toPlainText()
                    text2 = self.vNodeInfo.textMaxRangeCont.toPlainText()
                    try:
                        number = float(text)  # or int(text)
                        number2 = float(text2)  # or int(text)
                        if number > number2:
                            self.vNodeInfo.setWindowFlags(
                                self.windowFlags() & ~Qt.WindowType.WindowStaysOnTopHint
                            )
                            self.vNodeInfo.show()
                            QMessageBox.warning(
                                self,
                                "Error",
                                "The Minimum Range value cannot be higher than the Maximum Range value",
                            )
                            self.vNodeInfo.setWindowFlags(
                                self.windowFlags() | Qt.WindowType.WindowStaysOnTopHint
                            )
                            self.vNodeInfo.textMinRangeCont.clear()
                            self.vNodeInfo.show()
                            return

                    except (ValueError, AttributeError):
                        self.vNodeInfo.setWindowFlags(
                            self.windowFlags() & ~Qt.WindowType.WindowStaysOnTopHint
                        )
                        self.vNodeInfo.show()
                        QMessageBox.warning(
                            self, "Error", "The text is not a valid number"
                        )
                        self.vNodeInfo.setWindowFlags(
                            self.windowFlags() | Qt.WindowType.WindowStaysOnTopHint
                        )
                        self.vNodeInfo.textMinRangeCont.clear()
                        self.vNodeInfo.textMaxRangeCont.clear()
                        self.vNodeInfo.show()
                        return
                    else:
                        sender.unitType = "Continuous"
                        textDC = self.vNodeInfo.textDescCont.toPlainText()
                        sender.unitDescription = textDC
                        textUC = self.vNodeInfo.textUnitsCont.toPlainText()
                        sender.unitName = textUC
                        textMN = self.vNodeInfo.textMinRangeCont.toPlainText()
                        sender.minRange = textMN
                        textMX = self.vNodeInfo.textMaxRangeCont.toPlainText()
                        sender.maxRange = textMX
                        if self.vNodeInfo.radioBMPI.isChecked():
                            sender.mostPrefered = "Inf"
                        elif self.vNodeInfo.radioBMPS.isChecked():
                            sender.mostPrefered = "Sup"

                elif self.vNodeInfo.radioBDisc.isChecked():
                    if not sender.unitType == "Discrete":
                        sender.unitType = "Discrete"
                        textDD = self.vNodeInfo.textDescDisc.toPlainText()
                        sender.unitDescription = textDD
                        sender.optionsList.clear()
                        for i in range(self.vNodeInfo.tableDiscrete.rowCount()):
                            item = self.vNodeInfo.tableDiscrete.item(i, 0)
                            if item is not None:
                                sender.optionsList.append(item.text())
                        for i in range(1, len(sender.optionsList) + 1):
                            num = float((i - 1) / len(sender.optionsList))
                            variable_name = "UP{}1".format(i)
                            setattr(sender, variable_name, num)
                            variable_name2 = "UP{}2".format(i)
                            setattr(
                                sender,
                                variable_name2,
                                num + (1 / len(sender.optionsList)),
                            )

                            print(f"self.up i 1: {getattr(sender, variable_name)}")
                            print(f"self.up i 2: {getattr(sender, variable_name2)}")

                    else:
                        sender.unitType = "Discrete"
                        textDD = self.vNodeInfo.textDescDisc.toPlainText()
                        sender.unitDescription = textDD
                        if (
                            len(sender.optionsList)
                            != self.vNodeInfo.tableDiscrete.rowCount()
                        ):
                            sender.optionsList.clear()
                            for i in range(self.vNodeInfo.tableDiscrete.rowCount()):
                                item = self.vNodeInfo.tableDiscrete.item(i, 0)
                                if item is not None:
                                    sender.optionsList.append(item.text())
                        for i in range(1, len(sender.optionsList) + 1):
                            num = float((i - 1) / len(sender.optionsList))
                            variable_name = "UP{}1".format(i)
                            setattr(sender, variable_name, num)
                            variable_name2 = "UP{}2".format(i)
                            setattr(
                                sender,
                                variable_name2,
                                num + (1 / len(sender.optionsList)),
                            )

                            print(f"self.up i 1: {getattr(sender, variable_name)}")
                            print(f"self.up i 2: {getattr(sender, variable_name2)}")

                    # sender.interPoints = len(sender.optionsList)

                    # sender.optionDiscrete = ""
                    # for i in range(self.vNodeInfo.tableDiscrete.rowCount()):
                    #     radio_button = self.vNodeInfo.tableDiscrete.cellWidget(i, 1)
                    #     if isinstance(radio_button, QRadioButton) and radio_button.isChecked():
                    #         sender.optionDiscrete = self.vNodeInfo.tableDiscrete.item(i, 0).text()
                    #         break

                for attr in attributes:
                    attributesnames.append(attr.text())

                for altern in alternatives:
                    for attr in altern.attr:
                        if attr.name == sender.text():
                            sender.unitType
                            if isinstance(attr, ContinuousAttribute):
                                attr.value1 = sender.minRange
                                attr.value2 = sender.maxRange

                            elif isinstance(attr, DiscreteAttribute):
                                attr.attributenames = sender.optionsList
                                attr.selected = ""

            self.getFinalAttributes(self.labels)
            self.vNodeInfo.close()

        # If one of these widgets change, SAVE button available

        def enable_apply():
            if sender.finalNode:
                if (
                    (self.vNodeInfo.radioBCont.isChecked())
                    and (
                        self.vNodeInfo.textName.toPlainText().strip() != ""
                        and self.vNodeInfo.textDescription.toPlainText().strip() != ""
                        and self.vNodeInfo.textLabel.toPlainText().strip() != ""
                    )
                    and (
                        self.vNodeInfo.textDescCont.toPlainText()
                        and self.vNodeInfo.textUnitsCont.toPlainText()
                        and self.vNodeInfo.textMinRangeCont.toPlainText()
                        and self.vNodeInfo.textMaxRangeCont.toPlainText()
                        and (
                            self.vNodeInfo.radioBMPI.isChecked()
                            or self.vNodeInfo.radioBMPS.isChecked()
                        )
                    )
                ):
                    self.vNodeInfo.buttonApply.setEnabled(True)
                elif (
                    (self.vNodeInfo.radioBDisc.isChecked())
                    and (
                        self.vNodeInfo.textName.toPlainText().strip() != ""
                        and self.vNodeInfo.textDescription.toPlainText().strip() != ""
                        and self.vNodeInfo.textLabel.toPlainText().strip() != ""
                    )
                    and (
                        self.vNodeInfo.textDescDisc.toPlainText()
                        and (
                            self.vNodeInfo.tableDiscrete.rowCount() > 0
                            and self.vNodeInfo.tableDiscrete.columnCount() > 0
                        )
                    )
                ):
                    self.vNodeInfo.buttonApply.setEnabled(True)
                else:
                    self.vNodeInfo.buttonApply.setEnabled(False)
            else:
                if (
                    self.vNodeInfo.textName.toPlainText().strip() != ""
                    and self.vNodeInfo.textDescription.toPlainText().strip() != ""
                    and self.vNodeInfo.textLabel.toPlainText().strip() != ""
                ):
                    self.vNodeInfo.buttonApply.setEnabled(True)

        self.vNodeInfo.textName.textChanged.connect(enable_apply)
        self.vNodeInfo.textDescription.textChanged.connect(enable_apply)
        self.vNodeInfo.textLabel.textChanged.connect(enable_apply)

        self.vNodeInfo.radioBCont.toggled.connect(enable_apply)
        self.vNodeInfo.textDescCont.textChanged.connect(enable_apply)
        self.vNodeInfo.textUnitsCont.textChanged.connect(enable_apply)
        self.vNodeInfo.textMinRangeCont.textChanged.connect(enable_apply)
        self.vNodeInfo.textMaxRangeCont.textChanged.connect(enable_apply)

        self.vNodeInfo.radioBDisc.toggled.connect(enable_apply)
        self.vNodeInfo.textDescDisc.textChanged.connect(enable_apply)
        self.vNodeInfo.buttonApply.clicked.connect(copy_text)
        self.vNodeInfo.tableDiscrete.itemChanged.connect(enable_apply)

        # self.vNodeInfo.textName.textChanged.connect(enable_apply)
        # self.vNodeInfo.textDescription.textChanged.connect(enable_apply)
        # self.vNodeInfo.textLabel.textChanged.connect(enable_apply)

        # self.vNodeInfo.textDescCont.textChanged.connect(enable_apply)
        # self.vNodeInfo.textUnitsCont.textChanged.connect(enable_apply)
        # self.vNodeInfo.textMinRangeCont.textChanged.connect(enable_apply)
        # self.vNodeInfo.textMaxRangeCont.textChanged.connect(enable_apply)
        # self.vNodeInfo.textDescDisc.textChanged.connect(enable_apply)
        # self.vNodeInfo.buttonApply.clicked.connect(copy_text)
        self.vNodeInfo.show()

    #  shows a new screen with the Alternatives for a specific attribute
    # with the option of being able to modify the values. This new screen is the
    # initialisation of a class that we will see that is called
    # VentanaAltCon(QMainWindow).

    def modifyAltCon(self, sender):
        global attributes
        global alternatives
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowStaysOnTopHint)
        # # self.lower()
        self.show()
        self.vModAlt = VentanaModifyAltCon()
        self.vModAlt.setWindowFlags(
            self.windowFlags() | Qt.WindowType.WindowStaysOnTopHint
        )
        self.vModAlt.raise_()

        self.vModAlt.textAttributeName.setPlainText(sender.text())
        self.vModAlt.textAttributeDescription.setPlainText(sender.nodeDescription)
        self.vModAlt.textAttributeUnits.setPlainText(sender.unitDescription)

        self.vModAlt.textAttributeName.setReadOnly(True)
        self.vModAlt.textAttributeDescription.setReadOnly(True)
        self.vModAlt.textAttributeUnits.setReadOnly(True)

        self.vModAlt.tableWidgetMAC.clear()

        textMinRange = float(sender.minRange)
        textMaxRange = float(sender.maxRange)
        # print(f"textMinRange: "+str(textMinRange))
        # print(f"textMaxRange: "+str(textMaxRange))
        index = None

        for i, attr in enumerate(attributes):
            if attr.unitType == "Continuous":
                print(f"sender.text(): {sender.text()} and attr.text(): {attr.text()}")
                if (str(float(attr.minRange)) == str(textMinRange)) and (
                    str(float(attr.maxRange)) == str(textMaxRange)
                    and (sender.text() and attr.text())
                ):
                    index = i
                    break
                else:
                    index = None
            elif attr.unitType == "Discrete":
                items = []
                for j in range(self.vNodeInfo.tableDiscrete.rowCount()):
                    item = self.vNodeInfo.tableDiscrete.item(j, 0)
                    if item is not None:
                        items.append(item.text())
                if (attr.optionsList == items) and (sender.text() == attr.text()):
                    index = i
                    break
                else:
                    index = None

        if sender.unitType == "Continuous":
            self.vModAlt.labelMACAV.hide()
            self.vModAlt.tableWidgetMAC.setRowCount(len(alternatives))
            widthTable = self.vModAlt.tableWidgetMAC.width() // 2
            self.vModAlt.tableWidgetMAC.setColumnCount(2)
            self.vModAlt.tableWidgetMAC.setColumnWidth(0, widthTable)
            self.vModAlt.tableWidgetMAC.setColumnWidth(1, widthTable)
            for i, altern in enumerate(alternatives):
                elementCD = altern.attr[index]
                if isinstance(elementCD, ContinuousAttribute):
                    value1 = float(elementCD.value1)
                    value2 = float(elementCD.value2)
                    item = QTableWidgetItem(str(value1))
                    item2 = QTableWidgetItem(str(value2))
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    self.vModAlt.tableWidgetMAC.setItem(i, 0, item)
                    item2.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    self.vModAlt.tableWidgetMAC.setItem(i, 1, item2)

        elif sender.unitType == "Discrete":
            self.vModAlt.pushButtonSaveMAC.setEnabled(True)
            self.vModAlt.labelMACMin.hide()
            self.vModAlt.labelMACMax.hide()
            widthTable = self.vModAlt.tableWidgetMAC.width()
            self.vModAlt.tableWidgetMAC.setRowCount(len(alternatives))
            self.vModAlt.tableWidgetMAC.setColumnCount(1)
            self.vModAlt.tableWidgetMAC.setColumnWidth(0, widthTable)
            for i, altern in enumerate(alternatives):
                elementCD = altern.attr[index]
                print(
                    f"P: elementCD.name: {elementCD.name}, self.vModAlt.textAttributeName.toPlainText()  {self.vModAlt.textAttributeName.toPlainText()}\n"
                )
                if elementCD.name == self.vModAlt.textAttributeName.toPlainText():
                    if isinstance(elementCD, DiscreteAttribute):
                        combo_box = QComboBox()
                        combo_box.addItems(elementCD.attributenames)
                        if elementCD.selected:
                            selected_option = elementCD.selected
                            index1 = elementCD.attributenames.index(selected_option)
                            combo_box.setCurrentIndex(index1)
                        else:
                            selected_item = ""
                            combo_box.setEditText(selected_item)
                        selected_item = QTableWidgetItem(selected_option)
                        selected_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

                        # self.vNodeInfo.tableWidgetVAC.setItem(1, column+3, selected_item)
                        self.vModAlt.tableWidgetMAC.setCellWidget(i, 0, combo_box)

        else:
            self.vModAlt.show()
            pass

        self.vModAlt.show()

    def view_table(self, ventana, table, sender):
        columna2 = 2
        columna4 = 4
        sumNum = 0
        sumDenT = 0
        K = 0
        datos = []

        for filaLocal in range(table.rowCount()):
            try:
                valor_columna2L = float(table.item(filaLocal, 2).text())
                valor_columna4L = float(table.item(filaLocal, 4).text())
                datos.append((valor_columna2L, valor_columna4L))
                sumDenT += valor_columna2L + valor_columna4L
            except (ValueError, AttributeError):
                ventana.hide()
                QMessageBox.warning(self, "Warning", "Complete all values correctly.")
                ventana.show()
                traceback.print_exc()
                return

        for par in datos:
            firstpair = par[0]
            secondpair = par[1]
            if not (
                isinstance(firstpair, (float, int))
                and isinstance(secondpair, (float, int))
            ):
                ventana.hide()
                QMessageBox.warning(
                    self, "Warning", "Complete all values with the correct format."
                )
                ventana.show()
                traceback.print_exc()
                return
            if firstpair > secondpair:
                ventana.hide()
                QMessageBox.warning(
                    self, "Warning", "Lower Bound must be lower than Upper Bound."
                )
                ventana.show()
                traceback.print_exc()
                return

        for fila in range(table.rowCount()):
            try:

                parG = datos[fila]

                valor_columna2 = parG[0]
                valor_columna4 = parG[1]

                if not (
                    (valor_columna2 == sender.connections[fila].weightI)
                    or (valor_columna4 == sender.connections[fila].weightS)
                ):
                    # crea aquí las funciones
                    continue

                sumNum = valor_columna2 + valor_columna4
                K = sumNum / sumDenT

                KI = float((2 * K * valor_columna2) / sumNum)
                KI = "{:.3f}".format(KI)
                # sender.connections[fila].weightI = KI

                KS = float((2 * K * valor_columna4) / sumNum)
                KS = "{:.3f}".format(KS)
                # sender.connections[fila].weightS = KS
                print(
                    f"fila: {fila}, sumNum: {sumNum},sumDenT: {sumDenT}, K: {K}, KI: {KI}, KS: {KS}"
                )
                KI = QTableWidgetItem(str(KI))
                KS = QTableWidgetItem(str(KS))
                table.setItem(fila, 2, KI)
                table.setItem(fila, 4, KS)

            except (ValueError, AttributeError):
                QMessageBox.warning(self, "Warning", "Complete all values correctly.")
                traceback.print_exc()
                return

    def norm_table(self, table, sender):
        for fila in range(table.rowCount()):
            try:
                valor_columna2 = float(table.item(fila, 2).text())
                valor_columna4 = float(table.item(fila, 4).text())
                sender.connections[fila].weightI = valor_columna2
                sender.connections[fila].weightS = valor_columna4
            except (ValueError, AttributeError):
                traceback.print_exc()
                return

    # shows a new screen with the values of the attribute and the option
    # of being able to insert new intermediate points and a display screen of those
    # points with a line graph. This new screen is the initialisation of a class that we
    # will see called QMainWindow.

    def open_LUF(self, sender):
        self.vLuf = VentanaLUF()
        global attributes
        global alternatives
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowStaysOnTopHint)
        # # self.lower()
        self.show()
        self.vLuf = VentanaLUF()
        self.vLuf.setWindowFlags(
            self.windowFlags() | Qt.WindowType.WindowStaysOnTopHint
        )
        self.vLuf.raise_()

        self.vLuf.attNameLUF.setText(sender.text())
        self.vLuf.textLowerBound.setPlainText(str(sender.minRange))
        self.vLuf.textUpperBound.setPlainText(str(sender.maxRange))
        if sender.mostPrefered == "Sup":
            self.vLuf.radioButtonMI.setChecked(True)
        else:
            self.vLuf.radioButtonMD.setChecked(True)

        if sender.interPoints == 5:
            self.vLuf.checkBoxP1.setChecked(True)
            self.vLuf.checkBoxP2.setChecked(True)
            self.vLuf.checkBoxP3.setChecked(True)
            self.vLuf.checkBoxP4.setChecked(True)
            self.vLuf.checkBoxP5.setChecked(True)
            self.vLuf.textAVP1.setPlainText(str(sender.IPAV1))
            self.vLuf.textUP11.setPlainText(str(sender.IP11))
            self.vLuf.textUP12.setPlainText(str(sender.IP12))
            self.vLuf.textAVP2.setPlainText(str(sender.IPAV2))
            self.vLuf.textUP21.setPlainText(str(sender.IP21))
            self.vLuf.textUP22.setPlainText(str(sender.IP22))
            self.vLuf.textAVP3.setPlainText(str(sender.IPAV3))
            self.vLuf.textUP31.setPlainText(str(sender.IP31))
            self.vLuf.textUP32.setPlainText(str(sender.IP32))
            self.vLuf.textAVP4.setPlainText(str(sender.IPAV4))
            self.vLuf.textUP41.setPlainText(str(sender.IP41))
            self.vLuf.textUP42.setPlainText(str(sender.IP42))
            self.vLuf.textAVP5.setPlainText(str(sender.IPAV5))
            self.vLuf.textUP51.setPlainText(str(sender.IP51))
            self.vLuf.textUP52.setPlainText(str(sender.IP52))

        elif sender.interPoints == 4:
            self.vLuf.checkBoxP1.setChecked(True)
            self.vLuf.checkBoxP2.setChecked(True)
            self.vLuf.checkBoxP3.setChecked(True)
            self.vLuf.checkBoxP4.setChecked(True)
            self.vLuf.textAVP1.setPlainText(str(sender.IPAV1))
            self.vLuf.textUP11.setPlainText(str(sender.IP11))
            self.vLuf.textUP12.setPlainText(str(sender.IP12))
            self.vLuf.textAVP2.setPlainText(str(sender.IPAV2))
            self.vLuf.textUP21.setPlainText(str(sender.IP21))
            self.vLuf.textUP22.setPlainText(str(sender.IP22))
            self.vLuf.textAVP3.setPlainText(str(sender.IPAV3))
            self.vLuf.textUP31.setPlainText(str(sender.IP31))
            self.vLuf.textUP32.setPlainText(str(sender.IP32))
            self.vLuf.textAVP4.setPlainText(str(sender.IPAV4))
            self.vLuf.textUP41.setPlainText(str(sender.IP41))
            self.vLuf.textUP42.setPlainText(str(sender.IP42))
        elif sender.interPoints == 3:
            self.vLuf.checkBoxP1.setChecked(True)
            self.vLuf.checkBoxP2.setChecked(True)
            self.vLuf.checkBoxP3.setChecked(True)
            self.vLuf.textAVP1.setPlainText(str(sender.IPAV1))
            self.vLuf.textUP11.setPlainText(str(sender.IP11))
            self.vLuf.textUP12.setPlainText(str(sender.IP12))
            self.vLuf.textAVP2.setPlainText(str(sender.IPAV2))
            self.vLuf.textUP21.setPlainText(str(sender.IP21))
            self.vLuf.textUP22.setPlainText(str(sender.IP22))
            self.vLuf.textAVP3.setPlainText(str(sender.IPAV3))
            self.vLuf.textUP31.setPlainText(str(sender.IP31))
            self.vLuf.textUP32.setPlainText(str(sender.IP32))
        elif sender.interPoints == 2:
            self.vLuf.checkBoxP1.setChecked(True)
            self.vLuf.checkBoxP2.setChecked(True)
            self.vLuf.textAVP1.setPlainText(str(sender.IPAV1))
            self.vLuf.textUP11.setPlainText(str(sender.IP11))
            self.vLuf.textUP12.setPlainText(str(sender.IP12))
            self.vLuf.textAVP2.setPlainText(str(sender.IPAV2))
            self.vLuf.textUP21.setPlainText(str(sender.IP21))
            self.vLuf.textUP22.setPlainText(str(sender.IP22))
        elif sender.interPoints == 1:
            self.vLuf.checkBoxP1.setChecked(True)
            self.vLuf.textAVP1.setPlainText(str(sender.IPAV1))
            self.vLuf.textUP11.setPlainText(str(sender.IP11))
            self.vLuf.textUP12.setPlainText(str(sender.IP12))

        self.vLuf.show()

    # shows a new screen where we can see all the values of the
    # discrete attribute. This new screen is the initialisation of a class
    # that we will see that is called QMainWindow.
    def open_UDV(self, sender):
        self.vUDV = VentanaUDV()
        global attributes
        global alternatives
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowStaysOnTopHint)
        # # self.lower()
        self.show()
        self.vUDV = VentanaUDV()
        self.vUDV.setWindowFlags(
            self.windowFlags() | Qt.WindowType.WindowStaysOnTopHint
        )
        self.vUDV.raise_()

        self.vUDV.attNameUDV.setText(sender.text())

        self.vUDV.tableWidgetUDV.setContentsMargins(0, 0, 0, 0)
        self.vUDV.tableWidgetUDV.setStyleSheet("background-color: #F0F0F0;")
        self.vUDV.tableWidgetUDV.setFrameShape(QFrame.Shape.NoFrame)
        self.vUDV.tableWidgetUDV.setLineWidth(0)
        self.vUDV.tableWidgetUDV.setShowGrid(False)

        num_rows = len(sender.optionsList)
        num_columns = 7
        widthTable = self.vUDV.tableWidgetUDV.width() // 7
        print(f"P: widthTable {widthTable}")
        self.vUDV.tableWidgetUDV.setRowCount(num_rows)
        self.vUDV.tableWidgetUDV.setColumnCount(num_columns)
        self.vUDV.tableWidgetUDV.setColumnWidth(0, widthTable)
        # font = QFont()
        # font.setBold(True)
        # header_item.setFont(font)
        # item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignCenter)
        # self.vUDV.tableWidgetUDV.setSpan(0, 0, 1, 2) # ocupies two columns
        self.vUDV.tableWidgetUDV.verticalHeader().setVisible(False)
        self.vUDV.tableWidgetUDV.horizontalHeader().setVisible(False)

        for i in range(num_columns):
            if i == 4:
                self.vUDV.tableWidgetUDV.setColumnWidth(i, 35)
            elif i == 1:
                self.vUDV.tableWidgetUDV.setColumnWidth(i, 235)
            elif i == 3:
                self.vUDV.tableWidgetUDV.setColumnWidth(i, 80)
            elif i == 5:
                self.vUDV.tableWidgetUDV.setColumnWidth(i, 80)
            elif i == 6:
                self.vUDV.tableWidgetUDV.setColumnWidth(i, 35)
            else:
                self.vUDV.tableWidgetUDV.setColumnWidth(i, widthTable)

        for i, optL in enumerate(sender.optionsList):
            item = QTableWidgetItem("Attribute Value (x): ")
            item2 = QTableWidgetItem(optL)
            item3 = QTableWidgetItem("Utility: (")
            item4 = str(getattr(sender, "UP" + str(i + 1) + "1"))
            item4 = QTableWidgetItem(item4)
            item5 = QTableWidgetItem(" , ")
            item6 = str(getattr(sender, "UP" + str(i + 1) + "2"))
            item6 = QTableWidgetItem(item6)
            item7 = QTableWidgetItem(")")
            font = QFont()
            font.setBold(True)
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            item2.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            item3.setTextAlignment(
                Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignCenter
            )
            item2.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            item4.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            item5.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            item6.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            item7.setTextAlignment(
                Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignCenter
            )
            item.setFont(font)
            item3.setFont(font)
            item5.setFont(font)
            item7.setFont(font)
            # brush = QBrush(QColor(0, 0, 0, 25))  # Color negro con transparencia baja (25)
            # item.setBackground(brush)
            item.setFlags(Qt.ItemFlag.ItemIsEnabled)
            self.vUDV.tableWidgetUDV.setItem(i, 0, item)
            item2.setFlags(Qt.ItemFlag.ItemIsEnabled)
            self.vUDV.tableWidgetUDV.setItem(i, 1, item2)
            item3.setFlags(Qt.ItemFlag.ItemIsEnabled)
            self.vUDV.tableWidgetUDV.setItem(i, 2, item3)
            self.vUDV.tableWidgetUDV.setItem(i, 3, item4)
            item5.setFlags(Qt.ItemFlag.ItemIsEnabled)
            self.vUDV.tableWidgetUDV.setItem(i, 4, item5)
            self.vUDV.tableWidgetUDV.setItem(i, 5, item6)
            item7.setFlags(Qt.ItemFlag.ItemIsEnabled)
            self.vUDV.tableWidgetUDV.setItem(i, 6, item7)

            print(f"P: optL: {optL}")

        self.vUDV.pushButtonSaveUDV.setEnabled(True)
        self.vUDV.pushButtonViewUDV.setEnabled(True)
        self.vUDV.attNameUDV.setVisible(False)

        self.vUDV.show()

    # shows a new screen with the Alternatives and the consequences.
    # This new screen is the initialisation of a class that we will see that is called
    # WindowAltCon(QMainWindow).
    def open_AltCon(self):
        self.vAltCon = VentanaAltCon()
        self.vAltCon.show()

    # shows a new screen where we can see all the values of the
    # continuous or discrete attributes. This new screen is the initialisation of a class
    # that we will see that is called QMainWindow.
    def open_VCU(self):
        self.vVCU = VentanaCUV()
        self.vVCU.show()

    # shows a new screen where we can see all the values of the weights
    # of the children of the intermediate nodes. This new screen is the initialisation of
    # a class that we will see called QMainWindow.
    def open_VTW(self):
        self.vVTW = VentanaVTW()
        self.vVTW.show()

    def open_AltClas(self):
        self.vAlt = VentanaAltClas()
        self.vAlt.show()

    # deletes the node 'Overall Objective' which leads to the complete
    # deletion of all nodes (Labels) and the screen becomes empty.
    def delete_PO(self):
        global PrimaryObjective
        global currentColumn
        global currentRow
        global Branch
        global identifier_labels
        global Leaf
        global attributes
        global alternatives
        global attributesnames
        attributesnames.clear()

        self.place_lines()
        reply = QMessageBox.warning(
            self.parent(),
            "Delete Overall Objetive",
            "Are you sure you want to delete the Overall Objective? If you delete it, all other elements will be deleted.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.No:
            pass
        elif reply == QMessageBox.StandardButton.Yes:

            for child in self.labels:
                if isinstance(child, QLabel):
                    child.deleteLater()
            self.labels.clear()
            PrimaryObjective = False
            Branch = 0
            Leaf = 0  # if the delete button of the PO Label is triggered the num of Leaf is 0
            identifier_labels = 0
            currentRow = 0
            currentColumn = 0
            attributes.clear()
            alternatives.clear()
            attributesnames.clear()
            self.actionSaveWorkspace.setEnabled(False)
            self.actionSave_WorkSpace.setEnabled(False)
            self.actionSave_WorkSpace_As.setEnabled(False)
            print(f"Labels: {self.labels}")
            self.place_lines()

        self.place_lines()
        self.getFinalAttributes(self.labels)

    # once the upper right button has been pressed to close the screen,
    # a window pops up to confirm the closure, saving the workspace or discarding it.

    def closeEvent(self, event):
        global identifier_labels
        if self.labels != 0 and identifier_labels != 0:
            reply = QMessageBox.warning(
                self.parent(),
                "GMAA WorkSpace",
                "The WorkSpace Document has been modified. \n Do you want to save changes?",
                QMessageBox.StandardButton.Save
                | QMessageBox.StandardButton.Discard
                | QMessageBox.StandardButton.Cancel,
                QMessageBox.StandardButton.Save,
            )

            if reply == QMessageBox.StandardButton.Discard:
                event.accept()

            if reply == QMessageBox.StandardButton.Save:
                event.ignore()
                self.save_proInput()
                self.close_window()

            if reply == QMessageBox.StandardButton.Cancel:
                event.ignore()

        else:
            event.accept()

    def close_window(self):
        self.close()  # closes the program


# window to help the user


class VentanaHelp(QMainWindow):
    def __init__(self, parent=None):
        super(VentanaHelp, self).__init__(parent)
        uic.loadUi("aboutGMAA.ui", self)
        icono = QIcon("iconoUPM.ico")
        super(VentanaHelp, self).setWindowIcon(icono)
        super(VentanaHelp, self).setWindowTitle("About GMAA")

        self.botonOk.clicked.connect(self.close_windowH)

    def close_windowH(self):
        self.close()


# It shows the window designed with 'Qt Designer' where it is initialised with three
# QLineEdit: User, Institution and Password. If the User and Password match, the
# window closes and the main application window
# 'WindowPrincipalGMAA(QMainWindow)' opens.
class VentanaLogIn(QMainWindow):
    def __init__(self, parent=None):
        super(VentanaLogIn, self).__init__(parent)
        uic.loadUi("LogIn.ui", self)
        # carga el icono desde un archivo de imagen
        icono = QIcon("iconoUPM.ico")
        super(VentanaLogIn, self).setWindowIcon(
            icono
        )  # establece el icono de la ventana
        super(VentanaLogIn, self).setWindowTitle("Inicio Sesión")
        self.lineUser.setPlaceholderText(" Please enter your username...")
        self.linePw.setPlaceholderText(" Please enter your password...")
        self.lineInstitution.setPlaceholderText("Please enter your Institution...")
        palette = QPalette()
        color = QColor(255, 255, 255)  # White Color
        palette.setColor(QPalette.ColorRole.Text, color)
        self.lineUser.setPalette(palette)
        self.lineInstitution.setPalette(palette)
        self.linePw.setPalette(palette)
        self.linePw.setEchoMode(QLineEdit.EchoMode.Password)
        self.linePw.setEnabled(False)

        self.vPrincipal = VentanaPrincipalGMAA()
        self.vPrincipal.setEnabled(False)
        self.vPrincipal.setWindowFlags(Qt.WindowType.WindowCloseButtonHint)
        self.vPrincipal.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)
        # self.vPrincipal.setWindowFlags(Qt.WindowType.WindowCloseButtonHint, False)
        # self.vPrincipal.setWindowFlag(Qt.WindowCloseButtonHint, False)

        self.vPrincipal.showFullScreen()
        self.raise_()

        # button signals
        self.lineUser.textChanged.connect(self.enablePw)
        self.botonLogIn.clicked.connect(self.checkUserPw)
        self.destroyed.connect(
            app.quit
        )  # closes the application when the window closes

    # to know when we can write in LinePw's QLineEdit

    def enablePw(self, text):
        if self.lineUser.text():
            self.linePw.setEnabled(True)
        else:
            self.linePw.setEnabled(False)
            # self.linePw.setReadOnly(True)
            self.linePw.clear()

    # we check the user - password

    def checkUserPw(self):
        if self.lineUser.text() == "" and self.linePw.text() == "":  # to log in
            main_window_gmaa = VentanaPrincipalGMAA()
            main_window_gmaa.setWindowFlags(
                Qt.WindowType.Window
                | Qt.WindowType.WindowCloseButtonHint
                | Qt.WindowType.WindowMinimizeButtonHint
                | Qt.WindowType.WindowMaximizeButtonHint
                | Qt.WindowType.WindowFullscreenButtonHint
                | Qt.WindowType.WindowMinMaxButtonsHint
            )
            main_window_gmaa.showMaximized()
            # main_window_gmaa.show()
            self.close()

    def closeEvent(self, event):
        self.vPrincipal.close()
        event.accept()


# It shows the window designed with 'Qt Designer' where there is a QTableWidget
# with all the alternatives that have been added and the values of their attributes.
# Also as we find some buttons to add, modify and delete the alternatives.
class VentanaAltCon(QMainWindow):
    global attributes
    global attributesnames
    global alternatives

    def __init__(self, parent=None):
        super(VentanaAltCon, self).__init__(parent)
        uic.loadUi("alternativeConsequences.ui", self)
        icono = QIcon("iconoUPM.ico")
        super(VentanaAltCon, self).setWindowIcon(icono)
        super(VentanaAltCon, self).setWindowTitle("Alternative Consequences")
        self.VentanaPrincipalGMAA = parent
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)

        if alternatives:
            self.altName = []
            for obj in alternatives:
                self.altName.append(obj.name)

            self.comboBoxANames.addItems(self.altName)

        # button signals
        self.pushButtonAA.clicked.connect(self.open_AddAlt)
        self.pushButtonDA.clicked.connect(self.delete_Alt)
        self.pushButtonMA.clicked.connect(self.modify_Alt)
        self.pushButtonOkAC.clicked.connect(self.close)

        # self.radioBMinimum.toggled.connect(self.min_table)
        # self.radioBAverage.toggled.connect(self.ave_table)
        # self.radioBMaximum.toggled.connect(self.max_table)

        num_rows = len(attributes) + 2
        num_columns = (len(alternatives) + 1) * 2
        widthTable = self.tableWidgetAC.width() // 12
        self.tableWidgetAC.setRowCount(num_rows)
        self.tableWidgetAC.setColumnCount(num_columns)
        self.tableWidgetAC.setColumnWidth(0, widthTable)
        header_item = QTableWidgetItem("Attributes")
        # font = QFont()
        # font.setBold(True)
        # header_item.setFont(font)
        self.tableWidgetAC.setSpan(0, 0, 1, 2)
        item = QTableWidgetItem("Alternatives:")
        item.setTextAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignCenter
        )
        self.tableWidgetAC.setItem(0, 0, item)
        self.tableWidgetAC.setSpan(1, 0, 1, 2)
        self.tableWidgetAC.setItem(1, 0, header_item)

        # self.tableWidgetAC.setSpan(0, 0, 1, 2) # ocupies two columns
        self.tableWidgetAC.verticalHeader().setVisible(False)
        self.tableWidgetAC.horizontalHeader().setVisible(False)

        for i in range(num_columns):
            self.tableWidgetAC.setColumnWidth(i, widthTable)

        for i, attribute in enumerate(attributesnames):
            item = QTableWidgetItem(attribute)
            font = QFont()
            font.setBold(True)
            # item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            item.setFont(font)
            brush = QBrush(
                QColor(0, 0, 0, 25)
            )  # Color negro con transparencia baja (25)
            item.setBackground(brush)
            self.tableWidgetAC.setSpan(i + 2, 0, 1, 2)
            self.tableWidgetAC.setItem(i + 2, 0, item)
            # print(f"P: attribute: {attribute}")

        column = 0
        for i, altern in enumerate(alternatives):
            self.tableWidgetAC.setSpan(0, column + 2, 1, 2)
            header_item = QTableWidgetItem(altern.name)
            font = QFont()
            font.setBold(True)
            brush = QBrush(
                QColor(0, 0, 0, 25)
            )  # Color negro con transparencia baja (25)
            header_item.setBackground(brush)
            header_item.setFont(font)
            header_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.tableWidgetAC.setItem(0, column + 2, header_item)
            font = QFont()
            font.setBold(True)
            header_item.setFont(font)
            item = QTableWidgetItem("min")
            # item2 = QTableWidgetItem("ave")
            item3 = QTableWidgetItem("max")
            item.setFont(font)
            item.setBackground(brush)
            item3.setBackground(brush)
            # item2.setFont(font)
            item3.setFont(font)
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.tableWidgetAC.setItem(1, column + 2, item)
            # item2.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            # self.tableWidgetAC.setItem(1, column+4, item2)
            item3.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.tableWidgetAC.setItem(1, column + 3, item3)
            column += 2

        column = 0
        row = 2
        for i, altern in enumerate(alternatives):
            # self.tableWidgetAC.setSpan(i, 0, 1, 2)
            for elem in altern.attr:
                # optionCD = altern.attr[j]
                if isinstance(elem, ContinuousAttribute):
                    value1 = float(elem.value1)
                    value2 = float(elem.value2)
                    # value3 = float((value1 + value2) / 2)
                    item = QTableWidgetItem(str(value1))
                    item2 = QTableWidgetItem(str(value2))
                    # item3 = QTableWidgetItem(str(value3))
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    self.tableWidgetAC.setItem(row, column + 2, item)
                    # item3.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    # self.tableWidgetAC.setItem(row, column+4, item3)
                    item2.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    self.tableWidgetAC.setItem(row, column + 3, item2)
                elif isinstance(elem, DiscreteAttribute):
                    self.tableWidgetAC.setSpan(row, column + 2, 1, 2)
                    # combo_box = QComboBox()
                    # combo_box.addItems(elem.attributenames)
                    selected_option = elem.selected
                    if not elem.selected in elem.attributenames:
                        elem.selected = ""
                    selected_option = QTableWidgetItem(selected_option)

                    selected_option.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    # index = elem.attributenames.index(selected_option)
                    # combo_box.setCurrentIndex(index)
                    # self.tableWidgetAC.setCellWidget(row, column+2, combo_box)
                    self.tableWidgetAC.setItem(
                        row, column + 2, QTableWidgetItem(selected_option)
                    )
                row += 1
            column += 2
            row = 2

        # self.tableWidgetAC
        # for row in range(self.tableWidgetAC.rowCount()):
        #     for column in range(self.tableWidgetAC.columnCount()):
        #         item = self.tableWidgetAC.item(row, column)
        #         if item is None or item.text() == "":
        #             comp_item = self.tableWidgetAC.item(row, 0)
        #             if comp_item is not None:
        #                 comp_value = comp_item.text()
        #                 for attr in alternatives:
        #                     if attr.attr == attribute.name:
        #                         # Realiza la acción que deseas para la coincidencia encontrada
        #                         print("Coincidencia encontrada:", attribute.name)
        #                         break

    # enables the Save button on the screen once the table
    # is interacted with.

    def handleTableInteraction(self, row, column):
        self.push_button.setEnabled(False)

    # deletes the alternative
    def delete_Alt(self):
        try:
            current_value = self.comboBoxANames.currentText()
            reply = QMessageBox.question(
                self,
                "Confirmation",
                f"Surely you want to delete the alternative {current_value}?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No,
            )
            if reply == QMessageBox.StandardButton.Yes:
                for altern in alternatives:
                    if altern.name == current_value:
                        alternatives.remove(altern)
                        del altern

                self.vAltCon = VentanaAltCon()
                self.vAltCon.show()
                self.close()

            else:
                pass
        except RuntimeError:
            traceback.print_exc()
            pass

    #  opens a screen that will be explained in the next class explanation
    # called WindowAddAlt and gives the functionalities of that alternative to be
    # modified.

    def modify_Alt(
        self,
    ):  # en uno vemos los atributos de esa alternativa y apretando un button vamos a cambiarlo

        self.vAddAlt = VentanaAddAlt()
        self.vAddAlt.update()
        self.vAddAlt.pushButtonSave.setEnabled(True)
        self.vAddAlt.pushButtonSave.show()
        self.vAddAlt.pushButtonOk.hide()
        self.vAddAlt.tableWidgetAA.clear()
        alternativa = self.comboBoxANames.currentText()
        self.vAddAlt.textAlternativeName.setPlainText(alternativa)
        self.vAddAlt.ejecutar_funcion = False
        self.vAddAlt.modify = True

        for alternative in alternatives:
            if alternativa == alternative.name:
                self.vAddAlt.textAlternativeDescription.setPlainText(alternative.desc)
                break

        # button signal
        self.vAddAlt.pushButtonSave.clicked.connect(self.ok_modify)

        for alternative in alternatives:
            if alternativa == alternative.name:
                for j, attr in enumerate(alternative.attr):
                    if isinstance(attr, ContinuousAttribute):
                        value1 = attr.value1
                        value2 = attr.value2
                        item = QTableWidgetItem(str(value1))
                        item2 = QTableWidgetItem(str(value2))
                        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                        self.vAddAlt.tableWidgetAA.setItem(j, 0, item)
                        item2.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                        self.vAddAlt.tableWidgetAA.setItem(j, 1, item2)
                    elif isinstance(attr, DiscreteAttribute):
                        self.vAddAlt.tableWidgetAA.setSpan(j, 0, 1, 2)
                        combo_box = QComboBox()
                        print(attr.attributenames)
                        combo_box.addItems(attr.attributenames)
                        if not (attr.selected == ""):
                            selected_option = attr.selected
                            index1 = attr.attributenames.index(selected_option)
                            combo_box.setCurrentIndex(index1)
                        else:
                            combo_box.setEditText(attr.selected)
                            combo_box.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                        self.vAddAlt.tableWidgetAA.setCellWidget(j, 0, combo_box)

        self.vAddAlt.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)
        self.vAddAlt.show()

    # executes the changes to be modified in the open WindowAddAlt
    # window
    def ok_modify(self):  # aquí se cambian los valores de esa alternativa
        global attributes
        self.vAddAlt.pushButtonSave.setEnabled(True)
        alternativa = self.comboBoxANames.currentText()
        self.vAddAlt.ejecutar_funcion = False

        for alternative in alternatives:
            if alternativa == alternative.name:
                # alternative.name = self.vAddAlt.textAlternativeName.toPlainText()
                # alternative.desc = self.vAddAlt.textAlternativeDescription.toPlainText()
                break

        for alternative in alternatives:
            if alternativa == alternative.name:
                for j, attr in enumerate(alternative.attr):
                    if isinstance(attr, ContinuousAttribute):
                        for at in attributes:
                            print(f"{at.text()} == {attr.name}")
                            if at.text() == attr.name:
                                try:
                                    value1 = float(at.minRange)
                                    value2 = float(at.maxRange)
                                    valueT1 = self.vAddAlt.tableWidgetAA.item(
                                        j, 0
                                    ).text()
                                    valueT2 = self.vAddAlt.tableWidgetAA.item(
                                        j, 1
                                    ).text()
                                    print(f"{value1} {valueT1} {valueT2} {value2}")
                                    if (float(valueT1) >= value1) and (
                                        float(valueT2) <= value2
                                    ):
                                        continue
                                    else:
                                        QMessageBox.warning(
                                            self,
                                            "Warning",
                                            "Some parametres are not within the range set out in the attribute.",
                                        )
                                        print(
                                            f"float(attr.value1({float(attr.value1)})) <= value1({value1})) and (float(attr.value2({float(attr.value2)})) >= value2({value2})"
                                        )
                                        self.vAddAlt.raise_()
                                        return
                                except (ValueError, AttributeError):
                                    QMessageBox.warning(
                                        self,
                                        "Warning",
                                        "Complete all values correctly.",
                                    )
                                    self.vAddAlt.raise_()
                                    return

        for alternative in alternatives:
            if alternativa == alternative.name:
                for j, attr in enumerate(alternative.attr):
                    if isinstance(attr, ContinuousAttribute):
                        value1 = self.vAddAlt.tableWidgetAA.item(j, 0).text()
                        value2 = self.vAddAlt.tableWidgetAA.item(j, 1).text()
                        attr.value1 = value1
                        attr.value2 = value2
                    elif isinstance(attr, DiscreteAttribute):
                        attNames = attr.attributenames
                        combo_box = self.vAddAlt.tableWidgetAA.cellWidget(j, 0)
                        selected = combo_box.currentText()
                        attr.attributenames = attNames
                        attr.selected = selected
        self.vAddAlt.close()
        self.close()
        self.vVAC = VentanaAltCon()
        self.vVAC.close()
        self.vVAC = VentanaAltCon()
        self.vVAC.update()
        self.vVAC.show()

    #  opens the add alternative WindowAddAlt window.

    def open_AddAlt(self):
        self.vAddAlt = VentanaAddAlt()
        self.vAddAlt.show()
        self.close()


class VentanaAltClas(QMainWindow):
    def __init__(self, parent=None):
        super(VentanaAltClas, self).__init__(parent)
        uic.loadUi("AlternativeClassification.ui", self)
        icono = QIcon("iconoUPM.ico")
        super(VentanaAltClas, self).setWindowIcon(icono)
        super(VentanaAltClas, self).setWindowTitle("Classificate Alternatives")


class VentanaAddAlt(QMainWindow):
    def __init__(self, parent=None):
        global attributes
        global attributesnames
        super(VentanaAddAlt, self).__init__(parent)
        uic.loadUi("addAlternative.ui", self)
        icono = QIcon("iconoUPM.ico")
        super(VentanaAddAlt, self).setWindowIcon(icono)
        super(VentanaAddAlt, self).setWindowTitle("Add Alternative")

        self.pushButtonSave.setEnabled(False)
        self.ejecutar_funcion = True
        self.modify = False

        # buttons signals
        self.pushButtonCancelar.clicked.connect(self.closeW)
        self.pushButtonOk.clicked.connect(self.addAlternativeOption)
        self.pushButtonSave.hide()

        # connect the three table's ScrollBars
        self.tableWidgetAttributesNames.verticalScrollBar().valueChanged.connect(
            self.tableWidgetAA.verticalScrollBar().setValue
        )

        self.tableWidgetAttributesNames.verticalScrollBar().valueChanged.connect(
            self.tableWidgetMinMax.verticalScrollBar().setValue
        )

        self.tableWidgetAA.verticalScrollBar().valueChanged.connect(
            self.tableWidgetAttributesNames.verticalScrollBar().setValue
        )

        self.tableWidgetAA.verticalScrollBar().valueChanged.connect(
            self.tableWidgetMinMax.verticalScrollBar().setValue
        )

        self.tableWidgetMinMax.verticalScrollBar().valueChanged.connect(
            self.tableWidgetAttributesNames.verticalScrollBar().setValue
        )

        self.tableWidgetMinMax.verticalScrollBar().valueChanged.connect(
            self.tableWidgetAA.verticalScrollBar().setValue
        )

        try:
            self.attCD = []
            print(f"P: attributes: {attributes}")
            for attr in attributes:
                if attr.unitType == "Continuous":
                    continuous_attr = ContinuousAttribute(attr.minRange, attr.maxRange)
                    continuous_attr.name = attr.text()
                    self.attCD.append(continuous_attr)
                elif attr.unitType == "Discrete":
                    discrete_attr = DiscreteAttribute(attr.optionsList)
                    discrete_attr.name = attr.text()
                    self.attCD.append(discrete_attr)
                else:
                    # Si el valor de unitType no es ni 'Continuous' ni 'Discrete'
                    # hacer algo aquí en consecuencia
                    pass

            num_rows = len(attributes)
            widthTable = self.tableWidgetAttributesNames.width()
            self.tableWidgetAttributesNames.setRowCount(num_rows)
            self.tableWidgetAttributesNames.setColumnCount(1)
            self.tableWidgetAttributesNames.setColumnWidth(0, widthTable)

            for i, attribute in enumerate(attributesnames):
                item = QTableWidgetItem(attribute)
                # item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.tableWidgetAttributesNames.setItem(i, 0, item)

            widthTable = self.tableWidgetMinMax.width()
            self.tableWidgetMinMax.setRowCount(num_rows)
            self.tableWidgetMinMax.setColumnCount(1)
            self.tableWidgetMinMax.setColumnWidth(0, widthTable)

            for i, attribute in enumerate(self.attCD):
                if isinstance(attribute, ContinuousAttribute):
                    item = QTableWidgetItem(
                        " ( "
                        + str(attribute.value1)
                        + " , "
                        + str(attribute.value2)
                        + " )"
                    )
                    self.tableWidgetMinMax.setItem(i, 0, item)
                elif isinstance(attribute, DiscreteAttribute):
                    options_str = ", ".join(attribute.attributenames)
                    item = QTableWidgetItem(options_str)
                    self.tableWidgetMinMax.setItem(i, 0, item)

            widthTable = self.tableWidgetAA.width()
            self.tableWidgetAA.setRowCount(num_rows)
            self.tableWidgetAA.setColumnCount(2)
            self.tableWidgetAA.setColumnWidth(0, widthTable // 2)
            self.tableWidgetAA.setColumnWidth(1, widthTable // 2)

            for i, attribute in enumerate(self.attCD):
                if isinstance(attribute, DiscreteAttribute):
                    self.tableWidgetAA.setSpan(i, 0, 1, 2)
                    combo_box = QComboBox()
                    combo_box.addItems(attribute.attributenames)
                    self.tableWidgetAA.setCellWidget(i, 0, combo_box)
        except RuntimeError:
            traceback.print_exc()
            pass

        # tableWidgetAA

        # my_attribute_names = my_array[5].attributenames

    # Creamos un array para guardar los objetos de la clase ContinuousAttribute
    def addAlternativeOption(self):
        global alternatives
        global attributes
        self.alternativeList = []

        self.attCD = []
        for attr in attributes:
            if attr.unitType == "Continuous":
                continuous_attr = ContinuousAttribute(attr.minRange, attr.maxRange)
                continuous_attr.name = attr.text()
                self.attCD.append(continuous_attr)
            elif attr.unitType == "Discrete":
                discrete_attr = DiscreteAttribute(attr.optionsList)
                discrete_attr.name = attr.text()
                self.attCD.append(discrete_attr)
            else:
                # Si el valor de unitType no es ni 'Continuous' ni 'Discrete'
                # hacer algo aquí en consecuencia
                pass

        # check loop for correct interval values

        for i, attribute in enumerate(self.attCD):
            if isinstance(attribute, ContinuousAttribute) and self.ejecutar_funcion:
                try:
                    value1 = float(self.tableWidgetAA.item(i, 0).text())
                    # print(f"P: value1: {value1}")
                    value2 = float(self.tableWidgetAA.item(i, 1).text())
                    elem = self.attCD[i]
                    if (
                        (float(elem.value1) <= value1)
                        and (float(elem.value2) >= value2)
                        and (value1 <= value2)
                    ):
                        continue
                    else:
                        QMessageBox.warning(
                            self,
                            "Warning",
                            "Some parametres are not within the range set out in the attribute.",
                        )
                        print(
                            f"float(attr.value1({float(elem.value1)})) <= value1({value1})) and (float(attr.value2({float(elem.value2)})) >= value2({value2})"
                        )
                        return
                except (ValueError, AttributeError):
                    QMessageBox.warning(
                        self, "Warning", "Complete all values correctly."
                    )
                    return

        for i, attribute in enumerate(self.attCD):
            if isinstance(attribute, ContinuousAttribute):
                value1 = self.tableWidgetAA.item(i, 0).text()
                value2 = self.tableWidgetAA.item(i, 1).text()
                element = ContinuousAttribute(value1=value1, value2=value2)
                element.name = attribute.name
            elif isinstance(attribute, DiscreteAttribute):
                attNames = self.attCD[i]
                attNames = attNames.attributenames
                combo_box = self.tableWidgetAA.cellWidget(i, 0)
                selected = combo_box.currentText()
                element = DiscreteAttribute(attributenames=attNames)
                element.name = attribute.name
                element.selected = selected

            self.alternativeList.append(element)
        altName = self.textAlternativeName.toPlainText()
        altDesc = self.textAlternativeDescription.toPlainText()
        if altName and altDesc:
            alternative = Alternative(
                name=altName, desc=altDesc, attr=self.alternativeList
            )
            alternatives.append(alternative)
            self.vAltCon = VentanaAltCon()
            self.vAltCon.show()
            self.close()

        else:
            QMessageBox.warning(
                self,
                "Warning",
                "The Alternative Name and Alternative Description field cannot be empty. It cannot be added.",
            )

    def closeW(self):
        if not self.modify:
            self.vAltCon = VentanaAltCon()
            self.vAltCon.show()
            self.close()
        else:
            self.close()


class VentanaVTW(QMainWindow):
    global attributes
    global attributesnames

    def __init__(self, parent=None):
        super(VentanaVTW, self).__init__(parent)
        uic.loadUi("viewingTWeights.ui", self)
        icono = QIcon("iconoUPM.ico")
        super(VentanaVTW, self).setWindowIcon(icono)
        super(VentanaVTW, self).setWindowTitle("Viewing Total Weights")
        self.VentanaPrincipalGMAA = parent

        background_color = QColor("#F0F0F0")
        brush = QBrush(background_color)

        self.tableINodeNames.itemDoubleClicked.connect(self.on_item_double_clicked)
        self.comboBoxINodoNames.currentTextChanged.connect(self.on_combo_box_changed)
        self.pushButtonOKVTW.clicked.connect(self.close)

        nodo_overall = self.encontrar_padre(attributes[0])

        internodes = []
        internodes = self.recorrer_arbol(nodo_overall)

        internode = None
        # self.hLayoutVTW
        if internodes:
            self.comboBoxINodoNames.setCurrentText(internodes[0].text())
            internode = internodes[0]
        else:
            self.comboBoxINodoNames.setCurrentText("")

        num_rows = len(internodes)
        widthTable = self.tableINodeNames.width()
        self.tableINodeNames.setRowCount(num_rows)
        self.tableINodeNames.setColumnCount(1)
        self.tableINodeNames.setColumnWidth(0, widthTable)
        self.tableINodeNames.verticalHeader().setVisible(
            False
        )  # Ocultar el encabezado vertical
        self.tableINodeNames.horizontalHeader().setVisible(
            False
        )  # Ocultar el encabezado horizontal
        self.tableINodeNames.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        for i, intnode in enumerate(internodes):
            self.comboBoxINodoNames.addItem(intnode.text())
            item = QTableWidgetItem(intnode.text())
            # item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.tableINodeNames.setItem(i, 0, item)

        data = []
        valmins = []
        valmaxs = []
        for internod in internode.connections:
            if isinstance(internod, QLabel):
                valmins.append(float(internod.weightI))
                valmaxs.append(float(internod.weightS))

        for valmin, valmax in zip(valmins, valmaxs):
            data.append((valmin, valmax))

        self.connectionsNC = []
        for con in internode.connections:
            self.connectionsNC.append(con.text())
        chart_widget = BarChartWidget()
        name_widget = NamesChart()
        name_widget.set_connections(self.connectionsNC)
        chart_widget.set_data(data)
        # chart_widget.set_connections(internode.connections)
        self.hlayoutVTW = self.hLayoutVTW
        self.vlayoutVTW = self.vLayoutVTW
        self.clear_layout(self.hlayoutVTW)
        self.clear_layout(self.vlayoutVTW)
        self.vlayoutVTW.addWidget(name_widget)
        self.hlayoutVTW.addWidget(chart_widget)

    def encontrar_padre(self, nodo):
        while nodo.padre is not None:
            nodo = nodo.padre

        return nodo

    def recorrer_arbol(self, nodo_padre):
        # Array para almacenar los nodos con finalNode = False
        nodosIntermedios = []

        # Verificar si el nodo padre cumple la condición
        if not nodo_padre.finalNode:
            nodosIntermedios.append(nodo_padre)

        # Recorrer los nodos hijos del nodo padre
        for nodo_hijo in nodo_padre.connections:
            # Llamar recursivamente a la función para cada nodo hijo
            nodosIntermedios.extend(self.recorrer_arbol(nodo_hijo))

        return nodosIntermedios

    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.setParent(None)
            else:
                self.clear_layout(item.layout())

    def on_item_double_clicked(self, item):
        if isinstance(item, QTableWidgetItem):
            value = item.text()
            self.comboBoxINodoNames.setCurrentText(value)

    def on_combo_box_changed(self, text):
        selected_int = None
        # selected_text = self.comboBoxAltNames.currentText()
        internodes = []
        nodo_overall = self.encontrar_padre(attributes[0])
        internodes = self.recorrer_arbol(nodo_overall)

        for internod in internodes:
            # if attr.text() == selected_text:
            if internod.text() == text:
                selected_int = internod
                break

        self.clear_layout(self.hLayoutVTW)
        self.clear_layout(self.vLayoutVTW)

        data = []
        valmins = []
        valmaxs = []
        for internod in selected_int.connections:
            if isinstance(internod, QLabel):
                valmins.append(float(internod.weightI))
                valmaxs.append(float(internod.weightS))

        for valmin, valmax in zip(valmins, valmaxs):
            data.append((valmin, valmax))

        self.connectionsNC = []
        for con in selected_int.connections:
            self.connectionsNC.append(con.text())
        chart_widget = BarChartWidget()
        name_widget = NamesChart()
        name_widget.set_connections(self.connectionsNC)
        chart_widget.set_data(data)
        # chart_widget.set_connections(internode.connections)
        self.hlayoutVTW = self.hLayoutVTW
        self.vlayoutVTW = self.vLayoutVTW
        self.clear_layout(self.hlayoutVTW)
        self.clear_layout(self.vlayoutVTW)
        self.vlayoutVTW.addWidget(name_widget)
        self.hlayoutVTW.addWidget(chart_widget)


class VentanaUDV(QMainWindow):
    global attributes
    global attributesnames
    global alternatives

    def __init__(self, parent=None):
        super(VentanaUDV, self).__init__(parent)
        uic.loadUi("utilitiesDiscreteAttributes.ui", self)
        icono = QIcon("iconoUPM.ico")
        super(VentanaUDV, self).setWindowIcon(icono)
        super(VentanaUDV, self).setWindowTitle(
            "Utilities for Discrete Attribute Values"
        )
        self.VentanaPrincipalGMAA = parent

        self.pushButtonBackUDV.clicked.connect(self.close)
        self.pushButtonViewUDV.clicked.connect(self.onView)
        self.pushButtonSaveUDV.clicked.connect(self.save_DAtt)

        self.attNameUDV.setVisible(False)

    def save_DAtt(self):
        global attributes
        attNameUDV = self.attNameUDV.text()
        attr = None
        for att in attributes:
            if attNameUDV == att.text():
                attr = att
                break
        try:
            for row in range(self.tableWidgetUDV.rowCount()):
                item_column_3 = self.tableWidgetUDV.item(row, 3)  # Columna 3 (índice 2)
                item_column_5 = self.tableWidgetUDV.item(row, 5)  # Columna 5 (índice 4)

                if (
                    (float(item_column_3.text()) < 0)
                    or (float(item_column_5.text()) > 1)
                    or (float(item_column_3.text()) > float(item_column_5.text()))
                ):
                    QMessageBox.warning(
                        self,
                        "Warning",
                        "Some parametres are not within the range set out in the attribute.",
                    )
                    return

            for row in range(self.tableWidgetUDV.rowCount()):
                item_column_3 = self.tableWidgetUDV.item(row, 3)  # Columna 3 (índice 2)
                item_column_5 = self.tableWidgetUDV.item(row, 5)  # Columna 5 (índice 4)

                if item_column_3 is not None:
                    flo1 = float(item_column_3.text())
                    setattr(attr, "UP" + str(row + 1) + "1", flo1)

                if item_column_5 is not None:
                    flo2 = float(item_column_5.text())
                    setattr(attr, "UP" + str(row + 1) + "2", flo2)

        except (ValueError, AttributeError):
            QMessageBox.warning(self, "Warning", "Complete all values correctly.")
            return

        self.close()

    def onView(self):
        global attributes
        attNameLUF = self.attNameUDV.text()
        attr = None
        for att in attributes:
            if attNameLUF == att.text():
                attr = att
                break
        background_color = QColor("#F0F0F0")
        brush = QBrush(background_color)
        try:
            self.layoutUDV = self.hlayoutViewUDV
            self.vlayoutUDV = self.vlayoutViewUDV
            self.clear_layout(self.layoutUDV)
            self.clear_layout(self.vlayoutUDV)
            valmins = []
            valmaxs = []
            data = []

            for row in range(self.tableWidgetUDV.rowCount()):
                item_column_3 = self.tableWidgetUDV.item(row, 3)  # Columna 3 (índice 2)
                item_column_5 = self.tableWidgetUDV.item(row, 5)  # Columna 5 (índice 4)

                if (
                    (float(item_column_3.text()) < 0)
                    or (float(item_column_5.text()) > 1)
                    or (float(item_column_3.text()) > float(item_column_5.text()))
                ):
                    QMessageBox.warning(
                        self,
                        "Warning",
                        "Some parametres are not within the range set out in the attribute.",
                    )
                    return

            for row in range(self.tableWidgetUDV.rowCount()):
                item_column_3 = self.tableWidgetUDV.item(row, 3)  # Columna 3 (índice 2)
                item_column_5 = self.tableWidgetUDV.item(row, 5)  # Columna 5 (índice 4)

                if item_column_3 is not None:
                    flo1 = float(item_column_3.text())
                    print(f"flo1: {flo1}")
                    valmins.append(flo1)

                if item_column_5 is not None:
                    flo2 = float(item_column_5.text())
                    print(f"flo2: {flo2}")
                    valmaxs.append(flo2)

            for valmin, valmax in zip(valmins, valmaxs):
                data.append((valmin, valmax))

            print(f"data: {data}")
            chart_widget = LineBarChartWidget()
            names_chart = NamesChart()
            chart_widget.set_data(data)
            names_chart.set_connections(attr.optionsList)
            self.clear_layout(self.hlayoutViewUDV)
            self.clear_layout(self.vlayoutViewUDV)
            self.layoutUDV = self.hlayoutViewUDV
            self.vlayoutUDV = self.vlayoutViewUDV
            self.layoutUDV.addWidget(chart_widget)
            self.vlayoutUDV.addWidget(names_chart)

        except (ValueError, AttributeError):
            QMessageBox.warning(self, "Warning", "Complete all values correctly.")
            return

    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.setParent(None)
            else:
                self.clear_layout(item.layout())


class VentanaLUF(QMainWindow):
    global attributes
    global attributesnames
    global alternatives

    def __init__(self, parent=None):
        super(VentanaLUF, self).__init__(parent)
        uic.loadUi("linearUtilityFunction.ui", self)
        icono = QIcon("iconoUPM.ico")
        super(VentanaLUF, self).setWindowIcon(icono)
        super(VentanaLUF, self).setWindowTitle("Linear Utility Function")
        self.VentanaPrincipalGMAA = parent

        self.pushButtonBackLUF.clicked.connect(self.close)  # cambiar
        self.pushButtonViewLUF.clicked.connect(self.onView)  # cambiar
        self.pushButtonSaveLUF.clicked.connect(self.save_CAtt)  # cambiar

        self.intPoints = 0
        self.attNameLUF.setVisible(False)

        self.checkboxes = [
            self.checkBoxP1,
            self.checkBoxP2,
            self.checkBoxP3,
            self.checkBoxP4,
            self.checkBoxP5,
        ]
        self.checkBoxP1.stateChanged.connect(self.onStateChanged)
        self.checkBoxP2.stateChanged.connect(self.onStateChanged)
        self.checkBoxP3.stateChanged.connect(self.onStateChanged)
        self.checkBoxP4.stateChanged.connect(self.onStateChanged)
        self.checkBoxP5.stateChanged.connect(self.onStateChanged)

        self.textAVP1.setEnabled(False)
        self.textUP11.setEnabled(False)
        self.textUP12.setEnabled(False)
        self.textAVP2.setEnabled(False)
        self.textUP21.setEnabled(False)
        self.textUP22.setEnabled(False)
        self.textAVP3.setEnabled(False)
        self.textUP31.setEnabled(False)
        self.textUP32.setEnabled(False)
        self.textAVP4.setEnabled(False)
        self.textUP41.setEnabled(False)
        self.textUP42.setEnabled(False)
        self.textAVP5.setEnabled(False)
        self.textUP51.setEnabled(False)
        self.textUP52.setEnabled(False)

    def save_CAtt(self):
        global attributes
        attNameLUF = self.attNameLUF.text()
        attr = None
        for att in attributes:
            if attNameLUF == att.text():
                attr = att
                break
        try:
            if float(self.textLowerBound.toPlainText()) != float(attr.minRange):
                attr.minRange = float(self.textLowerBound.toPlainText())

            if float(self.textUpperBound.toPlainText()) != float(attr.maxRange):
                attr.maxRange = float(self.textUpperBound.toPlainText())
        except ValueError:
            traceback.print_exc()
            pass

        try:
            if self.radioButtonMI.isChecked():
                attr.mostPrefered = "Sup"
            if self.radioButtonMD.isChecked():
                attr.mostPrefered = "Inf"

            if (
                self.checkBoxP5.isChecked()
                and self.checkBoxP4.isChecked()
                and self.checkBoxP3.isChecked()
                and self.checkBoxP2.isChecked()
                and self.checkBoxP1.isChecked()
            ):
                if (
                    (
                        float(self.textUP11.toPlainText())
                        > float(self.textUP12.toPlainText())
                    )
                    or (
                        float(self.textUP21.toPlainText())
                        > float(self.textUP22.toPlainText())
                    )
                    or (
                        float(self.textUP31.toPlainText())
                        > float(self.textUP32.toPlainText())
                    )
                    or (
                        float(self.textUP41.toPlainText())
                        > float(self.textUP42.toPlainText())
                    )
                    or (
                        float(self.textUP51.toPlainText())
                        > float(self.textUP52.toPlainText())
                    )
                ):
                    QMessageBox.warning(
                        self,
                        "Warning",
                        "Some parametres are not within the range set out in the attribute.",
                    )
                    return
                if (
                    (float(self.textUP11.toPlainText()) < 0)
                    or (float(self.textUP12.toPlainText()) > 1)
                    or (float(self.textUP21.toPlainText()) < 0)
                    or (float(self.textUP22.toPlainText()) > 1)
                    or (float(self.textUP31.toPlainText()) < 0)
                    or (float(self.textUP32.toPlainText()) > 1)
                    or (float(self.textUP41.toPlainText()) < 0)
                    or (float(self.textUP42.toPlainText()) > 1)
                    or (float(self.textUP51.toPlainText()) < 0)
                    or (float(self.textUP52.toPlainText()) > 1)
                ):
                    QMessageBox.warning(
                        self,
                        "Warning",
                        "Some parametres are not within the range set out in the attribute.",
                    )
                    return
                if not (
                    (
                        float(self.textLowerBound.toPlainText())
                        > float(self.textAVP1.toPlainText())
                    )
                    or (
                        float(self.textUpperBound.toPlainText())
                        > float(self.textAVP5.toPlainText())
                    )
                ):
                    QMessageBox.warning(
                        self,
                        "Warning",
                        "Some parametres are not within the range set out in the attribute.",
                    )
                    return
                attr.interPoints = 5
                attr.IP11 = float(self.textUP11.toPlainText())
                attr.IP12 = float(self.textUP12.toPlainText())
                attr.IPAV1 = float(self.textAVP1.toPlainText())
                attr.IP21 = float(self.textUP21.toPlainText())
                attr.IP22 = float(self.textUP22.toPlainText())
                attr.IPAV2 = float(self.textAVP2.toPlainText())
                attr.IP31 = float(self.textUP31.toPlainText())
                attr.IP32 = float(self.textUP32.toPlainText())
                attr.IPAV3 = float(self.textAVP3.toPlainText())
                attr.IP41 = float(self.textUP41.toPlainText())
                attr.IP42 = float(self.textUP42.toPlainText())
                attr.IPAV4 = float(self.textAVP4.toPlainText())
                attr.IP51 = float(self.textUP51.toPlainText())
                attr.IP52 = float(self.textUP52.toPlainText())
                attr.IPAV5 = float(self.textAVP5.toPlainText())
            elif (
                self.checkBoxP4.isChecked()
                and self.checkBoxP3.isChecked()
                and self.checkBoxP2.isChecked()
                and self.checkBoxP1.isChecked()
            ):
                if (
                    (
                        float(self.textUP11.toPlainText())
                        > float(self.textUP12.toPlainText())
                    )
                    or (
                        float(self.textUP21.toPlainText())
                        > float(self.textUP22.toPlainText())
                    )
                    or (
                        float(self.textUP31.toPlainText())
                        > float(self.textUP32.toPlainText())
                    )
                    or (
                        float(self.textUP41.toPlainText())
                        > float(self.textUP42.toPlainText())
                    )
                ):
                    QMessageBox.warning(
                        self,
                        "Warning",
                        "Some parametres are not within the range set out in the attribute.",
                    )
                    return
                if (
                    (float(self.textUP11.toPlainText()) < 0)
                    or (float(self.textUP12.toPlainText()) > 1)
                    or (float(self.textUP21.toPlainText()) < 0)
                    or (float(self.textUP22.toPlainText()) > 1)
                    or (float(self.textUP31.toPlainText()) < 0)
                    or (float(self.textUP32.toPlainText()) > 1)
                    or (float(self.textUP41.toPlainText()) < 0)
                    or (float(self.textUP42.toPlainText()) > 1)
                ):
                    QMessageBox.warning(
                        self,
                        "Warning",
                        "Some parametres are not within the range set out in the attribute.",
                    )
                    return
                if not (
                    (
                        float(self.textLowerBound.toPlainText())
                        > float(self.textAVP1.toPlainText())
                    )
                    or (
                        float(self.textUpperBound.toPlainText())
                        > float(self.textAVP4.toPlainText())
                    )
                ):
                    QMessageBox.warning(
                        self,
                        "Warning",
                        "Some parametres are not within the range set out in the attribute.",
                    )
                    return
                attr.interPoints = 4
                attr.IP11 = float(self.textUP11.toPlainText())
                attr.IP12 = float(self.textUP12.toPlainText())
                attr.IPAV1 = float(self.textAVP1.toPlainText())
                attr.IP21 = float(self.textUP21.toPlainText())
                attr.IP22 = float(self.textUP22.toPlainText())
                attr.IPAV2 = float(self.textAVP2.toPlainText())
                attr.IP31 = float(self.textUP31.toPlainText())
                attr.IP32 = float(self.textUP32.toPlainText())
                attr.IPAV3 = float(self.textAVP3.toPlainText())
                attr.IP41 = float(self.textUP41.toPlainText())
                attr.IP42 = float(self.textUP42.toPlainText())
                attr.IPAV4 = float(self.textAVP4.toPlainText())
            elif (
                self.checkBoxP1.isChecked()
                and self.checkBoxP2.isChecked()
                and self.checkBoxP3.isChecked()
            ):
                if (
                    (
                        float(self.textUP11.toPlainText())
                        > float(self.textUP12.toPlainText())
                    )
                    or (
                        float(self.textUP21.toPlainText())
                        > float(self.textUP22.toPlainText())
                    )
                    or (
                        float(self.textUP31.toPlainText())
                        > float(self.textUP32.toPlainText())
                    )
                ):
                    QMessageBox.warning(
                        self,
                        "Warning",
                        "Some parametres are not within the range set out in the attribute.",
                    )
                    return
                if (
                    (float(self.textUP11.toPlainText()) < 0)
                    or (float(self.textUP12.toPlainText()) > 1)
                    or (float(self.textUP21.toPlainText()) < 0)
                    or (float(self.textUP22.toPlainText()) > 1)
                    or (float(self.textUP31.toPlainText()) < 0)
                    or (float(self.textUP32.toPlainText()) > 1)
                ):
                    QMessageBox.warning(
                        self,
                        "Warning",
                        "Some parametres are not within the range set out in the attribute.",
                    )
                    return
                if not (
                    (
                        float(self.textLowerBound.toPlainText())
                        > float(self.textAVP1.toPlainText())
                    )
                    or (
                        float(self.textUpperBound.toPlainText())
                        > float(self.textAVP3.toPlainText())
                    )
                ):
                    QMessageBox.warning(
                        self,
                        "Warning",
                        "Some parametres are not within the range set out in the attribute.",
                    )
                    return
                attr.interPoints = 3
                attr.IP11 = float(self.textUP11.toPlainText())
                attr.IP12 = float(self.textUP12.toPlainText())
                attr.IPAV1 = float(self.textAVP1.toPlainText())
                attr.IP21 = float(self.textUP21.toPlainText())
                attr.IP22 = float(self.textUP22.toPlainText())
                attr.IPAV2 = float(self.textAVP2.toPlainText())
                attr.IP31 = float(self.textUP31.toPlainText())
                attr.IP32 = float(self.textUP32.toPlainText())
                attr.IPAV3 = float(self.textAVP3.toPlainText())
            elif self.checkBoxP1.isChecked() and self.checkBoxP2.isChecked():
                if (
                    float(self.textUP11.toPlainText())
                    > float(self.textUP12.toPlainText())
                ) or (
                    float(self.textUP21.toPlainText())
                    > float(self.textUP22.toPlainText())
                ):
                    QMessageBox.warning(
                        self,
                        "Warning",
                        "Some parametres are not within the range set out in the attribute.",
                    )
                    return
                if (
                    (float(self.textUP11.toPlainText()) < 0)
                    or (float(self.textUP12.toPlainText()) > 1)
                    or (float(self.textUP21.toPlainText()) < 0)
                    or (float(self.textUP22.toPlainText()) > 1)
                ):
                    QMessageBox.warning(
                        self,
                        "Warning",
                        "Some parametres are not within the range set out in the attribute.",
                    )
                    return
                if not (
                    (
                        float(self.textLowerBound.toPlainText())
                        > float(self.textAVP1.toPlainText())
                    )
                    or (
                        float(self.textUpperBound.toPlainText())
                        > float(self.textAVP2.toPlainText())
                    )
                ):
                    QMessageBox.warning(
                        self,
                        "Warning",
                        "Some parametres are not within the range set out in the attribute.",
                    )
                    return
                attr.interPoints = 2
                attr.IP11 = float(self.textUP11.toPlainText())
                attr.IP12 = float(self.textUP12.toPlainText())
                attr.IPAV1 = float(self.textAVP1.toPlainText())
                attr.IP21 = float(self.textUP21.toPlainText())
                attr.IP22 = float(self.textUP22.toPlainText())
                attr.IPAV2 = float(self.textAVP2.toPlainText())
            elif self.checkBoxP1.isChecked():
                if float(self.textUP11.toPlainText()) > float(
                    self.textUP12.toPlainText()
                ):
                    QMessageBox.warning(
                        self,
                        "Warning",
                        "Some parametres are not within the range set out in the attribute.",
                    )
                    return
                if (float(self.textUP11.toPlainText()) < 0) or (
                    float(self.textUP12.toPlainText()) > 1
                ):
                    QMessageBox.warning(
                        self,
                        "Warning",
                        "Some parametres are not within the range set out in the attribute.",
                    )
                    return
                if not (
                    (
                        float(self.textLowerBound.toPlainText())
                        < float(self.textAVP1.toPlainText())
                    )
                    or (
                        float(self.textUpperBound.toPlainText())
                        > float(self.textAVP2.toPlainText())
                    )
                ):
                    QMessageBox.warning(
                        self,
                        "Warning",
                        "Some parametres are not within the range set out in the attribute.",
                    )
                    return
                attr.interPoints = 1
                attr.IP11 = float(self.textUP11.toPlainText())
                attr.IP12 = float(self.textUP12.toPlainText())
                attr.IPAV1 = float(self.textAVP1.toPlainText())
            else:
                attr.interPoints = 0
        except (ValueError, AttributeError):
            QMessageBox.warning(
                self,
                "Warning",
                "Some parametres are not within the range set out in the attribute.",
            )
            return

        self.close()

    def onView(self):
        background_color = QColor("#F0F0F0")
        brush = QBrush(background_color)

        try:
            widget = QWidget()
            # window.setCentralWidget(widget)
            self.layoutLUF = self.hlayoutView
            self.clear_layout(self.layoutLUF)
            self.layoutLUF.addWidget(widget)

            series = QLineSeries()
            series1 = QLineSeries()
            series2 = QLineSeries()
            if self.radioButtonMI.isChecked():
                series.append(
                    float(self.textLowerBound.toPlainText()), 0
                )  # Punto inicial
                series1.append(
                    float(self.textLowerBound.toPlainText()), 0
                )  # Punto inicial
                series2.append(
                    float(self.textLowerBound.toPlainText()), 0
                )  # Punto inicial
                if (
                    self.checkBoxP5.isChecked()
                    and self.checkBoxP4.isChecked()
                    and self.checkBoxP3.isChecked()
                    and self.checkBoxP2.isChecked()
                    and self.checkBoxP1.isChecked()
                ):
                    if (
                        (
                            float(self.textUP11.toPlainText())
                            > float(self.textUP12.toPlainText())
                        )
                        or (
                            float(self.textUP21.toPlainText())
                            > float(self.textUP22.toPlainText())
                        )
                        or (
                            float(self.textUP31.toPlainText())
                            > float(self.textUP32.toPlainText())
                        )
                        or (
                            float(self.textUP41.toPlainText())
                            > float(self.textUP42.toPlainText())
                        )
                        or (
                            float(self.textUP51.toPlainText())
                            > float(self.textUP52.toPlainText())
                        )
                    ):
                        QMessageBox.warning(
                            self,
                            "Warning",
                            "Some parametres are not within the range set out in the attribute.",
                        )
                        return
                    if (
                        (float(self.textUP11.toPlainText()) < 0)
                        or (float(self.textUP12.toPlainText()) > 1)
                        or (float(self.textUP21.toPlainText()) < 0)
                        or (float(self.textUP22.toPlainText()) > 1)
                        or (float(self.textUP31.toPlainText()) < 0)
                        or (float(self.textUP32.toPlainText()) > 1)
                        or (float(self.textUP41.toPlainText()) < 0)
                        or (float(self.textUP42.toPlainText()) > 1)
                        or (float(self.textUP51.toPlainText()) < 0)
                        or (float(self.textUP52.toPlainText()) > 1)
                    ):
                        QMessageBox.warning(
                            self,
                            "Warning",
                            "Some parametres are not within the range set out in the attribute.",
                        )
                        return
                    if not (
                        float(self.textAVP1.toPlainText())
                        < float(self.textAVP2.toPlainText())
                        < float(self.textAVP3.toPlainText())
                        < float(self.textAVP4.toPlainText())
                        < float(self.textAVP5.toPlainText())
                    ):
                        QMessageBox.warning(
                            self,
                            "Warning",
                            "Some parametres are not within the range set out in the attribute.",
                        )
                        return
                    if not (
                        float(self.textLowerBound.toPlainText())
                        < float(self.textAVP1.toPlainText())
                    ):
                        QMessageBox.warning(
                            self,
                            "Warning",
                            "Some parametres are not within the range set out in the attribute.",
                        )
                        return
                    if not (
                        (
                            float(self.textUpperBound.toPlainText())
                            > float(self.textAVP5.toPlainText())
                        )
                    ):
                        QMessageBox.warning(
                            self,
                            "Warning",
                            "Some parametres are not within the range set out in the attribute.",
                        )
                        return
                    series.append(
                        float(self.textAVP1.toPlainText()),
                        float(self.textUP11.toPlainText()),
                    )  # Punto intermedio 1
                    series.append(
                        float(self.textAVP2.toPlainText()),
                        float(self.textUP21.toPlainText()),
                    )  # Punto intermedio 1
                    series.append(
                        float(self.textAVP3.toPlainText()),
                        float(self.textUP31.toPlainText()),
                    )  # Punto intermedio 1
                    series.append(
                        float(self.textAVP4.toPlainText()),
                        float(self.textUP41.toPlainText()),
                    )  # Punto intermedio 1
                    series.append(
                        float(self.textAVP5.toPlainText()),
                        float(self.textUP51.toPlainText()),
                    )  # Punto intermedio 1
                    series1.append(
                        float(self.textAVP1.toPlainText()),
                        float(self.textUP12.toPlainText()),
                    )  # Punto intermedio 1
                    series1.append(
                        float(self.textAVP2.toPlainText()),
                        float(self.textUP22.toPlainText()),
                    )  # Punto intermedio 1
                    series1.append(
                        float(self.textAVP3.toPlainText()),
                        float(self.textUP32.toPlainText()),
                    )  # Punto intermedio 1
                    series1.append(
                        float(self.textAVP4.toPlainText()),
                        float(self.textUP42.toPlainText()),
                    )  # Punto intermedio 1
                    series1.append(
                        float(self.textAVP5.toPlainText()),
                        float(self.textUP52.toPlainText()),
                    )  # Punto intermedio 1
                    averagevar = float(
                        (
                            float(self.textUP11.toPlainText())
                            + float(self.textUP12.toPlainText())
                        )
                        / 2
                    )
                    series2.append(float(self.textAVP1.toPlainText()), averagevar)
                    averagevar = float(
                        (
                            float(self.textUP21.toPlainText())
                            + float(self.textUP22.toPlainText())
                        )
                        / 2
                    )
                    series2.append(float(self.textAVP2.toPlainText()), averagevar)
                    averagevar = float(
                        (
                            float(self.textUP31.toPlainText())
                            + float(self.textUP32.toPlainText())
                        )
                        / 2
                    )
                    series2.append(float(self.textAVP3.toPlainText()), averagevar)
                    averagevar = float(
                        (
                            float(self.textUP41.toPlainText())
                            + float(self.textUP42.toPlainText())
                        )
                        / 2
                    )
                    series2.append(float(self.textAVP4.toPlainText()), averagevar)
                    averagevar = float(
                        (
                            float(self.textUP51.toPlainText())
                            + float(self.textUP52.toPlainText())
                        )
                        / 2
                    )
                    series2.append(float(self.textAVP5.toPlainText()), averagevar)

                    series.append(
                        float(self.textUpperBound.toPlainText()), 1
                    )  # Punto final
                    series1.append(
                        float(self.textUpperBound.toPlainText()), 1
                    )  # Punto final
                    series2.append(
                        float(self.textUpperBound.toPlainText()), 1
                    )  # Punto final

                    chart = QChart()
                    chart.addSeries(series)
                    chart.addSeries(series1)
                    chart.addSeries(series2)

                elif (
                    self.checkBoxP4.isChecked()
                    and self.checkBoxP3.isChecked()
                    and self.checkBoxP2.isChecked()
                    and self.checkBoxP1.isChecked()
                ):
                    if (
                        (
                            float(self.textUP11.toPlainText())
                            > float(self.textUP12.toPlainText())
                        )
                        or (
                            float(self.textUP21.toPlainText())
                            > float(self.textUP22.toPlainText())
                        )
                        or (
                            float(self.textUP31.toPlainText())
                            > float(self.textUP32.toPlainText())
                        )
                        or (
                            float(self.textUP41.toPlainText())
                            > float(self.textUP42.toPlainText())
                        )
                    ):
                        QMessageBox.warning(
                            self,
                            "Warning",
                            "Some parametres are not within the range set out in the attribute.",
                        )
                        return
                    if (
                        (float(self.textUP11.toPlainText()) < 0)
                        or (float(self.textUP12.toPlainText()) > 1)
                        or (float(self.textUP21.toPlainText()) < 0)
                        or (float(self.textUP22.toPlainText()) > 1)
                        or (float(self.textUP31.toPlainText()) < 0)
                        or (float(self.textUP32.toPlainText()) > 1)
                        or (float(self.textUP41.toPlainText()) < 0)
                        or (float(self.textUP42.toPlainText()) > 1)
                    ):
                        QMessageBox.warning(
                            self,
                            "Warning",
                            "Some parametres are not within the range set out in the attribute.",
                        )
                        return
                    if not (
                        float(self.textAVP1.toPlainText())
                        < float(self.textAVP2.toPlainText())
                        < float(self.textAVP3.toPlainText())
                        < float(self.textAVP4.toPlainText())
                    ):
                        QMessageBox.warning(
                            self,
                            "Warning",
                            "Some parametres are not within the range set out in the attribute.",
                        )
                        return
                    if not (
                        float(self.textLowerBound.toPlainText())
                        < float(self.textAVP1.toPlainText())
                    ):
                        QMessageBox.warning(
                            self,
                            "Warning",
                            "Some parametres are not within the range set out in the attribute.",
                        )
                        return
                    if not (
                        (
                            float(self.textUpperBound.toPlainText())
                            > float(self.textAVP4.toPlainText())
                        )
                    ):
                        QMessageBox.warning(
                            self,
                            "Warning",
                            "Some parametres are not within the range set out in the attribute.",
                        )
                        return
                    series.append(
                        float(self.textAVP1.toPlainText()),
                        float(self.textUP11.toPlainText()),
                    )  # Punto intermedio 1
                    series.append(
                        float(self.textAVP2.toPlainText()),
                        float(self.textUP21.toPlainText()),
                    )  # Punto intermedio 1
                    series.append(
                        float(self.textAVP3.toPlainText()),
                        float(self.textUP31.toPlainText()),
                    )  # Punto intermedio 1
                    series.append(
                        float(self.textAVP4.toPlainText()),
                        float(self.textUP41.toPlainText()),
                    )  # Punto intermedio 1
                    series1.append(
                        float(self.textAVP1.toPlainText()),
                        float(self.textUP12.toPlainText()),
                    )  # Punto intermedio 1
                    series1.append(
                        float(self.textAVP2.toPlainText()),
                        float(self.textUP22.toPlainText()),
                    )  # Punto intermedio 1
                    series1.append(
                        float(self.textAVP3.toPlainText()),
                        float(self.textUP32.toPlainText()),
                    )  # Punto intermedio 1
                    series1.append(
                        float(self.textAVP4.toPlainText()),
                        float(self.textUP42.toPlainText()),
                    )  # Punto intermedio 1
                    averagevar = float(
                        (
                            float(self.textUP11.toPlainText())
                            + float(self.textUP12.toPlainText())
                        )
                        / 2
                    )
                    series2.append(float(self.textAVP1.toPlainText()), averagevar)
                    averagevar = float(
                        (
                            float(self.textUP21.toPlainText())
                            + float(self.textUP22.toPlainText())
                        )
                        / 2
                    )
                    series2.append(float(self.textAVP2.toPlainText()), averagevar)
                    averagevar = float(
                        (
                            float(self.textUP31.toPlainText())
                            + float(self.textUP32.toPlainText())
                        )
                        / 2
                    )
                    series2.append(float(self.textAVP3.toPlainText()), averagevar)
                    averagevar = float(
                        (
                            float(self.textUP41.toPlainText())
                            + float(self.textUP42.toPlainText())
                        )
                        / 2
                    )
                    series2.append(float(self.textAVP4.toPlainText()), averagevar)
                    series.append(
                        float(self.textUpperBound.toPlainText()), 1
                    )  # Punto final
                    series1.append(
                        float(self.textUpperBound.toPlainText()), 1
                    )  # Punto final
                    series2.append(
                        float(self.textUpperBound.toPlainText()), 1
                    )  # Punto final
                    chart = QChart()
                    chart.addSeries(series)
                    chart.addSeries(series1)
                    chart.addSeries(series2)

                elif (
                    self.checkBoxP1.isChecked()
                    and self.checkBoxP2.isChecked()
                    and self.checkBoxP3.isChecked()
                ):
                    if (
                        (
                            float(self.textUP11.toPlainText())
                            > float(self.textUP12.toPlainText())
                        )
                        or (
                            float(self.textUP21.toPlainText())
                            > float(self.textUP22.toPlainText())
                        )
                        or (
                            float(self.textUP31.toPlainText())
                            > float(self.textUP32.toPlainText())
                        )
                    ):
                        QMessageBox.warning(
                            self,
                            "Warning",
                            "Some parametres are not within the range set out in the attribute.",
                        )
                        return
                    if (
                        (float(self.textUP11.toPlainText()) < 0)
                        or (float(self.textUP12.toPlainText()) > 1)
                        or (float(self.textUP21.toPlainText()) < 0)
                        or (float(self.textUP22.toPlainText()) > 1)
                        or (float(self.textUP31.toPlainText()) < 0)
                        or (float(self.textUP32.toPlainText()) > 1)
                    ):
                        QMessageBox.warning(
                            self,
                            "Warning",
                            "Some parametres are not within the range set out in the attribute.",
                        )
                        return
                    if not (
                        float(self.textAVP1.toPlainText())
                        < float(self.textAVP2.toPlainText())
                        < float(self.textAVP3.toPlainText())
                    ):
                        QMessageBox.warning(
                            self,
                            "Warning",
                            "Some parametres are not within the range set out in the attribute.",
                        )
                        return
                    if not (
                        float(self.textLowerBound.toPlainText())
                        < float(self.textAVP1.toPlainText())
                    ):
                        QMessageBox.warning(
                            self,
                            "Warning",
                            "Some parametres are not within the range set out in the attribute.",
                        )
                        return
                    if not (
                        (
                            float(self.textUpperBound.toPlainText())
                            > float(self.textAVP3.toPlainText())
                        )
                    ):
                        QMessageBox.warning(
                            self,
                            "Warning",
                            "Some parametres are not within the range set out in the attribute.",
                        )
                        return
                    series.append(
                        float(self.textAVP1.toPlainText()),
                        float(self.textUP11.toPlainText()),
                    )  # Punto intermedio 1
                    series.append(
                        float(self.textAVP2.toPlainText()),
                        float(self.textUP21.toPlainText()),
                    )  # Punto intermedio 1
                    series.append(
                        float(self.textAVP3.toPlainText()),
                        float(self.textUP31.toPlainText()),
                    )  # Punto intermedio 1
                    series1.append(
                        float(self.textAVP1.toPlainText()),
                        float(self.textUP12.toPlainText()),
                    )  # Punto intermedio 1
                    series1.append(
                        float(self.textAVP2.toPlainText()),
                        float(self.textUP22.toPlainText()),
                    )  # Punto intermedio 1
                    series1.append(
                        float(self.textAVP3.toPlainText()),
                        float(self.textUP32.toPlainText()),
                    )  # Punto intermedio 1
                    averagevar = float(
                        (
                            float(self.textUP11.toPlainText())
                            + float(self.textUP12.toPlainText())
                        )
                        / 2
                    )
                    series2.append(float(self.textAVP1.toPlainText()), averagevar)
                    averagevar = float(
                        (
                            float(self.textUP21.toPlainText())
                            + float(self.textUP22.toPlainText())
                        )
                        / 2
                    )
                    series2.append(float(self.textAVP2.toPlainText()), averagevar)
                    averagevar = float(
                        (
                            float(self.textUP31.toPlainText())
                            + float(self.textUP32.toPlainText())
                        )
                        / 2
                    )
                    series2.append(float(self.textAVP3.toPlainText()), averagevar)
                    series.append(
                        float(self.textUpperBound.toPlainText()), 1
                    )  # Punto final
                    series1.append(
                        float(self.textUpperBound.toPlainText()), 1
                    )  # Punto final
                    series2.append(
                        float(self.textUpperBound.toPlainText()), 1
                    )  # Punto final
                    chart = QChart()
                    chart.addSeries(series)
                    chart.addSeries(series1)
                    chart.addSeries(series2)
                elif self.checkBoxP1.isChecked() and self.checkBoxP2.isChecked():
                    if (
                        float(self.textUP11.toPlainText())
                        > float(self.textUP12.toPlainText())
                    ) or (
                        float(self.textUP21.toPlainText())
                        > float(self.textUP22.toPlainText())
                    ):
                        QMessageBox.warning(
                            self,
                            "Warning",
                            "Some parametres are not within the range set out in the attribute.",
                        )
                        return
                    if (
                        (float(self.textUP11.toPlainText()) < 0)
                        or (float(self.textUP12.toPlainText()) > 1)
                        or (float(self.textUP21.toPlainText()) < 0)
                        or (float(self.textUP22.toPlainText()) > 1)
                    ):
                        QMessageBox.warning(
                            self,
                            "Warning",
                            "Some parametres are not within the range set out in the attribute.",
                        )
                        return
                    if not (
                        float(self.textAVP1.toPlainText())
                        < float(self.textAVP2.toPlainText())
                    ):
                        QMessageBox.warning(
                            self,
                            "Warning",
                            "Some parametres are not within the range set out in the attribute.",
                        )
                        return
                    if not (
                        float(self.textLowerBound.toPlainText())
                        < float(self.textAVP1.toPlainText())
                    ):
                        QMessageBox.warning(
                            self,
                            "Warning",
                            "Some parametres are not within the range set out in the attribute.",
                        )
                        return
                    if not (
                        (
                            float(self.textUpperBound.toPlainText())
                            > float(self.textAVP2.toPlainText())
                        )
                    ):
                        QMessageBox.warning(
                            self,
                            "Warning",
                            "Some parametres are not within the range set out in the attribute.",
                        )
                        return
                    series.append(
                        float(self.textAVP1.toPlainText()),
                        float(self.textUP11.toPlainText()),
                    )  # Punto intermedio 1
                    series.append(
                        float(self.textAVP2.toPlainText()),
                        float(self.textUP21.toPlainText()),
                    )  # Punto intermedio 1
                    series1.append(
                        float(self.textAVP1.toPlainText()),
                        float(self.textUP12.toPlainText()),
                    )  # Punto intermedio 1
                    series1.append(
                        float(self.textAVP2.toPlainText()),
                        float(self.textUP22.toPlainText()),
                    )  # Punto intermedio 1
                    averagevar = float(
                        (
                            float(self.textUP11.toPlainText())
                            + float(self.textUP12.toPlainText())
                        )
                        / 2
                    )
                    series2.append(float(self.textAVP1.toPlainText()), averagevar)
                    averagevar = float(
                        (
                            float(self.textUP21.toPlainText())
                            + float(self.textUP22.toPlainText())
                        )
                        / 2
                    )
                    series2.append(float(self.textAVP2.toPlainText()), averagevar)
                    series.append(
                        float(self.textUpperBound.toPlainText()), 1
                    )  # Punto final
                    series1.append(
                        float(self.textUpperBound.toPlainText()), 1
                    )  # Punto final
                    series2.append(
                        float(self.textUpperBound.toPlainText()), 1
                    )  # Punto final
                    chart = QChart()
                    chart.addSeries(series)
                    chart.addSeries(series1)
                    chart.addSeries(series2)
                elif self.checkBoxP1.isChecked():
                    if float(self.textUP11.toPlainText()) > float(
                        self.textUP12.toPlainText()
                    ):
                        QMessageBox.warning(
                            self,
                            "Warning",
                            "Some parametres are not within the range set out in the attribute.",
                        )
                        return
                    if (float(self.textUP11.toPlainText()) < 0) or (
                        float(self.textUP12.toPlainText()) > 1
                    ):
                        QMessageBox.warning(
                            self,
                            "Warning",
                            "Some parametres are not within the range set out in the attribute.",
                        )
                        return
                    if not (
                        float(self.textLowerBound.toPlainText())
                        < float(self.textAVP1.toPlainText())
                    ):
                        QMessageBox.warning(
                            self,
                            "Warning",
                            "Some parametres are not within the range set out in the attribute.",
                        )
                        return
                    if not (
                        (
                            float(self.textUpperBound.toPlainText())
                            > float(self.textAVP1.toPlainText())
                        )
                    ):
                        QMessageBox.warning(
                            self,
                            "Warning",
                            "Some parametres are not within the range set out in the attribute.",
                        )
                        return
                    series.append(
                        float(self.textAVP1.toPlainText()),
                        float(self.textUP11.toPlainText()),
                    )  # Punto intermedio 1
                    series1.append(
                        float(self.textAVP1.toPlainText()),
                        float(self.textUP12.toPlainText()),
                    )  # Punto intermedio 1
                    averagevar = float(
                        (
                            float(self.textUP11.toPlainText())
                            + float(self.textUP12.toPlainText())
                        )
                        / 2
                    )
                    series2.append(float(self.textAVP1.toPlainText()), averagevar)

                    series.append(
                        float(self.textUpperBound.toPlainText()), 1
                    )  # Punto final
                    series1.append(
                        float(self.textUpperBound.toPlainText()), 1
                    )  # Punto final
                    series2.append(
                        float(self.textUpperBound.toPlainText()), 1
                    )  # Punto final
                    chart = QChart()
                    chart.addSeries(series)
                    chart.addSeries(series1)
                    chart.addSeries(series2)
                else:
                    # self.AttMPVCU.setText(f"Index ({int(attribute.minRange)}: Worst, {int(attribute.maxRange)} Ideal)")
                    # series.append(3.5, 0.6)  # Punto intermedio
                    # series.append(3.5, 0.2)  # Punto intermedio
                    series.append(
                        float(self.textUpperBound.toPlainText()), 1
                    )  # Punto final
                    chart = QChart()
                    chart.addSeries(series)
            else:

                series.append(
                    float(self.textLowerBound.toPlainText()), 1
                )  # Punto final
                series1.append(
                    float(self.textLowerBound.toPlainText()), 1
                )  # Punto final
                series2.append(
                    float(self.textLowerBound.toPlainText()), 1
                )  # Punto final
                if (
                    self.checkBoxP5.isChecked()
                    and self.checkBoxP4.isChecked()
                    and self.checkBoxP3.isChecked()
                    and self.checkBoxP2.isChecked()
                    and self.checkBoxP1.isChecked()
                ):
                    if (
                        (
                            float(self.textUP11.toPlainText())
                            > float(self.textUP12.toPlainText())
                        )
                        or (
                            float(self.textUP21.toPlainText())
                            > float(self.textUP22.toPlainText())
                        )
                        or (
                            float(self.textUP31.toPlainText())
                            > float(self.textUP32.toPlainText())
                        )
                        or (
                            float(self.textUP41.toPlainText())
                            > float(self.textUP42.toPlainText())
                        )
                        or (
                            float(self.textUP51.toPlainText())
                            > float(self.textUP52.toPlainText())
                        )
                    ):
                        QMessageBox.warning(
                            self,
                            "Warning",
                            "Some parametres are not within the range set out in the attribute.",
                        )
                        return
                    if (
                        (float(self.textUP11.toPlainText()) < 0)
                        or (float(self.textUP12.toPlainText()) > 1)
                        or (float(self.textUP21.toPlainText()) < 0)
                        or (float(self.textUP22.toPlainText()) > 1)
                        or (float(self.textUP31.toPlainText()) < 0)
                        or (float(self.textUP32.toPlainText()) > 1)
                        or (float(self.textUP41.toPlainText()) < 0)
                        or (float(self.textUP42.toPlainText()) > 1)
                        or (float(self.textUP51.toPlainText()) < 0)
                        or (float(self.textUP52.toPlainText()) > 1)
                    ):
                        QMessageBox.warning(
                            self,
                            "Warning",
                            "Some parametres are not within the range set out in the attribute.",
                        )
                        return
                    if not (
                        float(self.textAVP1.toPlainText())
                        < float(self.textAVP2.toPlainText())
                        < float(self.textAVP3.toPlainText())
                        < float(self.textAVP4.toPlainText())
                        < float(self.textAVP5.toPlainText())
                    ):
                        QMessageBox.warning(
                            self,
                            "Warning",
                            "Some parametres are not within the range set out in the attribute.",
                        )
                        return
                    if not (
                        float(self.textLowerBound.toPlainText())
                        < float(self.textAVP1.toPlainText())
                    ):
                        QMessageBox.warning(
                            self,
                            "Warning",
                            "Some parametres are not within the range set out in the attribute.",
                        )
                        return
                    if not (
                        (
                            float(self.textUpperBound.toPlainText())
                            > float(self.textAVP5.toPlainText())
                        )
                    ):
                        QMessageBox.warning(
                            self,
                            "Warning",
                            "Some parametres are not within the range set out in the attribute.",
                        )
                        return
                    series.append(
                        float(self.textAVP1.toPlainText()),
                        float(self.textUP11.toPlainText()),
                    )  # Punto intermedio 1
                    series.append(
                        float(self.textAVP2.toPlainText()),
                        float(self.textUP21.toPlainText()),
                    )  # Punto intermedio 1
                    series.append(
                        float(self.textAVP3.toPlainText()),
                        float(self.textUP31.toPlainText()),
                    )  # Punto intermedio 1
                    series.append(
                        float(self.textAVP4.toPlainText()),
                        float(self.textUP41.toPlainText()),
                    )  # Punto intermedio 1
                    series.append(
                        float(self.textAVP5.toPlainText()),
                        float(self.textUP51.toPlainText()),
                    )  # Punto intermedio 1
                    series1.append(
                        float(self.textAVP1.toPlainText()),
                        float(self.textUP12.toPlainText()),
                    )  # Punto intermedio 1
                    series1.append(
                        float(self.textAVP2.toPlainText()),
                        float(self.textUP22.toPlainText()),
                    )  # Punto intermedio 1
                    series1.append(
                        float(self.textAVP3.toPlainText()),
                        float(self.textUP32.toPlainText()),
                    )  # Punto intermedio 1
                    series1.append(
                        float(self.textAVP4.toPlainText()),
                        float(self.textUP42.toPlainText()),
                    )  # Punto intermedio 1
                    series1.append(
                        float(self.textAVP5.toPlainText()),
                        float(self.textUP52.toPlainText()),
                    )  # Punto intermedio 1
                    averagevar = float(
                        (
                            float(self.textUP11.toPlainText())
                            + float(self.textUP12.toPlainText())
                        )
                        / 2
                    )
                    series2.append(float(self.textAVP1.toPlainText()), averagevar)
                    averagevar = float(
                        (
                            float(self.textUP21.toPlainText())
                            + float(self.textUP22.toPlainText())
                        )
                        / 2
                    )
                    series2.append(float(self.textAVP2.toPlainText()), averagevar)
                    averagevar = float(
                        (
                            float(self.textUP31.toPlainText())
                            + float(self.textUP32.toPlainText())
                        )
                        / 2
                    )
                    series2.append(float(self.textAVP3.toPlainText()), averagevar)
                    averagevar = float(
                        (
                            float(self.textUP41.toPlainText())
                            + float(self.textUP42.toPlainText())
                        )
                        / 2
                    )
                    series2.append(float(self.textAVP4.toPlainText()), averagevar)
                    averagevar = float(
                        (
                            float(self.textUP51.toPlainText())
                            + float(self.textUP52.toPlainText())
                        )
                        / 2
                    )
                    series2.append(float(self.textAVP5.toPlainText()), averagevar)

                    series.append(float(self.textUpperBound.toPlainText()), 0)
                    series1.append(float(self.textUpperBound.toPlainText()), 0)
                    series2.append(float(self.textUpperBound.toPlainText()), 0)

                    chart = QChart()
                    chart.addSeries(series)
                    chart.addSeries(series1)
                    chart.addSeries(series2)

                elif (
                    self.checkBoxP1.isChecked()
                    and self.checkBoxP4.isChecked()
                    and self.checkBoxP3.isChecked()
                    and self.checkBoxP2.isChecked()
                ):
                    if (
                        (
                            float(self.textUP11.toPlainText())
                            > float(self.textUP12.toPlainText())
                        )
                        or (
                            float(self.textUP21.toPlainText())
                            > float(self.textUP22.toPlainText())
                        )
                        or (
                            float(self.textUP31.toPlainText())
                            > float(self.textUP32.toPlainText())
                        )
                        or (
                            float(self.textUP41.toPlainText())
                            > float(self.textUP42.toPlainText())
                        )
                    ):
                        QMessageBox.warning(
                            self,
                            "Warning",
                            "Some parametres are not within the range set out in the attribute.",
                        )
                        return
                    if (
                        (float(self.textUP11.toPlainText()) < 0)
                        or (float(self.textUP12.toPlainText()) > 1)
                        or (float(self.textUP21.toPlainText()) < 0)
                        or (float(self.textUP22.toPlainText()) > 1)
                        or (float(self.textUP31.toPlainText()) < 0)
                        or (float(self.textUP32.toPlainText()) > 1)
                        or (float(self.textUP41.toPlainText()) < 0)
                        or (float(self.textUP42.toPlainText()) > 1)
                    ):
                        QMessageBox.warning(
                            self,
                            "Warning",
                            "Some parametres are not within the range set out in the attribute.",
                        )
                        return
                    if not (
                        float(self.textAVP1.toPlainText())
                        < float(self.textAVP2.toPlainText())
                        < float(self.textAVP3.toPlainText())
                        < float(self.textAVP4.toPlainText())
                    ):
                        QMessageBox.warning(
                            self,
                            "Warning",
                            "Some parametres are not within the range set out in the attribute.",
                        )
                        return
                    if not (
                        float(self.textLowerBound.toPlainText())
                        < float(self.textAVP1.toPlainText())
                    ):
                        QMessageBox.warning(
                            self,
                            "Warning",
                            "Some parametres are not within the range set out in the attribute.",
                        )
                        return
                    if not (
                        (
                            float(self.textUpperBound.toPlainText())
                            > float(self.textAVP4.toPlainText())
                        )
                    ):
                        QMessageBox.warning(
                            self,
                            "Warning",
                            "Some parametres are not within the range set out in the attribute.",
                        )
                        return
                    series.append(
                        float(self.textAVP1.toPlainText()),
                        float(self.textUP11.toPlainText()),
                    )  # Punto intermedio 1
                    series.append(
                        float(self.textAVP2.toPlainText()),
                        float(self.textUP21.toPlainText()),
                    )  # Punto intermedio 1
                    series.append(
                        float(self.textAVP3.toPlainText()),
                        float(self.textUP31.toPlainText()),
                    )  # Punto intermedio 1
                    series.append(
                        float(self.textAVP4.toPlainText()),
                        float(self.textUP41.toPlainText()),
                    )  # Punto intermedio 1
                    series1.append(
                        float(self.textAVP1.toPlainText()),
                        float(self.textUP12.toPlainText()),
                    )  # Punto intermedio 1
                    series1.append(
                        float(self.textAVP2.toPlainText()),
                        float(self.textUP22.toPlainText()),
                    )  # Punto intermedio 1
                    series1.append(
                        float(self.textAVP3.toPlainText()),
                        float(self.textUP32.toPlainText()),
                    )  # Punto intermedio 1
                    series1.append(
                        float(self.textAVP4.toPlainText()),
                        float(self.textUP42.toPlainText()),
                    )  # Punto intermedio 1
                    averagevar = float(
                        (
                            float(self.textUP11.toPlainText())
                            + float(self.textUP12.toPlainText())
                        )
                        / 2
                    )
                    series2.append(float(self.textAVP1.toPlainText()), averagevar)
                    averagevar = float(
                        (
                            float(self.textUP21.toPlainText())
                            + float(self.textUP22.toPlainText())
                        )
                        / 2
                    )
                    series2.append(float(self.textAVP2.toPlainText()), averagevar)
                    averagevar = float(
                        (
                            float(self.textUP31.toPlainText())
                            + float(self.textUP32.toPlainText())
                        )
                        / 2
                    )
                    series2.append(float(self.textAVP3.toPlainText()), averagevar)
                    averagevar = float(
                        (
                            float(self.textUP41.toPlainText())
                            + float(self.textUP42.toPlainText())
                        )
                        / 2
                    )
                    series2.append(float(self.textAVP4.toPlainText()), averagevar)

                    series.append(float(self.textUpperBound.toPlainText()), 0)
                    series1.append(float(self.textUpperBound.toPlainText()), 0)
                    series2.append(float(self.textUpperBound.toPlainText()), 0)

                    chart = QChart()
                    chart.addSeries(series)
                    chart.addSeries(series1)
                    chart.addSeries(series2)
                elif (
                    self.checkBoxP2.isChecked()
                    and self.checkBoxP1.isChecked()
                    and self.checkBoxP3.isChecked()
                ):
                    if (
                        (
                            float(self.textUP11.toPlainText())
                            > float(self.textUP12.toPlainText())
                        )
                        or (
                            float(self.textUP21.toPlainText())
                            > float(self.textUP22.toPlainText())
                        )
                        or (
                            float(self.textUP31.toPlainText())
                            > float(self.textUP32.toPlainText())
                        )
                    ):
                        QMessageBox.warning(
                            self,
                            "Warning",
                            "Some parametres are not within the range set out in the attribute.",
                        )
                        return
                    if (
                        (float(self.textUP11.toPlainText()) < 0)
                        or (float(self.textUP12.toPlainText()) > 1)
                        or (float(self.textUP21.toPlainText()) < 0)
                        or (float(self.textUP22.toPlainText()) > 1)
                        or (float(self.textUP31.toPlainText()) < 0)
                        or (float(self.textUP32.toPlainText()) > 1)
                    ):
                        QMessageBox.warning(
                            self,
                            "Warning",
                            "Some parametres are not within the range set out in the attribute.",
                        )
                        return
                    if not (
                        float(self.textAVP1.toPlainText())
                        < float(self.textAVP2.toPlainText())
                        < float(self.textAVP3.toPlainText())
                    ):
                        QMessageBox.warning(
                            self,
                            "Warning",
                            "Some parametres are not within the range set out in the attribute.",
                        )
                        return
                    if not (
                        float(self.textLowerBound.toPlainText())
                        < float(self.textAVP1.toPlainText())
                    ):
                        QMessageBox.warning(
                            self,
                            "Warning",
                            "Some parametres are not within the range set out in the attribute.",
                        )
                        return
                    if not (
                        (
                            float(self.textUpperBound.toPlainText())
                            > float(self.textAVP3.toPlainText())
                        )
                    ):
                        QMessageBox.warning(
                            self,
                            "Warning",
                            "Some parametres are not within the range set out in the attribute.",
                        )
                        return
                    series.append(
                        float(self.textAVP1.toPlainText()),
                        float(self.textUP11.toPlainText()),
                    )  # Punto intermedio 1
                    series.append(
                        float(self.textAVP2.toPlainText()),
                        float(self.textUP21.toPlainText()),
                    )  # Punto intermedio 1
                    series.append(
                        float(self.textAVP3.toPlainText()),
                        float(self.textUP31.toPlainText()),
                    )  # Punto intermedio 1
                    series1.append(
                        float(self.textAVP1.toPlainText()),
                        float(self.textUP12.toPlainText()),
                    )  # Punto intermedio 1
                    series1.append(
                        float(self.textAVP2.toPlainText()),
                        float(self.textUP22.toPlainText()),
                    )  # Punto intermedio 1
                    series1.append(
                        float(self.textAVP3.toPlainText()),
                        float(self.textUP32.toPlainText()),
                    )  # Punto intermedio 1
                    averagevar = float(
                        (
                            float(self.textUP11.toPlainText())
                            + float(self.textUP12.toPlainText())
                        )
                        / 2
                    )
                    series2.append(float(self.textAVP1.toPlainText()), averagevar)
                    averagevar = float(
                        (
                            float(self.textUP21.toPlainText())
                            + float(self.textUP22.toPlainText())
                        )
                        / 2
                    )
                    series2.append(float(self.textAVP2.toPlainText()), averagevar)
                    averagevar = float(
                        (
                            float(self.textUP31.toPlainText())
                            + float(self.textUP32.toPlainText())
                        )
                        / 2
                    )
                    series2.append(float(self.textAVP3.toPlainText()), averagevar)

                    series.append(float(self.textUpperBound.toPlainText()), 0)
                    series1.append(float(self.textUpperBound.toPlainText()), 0)
                    series2.append(float(self.textUpperBound.toPlainText()), 0)

                    chart = QChart()
                    chart.addSeries(series)
                    chart.addSeries(series1)
                    chart.addSeries(series2)
                elif self.checkBoxP1.isChecked() and self.checkBoxP2.isChecked():
                    if (
                        float(self.textUP11.toPlainText())
                        > float(self.textUP12.toPlainText())
                    ) or (
                        float(self.textUP21.toPlainText())
                        > float(self.textUP22.toPlainText())
                    ):
                        QMessageBox.warning(
                            self,
                            "Warning",
                            "Some parametres are not within the range set out in the attribute.",
                        )
                        return
                    if (
                        (float(self.textUP11.toPlainText()) < 0)
                        or (float(self.textUP12.toPlainText()) > 1)
                        or (float(self.textUP21.toPlainText()) < 0)
                        or (float(self.textUP22.toPlainText()) > 1)
                    ):
                        QMessageBox.warning(
                            self,
                            "Warning",
                            "Some parametres are not within the range set out in the attribute.",
                        )
                        return
                    if not (
                        float(self.textAVP1.toPlainText())
                        < float(self.textAVP2.toPlainText())
                    ):
                        QMessageBox.warning(
                            self,
                            "Warning",
                            "Some parametres are not within the range set out in the attribute.",
                        )
                        return
                    if not (
                        float(self.textLowerBound.toPlainText())
                        < float(self.textAVP1.toPlainText())
                    ):
                        QMessageBox.warning(
                            self,
                            "Warning",
                            "Some parametres are not within the range set out in the attribute.",
                        )
                        return
                    if not (
                        (
                            float(self.textUpperBound.toPlainText())
                            > float(self.textAVP2.toPlainText())
                        )
                    ):
                        QMessageBox.warning(
                            self,
                            "Warning",
                            "Some parametres are not within the range set out in the attribute.",
                        )
                        return
                    series.append(
                        float(self.textAVP1.toPlainText()),
                        float(self.textUP11.toPlainText()),
                    )  # Punto intermedio 1
                    series.append(
                        float(self.textAVP2.toPlainText()),
                        float(self.textUP21.toPlainText()),
                    )  # Punto intermedio 1
                    series1.append(
                        float(self.textAVP1.toPlainText()),
                        float(self.textUP12.toPlainText()),
                    )  # Punto intermedio 1
                    series1.append(
                        float(self.textAVP2.toPlainText()),
                        float(self.textUP22.toPlainText()),
                    )  # Punto intermedio 1
                    averagevar = float(
                        (
                            float(self.textUP11.toPlainText())
                            + float(self.textUP12.toPlainText())
                        )
                        / 2
                    )
                    series2.append(float(self.textAVP1.toPlainText()), averagevar)
                    averagevar = float(
                        (
                            float(self.textUP21.toPlainText())
                            + float(self.textUP22.toPlainText())
                        )
                        / 2
                    )
                    series2.append(float(self.textAVP2.toPlainText()), averagevar)

                    series.append(float(self.textUpperBound.toPlainText()), 0)
                    series1.append(float(self.textUpperBound.toPlainText()), 0)
                    series2.append(float(self.textUpperBound.toPlainText()), 0)

                    chart = QChart()
                    chart.addSeries(series)
                    chart.addSeries(series1)
                    chart.addSeries(series2)
                elif self.checkBoxP1.isChecked():
                    if float(self.textUP11.toPlainText()) > float(
                        self.textUP12.toPlainText()
                    ):
                        QMessageBox.warning(
                            self,
                            "Warning",
                            "Some parametres are not within the range set out in the attribute.",
                        )
                        return
                    if (float(self.textUP11.toPlainText()) < 0) or (
                        float(self.textUP12.toPlainText()) > 1
                    ):
                        QMessageBox.warning(
                            self,
                            "Warning",
                            "Some parametres are not within the range set out in the attribute.",
                        )
                        return
                    if not (
                        float(self.textLowerBound.toPlainText())
                        < float(self.textAVP1.toPlainText())
                    ):
                        QMessageBox.warning(
                            self,
                            "Warning",
                            "Some parametres are not within the range set out in the attribute.",
                        )
                        return
                    if not (
                        float(self.textLowerBound.toPlainText())
                        < float(self.textAVP1.toPlainText())
                    ):
                        QMessageBox.warning(
                            self,
                            "Warning",
                            "Some parametres are not within the range set out in the attribute.",
                        )
                        return
                    if not (
                        (
                            float(self.textUpperBound.toPlainText())
                            > float(self.textAVP1.toPlainText())
                        )
                    ):
                        QMessageBox.warning(
                            self,
                            "Warning",
                            "Some parametres are not within the range set out in the attribute.",
                        )
                        return
                    series.append(
                        float(self.textAVP1.toPlainText()),
                        float(self.textUP11.toPlainText()),
                    )  # Punto intermedio 1
                    series1.append(
                        float(self.textAVP1.toPlainText()),
                        float(self.textUP12.toPlainText()),
                    )  # Punto intermedio 1
                    averagevar = float(
                        (
                            float(self.textUP11.toPlainText())
                            + float(self.textUP12.toPlainText())
                        )
                        / 2
                    )
                    series2.append(float(self.textAVP1.toPlainText()), averagevar)

                    series.append(float(self.textUpperBound.toPlainText()), 0)
                    series1.append(float(self.textUpperBound.toPlainText()), 0)
                    series2.append(float(self.textUpperBound.toPlainText()), 0)

                    chart = QChart()
                    chart.addSeries(series)
                    chart.addSeries(series1)
                    chart.addSeries(series2)
                else:
                    # self.AttMPVCU.setText(f"Index ({int(attribute.minRange)}: Ideal, {int(attribute.maxRange)} Worst)")

                    # series.append(3.5, 0.6)  # Punto intermedio
                    # series.append(3.5, 0.2)  # Punto intermedio
                    series.append(float(self.textUpperBound.toPlainText()), 0)
                    chart = QChart()
                    chart.addSeries(series)

            # Crear el gráfico y añadir la serie de datos
            # chart = QChart()
            # chart.addSeries(series)
            # chart.setTitle("Gráfico de Línea")
            chart.legend().setVisible(False)

            # Crear los ejes X e Y y establecer etiquetas en los puntos
            x_axis = QValueAxis()
            x_axis.setLabelFormat("%.1f")
            x_axis.setTickCount(5)  # Número de etiquetas en el eje X
            x_axis.setRange(
                float(self.textLowerBound.toPlainText()),
                float(self.textUpperBound.toPlainText()),
            )

            y_axis = QValueAxis()
            y_axis.setLabelFormat("%.1f")
            y_axis.setTickCount(5)  # Número de etiquetas en el eje Y
            y_axis.setRange(0, 1)

            chart.addAxis(x_axis, Qt.AlignmentFlag.AlignBottom)
            chart.addAxis(y_axis, Qt.AlignmentFlag.AlignLeft)

            series.attachAxis(x_axis)
            series.attachAxis(y_axis)

            chart.setBackgroundBrush(brush)
            chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)

            # Crear la vista del gráfico
            # chart_view = QChartView()

            chart_view = ChartView(
                text_X=self.plainTextAVLUF,
                text_Y=self.plainTextULUF,
                posX_1=float(self.textLowerBound.toPlainText()),
                posX_2=float(self.textUpperBound.toPlainText()),
            )
            chart_view.setChart(chart)
            chart_view.setFrameShape(QFrame.Shape.NoFrame)
            chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)
            chart_view.setBackgroundBrush(brush)

            self.layoutLUF.addWidget(chart_view)
            # self.AttMPVCU.raise_()
        except (ValueError, AttributeError):
            QMessageBox.warning(
                self,
                "Warning",
                "Some parametres are not within the range set out in the attribute.",
            )
            return

    def onStateChanged(self, state):
        # Obtener el índice del QCheckBox que emitió la señal
        index = self.checkboxes.index(self.sender())

        if index == 0 and self.checkBoxP1.isChecked():
            self.textAVP1.setEnabled(True)
            self.textUP11.setEnabled(True)
            self.textUP12.setEnabled(True)
            self.textAVP2.setEnabled(False)
            self.textUP21.setEnabled(False)
            self.textUP22.setEnabled(False)
            self.textAVP3.setEnabled(False)
            self.textUP31.setEnabled(False)
            self.textUP32.setEnabled(False)
            self.textAVP4.setEnabled(False)
            self.textUP41.setEnabled(False)
            self.textUP42.setEnabled(False)
            self.textAVP5.setEnabled(False)
            self.textUP51.setEnabled(False)
            self.textUP52.setEnabled(False)
        elif index == 1 and self.checkBoxP2.isChecked():
            self.textAVP1.setEnabled(True)
            self.textUP11.setEnabled(True)
            self.textUP12.setEnabled(True)
            self.textAVP2.setEnabled(True)
            self.textUP21.setEnabled(True)
            self.textUP22.setEnabled(True)
            self.textAVP3.setEnabled(False)
            self.textUP31.setEnabled(False)
            self.textUP32.setEnabled(False)
            self.textAVP4.setEnabled(False)
            self.textUP41.setEnabled(False)
            self.textUP42.setEnabled(False)
            self.textAVP5.setEnabled(False)
            self.textUP51.setEnabled(False)
            self.textUP52.setEnabled(False)
        elif index == 2 and self.checkBoxP3.isChecked():
            self.textAVP1.setEnabled(True)
            self.textUP11.setEnabled(True)
            self.textUP12.setEnabled(True)
            self.textAVP2.setEnabled(True)
            self.textUP21.setEnabled(True)
            self.textUP22.setEnabled(True)
            self.textAVP3.setEnabled(True)
            self.textUP31.setEnabled(True)
            self.textUP32.setEnabled(True)
            self.textAVP4.setEnabled(False)
            self.textUP41.setEnabled(False)
            self.textUP42.setEnabled(False)
            self.textAVP5.setEnabled(False)
            self.textUP51.setEnabled(False)
            self.textUP52.setEnabled(False)
        elif index == 3 and self.checkBoxP4.isChecked():
            self.textAVP1.setEnabled(True)
            self.textUP11.setEnabled(True)
            self.textUP12.setEnabled(True)
            self.textAVP2.setEnabled(True)
            self.textUP21.setEnabled(True)
            self.textUP22.setEnabled(True)
            self.textAVP3.setEnabled(True)
            self.textUP31.setEnabled(True)
            self.textUP32.setEnabled(True)
            self.textAVP4.setEnabled(True)
            self.textUP41.setEnabled(True)
            self.textUP42.setEnabled(True)
            self.textAVP5.setEnabled(False)
            self.textUP51.setEnabled(False)
            self.textUP52.setEnabled(False)
        elif index == 4 and self.checkBoxP5.isChecked():
            self.textAVP1.setEnabled(True)
            self.textUP11.setEnabled(True)
            self.textUP12.setEnabled(True)
            self.textAVP2.setEnabled(True)
            self.textUP21.setEnabled(True)
            self.textUP22.setEnabled(True)
            self.textAVP3.setEnabled(True)
            self.textUP31.setEnabled(True)
            self.textUP32.setEnabled(True)
            self.textAVP4.setEnabled(True)
            self.textUP41.setEnabled(True)
            self.textUP42.setEnabled(True)
            self.textAVP5.setEnabled(True)
            self.textUP51.setEnabled(True)
            self.textUP52.setEnabled(True)

        else:
            self.textAVP1.setEnabled(False)
            self.textUP11.setEnabled(False)
            self.textUP12.setEnabled(False)
            self.textAVP2.setEnabled(False)
            self.textUP21.setEnabled(False)
            self.textUP22.setEnabled(False)
            self.textAVP3.setEnabled(False)
            self.textUP31.setEnabled(False)
            self.textUP32.setEnabled(False)
            self.textAVP4.setEnabled(False)
            self.textUP41.setEnabled(False)
            self.textUP42.setEnabled(False)
            self.textAVP5.setEnabled(False)
            self.textUP51.setEnabled(False)
            self.textUP52.setEnabled(False)

        if state == Qt.CheckState.Unchecked:
            # Establecer el estado seleccionado para los QCheckBoxes anteriores
            for i in range(len(self.checkboxes)):
                self.checkboxes[i].setChecked(False)
        else:
            for i in range(index):
                self.checkboxes[i].setChecked(True)

    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.setParent(None)
            else:
                self.clear_layout(item.layout())


class VentanaCUV(QMainWindow):
    global attributes
    global attributesnames

    def __init__(self, parent=None):
        super(VentanaCUV, self).__init__(parent)
        uic.loadUi("componentsUtilitiesView.ui", self)
        icono = QIcon("iconoUPM.ico")
        super(VentanaCUV, self).setWindowIcon(icono)
        super(VentanaCUV, self).setWindowTitle("Viewing Components Utilities")
        self.VentanaPrincipalGMAA = parent

        background_color = QColor("#F0F0F0")
        brush = QBrush(background_color)

        # signals
        self.tableAltName.itemDoubleClicked.connect(self.on_item_double_clicked)
        self.comboBoxAltNames.currentTextChanged.connect(self.on_combo_box_changed)
        self.pushButtonOKVCU.clicked.connect(self.close)

        attribute = None
        # we insert all the alternatives in the table
        if attributesnames:
            self.comboBoxAltNames.setCurrentText(attributesnames[0])
            attribute = attributes[0]

        else:
            self.comboBoxAltNames.setCurrentText("")

        num_rows = len(attributesnames)
        widthTable = self.tableAltName.width()
        self.tableAltName.setRowCount(num_rows)
        self.tableAltName.setColumnCount(1)
        self.tableAltName.setColumnWidth(0, widthTable)
        self.tableAltName.verticalHeader().setVisible(
            False
        )  # Ocultar el encabezado vertical
        self.tableAltName.horizontalHeader().setVisible(
            False
        )  # Ocultar el encabezado horizontal
        self.tableAltName.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )  # Deshabilitar la edición de los elementos

        # we insert also the options in the QComboBox
        for i, attr in enumerate(attributesnames):
            self.comboBoxAltNames.addItem(attr)
            item = QTableWidgetItem(attr)
            # item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.tableAltName.setItem(i, 0, item)

        if attribute.unitType == "Continuous":
            self.AttMPVCU.setVisible(True)
            # window = QMainWindow()
            widget = QWidget()
            # window.setCentralWidget(widget)

            self.clear_layout(self.vLayoutVCU)
            self.clear_layout(self.hLayoutVCU)
            self.layoutVCU = self.hLayoutVCU
            self.layoutVCU.addWidget(widget)

            series = QLineSeries()
            series1 = QLineSeries()
            series2 = QLineSeries()
            if attribute.mostPrefered == "Sup":
                series.append(float(attribute.minRange), 0)  # Punto inicial
                series1.append(float(attribute.minRange), 0)  # Punto inicial
                series2.append(float(attribute.minRange), 0)  # Punto inicial
                self.AttMPVCU.setText(
                    f"Index ({int(attribute.minRange)}: Worst, {int(attribute.maxRange)} Ideal)"
                )
                if attribute.interPoints == 5:
                    series.append(float(attribute.IPAV1), float(attribute.IP11))
                    series.append(float(attribute.IPAV2), float(attribute.IP21))
                    series.append(float(attribute.IPAV3), float(attribute.IP31))
                    series.append(float(attribute.IPAV4), float(attribute.IP41))
                    series.append(float(attribute.IPAV5), float(attribute.IP51))
                    series1.append(float(attribute.IPAV1), float(attribute.IP12))
                    series1.append(float(attribute.IPAV2), float(attribute.IP22))
                    series1.append(float(attribute.IPAV3), float(attribute.IP32))
                    series1.append(float(attribute.IPAV4), float(attribute.IP42))
                    series1.append(float(attribute.IPAV5), float(attribute.IP52))
                    averagevar = float(
                        (float(attribute.IP11) + float(attribute.IP12)) / 2
                    )
                    series2.append(float(attribute.IPAV1), averagevar)
                    averagevar = float(
                        (float(attribute.IP21) + float(attribute.IP22)) / 2
                    )
                    series2.append(float(attribute.IPAV2), averagevar)
                    averagevar = float(
                        (float(attribute.IP31) + float(attribute.IP32)) / 2
                    )
                    series2.append(float(attribute.IPAV3), averagevar)
                    averagevar = float(
                        (float(attribute.IP41) + float(attribute.IP42)) / 2
                    )
                    series2.append(float(attribute.IPAV4), averagevar)
                    averagevar = float(
                        (float(attribute.IP51) + float(attribute.IP52)) / 2
                    )
                    series2.append(float(attribute.IPAV5), averagevar)
                    # series.append(3.5, 0.6)  # Punto intermedio
                    # series.append(3.5, 0.2)  # Punto intermedio
                    series.append(float(attribute.maxRange), 1)  # Punto final
                    series1.append(float(attribute.maxRange), 1)  # Punto final
                    series2.append(float(attribute.maxRange), 1)  # Punto final

                    chart = QChart()
                    chart.addSeries(series)
                    chart.addSeries(series1)
                    chart.addSeries(series2)

                elif attribute.interPoints == 4:
                    series.append(float(attribute.IPAV1), float(attribute.IP11))
                    series.append(float(attribute.IPAV2), float(attribute.IP21))
                    series.append(float(attribute.IPAV3), float(attribute.IP31))
                    series.append(float(attribute.IPAV4), float(attribute.IP41))
                    series1.append(float(attribute.IPAV1), float(attribute.IP12))
                    series1.append(float(attribute.IPAV2), float(attribute.IP22))
                    series1.append(float(attribute.IPAV3), float(attribute.IP32))
                    series1.append(float(attribute.IPAV4), float(attribute.IP42))
                    averagevar = float(
                        (float(attribute.IP11) + float(attribute.IP12)) / 2
                    )
                    series2.append(float(attribute.IPAV1), averagevar)
                    averagevar = float(
                        (float(attribute.IP21) + float(attribute.IP22)) / 2
                    )
                    series2.append(float(attribute.IPAV2), averagevar)
                    averagevar = float(
                        (float(attribute.IP31) + float(attribute.IP32)) / 2
                    )
                    series2.append(float(attribute.IPAV3), averagevar)
                    averagevar = float(
                        (float(attribute.IP41) + float(attribute.IP42)) / 2
                    )
                    series2.append(float(attribute.IPAV4), averagevar)
                    series.append(float(attribute.maxRange), 1)  # Punto final
                    series1.append(float(attribute.maxRange), 1)  # Punto final
                    series2.append(float(attribute.maxRange), 1)  # Punto final

                    series.append(float(attribute.maxRange), 1)  # Punto final
                    series1.append(float(attribute.maxRange), 1)  # Punto final
                    series2.append(float(attribute.maxRange), 1)  # Punto final

                    chart = QChart()
                    chart.addSeries(series)
                    chart.addSeries(series1)
                    chart.addSeries(series2)

                elif attribute.interPoints == 3:
                    series.append(float(attribute.IPAV1), float(attribute.IP11))
                    series.append(float(attribute.IPAV2), float(attribute.IP21))
                    series.append(float(attribute.IPAV3), float(attribute.IP31))
                    series1.append(float(attribute.IPAV1), float(attribute.IP12))
                    series1.append(float(attribute.IPAV2), float(attribute.IP22))
                    series1.append(float(attribute.IPAV3), float(attribute.IP32))
                    averagevar = float(
                        (float(attribute.IP11) + float(attribute.IP12)) / 2
                    )
                    series2.append(float(attribute.IPAV1), averagevar)
                    averagevar = float(
                        (float(attribute.IP21) + float(attribute.IP22)) / 2
                    )
                    series2.append(float(attribute.IPAV2), averagevar)
                    averagevar = float(
                        (float(attribute.IP31) + float(attribute.IP32)) / 2
                    )
                    series2.append(float(attribute.IPAV3), averagevar)

                    series.append(float(attribute.maxRange), 1)  # Punto final
                    series1.append(float(attribute.maxRange), 1)  # Punto final
                    series2.append(float(attribute.maxRange), 1)  # Punto final

                    chart = QChart()
                    chart.addSeries(series)
                    chart.addSeries(series1)
                    chart.addSeries(series2)

                elif attribute.interPoints == 2:
                    series.append(float(attribute.IPAV1), float(attribute.IP11))
                    series.append(float(attribute.IPAV2), float(attribute.IP21))
                    series1.append(float(attribute.IPAV1), float(attribute.IP12))
                    series1.append(float(attribute.IPAV2), float(attribute.IP22))
                    averagevar = float(
                        (float(attribute.IP11) + float(attribute.IP12)) / 2
                    )
                    series2.append(float(attribute.IPAV1), averagevar)
                    averagevar = float(
                        (float(attribute.IP21) + float(attribute.IP22)) / 2
                    )
                    series2.append(float(attribute.IPAV2), averagevar)

                    series.append(float(attribute.maxRange), 1)  # Punto final
                    series1.append(float(attribute.maxRange), 1)  # Punto final
                    series2.append(float(attribute.maxRange), 1)  # Punto final

                    chart = QChart()
                    chart.addSeries(series)
                    chart.addSeries(series1)
                    chart.addSeries(series2)

                elif attribute.interPoints == 1:
                    series.append(float(attribute.IPAV1), float(attribute.IP11))
                    series1.append(float(attribute.IPAV1), float(attribute.IP12))
                    averagevar = float(
                        (float(attribute.IP11) + float(attribute.IP12)) / 2
                    )
                    series2.append(float(attribute.IPAV1), averagevar)

                    series.append(float(attribute.maxRange), 1)  # Punto final
                    series1.append(float(attribute.maxRange), 1)  # Punto final
                    series2.append(float(attribute.maxRange), 1)  # Punto final

                    chart = QChart()
                    chart.addSeries(series)
                    chart.addSeries(series1)
                    chart.addSeries(series2)
                else:
                    series.append(float(attribute.maxRange), 1)
                    chart = QChart()
                    chart.addSeries(series)
            else:
                self.AttMPVCU.setText(
                    f"Index ({int(attribute.minRange)}: Ideal, {int(attribute.maxRange)} Worst)"
                )
                series.append(float(attribute.minRange), 1)  # Punto inicial
                series1.append(float(attribute.minRange), 1)  # Punto inicial
                series2.append(float(attribute.minRange), 1)  # Punto inicial
                if attribute.interPoints == 5:
                    series.append(float(attribute.IPAV1), float(attribute.IP11))
                    series.append(float(attribute.IPAV2), float(attribute.IP21))
                    series.append(float(attribute.IPAV3), float(attribute.IP31))
                    series.append(float(attribute.IPAV4), float(attribute.IP41))
                    series.append(float(attribute.IPAV5), float(attribute.IP51))
                    series1.append(float(attribute.IPAV1), float(attribute.IP12))
                    series1.append(float(attribute.IPAV2), float(attribute.IP22))
                    series1.append(float(attribute.IPAV3), float(attribute.IP32))
                    series1.append(float(attribute.IPAV4), float(attribute.IP42))
                    series1.append(float(attribute.IPAV5), float(attribute.IP52))
                    averagevar = float(
                        (float(attribute.IP11) + float(attribute.IP12)) / 2
                    )
                    series2.append(float(attribute.IPAV1), averagevar)
                    averagevar = float(
                        (float(attribute.IP21) + float(attribute.IP22)) / 2
                    )
                    series2.append(float(attribute.IPAV2), averagevar)
                    averagevar = float(
                        (float(attribute.IP31) + float(attribute.IP32)) / 2
                    )
                    series2.append(float(attribute.IPAV3), averagevar)
                    averagevar = float(
                        (float(attribute.IP41) + float(attribute.IP42)) / 2
                    )
                    series2.append(float(attribute.IPAV4), averagevar)
                    averagevar = float(
                        (float(attribute.IP51) + float(attribute.IP52)) / 2
                    )
                    series2.append(float(attribute.IPAV5), averagevar)
                    # series.append(3.5, 0.6)  # Punto intermedio
                    # series.append(3.5, 0.2)  # Punto intermedio
                    series.append(float(attribute.maxRange), 0)  # Punto final
                    series1.append(float(attribute.maxRange), 0)  # Punto final
                    series2.append(float(attribute.maxRange), 0)  # Punto final

                    chart = QChart()
                    chart.addSeries(series)
                    chart.addSeries(series1)
                    chart.addSeries(series2)
                elif attribute.interPoints == 4:
                    series.append(float(attribute.IPAV1), float(attribute.IP11))
                    series.append(float(attribute.IPAV2), float(attribute.IP21))
                    series.append(float(attribute.IPAV3), float(attribute.IP31))
                    series.append(float(attribute.IPAV4), float(attribute.IP41))
                    series1.append(float(attribute.IPAV1), float(attribute.IP12))
                    series1.append(float(attribute.IPAV2), float(attribute.IP22))
                    series1.append(float(attribute.IPAV3), float(attribute.IP32))
                    series1.append(float(attribute.IPAV4), float(attribute.IP42))
                    averagevar = float(
                        (float(attribute.IP11) + float(attribute.IP12)) / 2
                    )
                    series2.append(float(attribute.IPAV1), averagevar)
                    averagevar = float(
                        (float(attribute.IP21) + float(attribute.IP22)) / 2
                    )
                    series2.append(float(attribute.IPAV2), averagevar)
                    averagevar = float(
                        (float(attribute.IP31) + float(attribute.IP32)) / 2
                    )
                    series2.append(float(attribute.IPAV3), averagevar)
                    averagevar = float(
                        (float(attribute.IP41) + float(attribute.IP42)) / 2
                    )
                    series2.append(float(attribute.IPAV4), averagevar)

                    # series.append(3.5, 0.6)  # Punto intermedio
                    # series.append(3.5, 0.2)  # Punto intermedio
                    series.append(float(attribute.maxRange), 0)  # Punto final
                    series1.append(float(attribute.maxRange), 0)  # Punto final
                    series2.append(float(attribute.maxRange), 0)  # Punto final

                    chart = QChart()
                    chart.addSeries(series)
                    chart.addSeries(series1)
                    chart.addSeries(series2)

                elif attribute.interPoints == 3:
                    series.append(float(attribute.IPAV1), float(attribute.IP11))
                    series.append(float(attribute.IPAV2), float(attribute.IP21))
                    series.append(float(attribute.IPAV3), float(attribute.IP31))
                    series1.append(float(attribute.IPAV1), float(attribute.IP12))
                    series1.append(float(attribute.IPAV2), float(attribute.IP22))
                    series1.append(float(attribute.IPAV3), float(attribute.IP32))
                    averagevar = float(
                        (float(attribute.IP11) + float(attribute.IP12)) / 2
                    )
                    series2.append(float(attribute.IPAV1), averagevar)
                    averagevar = float(
                        (float(attribute.IP21) + float(attribute.IP22)) / 2
                    )
                    series2.append(float(attribute.IPAV2), averagevar)
                    averagevar = float(
                        (float(attribute.IP31) + float(attribute.IP32)) / 2
                    )
                    series2.append(float(attribute.IPAV3), averagevar)

                    # series.append(3.5, 0.6)  # Punto intermedio
                    # series.append(3.5, 0.2)  # Punto intermedio
                    series.append(float(attribute.maxRange), 0)  # Punto final
                    series1.append(float(attribute.maxRange), 0)  # Punto final
                    series2.append(float(attribute.maxRange), 0)  # Punto final

                    chart = QChart()
                    chart.addSeries(series)
                    chart.addSeries(series1)
                    chart.addSeries(series2)

                elif attribute.interPoints == 2:
                    series.append(float(attribute.IPAV1), float(attribute.IP11))
                    series.append(float(attribute.IPAV2), float(attribute.IP21))
                    series1.append(float(attribute.IPAV1), float(attribute.IP12))
                    series1.append(float(attribute.IPAV2), float(attribute.IP22))
                    averagevar = float(
                        (float(attribute.IP11) + float(attribute.IP12)) / 2
                    )
                    series2.append(float(attribute.IPAV1), averagevar)
                    averagevar = float(
                        (float(attribute.IP21) + float(attribute.IP22)) / 2
                    )
                    series2.append(float(attribute.IPAV2), averagevar)

                    # series.append(3.5, 0.6)  # Punto intermedio
                    # series.append(3.5, 0.2)  # Punto intermedio
                    series.append(float(attribute.maxRange), 0)  # Punto final
                    series1.append(float(attribute.maxRange), 0)  # Punto final
                    series2.append(float(attribute.maxRange), 0)  # Punto final

                    chart = QChart()
                    chart.addSeries(series)
                    chart.addSeries(series1)
                    chart.addSeries(series2)
                elif attribute.interPoints == 1:
                    series.append(float(attribute.IPAV1), float(attribute.IP11))
                    series1.append(float(attribute.IPAV1), float(attribute.IP12))
                    averagevar = float(
                        (float(attribute.IP11) + float(attribute.IP12)) / 2
                    )
                    series2.append(float(attribute.IPAV1), averagevar)

                    series.append(float(attribute.maxRange), 0)  # Punto final
                    series1.append(float(attribute.maxRange), 0)  # Punto final
                    series2.append(float(attribute.maxRange), 0)  # Punto final

                    chart = QChart()
                    chart.addSeries(series)
                    chart.addSeries(series1)
                    chart.addSeries(series2)
                else:
                    series.append(float(attribute.maxRange), 0)  # Punto final
                    chart = QChart()
                    chart.addSeries(series)
                # series.append(3.5, 0.6)  # Punto intermedio
                # series.append(3.5, 0.2)  # Punto intermedio

            chart.legend().setVisible(False)

            # Crear los ejes X e Y y establecer etiquetas en los puntos
            x_axis = QValueAxis()
            x_axis.setLabelFormat("%.1f")
            x_axis.setTickCount(2)  # Número de etiquetas en el eje X
            x_axis.setRange(float(attribute.minRange), float(attribute.maxRange))

            y_axis = QValueAxis()
            y_axis.setLabelFormat("%.1f")
            y_axis.setTickCount(4)  # Número de etiquetas en el eje Y
            y_axis.setRange(0, 1)

            chart.addAxis(x_axis, Qt.AlignmentFlag.AlignBottom)
            chart.addAxis(y_axis, Qt.AlignmentFlag.AlignLeft)

            series.attachAxis(x_axis)
            series.attachAxis(y_axis)

            chart.setBackgroundBrush(brush)
            chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)

            # show Utility and Attribute Value for Continuous values
            self.groupBoxVCU.setVisible(True)

            # Crear la vista del gráfico
            # chart_view = QChartView()
            self.plainTextAVC.setReadOnly(True)

            chart_view = ChartView(
                text_X=self.plainTextAVC,
                text_Y=self.plainTextAU,
                posX_1=float(attribute.minRange),
                posX_2=float(attribute.maxRange),
            )
            chart_view.setChart(chart)
            chart_view.setFrameShape(QFrame.Shape.NoFrame)
            chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)
            chart_view.setBackgroundBrush(brush)

            self.layoutVCU.addWidget(chart_view)
            self.AttMPVCU.raise_()

        else:
            self.AttMPVCU.setVisible(False)
            data = []
            valmins = []
            valmaxs = []
            for i in range(1, len(attribute.optionsList) + 1):
                variable_name1 = "UP{}1".format(i)
                variable_name2 = "UP{}2".format(i)
                valmins.append(float(getattr(attribute, variable_name1)))
                valmaxs.append(float(getattr(attribute, variable_name2)))

            for valmin, valmax in zip(valmins, valmaxs):
                data.append((valmin, valmax))

            # hide Utility and Attribute Value for Continuous values
            self.groupBoxVCU.setVisible(False)

            chart_widget = LineBarChartWidget()
            names_chart = NamesChart()
            names_chart.set_connections(attribute.optionsList)
            chart_widget.set_data(data)
            # chart_widget.set_connections(attribute.optionsList)
            self.clear_layout(self.layoutVCU)
            self.clear_layout(self.vLayoutVCU)
            self.layoutVCU = self.hLayoutVCU
            self.vlayoutVCU = self.vLayoutVCU
            self.layoutVCU.addWidget(chart_widget)
            self.vlayoutVCU.addWidget(names_chart)

    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
            else:
                self.clear_layout(item.layout())

    def on_combo_box_changed(self, text):
        selected_attr = None
        # selected_text = self.comboBoxAltNames.currentText()
        for attr in attributes:
            # if attr.text() == selected_text:
            if attr.text() == text:
                selected_attr = attr
                break

        if selected_attr.unitType == "Continuous":
            # self.clear_layout(self.hLayoutVCU)
            if self.hLayoutVCU.count() > 0:
                widget_existente = self.hLayoutVCU.itemAt(0).widget()
                widget_existente.setParent(None)
                widget_existente = None
            widget = QWidget()
            # window.setCentralWidget(widget)
            self.clear_layout(self.hLayoutVCU)
            self.clear_layout(self.vLayoutVCU)
            self.layoutVCU = self.hLayoutVCU
            self.layoutVCU.addWidget(widget)

            background_color = QColor("#F0F0F0")
            brush = QBrush(background_color)
            self.AttMPVCU.setVisible(True)

            series = QLineSeries()
            series1 = QLineSeries()
            series2 = QLineSeries()
            if selected_attr.mostPrefered == "Sup":
                series.append(float(selected_attr.minRange), 0)  # Punto inicial
                series1.append(float(selected_attr.minRange), 0)  # Punto inicial
                series2.append(float(selected_attr.minRange), 0)  # Punto inicial
                self.AttMPVCU.setText(
                    f"Index ({int(selected_attr.minRange)}: Worst, {int(selected_attr.maxRange)} Ideal)"
                )
                if selected_attr.interPoints == 5:
                    series.append(float(selected_attr.IPAV1), float(selected_attr.IP11))
                    series.append(float(selected_attr.IPAV2), float(selected_attr.IP21))
                    series.append(float(selected_attr.IPAV3), float(selected_attr.IP31))
                    series.append(float(selected_attr.IPAV4), float(selected_attr.IP41))
                    series.append(float(selected_attr.IPAV5), float(selected_attr.IP51))
                    series1.append(
                        float(selected_attr.IPAV1), float(selected_attr.IP12)
                    )
                    series1.append(
                        float(selected_attr.IPAV2), float(selected_attr.IP22)
                    )
                    series1.append(
                        float(selected_attr.IPAV3), float(selected_attr.IP32)
                    )
                    series1.append(
                        float(selected_attr.IPAV4), float(selected_attr.IP42)
                    )
                    series1.append(
                        float(selected_attr.IPAV5), float(selected_attr.IP52)
                    )
                    averagevar = float(
                        (float(selected_attr.IP11) + float(selected_attr.IP12)) / 2
                    )
                    series2.append(float(selected_attr.IPAV1), averagevar)
                    averagevar = float(
                        (float(selected_attr.IP21) + float(selected_attr.IP22)) / 2
                    )
                    series2.append(float(selected_attr.IPAV2), averagevar)
                    averagevar = float(
                        (float(selected_attr.IP31) + float(selected_attr.IP32)) / 2
                    )
                    series2.append(float(selected_attr.IPAV3), averagevar)
                    averagevar = float(
                        (float(selected_attr.IP41) + float(selected_attr.IP42)) / 2
                    )
                    series2.append(float(selected_attr.IPAV4), averagevar)
                    averagevar = float(
                        (float(selected_attr.IP51) + float(selected_attr.IP52)) / 2
                    )
                    series2.append(float(selected_attr.IPAV5), averagevar)
                    # series.append(3.5, 0.6)  # Punto intermedio
                    # series.append(3.5, 0.2)  # Punto intermedio
                    series.append(float(selected_attr.maxRange), 1)  # Punto final
                    series1.append(float(selected_attr.maxRange), 1)  # Punto final
                    series2.append(float(selected_attr.maxRange), 1)  # Punto final

                    chart = QChart()
                    chart.addSeries(series)
                    chart.addSeries(series1)
                    chart.addSeries(series2)

                elif selected_attr.interPoints == 4:
                    series.append(float(selected_attr.IPAV1), float(selected_attr.IP11))
                    series.append(float(selected_attr.IPAV2), float(selected_attr.IP21))
                    series.append(float(selected_attr.IPAV3), float(selected_attr.IP31))
                    series.append(float(selected_attr.IPAV4), float(selected_attr.IP41))
                    series1.append(
                        float(selected_attr.IPAV1), float(selected_attr.IP12)
                    )
                    series1.append(
                        float(selected_attr.IPAV2), float(selected_attr.IP22)
                    )
                    series1.append(
                        float(selected_attr.IPAV3), float(selected_attr.IP32)
                    )
                    series1.append(
                        float(selected_attr.IPAV4), float(selected_attr.IP42)
                    )
                    averagevar = float(
                        (float(selected_attr.IP11) + float(selected_attr.IP12)) / 2
                    )
                    series2.append(float(selected_attr.IPAV1), averagevar)
                    averagevar = float(
                        (float(selected_attr.IP21) + float(selected_attr.IP22)) / 2
                    )
                    series2.append(float(selected_attr.IPAV2), averagevar)
                    averagevar = float(
                        (float(selected_attr.IP31) + float(selected_attr.IP32)) / 2
                    )
                    series2.append(float(selected_attr.IPAV3), averagevar)
                    averagevar = float(
                        (float(selected_attr.IP41) + float(selected_attr.IP42)) / 2
                    )
                    series2.append(float(selected_attr.IPAV4), averagevar)
                    series.append(float(selected_attr.maxRange), 1)  # Punto final
                    series1.append(float(selected_attr.maxRange), 1)  # Punto final
                    series2.append(float(selected_attr.maxRange), 1)  # Punto final

                    series.append(float(selected_attr.maxRange), 1)  # Punto final
                    series1.append(float(selected_attr.maxRange), 1)  # Punto final
                    series2.append(float(selected_attr.maxRange), 1)  # Punto final

                    chart = QChart()
                    chart.addSeries(series)
                    chart.addSeries(series1)
                    chart.addSeries(series2)

                elif selected_attr.interPoints == 3:
                    series.append(float(selected_attr.IPAV1), float(selected_attr.IP11))
                    series.append(float(selected_attr.IPAV2), float(selected_attr.IP21))
                    series.append(float(selected_attr.IPAV3), float(selected_attr.IP31))
                    series1.append(
                        float(selected_attr.IPAV1), float(selected_attr.IP12)
                    )
                    series1.append(
                        float(selected_attr.IPAV2), float(selected_attr.IP22)
                    )
                    series1.append(
                        float(selected_attr.IPAV3), float(selected_attr.IP32)
                    )
                    averagevar = float(
                        (float(selected_attr.IP11) + float(selected_attr.IP12)) / 2
                    )
                    series2.append(float(selected_attr.IPAV1), averagevar)
                    averagevar = float(
                        (float(selected_attr.IP21) + float(selected_attr.IP22)) / 2
                    )
                    series2.append(float(selected_attr.IPAV2), averagevar)
                    averagevar = float(
                        (float(selected_attr.IP31) + float(selected_attr.IP32)) / 2
                    )
                    series2.append(float(selected_attr.IPAV3), averagevar)

                    series.append(float(selected_attr.maxRange), 1)  # Punto final
                    series1.append(float(selected_attr.maxRange), 1)  # Punto final
                    series2.append(float(selected_attr.maxRange), 1)  # Punto final

                    chart = QChart()
                    chart.addSeries(series)
                    chart.addSeries(series1)
                    chart.addSeries(series2)

                elif selected_attr.interPoints == 2:
                    series.append(float(selected_attr.IPAV1), float(selected_attr.IP11))
                    series.append(float(selected_attr.IPAV2), float(selected_attr.IP21))
                    series1.append(
                        float(selected_attr.IPAV1), float(selected_attr.IP12)
                    )
                    series1.append(
                        float(selected_attr.IPAV2), float(selected_attr.IP22)
                    )
                    averagevar = float(
                        (float(selected_attr.IP11) + float(selected_attr.IP12)) / 2
                    )
                    series2.append(float(selected_attr.IPAV1), averagevar)
                    averagevar = float(
                        (float(selected_attr.IP21) + float(selected_attr.IP22)) / 2
                    )
                    series2.append(float(selected_attr.IPAV2), averagevar)

                    series.append(float(selected_attr.maxRange), 1)  # Punto final
                    series1.append(float(selected_attr.maxRange), 1)  # Punto final
                    series2.append(float(selected_attr.maxRange), 1)  # Punto final

                    chart = QChart()
                    chart.addSeries(series)
                    chart.addSeries(series1)
                    chart.addSeries(series2)

                elif selected_attr.interPoints == 1:
                    series.append(float(selected_attr.IPAV1), float(selected_attr.IP11))
                    series1.append(
                        float(selected_attr.IPAV1), float(selected_attr.IP12)
                    )
                    averagevar = float(
                        (float(selected_attr.IP11) + float(selected_attr.IP12)) / 2
                    )
                    series2.append(float(selected_attr.IPAV1), averagevar)

                    series.append(float(selected_attr.maxRange), 1)  # Punto final
                    series1.append(float(selected_attr.maxRange), 1)  # Punto final
                    series2.append(float(selected_attr.maxRange), 1)  # Punto final

                    chart = QChart()
                    chart.addSeries(series)
                    chart.addSeries(series1)
                    chart.addSeries(series2)
                else:
                    series.append(float(selected_attr.maxRange), 1)
                    chart = QChart()
                    chart.addSeries(series)
            else:
                self.AttMPVCU.setText(
                    f"Index ({int(selected_attr.minRange)}: Ideal, {int(selected_attr.maxRange)} Worst)"
                )
                series.append(float(selected_attr.minRange), 1)  # Punto inicial
                series1.append(float(selected_attr.minRange), 1)  # Punto inicial
                series2.append(float(selected_attr.minRange), 1)  # Punto inicial
                if selected_attr.interPoints == 5:
                    series.append(float(selected_attr.IPAV1), float(selected_attr.IP11))
                    series.append(float(selected_attr.IPAV2), float(selected_attr.IP21))
                    series.append(float(selected_attr.IPAV3), float(selected_attr.IP31))
                    series.append(float(selected_attr.IPAV4), float(selected_attr.IP41))
                    series.append(float(selected_attr.IPAV5), float(selected_attr.IP51))
                    series1.append(
                        float(selected_attr.IPAV1), float(selected_attr.IP12)
                    )
                    series1.append(
                        float(selected_attr.IPAV2), float(selected_attr.IP22)
                    )
                    series1.append(
                        float(selected_attr.IPAV3), float(selected_attr.IP32)
                    )
                    series1.append(
                        float(selected_attr.IPAV4), float(selected_attr.IP42)
                    )
                    series1.append(
                        float(selected_attr.IPAV5), float(selected_attr.IP52)
                    )
                    averagevar = float(
                        (float(selected_attr.IP11) + float(selected_attr.IP12)) / 2
                    )
                    series2.append(float(selected_attr.IPAV1), averagevar)
                    averagevar = float(
                        (float(selected_attr.IP21) + float(selected_attr.IP22)) / 2
                    )
                    series2.append(float(selected_attr.IPAV2), averagevar)
                    averagevar = float(
                        (float(selected_attr.IP31) + float(selected_attr.IP32)) / 2
                    )
                    series2.append(float(selected_attr.IPAV3), averagevar)
                    averagevar = float(
                        (float(selected_attr.IP41) + float(selected_attr.IP42)) / 2
                    )
                    series2.append(float(selected_attr.IPAV4), averagevar)
                    averagevar = float(
                        (float(selected_attr.IP51) + float(selected_attr.IP52)) / 2
                    )
                    series2.append(float(selected_attr.IPAV5), averagevar)
                    # series.append(3.5, 0.6)  # Punto intermedio
                    # series.append(3.5, 0.2)  # Punto intermedio
                    series.append(float(selected_attr.maxRange), 0)  # Punto final
                    series1.append(float(selected_attr.maxRange), 0)  # Punto final
                    series2.append(float(selected_attr.maxRange), 0)  # Punto final

                    chart = QChart()
                    chart.addSeries(series)
                    chart.addSeries(series1)
                    chart.addSeries(series2)
                elif selected_attr.interPoints == 4:
                    series.append(float(selected_attr.IPAV1), float(selected_attr.IP11))
                    series.append(float(selected_attr.IPAV2), float(selected_attr.IP21))
                    series.append(float(selected_attr.IPAV3), float(selected_attr.IP31))
                    series.append(float(selected_attr.IPAV4), float(selected_attr.IP41))
                    series1.append(
                        float(selected_attr.IPAV1), float(selected_attr.IP12)
                    )
                    series1.append(
                        float(selected_attr.IPAV2), float(selected_attr.IP22)
                    )
                    series1.append(
                        float(selected_attr.IPAV3), float(selected_attr.IP32)
                    )
                    series1.append(
                        float(selected_attr.IPAV4), float(selected_attr.IP42)
                    )
                    averagevar = float(
                        (float(selected_attr.IP11) + float(selected_attr.IP12)) / 2
                    )
                    series2.append(float(selected_attr.IPAV1), averagevar)
                    averagevar = float(
                        (float(selected_attr.IP21) + float(selected_attr.IP22)) / 2
                    )
                    series2.append(float(selected_attr.IPAV2), averagevar)
                    averagevar = float(
                        (float(selected_attr.IP31) + float(selected_attr.IP32)) / 2
                    )
                    series2.append(float(selected_attr.IPAV3), averagevar)
                    averagevar = float(
                        (float(selected_attr.IP41) + float(selected_attr.IP42)) / 2
                    )
                    series2.append(float(selected_attr.IPAV4), averagevar)

                    # series.append(3.5, 0.6)  # Punto intermedio
                    # series.append(3.5, 0.2)  # Punto intermedio
                    series.append(float(selected_attr.maxRange), 0)  # Punto final
                    series1.append(float(selected_attr.maxRange), 0)  # Punto final
                    series2.append(float(selected_attr.maxRange), 0)  # Punto final

                    chart = QChart()
                    chart.addSeries(series)
                    chart.addSeries(series1)
                    chart.addSeries(series2)

                elif selected_attr.interPoints == 3:
                    series.append(float(selected_attr.IPAV1), float(selected_attr.IP11))
                    series.append(float(selected_attr.IPAV2), float(selected_attr.IP21))
                    series.append(float(selected_attr.IPAV3), float(selected_attr.IP31))
                    series1.append(
                        float(selected_attr.IPAV1), float(selected_attr.IP12)
                    )
                    series1.append(
                        float(selected_attr.IPAV2), float(selected_attr.IP22)
                    )
                    series1.append(
                        float(selected_attr.IPAV3), float(selected_attr.IP32)
                    )
                    averagevar = float(
                        (float(selected_attr.IP11) + float(selected_attr.IP12)) / 2
                    )
                    series2.append(float(selected_attr.IPAV1), averagevar)
                    averagevar = float(
                        (float(selected_attr.IP21) + float(selected_attr.IP22)) / 2
                    )
                    series2.append(float(selected_attr.IPAV2), averagevar)
                    averagevar = float(
                        (float(selected_attr.IP31) + float(selected_attr.IP32)) / 2
                    )
                    series2.append(float(selected_attr.IPAV3), averagevar)

                    # series.append(3.5, 0.6)  # Punto intermedio
                    # series.append(3.5, 0.2)  # Punto intermedio
                    series.append(float(selected_attr.maxRange), 0)  # Punto final
                    series1.append(float(selected_attr.maxRange), 0)  # Punto final
                    series2.append(float(selected_attr.maxRange), 0)  # Punto final

                    chart = QChart()
                    chart.addSeries(series)
                    chart.addSeries(series1)
                    chart.addSeries(series2)

                elif selected_attr.interPoints == 2:
                    series.append(float(selected_attr.IPAV1), float(selected_attr.IP11))
                    series.append(float(selected_attr.IPAV2), float(selected_attr.IP21))
                    series1.append(
                        float(selected_attr.IPAV1), float(selected_attr.IP12)
                    )
                    series1.append(
                        float(selected_attr.IPAV2), float(selected_attr.IP22)
                    )
                    averagevar = float(
                        (float(selected_attr.IP11) + float(selected_attr.IP12)) / 2
                    )
                    series2.append(float(selected_attr.IPAV1), averagevar)
                    averagevar = float(
                        (float(selected_attr.IP21) + float(selected_attr.IP22)) / 2
                    )
                    series2.append(float(selected_attr.IPAV2), averagevar)

                    # series.append(3.5, 0.6)  # Punto intermedio
                    # series.append(3.5, 0.2)  # Punto intermedio
                    series.append(float(selected_attr.maxRange), 0)  # Punto final
                    series1.append(float(selected_attr.maxRange), 0)  # Punto final
                    series2.append(float(selected_attr.maxRange), 0)  # Punto final

                    chart = QChart()
                    chart.addSeries(series)
                    chart.addSeries(series1)
                    chart.addSeries(series2)
                elif selected_attr.interPoints == 1:
                    series.append(float(selected_attr.IPAV1), float(selected_attr.IP11))
                    series1.append(
                        float(selected_attr.IPAV1), float(selected_attr.IP12)
                    )
                    averagevar = float(
                        (float(selected_attr.IP11) + float(selected_attr.IP12)) / 2
                    )
                    series2.append(float(selected_attr.IPAV1), averagevar)

                    series.append(float(selected_attr.maxRange), 0)  # Punto final
                    series1.append(float(selected_attr.maxRange), 0)  # Punto final
                    series2.append(float(selected_attr.maxRange), 0)  # Punto final

                    chart = QChart()
                    chart.addSeries(series)
                    chart.addSeries(series1)
                    chart.addSeries(series2)
                else:
                    series.append(float(selected_attr.maxRange), 0)  # Punto final
                    chart = QChart()
                    chart.addSeries(series)
            # chart.setTitle("Gráfico de Línea")
            chart.legend().setVisible(False)

            # Crear los ejes X e Y y establecer etiquetas en los puntos
            x_axis = QValueAxis()
            x_axis.setLabelFormat("%.1f")
            x_axis.setTickCount(2)  # Número de etiquetas en el eje X
            x_axis.setRange(
                float(selected_attr.minRange), float(selected_attr.maxRange)
            )

            y_axis = QValueAxis()
            y_axis.setLabelFormat("%.1f")
            y_axis.setTickCount(4)  # Número de etiquetas en el eje Y
            y_axis.setRange(0, 1)

            chart.addAxis(x_axis, Qt.AlignmentFlag.AlignBottom)
            chart.addAxis(y_axis, Qt.AlignmentFlag.AlignLeft)

            series.attachAxis(x_axis)
            series.attachAxis(y_axis)

            chart.setBackgroundBrush(brush)
            chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)

            # Crear la vista del gráfico
            # chart_view = QChartView()
            self.plainTextAVC.setReadOnly(True)
            self.groupBoxVCU.setVisible(True)

            chart_view = ChartView(
                text_X=self.plainTextAVC,
                text_Y=self.plainTextAU,
                posX_1=float(selected_attr.minRange),
                posX_2=float(selected_attr.maxRange),
            )
            chart_view.setChart(chart)
            chart_view.setFrameShape(QFrame.Shape.NoFrame)
            chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)
            chart_view.setBackgroundBrush(brush)

            self.layoutVCU.addWidget(chart_view)
        else:
            self.AttMPVCU.setVisible(False)
            data = []
            valmins = []
            valmaxs = []
            for i in range(1, len(selected_attr.optionsList) + 1):
                variable_name1 = "UP{}1".format(i)
                variable_name2 = "UP{}2".format(i)
                valmins.append(float(getattr(selected_attr, variable_name1)))
                valmaxs.append(float(getattr(selected_attr, variable_name2)))

            for valmin, valmax in zip(valmins, valmaxs):
                data.append((valmin, valmax))

            self.groupBoxVCU.setVisible(False)

            chart_widget = LineBarChartWidget()
            names_chart = NamesChart()
            names_chart.set_connections(selected_attr.optionsList)
            chart_widget.set_data(data)
            # chart_widget.set_connections(selected_attr.optionsList)
            self.clear_layout(self.hLayoutVCU)
            self.clear_layout(self.vLayoutVCU)
            self.layoutVCU = self.hLayoutVCU
            self.vlayoutVCU = self.vLayoutVCU

            self.layoutVCU.addWidget(chart_widget)
            self.vlayoutVCU.addWidget(names_chart)

    # assigns to the QComboBox the value obtained from the cell that has been clicked twice
    def on_item_double_clicked(self, item):
        if isinstance(item, QTableWidgetItem):
            value = item.text()
            self.comboBoxAltNames.setCurrentText(value)


class VentanaModifyAltCon(QMainWindow):
    global alternatives
    global attributes
    global attributesnames

    def __init__(self, parent=None):
        super(VentanaModifyAltCon, self).__init__(parent)
        uic.loadUi("modifyAltCon.ui", self)
        icono = QIcon("iconoUPM.ico")
        super(VentanaModifyAltCon, self).setWindowIcon(icono)
        super(VentanaModifyAltCon, self).setWindowTitle(
            "Modifying alternative consequences for an attribute"
        )
        self.VentanaPrincipalGMAA = parent

        self.pushButtonCancelar.clicked.connect(self.closeM)
        self.pushButtonSaveMAC.clicked.connect(self.save_modAltCon)
        self.tableWidgetMAC.clicked.connect(self.handleCellClick)
        self.tableWidgetMAC.cellClicked.connect(self.handleCellClick)
        # self.tableWidgetMAC.itemChanged.connect(self.handleTableChange)
        self.pushButtonSaveMAC.setEnabled(False)

        num_rows = len(alternatives)
        widthTable = self.tableWidgetANamesMAC.width()
        self.tableWidgetANamesMAC.setRowCount(num_rows)
        self.tableWidgetANamesMAC.setColumnCount(1)
        self.tableWidgetANamesMAC.setColumnWidth(0, widthTable)

        for i, altern in enumerate(alternatives):
            item = QTableWidgetItem(altern.name)
            # item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.tableWidgetANamesMAC.setItem(i, 0, item)

    def save_modAltCon(self):
        global alternatives
        for i, altern in enumerate(alternatives):
            for attr in altern.attr:
                if attr.name == self.textAttributeName.toPlainText():
                    if isinstance(attr, ContinuousAttribute):
                        item1 = self.tableWidgetMAC.item(i, 0)
                        item2 = self.tableWidgetMAC.item(i, 1)
                        value1 = float(item1.text())
                        value2 = float(item2.text())
                        try:
                            if value1 and value2:
                                attr.value1 = value1
                                attr.value2 = value2
                            else:
                                raise ValueError
                        except ValueError:
                            QMessageBox.critical(
                                self.tableWidgetMAC,
                                "Error",
                                "It cannot convert the cell value",
                            )
                    elif isinstance(attr, DiscreteAttribute):
                        combo_box = self.tableWidgetMAC.cellWidget(i, 0)
                        selected_value = combo_box.currentText()
                        attr.selected = selected_value
                        self.pushButtonSaveMAC.setEnabled(True)

        self.close()
        # self.vNI = VentanaNodeInfo()
        # self.vNI.show()

    def handleCellClick(self):
        self.pushButtonSaveMAC.setEnabled(True)

    def closeM(self):
        self.close()
        # self.vNI = VentanaNodeInfo()
        # self.vNI.show()


class VentanaNodeInfo(QMainWindow):
    def __init__(self, parent=None):
        super(VentanaNodeInfo, self).__init__(parent)
        uic.loadUi("nodeInformation.ui", self)
        icono = QIcon("iconoUPM.ico")
        super(VentanaNodeInfo, self).setWindowIcon(icono)
        super(VentanaNodeInfo, self).setWindowTitle("Node Information")
        self.VentanaPrincipalGMAA = parent

        self.max_length = 15  # maximum number of char

        # button signals
        # self.radioBAverageVAC.toggled.connect(self.min_alt)
        # self.radioBMaximumVAC.toggled.connect(self.ave_alt)
        # self.radioBMinimumVAC.toggled.connect(self.max_alt)
        self.buttonCancel.clicked.connect(self.close_windowNI)
        self.textLabel.textChanged.connect(self.update_label)
        # self.textUnits.textChanged.connect(self.update_label)
        # self.textMinRange.textChanged.connect(self.update_label)
        # self.textMaxRange.textChanged.connect(self.update_label)
        self.textName.textChanged.connect(self.update_label)
        self.buttonEnter.clicked.connect(self.create_table)
        self.textDescription.textChanged.connect(self.update_label)
        self.buttonApply.setEnabled(True)
        # self.buttonOk.clicked.connect(lambda: self.ok_button_clicked(self.sender()))
        self.spinBoxDiscrete.valueChanged.connect(lambda: self.onValueChanged)

        self.radioBCont.toggled.connect(self.disable_discrete)
        self.radioBDisc.toggled.connect(self.disable_continuous)

        # Hide or show Save and Cancel Buttons
        self.tabWidgetNI.currentChanged.connect(self.update_buttons)

        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)

        # self.textDescription.textChanged.connect(self.onTextChanged)
        # self.textLabel.textChanged.connect(self.onTextChanged)

        # self.textDescCont.textChanged.connect(self.onTextChanged)
        # self.textUnitsCont.textChanged.connect(self.onTextChanged)
        # self.textMinRangeCont.textChanged.connect(self.onTextChanged)
        # self.textMaxRangeCont.textChanged.connect(self.onTextChanged)
        # self.textDescDisc.textChanged.connect(self.onTextChanged)
        # self.textName.textChanged.connect(self.onTextChanged)

    # def min_alt(self):
    #     self.tableWidgetVAC.clear()

    # def ave_alt(self):
    #     self.tableWidgetVAC.clear()

    # def max_alt(self):
    #     self.tableWidgetVAC.clear()

    def update_buttons(self, index):
        # Comprobamos qué pestaña está activa y mostramos/ocultamos los botones
        current_tab_name = self.tabWidgetNI.tabText(index)
        if current_tab_name == "Leaf Information":
            self.buttonApply.show()
            self.buttonCancel.show()
            self.buttonNext.hide()
        elif current_tab_name == "Leaf Attribute":
            self.buttonApply.show()
            self.buttonCancel.show()
            self.buttonNext.hide()
        elif current_tab_name == "Viewing Component Utilities":
            self.buttonApply.hide()
            self.buttonCancel.hide()
            self.buttonNext.hide()
        elif current_tab_name == "Viewing Alternative Consequences":
            self.buttonApply.hide()
            self.buttonCancel.hide()
            self.buttonNext.hide()
        elif current_tab_name == "Subjective Scale":
            self.buttonApply.hide()
            self.buttonCancel.hide()
            self.buttonNext.hide()
        elif current_tab_name == "Weight Elicitation":
            self.buttonApply.show()
            self.buttonCancel.show()
            self.buttonNext.hide()
        elif current_tab_name == "Quantifying Preferences":
            self.buttonApply.hide()
            self.buttonCancel.hide()
            self.buttonNext.show()
        elif current_tab_name == "Viewing Weights":
            self.buttonApply.hide()
            self.buttonCancel.hide()
            self.buttonNext.hide()
        elif current_tab_name == "Viewing Stability Intervals":
            self.buttonApply.hide()
            self.buttonCancel.hide()
            self.buttonNext.hide()
        else:
            pass

    def update_label(self):
        self.buttonApply.setEnabled(False)
        self.textLabel.toPlainText()
        # self.parent().labels[identifier_labels-1].setText(text)

    def create_table(self):
        # Get number of rows
        self.buttonApply.setEnabled(True)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowStaysOnTopHint)
        self.show()
        reply = QMessageBox.warning(
            self.parent(),
            f"Modify Discrete Attribute",
            f"Are you sure you want to modify the options?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)
            self.show()
            num_rows = self.spinBoxDiscrete.value()
            # Create table with number of rows and two columns
            widthTable = self.tableDiscrete.width()
            self.tableDiscrete.setRowCount(num_rows)
            self.tableDiscrete.setColumnCount(1)
            self.tableDiscrete.setColumnWidth(0, widthTable)
            self.tableDiscrete.setHorizontalHeaderLabels(["Attributes"])

            # self.tableDiscrete.setColumnWidth(1, self.tableDiscrete.columnWidth(1) // 16)

            # Adding elements to the table
            for i in range(num_rows):
                # Add text in the first column
                item = QTableWidgetItem(f"Attribute {i+1}")
                self.tableDiscrete.setItem(i, 0, item)

                # Add option in second column
                # radio_button = QRadioButton()
                # radio_button.setObjectName(str(i))
                # self.tableDiscrete.setCellWidget(i, 1, radio_button)
                # self.tableDiscrete.cellWidget(i, 1).setStyleSheet('margin-left: 10px;')

            # Select default option in the first row
            # first_radio_button = self.tableDiscrete.cellWidget(0, 1)
            # first_radio_button.setChecked(True)

        else:
            self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)
            self.show()
            pass

    def disable_discrete(self, state):
        # self.continu
        if state:
            self.textDescDisc.setEnabled(False)
            self.spinBoxDiscrete.setEnabled(False)
            self.buttonEnter.setEnabled(False)
            self.tableDiscrete.setEnabled(False)
        else:
            self.textDescDisc.setEnabled(True)
            self.spinBoxDiscrete.setEnabled(True)
            self.buttonEnter.setEnabled(True)
            self.tableDiscrete.setEnabled(True)

    def disable_continuous(self, state):
        if state:
            self.textDescCont.setEnabled(False)
            self.textUnitsCont.setEnabled(False)
            self.textMinRangeCont.setEnabled(False)
            self.textMaxRangeCont.setEnabled(False)
        else:
            self.textDescCont.setEnabled(True)
            self.textUnitsCont.setEnabled(True)
            self.textMinRangeCont.setEnabled(True)
            self.textMaxRangeCont.setEnabled(True)

    def onValueChanged(self):
        # Verificar si el valor del QSpinBox es mayor que cero
        if self.spinBoxDiscrete.value() > 0:
            # Habilitar el QPushButton
            self.buttonEnter.setEnabled(True)
        else:
            # Deshabilitar el QPushButton
            self.buttonEnter.setEnabled(False)

    # def onTextChanged(self):
    #     self.buttonApply.setEnabled(True)
    #     self.textDescription.setPlainText(self.textDescription.toPlainText())
    #     self.textLabel.setPlainText(self.textLabel.toPlainText())

    #     self.textDescCont.setPlainText(self.textDescCont.toPlainText())
    #     self.textUnitsCont.setPlainText(self.textUnitsCont.toPlainText())
    #     self.textMinRangeCont.setPlainText(self.textMinRangeCont.toPlainText())
    #     self.textMaxRangeCont.setPlainText(self.textMaxRangeCont.toPlainText())
    #     self.textDescDisc.setPlainText(self.textDescDisc.toPlainText())
    #     self.textName.setPlainText(self.textName.toPlainText())

    def close_windowNI(self):
        self.close()


class LabelNode(QLabel):
    # connect signals
    double_clicked = pyqtSignal()
    _first_created = False

    def __init__(
        self, identifier, text, label_name, posArray, cRow, cColumn, parent=None
    ):
        super().__init__(text, parent)
        global PrimaryObjective
        PrimaryObjective = True
        # self.parent = self.parent()
        # Mouse Tracking
        self.setMouseTracking(True)
        self.setObjectName("Node")
        self.clicked = False
        self.identifier = identifier
        self.label_name = label_name
        self.posArray = posArray
        # print(f"P: Parent: {parent.parent}")

        # parent, connections and weights
        self.padre = None
        self.connections = (
            []
        )  # this are connections between nodes to know which ones are related
        self.finalNode = True  # we make sure it is a final node
        self.weightI = 1  # default values
        self.weightS = 1

        #  also have cRow, cColumn and sons so that when a child is created it will be in the next column but in the same row as its ancestor.
        self.cRow = cRow
        self.cColumn = cColumn

        # tipe of the node

        self.nodeDescription = ""

        # tipe of the unit

        self.unitType = ""
        self.unitDescription = ""
        self.unitName = ""
        self.minRange = 0
        self.maxRange = 1
        self.mostPrefered = ""
        # self.optionDiscrete = ""
        self.optionsList = []

        self.interPoints = 0

        self.IP11 = 0
        self.IP12 = 0
        self.IP21 = 0
        self.IP22 = 0
        self.IP31 = 0
        self.IP32 = 0
        self.IP41 = 0
        self.IP42 = 0
        self.IP51 = 0
        self.IP52 = 0
        self.IPAV1 = 0
        self.IPAV2 = 0
        self.IPAV3 = 0
        self.IPAV4 = 0
        self.IPAV5 = 0

        # Generar variables UP11, UP12, UP21, UP22, ..., UP9
        for i in range(1, 51):  # Generar números del 1 al 10
            for j in range(1, 3):  # Generar números del 1 al 2
                setattr(self, f"UP{i}{j}", None)

        # connections between labels
        # self.connections = []

        if not LabelNode._first_created:
            LabelNode._first_created = True
            self._active = True
        else:
            self._active = False

        self.setGeometry(130, 210, 131, 41)
        self.setMinimumSize(131, 41)
        self.setMaximumSize(131, 41)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setFrameShape(QLabel.Shape.Box)
        self.setFrameShadow(QLabel.Shadow.Sunken)
        if PrimaryObjective == False:
            self.setStyleSheet(
                "background-color: #AAA8A8; border-radius: 6px; border: 1px solid #7CEE69;"
            )
        else:
            self.setStyleSheet(
                "background-color: #AAA8A8; border-radius: 6px; border: 1px solid #1F1F1F;"
            )
        self.setText(text)
        # We can name the PO Label
        # self.setObjectName("Primary Objective Label")
        self.show()

        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.showContextMenu)

    def add_connection(self, label):
        self.connections.append(label)

    def remove_connection(self, label):
        if label in self.connections:
            self.connections.remove(label)
            if len(self.connections) == 0:
                self.finalNode = True
                self.changeStyleSheet()

    def count_parents(self, node):
        if node.padre is None:
            # Si el padre es None, hemos llegado al nodo raíz
            return 0
        else:
            # Si no es None, hay un padre y contamos también ese nodo
            return 1 + self.count_parents(node.padre)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        self.clicked = True
        self.offset = event.pos()

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if self.clicked:
            self.move(self.mapToParent(event.pos() - self.offset))
            event.accept()

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        self.clicked = False

    def mouseDoubleClickEvent(self, event):
        self.double_clicked.emit()
        # self.textChanged.emit(self.text())

    def showContextMenu(self, pos):
        global Leaf
        global identifier_labels

        menu = QMenu()
        if self.identifier == 0:
            action_name = QAction(f"Name: {self.label_name}", self)
            action_label = QAction(f"Label: {self.text()}", self)
            action_createSon = QAction("Create a son", self)

            action_createSon.triggered.connect(self.create_sonPO)
            delete_action = QAction("Delete", self)
            delete_action.triggered.connect(self.deleteLabelPO)
            menu.addAction(action_name)
            menu.addAction(action_label)
            menu.addSeparator()
            menu.addAction(action_createSon)
            menu.addAction(delete_action)
            menu.exec(self.mapToGlobal(pos))
        else:
            action_name = QAction("Name: " + str(self.text()), self)
            action_label = QAction("Label: " + str(self.label_name), self)
            print("P: Number of Leaf now: " + str(Leaf))
            action_createSon = QAction("Create a son", self)

            action_createSon.triggered.connect(self.create_son)
            delete_action = QAction("Delete", self)
            delete_action.triggered.connect(self.deleteLabelSon)
            # stylesheet_action = QAction("Final node")
            # stylesheet_action.triggered.connect(self.changeStyleSheet)
            menu.addAction(action_name)
            menu.addAction(action_label)
            menu.addSeparator()
            menu.addAction(action_createSon)
            menu.addAction(delete_action)
            menu.addSeparator()
            # menu.addAction(stylesheet_action)
            menu.exec(self.mapToGlobal(pos))

    # def to_xml(self):
    #     element = ET.Element("Node")
    #     element.set("text", self.text())
    #     element.set("x", str(self.pos().x()))
    #     element.set("y", str(self.pos().y()))
    #     element.set("width", str(self.size().width()))
    #     element.set("height", str(self.size().height()))
    #     element.set("id",str(self.identifier))
    #     element.set("label_name",self.label_name)
    #     psArray = str(self.posArray)
    #     element.set("posArray",psArray)
    #     return element

    # function I need to fix

    def create_sonPO(self):
        global Leaf
        global Branch
        global identifier_labels
        global PrimaryObjective
        global currentColumn
        global currentRow
        global attributesnames
        attributesnames.clear()
        PrimaryObjective = True
        parent = self.parent()

        number_connection = len(parent.parent.labels[0].connections)
        numColumn = 0

        numColumn = 20 * number_connection

        parent.parent.actionViewComponentUtilities.setEnabled(True)
        parent.parent.actionAltConsequences.setEnabled(True)
        parent.parent.actionViewTotalWeights.setEnabled(True)

        labelLE = LabelNode(
            identifier=identifier_labels,
            text="Label" + str(identifier_labels),
            label_name="Label" + str(identifier_labels),
            posArray=len(parent.parent.labels),
            cRow=numColumn,
            cColumn=2,
        )
        labelLE.padre = parent.parent.labels[0]
        labelLE.finalNode = True
        labelLE.changeStyleSheet()
        identifier_labels += 1
        parent.parent.labels.append(labelLE)
        # self.layout.getItemPosition(self.layout.indexOf(self.labels[identifier_labels-2]))
        print(f"P: Number of Labels: {len(parent.parent.labels)}")
        # print(f"P: Nodes Identifier is {labelLE.identifier}")
        Leaf = Leaf + 1
        labelLE.setVisible(True)
        labelLE.setFixedSize(120, 40)

        parent.parent.layout.addWidget(labelLE, numColumn, 2)
        currentColumn += 1
        Branch += 1
        sonsPO = parent.parent.labels[0]
        print(f"P: Tipo de Objeto: {sonsPO}")
        sonsPO.add_connection(labelLE)

        print(f"P: Numero de conexiones padre: {number_connection}")

        print("P: Number of Labels: " + str(len(parent.parent.labels)))
        labelLE.double_clicked.connect(parent.parent.open_NodeInfo)
        divisor = len(sonsPO.connections)
        for connection in sonsPO.connections:
            connection.weightI = 1 / divisor  # default value
            connection.weightS = 1 / divisor  # default value

        central_pos = math.floor(currentRow / 2)
        parent.parent.layout.addWidget(parent.parent.labels[0], central_pos - 1, 0)
        parent.parent.layout.update()
        self.create_lines_layout()
        self.getFinalAttributes(parent.parent.labels)

    def create_son(self):
        global Leaf
        global Branch
        global identifier_labels
        global PrimaryObjective
        global currentColumn
        global currentRow
        global attributesnames
        attributesnames.clear()
        PrimaryObjective = True
        parent = self.parent()
        try:
            labelAnc = parent.parent.labels[self.posArray]
            posA = len(labelAnc.connections)

            # we do this loop to find out the number of children that have been previously introduced.
            father = labelAnc.padre
            children = father.connections
            childsB = 0
            hijosAnt = 0
            labelItem = None
            for child in children:
                if not (child.padre == parent.parent.labels[0]):
                    if child == labelAnc:
                        break
                    else:
                        hijosAnt += 1
                        childsB += len(child.connections)
                        print(f"P: child.connections: {child.connections}")

            labelAnc.finalNode = False
            labelAnc.changeStyleSheet()
            rowS = 0
            if self.count_parents(labelAnc) == 1:
                posA *= 2
                rowS = labelAnc.cRow + posA  # le suma el número de hijos que tiene
                print(f"posA: {posA}")
            else:
                posA *= 1
                print(f"Entra en el else")
                for i in range(labelAnc.cRow, 10000000):
                    # print(f"i: {i}")
                    labelItem = parent.parent.layout.itemAtPosition(
                        i, labelAnc.cColumn + 2
                    )
                    print(f"label widget: {labelItem}")
                    if not labelItem:
                        rowS = i
                        # print(f"i: {i}")
                        break

            # place the QLabels according to the number of children of the ancestor node
            print(f"P: Generación labelAnc: {posA}")

            # print(f"widget: {widget}")

            print(
                f"labelAnc.cRow = {labelAnc.cRow}, posA = {posA}, childsB = {childsB}"
            )

            print(f"P: rowS: {rowS}")

            labelLE = LabelNode(
                identifier=identifier_labels,
                text="Label" + str(identifier_labels),
                label_name="Label" + str(identifier_labels),
                posArray=len(parent.parent.labels),
                cRow=rowS,
                cColumn=labelAnc.cColumn + 2,
            )

            labelLE.padre = labelAnc
            labelLE.finalNode = True
            labelLE.changeStyleSheet()

            res = self.count_parents(labelLE)
            print(f"P: Generación labelLE: {res}")

            identifier_labels += 1
            # labelLE.posArray = len(parent.parent.labels)
            parent.parent.labels.append(labelLE)
            # self.layout.getItemPosition(self.layout.indexOf(self.labels[identifier_labels-2]))
            print("P: Number of Labels: " + str(len(parent.parent.labels)))
            # print(f"P: Nodes Identifier is {labelLE.identifier}")
            Leaf = Leaf + 1
            labelLE.setVisible(True)
            labelLE.setFixedSize(120, 40)

            widget = parent.parent.layout.itemAtPosition(labelLE.cRow, labelLE.cColumn)
            if widget is None:
                parent.parent.layout.addWidget(labelLE, labelLE.cRow, labelLE.cColumn)
            else:
                labelLE.cRow += 1
                parent.parent.layout.addWidget(labelLE, labelLE.cRow, labelLE.cColumn)

            # prueba para ver si está ocupada una posición del layout

            # widget = parent.parent.layout.itemAtPosition(labelLE.cRow,labelLE.cColumn)
            # if widget is None:
            #     print("La posición de labelLE está vacía")
            # else:
            #     print("La posición labelLE está ocupada")

            currentColumn += 1

            labelAnc.add_connection(labelLE)
            labelAnc = parent.parent.labels[self.posArray]
            labelLE.double_clicked.connect(parent.parent.open_NodeInfo)
            print(f"P: Número de hijos del nodo anterior: {len(labelAnc.connections)}")
            for connection in labelAnc.connections:
                connection.weightI = 1 / len(labelAnc.connections)  # default value
                connection.weightS = 1 / len(labelAnc.connections)  # default value

            self.create_lines_layout()
            self.getFinalAttributes(parent.parent.labels)
        except RuntimeError:
            traceback.print_exc()
            pass

    # returns the final Nodes attributes

    def getFinalAttributes(self, finalNodes):
        global attributes
        global attributesnames
        attributes.clear()
        attributesnames.clear()
        for node in finalNodes:
            node.finalNode = False
            if not node.connections:
                node.finalNode = True
                attributes.append(node)
                attributesnames.append(node.text())

    def create_lines_layout(self):
        parent = self.parent()

        for line in parent.parent.lineB:
            try:
                line.deleteLater()
                # parent.parent.lineB.pop(line)
            except:
                traceback.print_exc()
                pass

        for line in parent.parent.lines:
            try:
                line.deleteLater()
                # parent.parent.lines.pop(line)

            except:
                traceback.print_exc()
                pass
            # parent.parent.layout.removeWidget(line)
        if not parent.parent.labels:
            return

        labelPO = parent.parent.labels[0]
        if labelPO is not None and labelPO.connections:
            connection_listPO = labelPO.connections
            for k in range(len(connection_listPO)):
                if k == 0:
                    line = DLineFrameB()
                    parent.parent.layout.addWidget(line, 0, 1, 3, 1)
                    line.lower()
                    parent.parent.lineB.append(line)

                else:
                    numero = k * 20
                    connection = connection_listPO[k]
                    line = DLineFrame(
                        dRow=labelPO.cRow,
                        dColumn=connection.cColumn - 1,
                        dNum=numero - 1,
                    )
                    line.dRow = labelPO.cRow
                    line.dColumn = connection.cColumn - 1
                    line.dNum = numero - 1
                    parent.parent.layout.addWidget(
                        line, line.dRow, line.dColumn, line.dNum, 2
                    )
                    line.lower()
                    parent.parent.lines.append(line)

        for i in range(1, len(parent.parent.labels)):
            label = parent.parent.labels[i]
            # countParent = self.count_parents(label)
            # if countParent == 1:
            #     mulS = 45
            # elif countParent == 2:
            #     mulS = 11
            # elif countParent == 3:
            #     mulS = 2
            # else:
            #     mulS = 1
            if label.connections:
                for k, connection in enumerate(label.connections):
                    if (k == 0) and (label.cRow == connection.cRow):
                        line = HLineFrame()
                        parent.parent.layout.addWidget(
                            line, label.cRow, connection.cColumn - 1, 1, 2
                        )
                        line.lower()
                        parent.parent.lines.append(line)
                    else:
                        numero = connection.cRow - label.cRow
                        line = DLineFrame(
                            dRow=label.cRow,
                            dColumn=connection.cColumn - 1,
                            dNum=numero - 1,
                        )
                        line.dRow = label.cRow
                        line.dColumn = connection.cColumn - 1
                        line.dNum = numero - 1
                        parent.parent.layout.addWidget(
                            line, line.dRow, line.dColumn, line.dNum + 2, 2
                        )
                        line.lower()
                        parent.parent.lines.append(line)
                parent.parent.layout.update()

    def deleteLabelPO(self):
        global PrimaryObjective
        global currentColumn
        global currentRow
        global Branch
        global identifier_labels
        global Leaf
        global attributes
        global alternatives
        global attributesnames
        attributesnames.clear()

        parent = self.parent()
        self.create_lines_layout()

        reply = QMessageBox.warning(
            self.parent(),
            "Delete Overall Objetive",
            "Are you sure you want to delete the Overall Objective? If you delete it, all other elements will be deleted.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.No:
            pass
        elif reply == QMessageBox.StandardButton.Yes:
            for child in parent.children():
                if isinstance(child, QLabel):
                    child.deleteLater()
            parent.parent.labels.clear()
            PrimaryObjective = False
            Branch = 0
            Leaf = 0  # if the delete button of the PO Label is triggered the num of Leaf is 0
            identifier_labels = 0
            currentRow = 0
            currentColumn = 0
            attributes.clear()
            alternatives.clear()
            attributesnames.clear()
            parent.parent.actionSaveWorkspace.setEnabled(False)
            parent.parent.actionSave_WorkSpace.setEnabled(False)
            parent.parent.actionSave_WorkSpace_As.setEnabled(False)

            print(parent.parent.labels)
            self.create_lines_layout()

        self.create_lines_layout()
        self.getFinalAttributes(parent.parent.labels)

    # recursive method for subtracting -20 from each row in each label

    def update_cRow(self, label):
        global attributes
        global alternatives
        global attributesnames
        attributesnames.clear()
        parent = self.parent()
        self.create_lines_layout()
        for conn in label.connections:
            conn.cRow -= 20
            parent.parent.layout.addWidget(conn, conn.cRow, conn.cColumn)
            parent.parent.layout.update()
            self.update_cRow(conn)
        self.create_lines_layout()
        self.getFinalAttributes(parent.parent.labels)

    # def update_cRow(self,label):
    #     stack = [label]
    #     while stack:
    #         node = stack.pop()
    #         for conn in node.connections:
    #             conn.cRow -= 20
    #             stack.append(conn)

    def deleteLabelSon(self):
        global PrimaryObjective
        global currentColumn
        global currentRow
        global Branch
        global identifier_labels
        global Leaf
        global attributes
        global alternatives
        global attributesnames
        attributesnames.clear()

        parent = self.parent()

        label_remove = parent.findChildren(QLabel, self.objectName())[self.posArray]

        self.create_lines_layout()

        if not label_remove.connections:
            reply = QMessageBox.warning(
                self.parent(),
                f"Delete Leaf {label_remove.label_name}",
                f"Are you sure you want to delete {label_remove.label_name}?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No,
            )
        else:
            reply = QMessageBox.warning(
                self.parent(),
                f"Delete Intermediate Node {label_remove.label_name}",
                f"Are you sure you want to delete {label_remove.label_name}? If you delete it, all the connected elements to {label_remove.label_name} will be deleted.",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No,
            )

        if reply == QMessageBox.StandardButton.No:
            pass
        else:

            # with these loops I want to subtract -20 from all subsequent rows

            found_index = None
            for i, label in enumerate(parent.parent.labels[0].connections):
                if label.text() == label_remove.text():
                    found_index = i
                    break

            if found_index is not None:
                for label in parent.parent.labels[0].connections[found_index + 1 :]:
                    if label.connections:
                        label.cRow -= 20
                        self.update_cRow(label)
                    else:
                        label.cRow -= 20

            for label in parent.parent.labels:
                parent.parent.layout.addWidget(label, label.cRow, label.cColumn)
                parent.parent.layout.update()

            self.create_lines_layout()

            print(f"P: {parent.parent.labels}")
            print(f"P: Label: {label_remove}")

            print(f"P: El QLabel a eliminar es: {label_remove.label_name}")
            if len(label_remove.connections) == 0:
                if label_remove is not None:
                    # I do this to delete the connection with the ancestor since deleting the child is not enough
                    for labelRC in parent.parent.labels:
                        # create a copy of the array before iterating over it
                        labelRC.remove_connection(label_remove)

                    parent.parent.labels.pop(self.posArray)
                    label_remove.deleteLater()
                    # parent.parent.labels[self.identifier] = None
                    print(f"P: ID del Label: {self.identifier}")
                    for i in range(self.posArray, len(parent.parent.labels)):
                        parent.parent.labels[i].posArray = i

                    print("P: Accede a len(label_remove.connections) == 0")
                    # print(parent.parent.labels)

            else:
                label_remove.remove_label(label_remove)

        print(f"P: {parent.parent.labels}")

        self.create_lines_layout()
        self.getFinalAttributes(parent.parent.labels)

    def remove_label(self, label):
        # Buscar todos los QLabel conectados a este QLabel
        for connected_label in set(label.connections):

            # Eliminar los QLabel conectados de forma recursiva
            self.remove_label(connected_label)

        # Eliminar el QLabel
        parent = self.parent()
        parent.parent.labels.pop(self.posArray)
        for labelRC in parent.parent.labels:
            # create a copy of the array before iterating over it
            labelRC.remove_connection(label)
        # self.connections.remove(label)
        label.deleteLater()
        # del label
        for i in range(self.posArray, len(parent.parent.labels)):
            parent.parent.labels[i].posArray = i

        self.create_lines_layout()
        self.getFinalAttributes(parent.parent.labels)

    # for every new node that is created dynamically

    def changeStyleSheet(self):
        if self.finalNode:
            self.setStyleSheet(
                "background-color: #AAA8A8; border-radius: 6px; border: 1px solid #7CEE69;"
            )
        else:
            self.setStyleSheet(
                "background-color: #AAA8A8; border-radius: 6px; border: 1px solid #1F1F1F;"
            )

    # when we import a new project so that every final node is marked

    def __repr__(self):
        return f"LabelNode({self.text()})"


# class InitialOptionLabels(QPushButton):
#     def __init__(self,text):
#         super().__init__(text)
#         self.setGeometry(130, 210, 101, 21)
#         self.setMinimumSize(131,21)
#         self.setMaximumSize(131,21)
#         self.setText(text)
#         self.setStyleSheet(
#             "background-color: #AAA8A8; border-radius: 6px; border: 1px solid #1F1F1F;")
#         self.show()


class ChartView(QChartView):
    def __init__(self, text_X, text_Y, posX_1, posX_2):
        super().__init__()
        self.chart = None  # El gráfico se establecerá más adelante
        self.text_X = text_X
        self.text_Y = text_Y
        self.posX_1 = posX_1
        self.posX_2 = posX_2

    def setChart(self, chart):
        self.chart = chart
        super().setChart(chart)

    def mouseMoveEvent(self, event):
        pos = event.pos()
        pos_chart = self.mapToScene(pos)
        if self.chart:
            x_value = self.chart.mapToValue(pos_chart).x()
            y_value = self.chart.mapToValue(pos_chart).y()
            if x_value <= self.posX_1:
                self.text_X.setPlainText(f"{self.posX_1: .2f}")
            elif x_value >= self.posX_2:
                self.text_X.setPlainText(f"{self.posX_2: .2f}")
            else:
                self.text_X.setPlainText(f"{x_value: .2f}")

            if y_value <= 0:
                self.text_Y.setPlainText(f"{0.00: .2f}")
            elif y_value >= 1:
                self.text_Y.setPlainText(f"{1.00: .2f}")
            else:
                self.text_Y.setPlainText(f"{y_value: .2f}")

        super().mouseMoveEvent(event)


class NamesChart(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.connections = []
        self.spacing = 10  # Espacio entre cada barra

    def set_connections(self, connections):
        self.connections = connections
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        try:
            total_bars = len(self.connections)
            total_spacing = (total_bars - 1) * self.spacing
            bar_width = (self.width() - total_spacing) / total_bars

            font = QFont("Neue Haas Grotesk Text Pro Extr", 11)
            painter.setFont(font)

            label_height = (
                self.height() - 30
            )  # Posición vertical para las etiquetas en el eje X

            for i, connection_name in enumerate(self.connections):
                x = int(i * (bar_width + self.spacing) + 10)
                y = label_height
                painter.drawText(
                    QRectF(x, y, bar_width, 20),
                    Qt.AlignmentFlag.AlignCenter,
                    connection_name,
                )
        except ZeroDivisionError:
            traceback.print_exc()
            pass


class LineBarChartWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.data = []  # Pares de valores Y para cada barra
        self.connections = []
        self.spacing = 10  # Espacio entre cada barra

    def set_data(self, data):
        self.data = data
        self.update()  # Actualizamos el widget cuando se establecen nuevos datos

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Dibujar ejes
        try:
            total_bars = len(self.data)
            total_spacing = (total_bars - 1) * self.spacing
            bar_width = (self.width() - total_spacing) / total_bars

            font = QFont("Neue Haas Grotesk Text Pro Extr", 11)
            painter.setFont(font)

            # Dibujar líneas verticales y etiquetas de valores
            for i, (start_y, end_y) in enumerate(self.data):
                x = i * (bar_width + self.spacing) + 70
                y_start = round((1 - start_y) * self.height())
                y_end = round((1 - end_y) * self.height())

                # Dibujar línea vertical
                pen = QPen(QColor(0, 0, 0))  # Color negro
                pen.setWidth(1)
                painter.setPen(pen)
                painter.drawLine(round(x), round(y_start), round(x), round(y_end))

                # pen.setWidth(1)
                # painter.setPen(pen)
                # painter.drawLine(round(x), self.height()-50, round(x), self.height()-60)

                # Dibujar etiquetas
                mean_value = (start_y + end_y) / 2
                mean_y = round((1 - mean_value) * self.height())

                pen.setWidth(1)
                painter.setPen(pen)

                line_start_x = x - 5
                line_end_x = x + 5
                painter.drawLine(
                    round(line_start_x),
                    round(y_start),
                    round(line_end_x),
                    round(y_start),
                )
                painter.drawLine(
                    round(line_start_x), round(y_end), round(line_end_x), round(y_end)
                )
                painter.drawLine(
                    round(line_start_x), round(mean_y), round(line_end_x), round(mean_y)
                )

                # Etiqueta de la media de la barra
                print(f"start_y {start_y}")
                if start_y == 0.0:
                    value_label_start = "{:.2f}".format(start_y)
                    painter.drawText(
                        QRectF(line_end_x + 5, y_start - 20, 50, 20),
                        Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter,
                        value_label_start,
                    )
                else:
                    value_label_start = "{:.2f}".format(start_y)
                    painter.drawText(
                        QRectF(line_end_x + 5, y_start - 10, 50, 20),
                        Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter,
                        value_label_start,
                    )

                # Etiqueta de la media de la barra
                value_label_mean = "{:.2f}".format(mean_value)
                painter.drawText(
                    QRectF(line_end_x + 5, mean_y - 10, 50, 20),
                    Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter,
                    value_label_mean,
                )

                # Etiqueta del intervalo abajo
                print(f"end_y {end_y}")

                if end_y == 1.0:
                    value_label_end = "{:.2f}".format(end_y)
                    painter.drawText(
                        QRectF(line_end_x + 5, y_end, 50, 20),
                        Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter,
                        value_label_end,
                    )
                else:
                    value_label_end = "{:.2f}".format(end_y)
                    painter.drawText(
                        QRectF(line_end_x + 5, y_end - 10, 50, 20),
                        Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter,
                        value_label_end,
                    )

            # Dibujar etiquetas de conexiones
            font = QFont("Neue Haas Grotesk Text Pro Extr", 10)
            painter.setFont(font)
            for i, bar_name in enumerate(self.connections):
                x = i * (bar_width + self.spacing)
                painter.drawText(
                    QRectF(x, self.height() + 40, bar_width, 20),
                    Qt.AlignmentFlag.AlignCenter,
                    bar_name,
                )
        except ZeroDivisionError:
            traceback.print_exc()
            pass


class BarChartWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # self.data = [(0.4, 0.6), (0.5, 0.7), (0.5, 0.7), (0.3, 0.4), (0.2, 0.7)]  # Pares de valores Y para cada barra
        self.data = []  # Pares de valores Y para cada barra
        self.spacing = 10  # Espacio entre cada barra

    def set_data(self, data):
        self.data = data
        self.update()  # Actualizamos el widget cuando se establecen nuevos datos

    # def set_connections(self, connections):
    #     self.connections = []
    #     for con in connections:
    #         self.connections.append(con.text())
    #     self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        font = QFont("Neue Haas Grotesk Text Pro Extr", 9)
        painter.setFont(font)

        total_width = self.width()
        total_bars = len(self.data)
        total_spacing = (total_bars - 1) * self.spacing
        bar_width = (total_width - total_spacing) / total_bars
        max_bar_width_ratio = (
            0.7  # Relación de ancho máximo de las barras con el espacio disponible
        )
        min_bar_width_ratio = (
            0.2  # Relación de ancho mínimo de las barras con el espacio disponible
        )

        # Dibujar ejes
        # painter.drawLine(0, self.height(), self.width(), self.height())  # Eje X
        # painter.drawLine(0, 0, 0, self.height())  # Eje Y

        # Dibujar marcas en el eje Y y etiquetas de valores
        for y in range(0, 11, 1):
            y_value = y / 10
            y_pos = round((1 - y_value) * self.height())
            painter.drawLine(0, y_pos, 10, y_pos)  # Marca en el eje lateral
            painter.drawText(
                QRectF(7, y_pos, 22, 20), Qt.AlignmentFlag.AlignRight, str(y_value)
            )  # Etiqueta en el eje lateral

        # Dibujar barras y etiquetas de valores al lado de cada barra
        for i, (start_y, end_y) in enumerate(self.data):
            bar_height = (end_y - start_y) * self.height()
            x = i * (bar_width + self.spacing)
            y = round((1 - end_y) * self.height())
            bar_width_ratio = max(
                min_bar_width_ratio, min(max_bar_width_ratio, bar_width / total_width)
            )  # Ajuste de ancho de la barra

            bar_width_actual = bar_width * bar_width_ratio
            bar_offset = (bar_width - bar_width_actual) / 2

            bar_rect = QRectF(x + bar_offset, y, bar_width_actual, bar_height).toRect()
            bar_color = QColor(200, 200, 255)  # Color azul claro
            painter.fillRect(bar_rect, bar_color)

            # Etiqueta de valor arriba de la barra
            value_label_top = "{:.2f}".format(end_y)
            painter.drawText(
                QRectF(x, y - 20, bar_width, 20),
                Qt.AlignmentFlag.AlignCenter,
                value_label_top,
            )

            # Etiqueta de valor abajo de la barra
            value_label_bottom = "{:.2f}".format(start_y)
            painter.drawText(
                QRectF(x, y + bar_height, bar_width, 20),
                Qt.AlignmentFlag.AlignCenter,
                value_label_bottom,
            )

            # Línea que representa la media de la barra
            mean_value = (start_y + end_y) / 2
            mean_y = round((1 - mean_value) * self.height())

            pen = QPen(QColor(0, 0, 0))  # Color negro
            pen.setWidth(2)
            painter.setPen(pen)

            line_start_x = x + bar_offset
            line_end_x = x + bar_offset + bar_width_actual
            painter.drawLine(
                round(line_start_x), round(mean_y), round(line_end_x), round(mean_y)
            )

            # Etiqueta de la media de la barra
            value_label_mean = "{:.2f}".format(mean_value)
            painter.drawText(
                QRectF(line_end_x + 5, mean_y - 10, 50, 20),
                Qt.AlignmentFlag.AlignLeft,
                value_label_mean,
            )

            # if i < len(self.connections):
            #     bar_name = self.connections[i]
            #     painter.drawText(QRectF(x, y + bar_height + 40, bar_width, 20), Qt.AlignmentFlag.AlignCenter, bar_name)


# horizontal line


class HLineFrame(QFrame):
    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setPen(QPen(Qt.GlobalColor.black, 0.79, Qt.PenStyle.SolidLine))
        y = self.height() // 2
        painter.drawLine(0, y, self.width(), y)


# down diagonal line


class DLineFrame(QFrame):
    def __init__(self, dRow=0, dColumn=0, dNum=0):
        super().__init__()
        self.dRow = dRow
        self.dColumn = dColumn
        self.dNum = dNum
        self.dDist = 2

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setPen(QPen(Qt.GlobalColor.black, 1.2, Qt.PenStyle.SolidLine))
        painter.drawLine(-10, 18, self.width() - 100, self.height() - 10)

    def __repr__(self):
        return f"DLineFrame({self.dRow},{self.dColumn},{self.dNum},{self.dDist})"


# upper diagonal line


class DLineFrameB(QFrame):
    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        pen = QPen(QBrush(QColor("black")), 1.2, Qt.PenStyle.SolidLine)
        painter.setPen(pen)
        painter.drawLine(-100, self.height(), self.width(), 20)

        self.dbRow = 0
        self.dbColumn = 1
        self.dbNum = 3
        self.dbDist = 1

    def __repr__(self):
        return "DLineFrameB()"


# we create two classes: one for discrete and another for continuous


class ContinuousAttribute:
    def __init__(self, value1, value2):
        self.value1 = value1
        self.value2 = value2
        self.name = ""

    def __repr__(self):
        return f"ContinuousAttribute: {self.name} {self.value1}, {self.value2};"


class DiscreteAttribute:
    def __init__(self, attributenames):
        self.attributenames = attributenames
        self.selected = ""
        self.name = ""

    def __repr__(self):
        return f"DiscreteAttribute: {self.name}, Nº Options {len(self.attributenames)}, {self.selected};"


class Alternative:
    def __init__(self, name, desc, attr):
        self.name = name
        self.desc = desc
        self.attr = attr

    def __repr__(self):
        return f"Alternative: {self.name}, Attributes: {self.attr}"


if __name__ == "__main__":
    app = QApplication(sys.argv)
    GUI = VentanaLogIn()
    GUI.show()
    sys.exit(app.exec())
