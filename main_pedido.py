import sys
from PyQt5 import uic, QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QPushButton, QWidget, QHBoxLayout, QTableWidgetItem
import mysql.connector
from novo_pedido import NovoPedido
from edita_pedido import EditarPedido
from lista_clientes import ListaClientes
from lista_entregadores import ListaEntregadores  
from lista_produtos import ListaProdutos
from gera_qrcode import GeraQrcode
from gera_relatorio import MainRelatorio

class MainPedidos(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("main_pedidos.ui", self)

        self.carregar_pedidos()
        self.pushButton.clicked.connect(self.abrir_novo_pedido)
        self.pushButton_6.clicked.connect(self.carregar_pedidos)
        self.pushButton_2.clicked.connect(self.abrir_lista_clientes)
        self.pushButton_4.clicked.connect(self.abrir_lista_entregadores)
        self.pushButton_3.clicked.connect(self.abrir_lista_produtos)
        self.pushButton_5.clicked.connect(self.abrir_relatorio)
    
    def carregar_pedidos(self):
        print("Botão Atualizar clicado!")
        self.conexao = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="crud"
        )
        
        query = '''
            SELECT pedidos.id_pedido, pedidos.data, pedidos.hora, clientes.nome, 
                pedidos.endereco_entrega, pedidos.total, pedidos.status 
            FROM pedidos 
            JOIN clientes ON pedidos.cliente_id = clientes.id_cliente
            ORDER BY pedidos.data DESC, pedidos.hora DESC
        '''
        
        cursor = self.conexao.cursor()
        cursor.execute(query)
        self.dados = cursor.fetchall()  # Armazenar os dados como atributo da classe
        cursor.close()
        
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(8)
        self.tableWidget.setHorizontalHeaderLabels(["ID", "Data", "Hora", "Cliente", "Endereço", "Total", "Status", "Ações"])
        self.tableWidget.setRowCount(len(self.dados))
        
        for row_idx, row_data in enumerate(self.dados):
            for col_idx, col_data in enumerate(row_data):
                self.tableWidget.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))
            
            widget = QWidget()
            layout = QHBoxLayout(widget)
            layout.setContentsMargins(0, 0, 0, 0)
            
            button_detalhes = QPushButton("Detalhes")
            button_qrcode = QPushButton("QrCode")
            
            button_detalhes.clicked.connect(lambda _, r=row_idx: self.detalhes_clicked(r))
            button_qrcode.clicked.connect(lambda _, r=row_idx: self.qrcode_clicked(r))
            
            layout.addWidget(button_detalhes)
            layout.addWidget(button_qrcode)
            widget.setLayout(layout)
            
            self.tableWidget.setCellWidget(row_idx, 7, widget)  # Ajustado para coluna 7

        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
    
    def detalhes_clicked(self, row):
        # Pegar os dados da linha clicada
        pedido_data = self.dados[row] 
        id_pedido = pedido_data[0]  
        self.detalhes_window = EditarPedido(id_pedido=id_pedido)
        self.detalhes_window.show()
    
    def qrcode_clicked(self, row):

        pedido_data = self.dados[row] 
        id_pedido = pedido_data[0]  
        self.detalhes_window = GeraQrcode(id_pedido=id_pedido)
        self.detalhes_window.show()
    
    def abrir_novo_pedido(self):
        self.novo_pedido_window = NovoPedido()
        self.novo_pedido_window.show()

    def abrir_lista_clientes(self):
        self.lista_clientes_window = ListaClientes()
        self.lista_clientes_window.show()

    def abrir_lista_entregadores(self):
        self.lista_clientes_window = ListaEntregadores()
        self.lista_clientes_window.show()
        
    def abrir_lista_produtos(self):
        self.lista_clientes_window = ListaProdutos()
        self.lista_clientes_window.show()
    
    def abrir_relatorio(self):
        self.lista_clientes_window = MainRelatorio()
        self.lista_clientes_window.show()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainPedidos()
    window.show()
    sys.exit(app.exec_())