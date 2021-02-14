import logging
import sys
import os

from PySide2 import QtWidgets as qtw
from PySide2 import QtGui as qtg
from PySide2 import QtCore as qtc
from PySide2 import QtUiTools as qtu
from PySide2 import Qt

import database as db


logger = logging.getLogger("app_logger")
logging.basicConfig(
    level=logging.DEBUG, format="%(process)d - %(levelname)s - %(message)s"
)



class MainInterface(qtw.QMainWindow):
    def __init__(self, ui_file, parent=None):
        super(MainInterface, self).__init__(parent)
        ui_file = qtc.QFile(ui_file)
        ui_file.open(qtc.QFile.ReadOnly)

        loader = qtu.QUiLoader()
        self.window = loader.load(ui_file)
        ui_file.close()

        self.list_dict = {}  # for keeping track of contact_id's for list names
        self.save_contact_id:int = None  # to save which contact to save to.
        # Bring in interface widgets for use

        # Labels
        self.lbl_full_name = self.window.findChild(qtw.QLabel, "lbl_full_name")
        self.lbl_company = self.window.findChild(qtw.QLabel, "lbl_company")
        self.lbl_message = self.window.findChild(qtw.QLabel, 'lbl_message')

        # Listviews
        self.lw_contact_list = self.window.findChild(qtw.QListWidget, "lw_contact_list")
        self.lw_contact_list.itemClicked.connect(self.load_contact)

        # Line Edits
        self.le_last_name = self.window.findChild(qtw.QLineEdit, "le_last_name")
        self.le_first_name = self.window.findChild(qtw.QLineEdit, "le_first_name")
        self.le_company = self.window.findChild(qtw.QLineEdit, "le_company")
        self.le_email = self.window.findChild(qtw.QLineEdit, "le_email")
        self.le_home_phone = self.window.findChild(qtw.QLineEdit, "le_home_phone")
        self.le_work_phone = self.window.findChild(qtw.QLineEdit, "le_work_phone")

        # Text Edits
        self.te_notes = self.window.findChild(qtw.QTextEdit, "te_notes")

        # Buttons
        self.btn_new_contact = self.window.findChild(qtw.QPushButton, "btn_new_contact")
        self.btn_new_contact.clicked.connect(self.new_contact)
        self.btn_save = self.window.findChild(qtw.QPushButton, 'btn_save')
        self.btn_save.clicked.connect(self.save_contact)
        self.btn_edit = self.window.findChild(qtw.QPushButton, 'btn_edit')
        self.btn_edit.clicked.connect(self.edit_contact)

        self.load_interface()
        self.lw_contact_list.setCurrentRow(0)

        self.window.show()

    def load_interface(self):
        """
        load_interface calls db.read_db() to collect contact data from the 
        database. A list is returned from db.read_db() as follows:
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


        """

        # load contact_list and get back sorted list of contacts.
        contact_names = self.load_contact_list()
        c_id = self.list_dict[contact_names[0]]
        initial_contact = db.get_contact(c_id)


        # set fields in ui
        self.lbl_full_name.setText(f"{initial_contact[2]} {initial_contact[1]}")
        self.lbl_company.setText(initial_contact[3])
        self.lbl_message.setText('')
        self.le_last_name.setText(initial_contact[1])
        self.le_first_name.setText(initial_contact[2])
        self.le_company.setText(initial_contact[3])
        self.le_email.setText(initial_contact[4])
        self.le_home_phone.setText(initial_contact[5])
        self.le_work_phone.setText(initial_contact[6])
        self.te_notes.setText(initial_contact[7])

        logger.info(initial_contact)


    def load_contact_list(self):
        logger.info("Loading interface")
        contacts = db.read_db()

        # Remove column headers if in list of contacts
        if contacts[0][1] == "last_name":
            contacts.pop(0)
        contact_names = []

        for c in contacts:
            # Cycle through contacts and generate a dictionary
            # of full names, to match listwidget items, and the
            # contact_id associated for that name for
            # database lookup.
            list_name = f"{c[1]}, {c[2]}"
            contact_names.append(list_name)
            self.list_dict[list_name] = c[0]

        contact_names.sort()
        self.lw_contact_list.clear()
        self.lw_contact_list.addItems(contact_names)
        return contact_names

    def load_contact(self, item):
        self.save_contact_id = self.list_dict[item.text()]
        print(self.save_contact_id)
        contact = db.get_contact(self.list_dict[item.text()])
        self.lbl_full_name.setText(f"{contact[2]} {contact[1]}")
        self.lbl_company.setText(contact[3])
        self.le_last_name.setText(contact[1])
        self.le_first_name.setText(contact[2])
        self.le_company.setText(contact[3])
        self.le_email.setText(contact[4])
        self.le_home_phone.setText(contact[5])
        self.le_work_phone.setText(contact[6])
        self.te_notes.setText(contact[7])
        self.disable_editing()
        logger.info(contact)


    def enable_editing(self):
        self.btn_save.setEnabled(True)
        self.le_last_name.setReadOnly(False)
        self.le_first_name.setReadOnly(False)
        self.le_company.setReadOnly(False)
        self.le_email.setReadOnly(False)
        self.le_home_phone.setReadOnly(False)
        self.le_work_phone.setReadOnly(False)
        self.te_notes.setReadOnly(False)

    def disable_editing(self):
        self.btn_save.setEnabled(False)
        self.le_last_name.setReadOnly(True)
        self.le_first_name.setReadOnly(True)
        self.le_company.setReadOnly(True)
        self.le_email.setReadOnly(True)
        self.le_home_phone.setReadOnly(True)
        self.le_work_phone.setReadOnly(True)
        self.te_notes.setReadOnly(True)

    def new_contact(self):
        self.save_contact_id = None
        self.enable_editing()
        self.lbl_full_name.setText("")
        self.lbl_company.setText("")
        self.le_last_name.setText("")
        self.le_first_name.setText("")
        self.le_company.setText("")
        self.le_email.setText("")
        self.le_home_phone.setText("")
        self.le_work_phone.setText("")
        self.te_notes.setText("")
    
    def save_contact(self):
        last = self.le_last_name.text()
        first = self.le_first_name.text()
        company = self.le_company.text()
        email = self.le_email.text()
        home_phone = self.le_home_phone.text()
        work_phone = self.le_work_phone.text()
        notes = self.te_notes.toPlainText()

        valid = False

        params = [
            last,
            first,
            company,
            email,
            home_phone,
            work_phone,
            notes
        ]

        for p in params[:3]:
            if len(p.strip()) != 0:
                valid = True
        if valid:
            if self.save_contact_id:
                params.insert(0, self.save_contact_id)
                db.update_contact(params)
                self.btn_save.setEnabled(False)
                self.lbl_message.setText('')
                items = self.lw_contact_list.findItems(f'{last}, {first}', qtc.Qt.MatchContains)
                if len(items) > 0:
                    item = items[0]
                    self.lw_contact_list.setCurrentItem(item)
                    self.load_contact(item)
                else:
                    logger.info('Item not found.')
            else:
                db.add_contact(*params)
                self.btn_save.setEnabled(False)
                self.lbl_message.setText('')
                self.load_contact_list()
                items = self.lw_contact_list.findItems(f'{last}, {first}', qtc.Qt.MatchContains)
                if len(items) > 0:
                    item = items[0]
                    self.lw_contact_list.setCurrentItem(item)
                    self.load_contact(item)
                else:
                    logger.info('Item not found.')
                

        else:
            logger.warning('Did not save contact. Contact must have either last of first name, or company name.')
            self.lbl_message.setText('Missing required fields.')
            self.lbl_message.setStyleSheet('QLabel {color: red;}')
            pass

    def edit_contact(self):
        print(self.save_contact_id)
        self.enable_editing()
        pass


if __name__ == "__main__":
    import sys

    qtc.QCoreApplication.setAttribute(qtc.Qt.AA_ShareOpenGLContexts)
    app = qtw.QApplication(sys.argv)
    MainWindow = MainInterface("interface.ui")
    sys.exit(app.exec_())
