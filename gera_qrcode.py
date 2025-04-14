import sys
import mysql.connector
import qrcode
from PyQt5.QtWidgets import QApplication, QDialog, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PIL.ImageQt import ImageQt
from PyQt5.QtGui import QImage
import io
from PIL import Image

class GeraQrcode(QDialog):
    def __init__(self, id_pedido):
        super().__init__()
        self.setWindowTitle("QR Code do Pedido")
        self.resize(300, 300)
        self.id_pedido = id_pedido

        # Conectar ao banco de dados
        self.conexao = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="crud"
        )
        self.cursor = self.conexao.cursor()

        # Layout
        self.layout = QVBoxLayout()
        self.label_qrcode = QLabel("Gerando QR Code...")
        self.label_qrcode.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.label_qrcode)
        self.setLayout(self.layout)

        self.gerar_qrcode()
    
    def gerar_qrcode(self):
        try:
            self.cursor.execute("SELECT endereco_entrega FROM pedidos WHERE id_pedido = %s", (self.id_pedido,))
            pedido = self.cursor.fetchone()

            if pedido:
                texto_qrcode = f"endereco: {pedido[0]}"
                qr = qrcode.make(texto_qrcode)
                qr = qr.convert("RGB")

                # Converter imagem para QPixmap usando BytesIO
                buffer = io.BytesIO()
                qr.save(buffer, format="PNG")
                buffer.seek(0)

                pixmap = QPixmap()
                pixmap.loadFromData(buffer.read())

                self.label_qrcode.setPixmap(pixmap)
            else:
                self.label_qrcode.setText("Pedido não encontrado.")

        except Exception as e:
            self.label_qrcode.setText(f"Erro: {str(e)}")
