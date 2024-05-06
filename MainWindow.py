import sys
from hashlib import sha256

from PIL import Image
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QFileDialog
from bitarray import bitarray
from numpy import asarray, concatenate, random, arange

from ui_mainwindow import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

    @pyqtSlot()
    def on_pushButton_fileDialogIn_clicked(self) -> None:
        self.ui.lineEdit_pathIn.setText(
            QFileDialog.getOpenFileName(self, "Select the input image", sys.path[0],
                                        "All image types (*.bmp *.png);; BMP (*.bmp);; PNG (*.png)")[0])

    @pyqtSlot()
    def on_pushButton_fileDialogOut_clicked(self) -> None:
        self.ui.lineEdit_pathOut.setText(
            QFileDialog.getSaveFileName(self, "Select the save path the output image", sys.path[0],
                                        "All image types (*.bmp *.png);; BMP (*.bmp);; PNG (*.png)")[0])

    @pyqtSlot()
    def on_pushButton_getMessage_clicked(self) -> None:
        password = self.ui.lineEdit_password.text()
        img_path = self.ui.lineEdit_pathIn.text()
        if len(img_path) == 0:
            return
        with Image.open(img_path) as img:
            img.convert(mode="RGB")
            self.ui.plainTextEdit.insertPlainText(MainWindow.get_message(password, img))
        self.ui.lineEdit_pathOut.clear()
        self.ui.lineEdit_pathIn.clear()

    @pyqtSlot()
    def on_pushButton_hideMessage_clicked(self) -> None:
        text = self.ui.plainTextEdit.toPlainText()
        password = self.ui.lineEdit_password.text()
        img_path = self.ui.lineEdit_pathIn.text()
        save_path = self.ui.lineEdit_pathOut.text()
        if len(img_path) == 0 or len(save_path) == 0:
            return
        img_out: Image.Image
        img = Image.open(img_path)
        img.load()
        img.convert(mode="RGB")
        out = MainWindow.hide_message(text, password, img)
        out.save(save_path, mode="RGB", quality=100)
        self.ui.lineEdit_pathOut.clear()
        self.ui.lineEdit_pathIn.clear()
        self.ui.plainTextEdit.clear()

    @staticmethod
    def hide_message(text: str, password: str, img: Image.Image) -> Image.Image:
        random.seed(int.from_bytes(sha256(password.encode()).digest()[:4], 'little'))
        img_array = concatenate(asarray(img))
        bit_text = bitarray()
        bit_text.frombytes(text.encode())
        rnd_array = arange(len(img_array))
        random.shuffle(rnd_array)
        bit_text += bitarray("00000000")
        itr = iter(bit_text)
        for i in rnd_array:
            try:
                img_array[i][0] = img_array[i][0] & ~1 if next(itr) == 0 else img_array[i][0] | 1
                img_array[i][1] = img_array[i][1] & ~1 if next(itr) == 0 else img_array[i][1] | 1
                img_array[i][2] = img_array[i][2] & ~1 if next(itr) == 0 else img_array[i][2] | 1
            except StopIteration:
                break
        return Image.fromarray(img_array.reshape((img.size[1], img.size[0], 3)), mode="RGB")

    @staticmethod
    def get_message(password: str, img: Image.Image) -> str:
        random.seed(int.from_bytes(sha256(password.encode()).digest()[:4], 'little'))
        img_array = concatenate(asarray(img))
        bit_text = bitarray()
        rnd_array = arange(len(img_array))
        random.shuffle(rnd_array)
        for i in rnd_array:
            bit_text.append(img_array[i][0] & 1)
            if len(bit_text) % 8 == 0 and int.from_bytes(bit_text[-8:].tobytes(), 'little') == 0:
                break
            bit_text.append(img_array[i][1] & 1)
            if len(bit_text) % 8 == 0 and int.from_bytes(bit_text[-8:].tobytes(), 'little') == 0:
                break
            bit_text.append(img_array[i][2] & 1)
            if len(bit_text) % 8 == 0 and int.from_bytes(bit_text[-8:].tobytes(), 'little') == 0:
                break
        return bit_text.tobytes().decode()
