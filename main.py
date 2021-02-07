import logging
import sys
import os

from PySide2 import QtWidgets as qtw    
from PySide2 import QtGui as qtg
from PySide2 import QtCore as qtc
from PySide2 import QtUiTools as qtu

import database as db


logger = logging.getLogger('app_logger')
logging.basicConfig(
        level=logging.DEBUG,
        format='%(process)d - %(levelname)s - %(message)s')


class MainInterface(qtw.QMainWindow):
    def __init__(self, ui_file, parent=None):
        super(MainInterface, self).__init__(parent)
        ui_file = qtc.QFile(ui_file)
        ui_file.open(qtc.QFile.ReadOnly)

        loader = qtu.QUiLoader()
        self.window = loader.load(ui_file)
        ui_file.close()

        # Bring in interface widgets for use

        # Labels
        self.lbl_full_name = self.window.findChild(qtw.QLabel, 'lbl_full_name')
        self.lbl_company = self.window.findChild(qtw.QLabel, 'lbl_company')

        # Listviews
        self.lw_contact_list = self.window.findChild(qtw.QListWidget, 'lw_contact_list')
        self.lw_contact_list.itemSelectionChanged.connect(self.get_item())

        # Line Edits
        self.le_last_name = self.window.findChild(qtw.QLineEdit, 'le_last_name')
        self.le_first_name = self.window.findChild(qtw.QLineEdit, 'le_first_name')
        self.le_company = self.window.findChild(qtw.QLineEdit, 'le_company')
        self.le_email = self.window.findChild(qtw.QLineEdit, 'le_email')
        self.le_home_phone = self.window.findChild(qtw.QLineEdit, 'le_home_phone')
        self.le_work_phone = self.window.findChild(qtw.QLineEdit, 'le_work_phone')

        # Text Edits
        self.te_notes = self.window.findChild(qtw.QTextEdit, 'te_notes')

        # Buttons
        self.btn_new_contact = self.window.findChild(qtw.QPushButton,
                                            'btn_new_contact')

        self.load_interface()

        self.window.show()

    
    def load_interface(self, initial_id=None):
        '''
            list is return from db.read_db() as follows:
            (
                contact_id,
                last_name,
                first_name,
                company,
                email,
                home_phone,
                work_phone,
                notes
            )
        '''

        logger.info('Loading interface')
        contacts = db.read_db()
        if contacts[0][1] == 'last_name':
            contacts.pop(0)
        contact_names = []
        list_dict = {}
        for c in contacts:
            list_name = f'{c[1]}, {c[2]}'
            contact_names.append(list_name)
            list_dict[list_name] = c[0]
        if not initial_id:
            initial_id = contacts[0][0]

        initial_contact = db.get_contact(initial_id)
        logger.info(initial_contact)
        self.lw_contact_list.addItems(contact_names)
        self.lw_contact_list.setCurrentRow(initial_id)
        self.lbl_full_name.setText(f'{initial_contact[2]} {initial_contact[1]}')


    def get_item(self):
        item = self.lw_contact_list.currentItem()
        print(item)


if __name__ == "__main__":
    import sys
    qtc.QCoreApplication.setAttribute(qtc.Qt.AA_ShareOpenGLContexts)
    app = qtw.QApplication(sys.argv)
    MainWindow = MainInterface('interface.ui')
    sys.exit(app.exec_())