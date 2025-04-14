# from fpdf import FPDF
# import pandas as pd

# # Dados fictícios
# import pandas as pd

# df = pd.DataFrame({
#     'Clientes': ['Dan', 'Pedreirinha', '91952426549'],
#     'Produtos': ['Agua Mineral', 'Pizza de Mussarela', 'Suco de Laranja'],
#     'Entregadores': ['Senac', 'João', 'Maria']
# })

# print(df)

# # Criar PDF
# pdf = FPDF()
# pdf.add_page()
# pdf.set_font("Arial", size=12)

# # Título
# pdf.cell(200, 10, txt="Relatórios", ln=True, align='C')

# # Cabeçalho
# pdf.set_font("Arial", 'B', size=12)
# for coluna in df.columns:
#     pdf.cell(60, 10, coluna, border=1)
# pdf.ln()

# # Dados
# pdf.set_font("Arial", size=12)
# for i in range(len(df)):
#     for coluna in df.columns:
#         pdf.cell(60, 10, str(df[coluna][i]), border=1)
#     pdf.ln()

# pdf.output("relatorio.pdf")

# import sys
# import mysql.connector
# import qrcode
# from PyQt5.QtWidgets import QApplication, QDialog, QLabel, QVBoxLayout
# from PyQt5.QtGui import QPixmap
# from PyQt5.QtCore import Qt
# from PIL.ImageQt import ImageQt
# from PyQt5.QtGui import QImage
# import io
# from PIL import Image

# class GerarRelatorio(QDialog):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Relatorio")
#         self.resize(300, 300)
#         # self.id_pedido = id_pedido

#         # Conectar ao banco de dados
#         self.conexao = mysql.connector.connect(
#             host="localhost",
#             user="root",
#             password="",
#             database="crud"
#         )
#         self.cursor = self.conexao.cursor()

import sys
import mysql.connector
from PyQt5.QtWidgets import QApplication, QDialog, QLabel, QVBoxLayout, QMessageBox
from datetime import date

class GerarRelatorio(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Relatório de Pedidos do Dia")
        self.resize(400, 400)

        layout = QVBoxLayout()
        self.setLayout(layout)

        try:
            # Conectar ao banco de dados
            self.conexao = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="crud"
            )
            self.cursor = self.conexao.cursor()

            # Obter a data atual no formato 'YYYY-MM-DD'
            data_hoje = date.today().strftime('%Y-%m-%d')

            # Consultar os pedidos do dia
            query = "SELECT id_pedido, cliente_id, data FROM pedidos WHERE data = %s"
            self.cursor.execute(query, (data_hoje,))
            resultados = self.cursor.fetchall()

            if resultados:
                for pedido in resultados:
                    id_pedido, cliente_id, data = pedido
                    texto = f"ID: {id_pedido} | Cliente: {cliente_id} | Data: {data}"
                    layout.addWidget(QLabel(texto))
            else:
                layout.addWidget(QLabel("Nenhum pedido encontrado para hoje."))

        except mysql.connector.Error as erro:
            QMessageBox.critical(self, "Erro", f"Erro ao acessar o banco de dados:\n{erro}")
        finally:
            if self.cursor:
                self.cursor.close()
            if self.conexao:
                self.conexao.close()

# Execução da aplicação
if __name__ == "__main__":
    app = QApplication(sys.argv)
    janela = GerarRelatorio()
    janela.exec_()