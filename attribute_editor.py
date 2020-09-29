from PySide2 import QtCore, QtGui, QtWidgets
from shiboken2 import wrapInstance

import maya.cmds as mc
import maya.api.OpenMaya as om
import maya.OpenMayaUI as omui


# don't use reload() if you want to keep ui position
class RDataBase(QtWidgets.QDialog):
    WINDOW_TITLE = "Rigs"
    dlg_instance = None

    # override in child class (change 'cls.dlg_instance = RDataBase()' to 'cls.dlg_instance = ChildClassName()')
    @classmethod
    def show_dialog(cls):
        if not cls.dlg_instance:
            cls.dlg_instance = RDataBase()
            
        if cls.dlg_instance.isHidden():
            cls.dlg_instance.show()
        else:
            cls.dlg_instance.raise_()
            cls.dlg_instance.activateWindow()
    
    @classmethod
    def maya_main_window(cls):
        """ Return Maya main window as Python Object """
        main_window_ptr = omui.MQtUtil.mainWindow()
        return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)

    def __init__(self):
        super(RDataBase, self).__init__(self.maya_main_window())

        self.setWindowTitle(self.WINDOW_TITLE)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)

        self.geometry = None

        self.create_widgets()
        self.create_layouts()
        self.create_connections()


    def create_widgets(self):
        
        self.LongName_entry= QtWidgets.QLineEdit()
        self.LongName_label= QtWidgets.QLabel('long name: ')
                
        self.tabs= QtWidgets.QTabWidget()
        #self.tabs.addTab(NumeriqueValueAttr(), 'numerique value')
        self.tabs.addTab(ShapeAttr(), 'Shape/dataType')
        self.tabs.addTab(VectorAttr(), 'vector')
        
        self.add_button= QtWidgets.QPushButton('add Attribute')

    def create_layouts(self):
        
        self.rootLayout= QtWidgets.QVBoxLayout()
        self.nameLayout= QtWidgets.QGridLayout()
        
        
        #rootLayout
        self.rootLayout.addLayout(self.nameLayout)
        self.rootLayout.addWidget(self.tabs)
        self.rootLayout.addWidget(self.add_button)
        
        #nameLayout
        self.nameLayout.addWidget(self.LongName_label, 0, 0, 1, 1)
        self.nameLayout.addWidget(self.LongName_entry, 0, 1, 1, 1)
                
        self.setLayout(self.rootLayout)

    def create_connections(self):
        
        self.add_button.clicked.connect(self.sendAttr)
        
    def enable_niceName_entry(self, value):
        
        if value == 2:
            
            self.niceName_entry.setEnabled(True)

        elif value == 0:
            
            self.niceName_entry.setEnabled(False)

    def enable_shortName_entry(self, value):
        
        if value == 2:
            
            self.shortName_entry.setEnabled(True)

        elif value == 0:
            
            self.shortName_entry.setEnabled(False)

    def sendAttr(self):
        
        new_ln= self.LongName_entry.text()
        
        if len(new_ln) != 0:
            
            self.tabs.currentWidget().buildAttr(cmds.ls(sl= True), ln= new_ln)
        
            
    def showEvent(self, e):
        super(RDataBase, self).showEvent(e)
        if self.geometry:
            self.restoreGeometry(self.geometry)
   
    def closeEvent(self, e):
        if isinstance(self, RDataBase):
            super(RDataBase, self).closeEvent(e)
            self.geometry = self.saveGeometry()

