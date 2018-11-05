from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import networkx as nx

class View(QWidget):

    NumButtons = ['update']

    def __init__(self, model):
        super(View, self).__init__()
        font = QFont()
        font.setPointSize(16)

        self.initUI(model)

    def initUI(self, model):

        self.setGeometry(100, 100, 800, 600)
        #self.center()
        self.setWindowTitle('S Plot')
        grid = QGridLayout()
        self.setLayout(grid)
        self.createVerticalGroupBox()
        self.model = model
        self.num_processes = self.model.num_processes
        self.num_resources = self.model.num_resources


        buttonLayout = QVBoxLayout()
        buttonLayout.addWidget(self.verticalGroupBox)

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)        
        grid.addWidget(self.canvas, 0, 1, 9, 9)          
        grid.addLayout(buttonLayout, 0, 0)

        self.display(self.model.state_dict)
        self.show()


    def createVerticalGroupBox(self):
        self.verticalGroupBox = QGroupBox()

        layout = QVBoxLayout()
        for i in self.NumButtons:
                button = QPushButton(i)
                button.setObjectName(i)
                layout.addWidget(button)
                layout.setSpacing(10)
                self.verticalGroupBox.setLayout(layout)
                button.clicked.connect(self.update)


    def update(self):
        self.model.next_step()

    def set_state_dict(self, state_dict):
        self.state_dict = state_dict
        self.display(state_dict)


    def display(self, state_dict):
        self.figure.clf()
        print(state_dict, self.num_processes, self.num_resources)
        G = nx.cubical_graph()
        G = G.to_directed()

        processes = []
        resources = []

        labels = {}

        for i in range(self.num_processes):
            processes.append(i)
            labels[i] = 'p' + str(i)

        for j in range(self.num_resources):
            resources.append(j + i + 1)
            var = j + i + 1
            labels[var] = 'r' + str(j)

        pos = nx.bipartite_layout(G, nodes=processes)
        #print('p', processes)
        #print('r', resources)
        nx.draw_networkx_nodes(G, pos,
                               nodelist=processes,
                               node_color='r',
                               node_size=500,
                               alpha=0.8)

        nx.draw_networkx_nodes(G, pos,
                               nodelist=resources,
                               node_color='b',
                               node_size=500,
                               alpha=0.8)

        edge_list_1 = []
        edge_list_2 = []

        for k, v in state_dict.items():
            for num in v[0]:
                edge_list_1.append((num + self.num_processes, k))

            for num2 in v[1]:
                edge_list_2.append((k, num2 + self.num_processes))

        nx.draw_networkx_edges(G, pos,
                               edgelist=edge_list_1,
                               width=1, alpha=1, arrows=True, arrowstyle='->', arrowsize=20)
        nx.draw_networkx_edges(G, pos,
                               edgelist=edge_list_2,
                               width=1, alpha=1, arrows=True, arrowstyle='->', arrowsize=20)
        nx.draw_networkx_labels(G, pos, labels, font_size=16)
        #nx.draw(G, pos=pos, with_labels=False)
        plt.axis('off')
        self.canvas.draw()
        #self.canvas.draw_idle()
