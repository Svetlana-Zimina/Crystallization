import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
from ui import Ui_MainWindow
import json
import os
from datetime import date

with open("elements.json", "r", encoding="utf-8") as file:
    elements = json.load(file)

with open("oxides.json", "r", encoding="utf-8") as file:
    oxides = json.load(file)


class OxideMassCalculate(QtWidgets.QMainWindow):
    """Class for calculation of oxide mass."""

    def __init__(self):
        super(OxideMassCalculate, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.init_UI()

    def init_UI(self):
        self.setWindowTitle("Crystallization")

        self.ui.comboBox_elem_1.addItems([*elements])
        self.ui.comboBox_elem_2.addItems([*elements])
        self.ui.comboBox_elem_3.addItems([*elements])
        self.ui.comboBox_elem_4.addItems([*elements])
        self.ui.comboBox_elem_5.addItems([*elements])
        self.ui.comboBox_elem_6.addItems([*elements])
        self.ui.comboBox_elem_7.addItems([*elements])
        self.ui.comboBox_elem_8.addItems([*elements])
        self.ui.comboBox_elem_9.addItems([*elements])
        self.ui.comboBox_elem_10.addItems([*elements])
        self.ui.comboBox_oxide_1.addItems([*oxides])
        self.ui.comboBox_oxide_2.addItems([*oxides])
        self.ui.comboBox_oxide_3.addItems([*oxides])
        self.ui.comboBox_oxide_4.addItems([*oxides])
        self.ui.comboBox_oxide_5.addItems([*oxides])
        self.ui.comboBox_oxide_6.addItems([*oxides])

        self.ui.pushButton_count.clicked.connect(self.calculation)
        self.ui.pushButton_clear_result.clicked.connect(self.clear_text)
    
    @staticmethod
    def is_float(string):
        """Check if data is number."""
        try:
            return float(string)
        except ValueError:
            QMessageBox.warning(
                None,
                "Attention",
                "<font size = 8 color = red > Check next parameters: melt density, crusible parameters, elements indexes </font>"
            )
    
    @staticmethod
    def arr_preparation(arr: list[str]):
        """Check if list is not empty. Delete 'None' from list."""
        new_arr = []
        for item in arr:
            if item != 'None':
                new_arr.append(item)
        if len(new_arr) == 0:
            QMessageBox.warning(
                None,
                "Attention",
                "<font size = 8 color = red > You should select at least one oxide! </font>"
            )
        return new_arr
    
    @staticmethod
    def dict_preparation(**data):
        """Check if dict is not empty. Delete 'None' from dict."""
        new_dict = {}
        for k in data:
            if k != 'None':
                new_dict[k] = data[k]
        if len(new_dict) == 0:
            QMessageBox.warning(
                None,
                "Attention",
                "<font size = 8 color = red > You should select at least one element! </font>"
            )
        return new_dict
    
    @staticmethod
    def validate_two_arrs(arr1, arr2):
        """Check if one str is a part of other str."""
        for i in range(len(arr1)):
            if arr1[i] == 'O' or arr1[i] == 'C':
                break
            elif arr1[i] not in arr2[i]:
                QMessageBox.warning(
                    None,
                    "Attention",
                    "<font size = 8 color = red > The order of the oxides does not correspond to the order of the elements! </font>"
                ) 

    def data_preparation(self):
        
        oxides_data = [
            self.ui.comboBox_oxide_1.currentText(),
            self.ui.comboBox_oxide_2.currentText(),
            self.ui.comboBox_oxide_3.currentText(),
            self.ui.comboBox_oxide_4.currentText(),
            self.ui.comboBox_oxide_5.currentText(),
            self.ui.comboBox_oxide_6.currentText()
        ]

        cleared_oxides = self.arr_preparation(oxides_data)
        
        crystal_elem_data = {
            self.ui.comboBox_elem_1.currentText(): self.ui.lineEdit_index_1.text(),
            self.ui.comboBox_elem_2.currentText(): self.ui.lineEdit_index_2.text(),
            self.ui.comboBox_elem_3.currentText(): self.ui.lineEdit_index_3.text(),
            self.ui.comboBox_elem_4.currentText(): self.ui.lineEdit_index_4.text(),
            self.ui.comboBox_elem_5.currentText(): self.ui.lineEdit_index_5.text(),
            self.ui.comboBox_elem_6.currentText(): self.ui.lineEdit_index_6.text(),
            self.ui.comboBox_elem_7.currentText(): self.ui.lineEdit_index_7.text(),
            self.ui.comboBox_elem_8.currentText(): self.ui.lineEdit_index_8.text(),
            self.ui.comboBox_elem_9.currentText(): self.ui.lineEdit_index_9.text(),
            self.ui.comboBox_elem_10.currentText(): self.ui.lineEdit_index_10.text()
        }

        cleared_crystal_data = self.dict_preparation(**crystal_elem_data)
        
        elem_list = list(cleared_crystal_data.keys())
        self.validate_two_arrs(elem_list, cleared_oxides)

        for val in list(cleared_crystal_data.values()):
            self.is_float(val)
        
        return [
            self.is_float(self.ui.lineEdit_tigel_diametr.text()),
            self.is_float(self.ui.lineEdit_tigel_height.text()),
            self.is_float(self.ui.lineEdit_crystal_desity.text()),
            cleared_oxides,
            cleared_crystal_data
        ]
        
    def calculation(self):
        """Basic calculations."""
        
        validated_data = self.data_preparation()
        
        tigel_diametr = validated_data[0]
        tigel_hight = validated_data[1]
        crystal_density = validated_data[2]
        oxide_list = validated_data[3]
        crystal_elem_data = validated_data[4]

        tigel_volume = 3.14 * tigel_hight * (tigel_diametr ** 2) / 4
        mixture_weight = tigel_volume * crystal_density
        mixture_weight_text = f'{mixture_weight:.4f}'
        self.ui.textBrowser_crystal_mass.append(mixture_weight_text)

        crystal_molar_mass = 0
        crystal_formula = ""
        for item in crystal_elem_data:
            crystal_molar_mass += (
                elements[item] *
                float(crystal_elem_data[item])
            )
            crystal_formula = (
                crystal_formula +
                item +
                crystal_elem_data[item]
            )

        matter_amount = mixture_weight / crystal_molar_mass

        text = 'Masses of oxides: '

        if len(oxide_list) == 1:
            oxide1_weight = (
                (float(self.ui.lineEdit_index_1.text()) /
                oxides[oxide_list[0]]['index']) *
                oxides[oxide_list[0]]['molar_mass'] *
                matter_amount
            )
            text = (
                text +
                f'\n\n{oxide_list[0]} - {oxide1_weight:.4f} g'
            )

        elif len(oxide_list) == 2:
            oxide1_weight = (
                (float(self.ui.lineEdit_index_1.text()) /
                oxides[oxide_list[0]]['index']) *
                oxides[oxide_list[0]]['molar_mass'] *
                matter_amount
            )

            oxide2_weight = (
                (float(self.ui.lineEdit_index_2.text()) /
                oxides[oxide_list[1]]['index']) *
                oxides[oxide_list[1]]['molar_mass'] *
                matter_amount
            )

            text = (
                text +
                f'\n\n{oxide_list[0]} - {oxide1_weight:.4f} g' +
                f'\n\n{oxide_list[1]} - {oxide2_weight:.4f} g'
            )

        elif len(oxide_list) == 3:
            oxide1_weight = (
                (float(self.ui.lineEdit_index_1.text()) /
                oxides[oxide_list[0]]['index']) *
                oxides[oxide_list[0]]['molar_mass'] *
                matter_amount
            )

            oxide2_weight = (
                (float(self.ui.lineEdit_index_2.text()) /
                oxides[oxide_list[1]]['index']) *
                oxides[oxide_list[1]]['molar_mass'] *
                matter_amount
            )

            oxide3_weight = (
                (float(self.ui.lineEdit_index_3.text()) /
                oxides[oxide_list[2]]['index']) *
                oxides[oxide_list[2]]['molar_mass'] *
                matter_amount
            )

            text = (
                text +
                f'\n\n{oxide_list[0]} - {oxide1_weight:.4f} g' +
                f'\n\n{oxide_list[1]} - {oxide2_weight:.4f} g' +
                f'\n\n{oxide_list[2]} - {oxide3_weight:.4f} g'
            )

        elif len(oxide_list) == 4:
            oxide1_weight = (
                (float(self.ui.lineEdit_index_1.text()) /
                oxides[oxide_list[0]]['index']) *
                oxides[oxide_list[0]]['molar_mass'] *
                matter_amount
            )

            oxide2_weight = (
                (float(self.ui.lineEdit_index_2.text()) /
                oxides[oxide_list[1]]['index']) *
                oxides[oxide_list[1]]['molar_mass'] *
                matter_amount
            )

            oxide3_weight = (
                (float(self.ui.lineEdit_index_3.text()) /
                oxides[oxide_list[2]]['index']) *
                oxides[oxide_list[2]]['molar_mass'] *
                matter_amount
            )

            oxide4_weight = (
                (float(self.ui.lineEdit_index_4.text()) /
                oxides[oxide_list[3]]['index']) *
                oxides[oxide_list[3]]['molar_mass'] *
                matter_amount
            )

            text = (
                text +
                f'\n\n{oxide_list[0]} - {oxide1_weight:.4f} g' +
                f'\n\n{oxide_list[1]} - {oxide2_weight:.4f} g' +
                f'\n\n{oxide_list[2]} - {oxide3_weight:.4f} g' +
                f'\n\n{oxide_list[3]} - {oxide4_weight:.4f} g'
            )

        elif len(oxide_list) == 5:
            oxide1_weight = (
                (float(self.ui.lineEdit_index_1.text()) /
                oxides[oxide_list[0]]['index']) *
                oxides[oxide_list[0]]['molar_mass'] *
                matter_amount
            )

            oxide2_weight = (
                (float(self.ui.lineEdit_index_2.text()) /
                oxides[oxide_list[1]]['index']) *
                oxides[oxide_list[1]]['molar_mass'] *
                matter_amount
            )

            oxide3_weight = (
                (float(self.ui.lineEdit_index_3.text()) /
                oxides[oxide_list[2]]['index']) *
                oxides[oxide_list[2]]['molar_mass'] *
                matter_amount
            )

            oxide4_weight = (
                (float(self.ui.lineEdit_index_4.text()) /
                oxides[oxide_list[3]]['index']) *
                oxides[oxide_list[3]]['molar_mass'] *
                matter_amount
            )

            oxide5_weight = (
                (float(self.ui.lineEdit_index_5.text()) /
                oxides[oxide_list[4]]['index']) *
                oxides[oxide_list[4]]['molar_mass'] *
                matter_amount
            )

            text = (
                text +
                f'\n\n{oxide_list[0]} - {oxide1_weight:.4f} g' +
                f'\n\n{oxide_list[1]} - {oxide2_weight:.4f} g' +
                f'\n\n{oxide_list[2]} - {oxide3_weight:.4f} g' +
                f'\n\n{oxide_list[3]} - {oxide4_weight:.4f} g' +
                f'\n\n{oxide_list[4]} - {oxide5_weight:.4f} g'
            )

        elif len(oxide_list) == 6:
            oxide1_weight = (
                (float(self.ui.lineEdit_index_1.text()) /
                oxides[oxide_list[0]]['index']) *
                oxides[oxide_list[0]]['molar_mass'] *
                matter_amount
            )

            oxide2_weight = (
                (float(self.ui.lineEdit_index_2.text()) /
                oxides[oxide_list[1]]['index']) *
                oxides[oxide_list[1]]['molar_mass'] *
                matter_amount
            )

            oxide3_weight = (
                (float(self.ui.lineEdit_index_3.text()) /
                oxides[oxide_list[2]]['index']) *
                oxides[oxide_list[2]]['molar_mass'] *
                matter_amount
            )

            oxide4_weight = (
                (float(self.ui.lineEdit_index_4.text()) /
                oxides[oxide_list[3]]['index']) *
                oxides[oxide_list[3]]['molar_mass'] *
                matter_amount
            )

            oxide5_weight = (
                (float(self.ui.lineEdit_index_5.text()) /
                oxides[oxide_list[4]]['index']) *
                oxides[oxide_list[4]]['molar_mass'] *
                matter_amount
            )

            oxide6_weight = (
                (float(self.ui.lineEdit_index_6.text()) /
                oxides[oxide_list[5]]['index']) *
                oxides[oxide_list[5]]['molar_mass'] *
                matter_amount
            )

            text = (
                text +
                f'\n\n{oxide_list[0]} - {oxide1_weight:.4f} g' +
                f'\n\n{oxide_list[1]} - {oxide2_weight:.4f} g' +
                f'\n\n{oxide_list[2]} - {oxide3_weight:.4f} g' +
                f'\n\n{oxide_list[3]} - {oxide4_weight:.4f} g' +
                f'\n\n{oxide_list[4]} - {oxide5_weight:.4f} g' +
                f'\n\n{oxide_list[5]} - {oxide6_weight:.4f} g'
            )

        self.ui.textBrowser_result.append(text)

        save_data_text = (
            f"Date: {date.today()}\n\n" +
            f"Crystal: {crystal_formula}\n\n" +
            f"Crucible diametr, cm: {self.ui.lineEdit_tigel_diametr.text()}\n\n" +
            f"Crucible hight, cm: {self.ui.lineEdit_tigel_height.text()}\n\n" +
            f"Melt density, g/cm3: {self.ui.lineEdit_crystal_desity.text()}\n\n" +
            f"Сalculated mass of the crystal, g:  {mixture_weight:.4f}\n\n\n" +
            text
        )
        self.save_data(save_data_text)
                   
    def clear_text(self):
        """Clean textBrowsers windows."""
        self.ui.textBrowser_result.clear()
        self.ui.textBrowser_crystal_mass.clear()

    def save_data(self, text):
        """Save data to txt file."""
        with open("Crystallization.txt", "a") as my_file:
            my_file.write(text)


if __name__ == "__main__":
    os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "1"
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    os.environ["QT_SCALE_FACTOR"] = "1"
    app = QtWidgets.QApplication([])
    application = OxideMassCalculate()
    application.show()

    sys.exit(app.exec())
