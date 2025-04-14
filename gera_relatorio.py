import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget
from PyQt5 import uic
from fpdf import FPDF

# Dados de exemplo para o relatório
dados = [
    ["Produto", "Quantidade", "Preço Unitário", "Total"],
    ["Agua Mineral", "10", "R$ 0,50", "R$ 5,00"],
    ["Pizza de Mussarela", "8", "R$ 0,30", "R$ 2,40"],
    ["Refrigerante Fanta Laranja", "100", "R$ 0,70", "R$ 3,50"]
]

class MainRelatorio(QMainWindow):
    def __init__(self):
        super().__init__()
        # Carregar o arquivo .ui diretamente
        uic.loadUi("janela.ui", self)

        # Alterar texto do botão
        self.btnGerarRelatorio.setText("Gerar PDF")

        # Conectar o botão à função
        self.btnGerarRelatorio.clicked.connect(self.gerar_pdf)

        # Criar e configurar a tabela
        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(len(dados))
        self.tableWidget.setColumnCount(len(dados[0]))
        
        # Definir cabeçalhos
        headers = dados[0]
        self.tableWidget.setHorizontalHeaderLabels(headers)
        
        # Preencher tabela com dados
        for row_idx, row in enumerate(dados[1:], 1):  # Começa do 1 para pular o cabeçalho
            for col_idx, item in enumerate(row):
                self.tableWidget.setItem(row_idx, col_idx, QTableWidgetItem(item))
        
        # Ajustar tamanho das colunas
        self.tableWidget.resizeColumnsToContents()
        
        # Adicionar tabela a um layout existente no .ui
        # Assumindo que existe um QWidget chamado 'centralWidget' ou um layout
        central_widget = self.centralWidget()
        if central_widget.layout() is None:
            layout = QVBoxLayout()
            central_widget.setLayout(layout)
        else:
            layout = central_widget.layout()
        
        layout.addWidget(self.tableWidget)
        # Garantir que o botão não seja sobrescrito
        if self.btnGerarRelatorio not in [layout.itemAt(i).widget() for i in range(layout.count())]:
            layout.addWidget(self.btnGerarRelatorio)

    def gerar_pdf(self):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, "Relatório de Vendas", ln=True, align="C")
        pdf.ln(10)

        pdf.set_font("Arial", size=12)
        col_widths = [50, 40, 50, 40]

        for row in dados:
            for i, item in enumerate(row):
                pdf.cell(col_widths[i], 10, item, border=1)
            pdf.ln()

        try:
            pdf.output("relatorio.pdf")
            QMessageBox.information(self, "Sucesso", "Relatório PDF gerado com sucesso!")
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao gerar PDF:\n{str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainRelatorio()
    window.show()
    sys.exit(app.exec_())