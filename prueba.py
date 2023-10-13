from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QSpinBox, QDoubleSpinBox, QFrame, QLabel, QAbstractSpinBox, QScrollArea, QComboBox, QLineEdit,QPushButton
import numpy as np
import random
import sys
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


class tableItem(QDoubleSpinBox):
    valores = None
    def __init__(self, tableName, row, column,spinboxe):
        super().__init__()

        self.tableName = tableName
        self.spinboxe = spinboxe
        self.row = row
        self.column = column

        self.setMinimum(-9999)
        self.setMaximum(9999)
        self.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)

    def get_values(self):
        return {"tableName": self.tableName, "row": self.row, "column": self.column, "value": self.value(),"Dimension": self.spinboxe}


class SpinboxTableApp(QWidget):
    __Opciones = ["Suma","Resta","Producto","Inversa","Resolver por metodo de Gauss Jordan", "Resolver por regla de Cramer"]
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        self.result_label = QLabel()
        
        tablesLayout = QHBoxLayout()

        table1 = QScrollArea()
        self.frame = QFrame()
        v_table1_layout = QVBoxLayout()
        v_table1_layout.setContentsMargins(0, 0, 0, 0)
        v_table1_layout.setSpacing(0)
        self.frame.setLayout(v_table1_layout)
        table1.setWidget(self.frame)  # Set the widget to the scroll area
        table1.setWidgetResizable(True)  # Make the widget resizable
        tablesLayout.addWidget(table1)

        #cambio de operacion
        tablesLayout.addWidget(QLabel("+I*I-1"))

        self.table2 = QScrollArea()
        self.frame2 = QFrame()
        v_table2_layout = QVBoxLayout()
        v_table2_layout.setContentsMargins(0, 0, 0, 0)
        v_table2_layout.setSpacing(0)
        self.frame2.setLayout(v_table2_layout)
        self.table2.setWidget(self.frame2)  # Set the widget to the scroll area
        self.table2.setWidgetResizable(True)  # Make the widget resizable
        tablesLayout.addWidget(self.table2)

        tablesLayout.addWidget(QLabel("="))

        frameTotal = QFrame()
        tableTotal_layout = QVBoxLayout()
        tableTotal_layout.setContentsMargins(0, 0, 0, 0)
        tableTotal_layout.setSpacing(0)
        frameTotal.setLayout(tableTotal_layout)

        self.tableTotal = QScrollArea()
        
        self.frameTotal = QFrame()
        v_tableTotal_layout = QVBoxLayout()
        v_tableTotal_layout.setContentsMargins(0, 0, 0, 0)
        v_tableTotal_layout.setSpacing(0)
        self.frameTotal.setLayout(v_tableTotal_layout)
        
        self.tableTotal.setWidget(self.frameTotal)  # Set the widget to the scroll area
        self.tableTotal.setWidgetResizable(True)  # Make the widget resizable

        self.gausTotal = QLabel()
        tableTotal_layout.addWidget(self.gausTotal)
        tableTotal_layout.addWidget(self.tableTotal)

        tablesLayout.addWidget(frameTotal)

        self.tableSize = QSpinBox()
        self.tableSize.valueChanged.connect(self.make_tables)
        layout.addWidget(self.tableSize)

        self.make_tables()

        #lista opciones
        self.options = QComboBox()
        self.options.currentIndexChanged.connect(self.update)
        self.options.addItems(self.__Opciones)
        
        layout.addWidget(self.options)

        #terminos indepentdientes
        terms_label = QLabel('Términos Independientes (separalos por coma):')
        layout.addWidget(terms_label)
        self.input_line = QLineEdit()
        self.input_line.textChanged.connect(self.update)
        layout.addWidget(self.input_line)

        layout.addWidget(self.result_label)

        #boton_graficar
        self.plot = QPushButton("Graficar")
        layout.addWidget(self.plot)
        self.plot.clicked.connect(self.plotgraph)


        self.plot.hide()


        layout.addLayout(tablesLayout)
        self.setWindowTitle('Spinbox Table App')
        self.setGeometry(100, 100, 400, 300)

        self.setLayout(layout)

    def make_tables(self):
        dimension = (self.tableSize.value(), self.tableSize.value())
        self.matriz1 = np.zeros(dimension)
        self.matriz2= np.zeros(dimension)
        self.__matriz_resultante = np.zeros(dimension)
        

        self.make_table(tableName="Table1", tableFrame=self.frame)
        self.make_table(tableName="Table2", tableFrame=self.frame2)
        self.make_table(tableName="TableTotal", tableFrame=self.frameTotal, total_values=self.__matriz_resultante)

    def make_table(self, tableName, tableFrame, total_values=None):
        for row in reversed(range(tableFrame.layout().count())):
            widget = tableFrame.layout().itemAt(row).widget()
            if widget is not None:
                widget.deleteLater()
                widget.setParent(None)

        for row in range(self.tableSize.value()):
            frame = QFrame()
            h_table_layout = QHBoxLayout()
            h_table_layout.setContentsMargins(0, 0, 0, 0)
            h_table_layout.setSpacing(0)
            for column in range(self.tableSize.value()):
                spinbox = tableItem(tableName, row, column,self.tableSize.value())
                if total_values is not None:
                    spinbox.setValue(total_values[row][column])
                    spinbox.setReadOnly(True)
                spinbox.valueChanged.connect(self.tableEdited)
                h_table_layout.addWidget(spinbox)
            frame.setLayout(h_table_layout)
            tableFrame.layout().addWidget(frame)
    

    def plotgraph(self):
        if len(self.__matriz_resultante) == 3:
            x_coeficiente = self.__matriz_resultante[0]
            y_coeficiente = self.__matriz_resultante[1]
            z_coeficiente = self.__matriz_resultante[2]
            #creamos datos para graficarlos en el plano
            x = np.linspace(-10, 10, 100)
            y = np.linspace(-10, 10, 100)
            x, y = np.meshgrid(x, y)
            
            z = (x_coeficiente * x - y_coeficiente * y) / z_coeficiente
            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')

            # Graficar el plano
            ax.plot_surface(x, y, z, alpha=0.5, rstride=100, cstride=100, color='cyan')

            # Configuraciones adicionales
            ax.set_xlabel('X')
            ax.set_ylabel('Y')  
            ax.set_zlabel('Z')
            ax.set_title('Plano resultante del sistema de ecuaciones')

            plt.show()




    def tableEdited(self):
        sender = self.sender()
        self.valores = sender.get_values()

        if self.valores['tableName'] == 'Table1':
            self.matriz1[self.valores['row'], self.valores['column']] = self.valores['value']
        else:
            self.matriz2[self.valores['row'], self.valores['column']] = self.valores['value']
            print(self.matriz2)
        self.update()
    
    def update(self):
        self.tableTotal.show()
        self.gausTotal.hide()
        self.result_label.setText("")
        self.table2.show()
        if self.options.currentText() == "Suma":
            self.matriz_resultante = np.add(self.matriz1,self.matriz2)
            self.make_table("TableTotal", self.frameTotal, self.matriz_resultante)
        
        elif self.options.currentText() == "Resta":
            print("es resta")
            self.matriz_resultante = np.subtract(self.matriz1,self.matriz2)
            self.make_table("TableTotal", self.frameTotal, self.matriz_resultante)
        
        elif self.options.currentText() == "Producto":
             self.matriz_resultante = np.dot(self.matriz1,self.matriz2)
             self.make_table("TableTotal", self.frameTotal, self.matriz_resultante)

        elif self.options.currentText() == "Inversa":
            self.table2.hide()
            try:
                 self.matriz_resultante = np.linalg.inv(self.matriz1)
                 self.make_table("TableTotal", self.frameTotal, self.matriz_resultante)
            except:
                 print("La matrizz no tiene inversa")

        elif self.options.currentText() == "Resolver por metodo de Gauss Jordan":
            self.table2.hide()
            
            self.tableTotal.hide()
            self.gausTotal.show()
            self.plot.show()
            self.plot.setDisabled(True)
            try:
                augmented_matrix = np.column_stack((self.matriz1, [float(n) for n in self.input_line.text().split(',')]))
                rows, cols = augmented_matrix.shape

                for i in range(rows):
                    if augmented_matrix[i][i] == 0.0: #equqals to 0 == return
                        return

                    for j in range(rows):
                        if i != j:
                            ratio = augmented_matrix[j][i] / augmented_matrix[i][i]

                            for k in range(cols):
                                augmented_matrix[j][k] = augmented_matrix[j][k] - ratio * augmented_matrix[i][k]

                # Obtener la solución
                for i in range(rows):
                    augmented_matrix[i] = augmented_matrix[i] / augmented_matrix[i][i]

                self.__matriz_resultante = augmented_matrix[:, -1]
                print(f'Resultado: {self.__matriz_resultante}')
                self.gausTotal.setText(f'Resultado:\n x: {self.__matriz_resultante[0]} \n y: {self.__matriz_resultante[1] } z: {self.__matriz_resultante[2]}')
                self.make_table("TableTotal", self.frameTotal, self.matriz1)  # La solución es una lista de valores
                self.plot.setEnabled(True)



            except ValueError:
                    self.result_label.setText('Entrada inválida. Asegúrate de ingresar los términos independientes correctamente.')


        
             
             
        

            


            

        

def main():
    app = QApplication(sys.argv)
    window = SpinboxTableApp()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
