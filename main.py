import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
from ui import Ui_MainWindow
import json
import os

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
        
    def calculation(self):
        """Basic calculations."""
        try:
            tigel_diametr = float(self.ui.lineEdit_tigel_diametr.text())
            tigel_hight = float(self.ui.lineEdit_tigel_height.text())
            tigel_volume = 3.14 * tigel_hight * (tigel_diametr ** 2) / 4

            crystal_density = float(self.ui.lineEdit_crystal_desity.text())
            mixture_weight = tigel_volume * crystal_density
            mixture_weight_text = f'{mixture_weight:.4f}'
            self.ui.textBrowser_crystal_mass.append(mixture_weight_text)

            crystal_elements_data = {
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

            crystal_molar_mass = 0
            crystal_formula = ""
            for item in crystal_elements_data:
                if item != 'None':
                    crystal_molar_mass += (
                        elements[item] *
                        float(crystal_elements_data[item])
                    )
                    crystal_formula = (
                        crystal_formula +
                        item +
                        crystal_elements_data[item]
                    )

            matter_amount = mixture_weight / crystal_molar_mass

            oxides_data = [
                self.ui.comboBox_oxide_1.currentText(),
                self.ui.comboBox_oxide_2.currentText(),
                self.ui.comboBox_oxide_3.currentText(),
                self.ui.comboBox_oxide_4.currentText(),
                self.ui.comboBox_oxide_5.currentText(),
                self.ui.comboBox_oxide_6.currentText()
            ]
            oxide_list = []
            for item in oxides_data:
                if item != 'None':
                    oxide_list.append(item)

            text = 'Masses of oxides: '

            if len(oxide_list) == 2:
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
                f"Crystal: {crystal_formula}\n\n" +
                f"Crucible diametr, cm: {self.ui.lineEdit_tigel_diametr.text()}\n\n" +
                f"Crucible hight, cm: {self.ui.lineEdit_tigel_height.text()}\n\n" +
                f"Melt density, g/cm3: {self.ui.lineEdit_crystal_desity.text()}\n\n" +
                f"Сalculated mass of the crystal, g:  {mixture_weight:.4f}\n\n\n" +
                text
            )
            self.save_data(save_data_text)

        except ValueError:
            QMessageBox.warning(
                None,
                "Attention",
                "<font size = 8 color = red > Сheck if all data is entered! </font>"
            )

    def clear_text(self):
        """Clean textBrowsers windows."""
        self.ui.textBrowser_result.clear()
        self.ui.textBrowser_crystal_mass.clear()

    def save_data(self, text):
        """Save data to txt file."""
        my_file = open("Crystallization.txt", "w+")
        my_file.write(text)
        my_file.close()


if __name__ == "__main__":
    os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "1"
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    os.environ["QT_SCALE_FACTOR"] = "1"
    app = QtWidgets.QApplication([])
    application = OxideMassCalculate()
    application.show()

    sys.exit(app.exec())