class NumeriqueValueAttr(QtWidgets.QWidget):

    def __init__(self, parent= None):
        super(NumeriqueValueAttr, self).__init__(parent)

        self.geometry = None

        self.create_widgets()
        self.create_layouts()
        self.create_connections()


    def create_widgets(self):
        
        self.isMulti_checkbox= QtWidgets.QCheckBox('is multi attribute')
        
        self.integrationType_gbox= QtWidgets.QGroupBox('integration type')
        self.numeriqueSettings_gbox= QtWidgets.QGroupBox('numerique Settings')

        self.keyable_RButton= QtWidgets.QRadioButton('keyable')
        self.keyable_RButton.setChecked(True)
        
        self.displayable_RButton= QtWidgets.QRadioButton('displayable')
        
        self.hidden_RButton= QtWidgets.QRadioButton('hidden')
        
        self.attribute_chooser_combobox= QtWidgets.QComboBox()
        self.attribute_chooser_combobox.addItems(['double', 'doubleAngle', 'doubleLinear', 'bool', 'message'])
        
        self.hasMin= QtWidgets.QCheckBox('has minimum')
        self.hasMax= QtWidgets.QCheckBox('has maximum')
        self.hasDefault= QtWidgets.QCheckBox('has Default')
        
        self.min_value= QtWidgets.QDoubleSpinBox()
        self.min_value.setEnabled(False)
        
        self.max_value= QtWidgets.QDoubleSpinBox()
        self.max_value.setEnabled(False)
        
        self.default_value= QtWidgets.QDoubleSpinBox()
        self.default_value.setEnabled(False)
        
    def create_layouts(self):
        
        #create Layouts
        self.rootLayout= QtWidgets.QVBoxLayout()
        self.integrationTypeLayout= QtWidgets.QHBoxLayout()
        self.numeriqueSettingsLayout= QtWidgets.QGridLayout()
        
        self.rootLayout.addWidget(self.isMulti_checkbox)
        self.rootLayout.addWidget(self.integrationType_gbox)
        self.rootLayout.addWidget(self.attribute_chooser_combobox)
        self.rootLayout.addWidget(self.numeriqueSettings_gbox)

        #integrationTypeLayout
        self.integrationTypeLayout.addWidget(self.keyable_RButton)
        self.integrationTypeLayout.addWidget(self.displayable_RButton)
        self.integrationTypeLayout.addWidget(self.hidden_RButton)
        
        #numeriqueSettingsLayout
        self.numeriqueSettingsLayout.addWidget(self.hasDefault, 0, 0, 1, 1)
        self.numeriqueSettingsLayout.addWidget(self.default_value, 0, 1, 1, 1)
        self.numeriqueSettingsLayout.addWidget(self.hasMin, 1, 0, 1, 1)
        self.numeriqueSettingsLayout.addWidget(self.min_value, 1, 1, 1, 1)
        self.numeriqueSettingsLayout.addWidget(self.hasMax, 2, 0, 1, 1)
        self.numeriqueSettingsLayout.addWidget(self.max_value, 2, 1, 1, 1)
        
        self.setLayout(self.rootLayout)
        self.integrationType_gbox.setLayout(self.integrationTypeLayout)
        self.numeriqueSettings_gbox.setLayout(self.numeriqueSettingsLayout)
        
    def create_connections(self):
        
        self.hasMin.stateChanged.connect(self.min_value.setEnabled)
        self.hasMax.stateChanged.connect(self.max_value.setEnabled)
        self.hasDefault.stateChanged.connect(self.default_value.setEnabled)

    def buildAttr(self, listAdd, ln):
        
        pass

class ShapeAttr(QtWidgets.QWidget):

    def __init__(self, parent= None):
        super(ShapeAttr, self).__init__(parent)

        self.geometry = None

        self.create_widgets()
        self.create_layouts()
        self.create_connections()


    def create_widgets(self):
        
        self.isMulti_checkbox= QtWidgets.QCheckBox('is multi attribute')
        
        self.attribute_chooser_combobox= QtWidgets.QComboBox()
        self.attribute_chooser_combobox.addItems(['nurbsCurve', 'nurbsSurface', 'mesh', 'lattice', 'matrix'])
        
    def create_layouts(self):
        
        #create Layouts
        self.rootLayout= QtWidgets.QVBoxLayout()
        
        self.rootLayout.addWidget(self.isMulti_checkbox)
        self.rootLayout.addWidget(self.attribute_chooser_combobox)
        
        self.setLayout(self.rootLayout)
        
    def create_connections(self):
        
        pass
        
    def buildAttr(self, listAdd, ln):
        
        for node in listAdd:
                
            if not cmds.attributeQuery(ln, n= node, ex= True):
                
                cmds.addAttr(ln= ln, dt= self.attribute_chooser_combobox.currentText(), multi= self.isMulti_checkbox.isChecked())                
                
class VectorAttr(QtWidgets.QWidget):

    def __init__(self, parent= None):
        super(VectorAttr, self).__init__(parent)

        self.geometry = None

        self.create_widgets()
        self.create_layouts()
        self.create_connections()


    def create_widgets(self):
        
        self.isMulti_checkbox= QtWidgets.QCheckBox('is multi attribute')
        
        self.integrationType_gbox= QtWidgets.QGroupBox('integration type')
        self.vectorSize_gbox= QtWidgets.QGroupBox('vector Size')
        self.vectorType_gbox= QtWidgets.QGroupBox('vector Type')
        
        #integrationType_gbox
        self.keyable_RButton= QtWidgets.QRadioButton('keyable')
        self.keyable_RButton.setChecked(True)
        self.displayable_RButton= QtWidgets.QRadioButton('displayable')
        self.hidden_RButton= QtWidgets.QRadioButton('hidden')
        
        #vectorSize gb
        self.vector2D_RButton= QtWidgets.QRadioButton('2D vector')
        self.vector3D_RButton= QtWidgets.QRadioButton('3D vector')
        self.vector3D_RButton.setChecked(True)
        self.vectorND_RButton= QtWidgets.QRadioButton('ND vector')
        
        self.vectorND_choose= QtWidgets.QSpinBox()
        self.vectorND_choose.setEnabled(False)

        #vectorType gb
        self.doubleType= QtWidgets.QComboBox()
        self.doubleType.addItems(['double', 'doubleAngle'])

    def create_layouts(self):
        
        #create Layouts
        self.rootLayout= QtWidgets.QVBoxLayout()
        self.integrationTypeLayout= QtWidgets.QHBoxLayout()
        self.vectorSizeLayout= QtWidgets.QGridLayout()
        self.vectorTypeLayout= QtWidgets.QHBoxLayout()
        
        #rootLayout
        self.rootLayout.addWidget(self.isMulti_checkbox)
        self.rootLayout.addWidget(self.integrationType_gbox)
        self.rootLayout.addWidget(self.vectorSize_gbox)
        self.rootLayout.addWidget(self.vectorType_gbox)
        
        #integrationTypeLayout
        self.integrationTypeLayout.addWidget(self.keyable_RButton)
        self.integrationTypeLayout.addWidget(self.displayable_RButton)
        self.integrationTypeLayout.addWidget(self.hidden_RButton)
        
        #vectorSizeLayout
        self.vectorSizeLayout.addWidget(self.vector2D_RButton, 0, 0, 1, 1)
        self.vectorSizeLayout.addWidget(self.vector3D_RButton, 0, 1, 1, 1)
        self.vectorSizeLayout.addWidget(self.vectorND_RButton, 1, 0, 1, 1)
        self.vectorSizeLayout.addWidget(self.vectorND_choose, 1, 1, 1, 1)
        
        #vectorTypeLayout
        self.vectorTypeLayout.addWidget(self.doubleType)
        
        #setLayouts
        self.integrationType_gbox.setLayout(self.integrationTypeLayout)
        self.vectorSize_gbox.setLayout(self.vectorSizeLayout)
        self.vectorType_gbox.setLayout(self.vectorTypeLayout)
        self.setLayout(self.rootLayout)

    def create_connections(self):
    
        self.vectorND_RButton.toggled.connect(self.vectorND_choose.setEnabled)

    def buildAttr(self, listAdd, ln):
        
        nbr_dimention= self.vectorND_choose.value()
        double_type= self.doubleType.currentText()
        is_multi= self.isMulti_checkbox.isChecked()
        
        for node in listAdd:
            
            if self.vector2D_RButton.isChecked():
                
                print 'je passe par vector2'
                
                if not cmds.attributeQuery(ln, n= node, ex= True):
                
                    cmds.addAttr(node, ln= ln, at= 'double2', multi= is_multi)
                    cmds.addAttr(node, ln= '{0}X'.format(ln), at= double_type, p= ln, k= self.keyable_RButton.isChecked())
                    cmds.addAttr(node, ln= '{0}Y'.format(ln), at= double_type, p= ln, k= self.keyable_RButton.isChecked())
                        
                    cmds.setAttr('{0}.{1}X'.format(node, ln), e= True, channelBox= self.displayable_RButton.isChecked())
                    cmds.setAttr('{0}.{1}Y'.format(node, ln), e= True, channelBox= self.displayable_RButton.isChecked())


            if self.vector3D_RButton.isChecked():
                
                print 'je passe par vector3'
                
                if not cmds.attributeQuery(ln, n= node, ex= True):
                
                    cmds.addAttr(node, ln= '{0}'.format(ln), at= 'double3', multi= is_multi)
                    cmds.addAttr(node, ln= '{0}X'.format(ln), at= double_type, p= ln, k= self.keyable_RButton.isChecked())
                    cmds.addAttr(node, ln= '{0}Y'.format(ln), at= double_type, p= ln, k= self.keyable_RButton.isChecked())
                    cmds.addAttr(node, ln= '{0}Z'.format(ln), at= double_type, p= ln, k= self.keyable_RButton.isChecked())
                    
                    cmds.setAttr('{0}.{1}X'.format(node, ln), e= True, channelBox= self.displayable_RButton.isChecked())
                    cmds.setAttr('{0}.{1}Y'.format(node, ln), e= True, channelBox= self.displayable_RButton.isChecked())
                    cmds.setAttr('{0}.{1}Z'.format(node, ln), e= True, channelBox= self.displayable_RButton.isChecked())

            if self.vectorND_RButton.isChecked():
                
                print 'je passe par vectorN'
                
                if not cmds.attributeQuery(ln, n= node, ex= True):

                    cmds.addAttr(node, ln= ln, at= 'compound', nc= nbr_dimention, multi= is_multi)
        
                    for idx in range(nbr_dimention):
                    
                        cmds.addAttr(node, ln= '{0}{1}'.format(ln, idx+1), at= double_type, p= ln, k= self.keyable_RButton.isChecked())
                        #cmds.setAttr(node+ '{0}{1}'.format(ln, idx+1), e= True, channelBox= self.displayable_RButton.isChecked())
                        
if __name__ == "__main__":
    
    try:    
        template_ui.close()
        template_ui.deleteLater()
    except:
        pass
        
    template_ui = RDataBase()
    template_ui.show_dialog()
