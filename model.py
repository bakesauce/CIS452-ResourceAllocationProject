import networkx as nx
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from view import View

class Model:

    def __init__(self):

        inputfile = open("input.txt", "r")

        firstline = inputfile.readline()
        print(firstline)
        secondline = inputfile.readline()
        print(secondline)
        num_processes = firstline[0]
        num_resources = secondline[0]

        self.view = None
        self.num_processes = int(num_processes)
        self.num_resources = int(num_resources)
        self.statement_list = []
        self.current_statement_counter = 0
        self.request_dict = {}

        for i in range(self.num_resources):
            self.request_dict[i] = []

        for line in inputfile:
            self.statement_list.append(line)

        print(self.num_processes)
        print(self.num_resources)
        print(self.statement_list)

        self.state_dict = {}

        for i in range(self.num_processes):
            request_list = []
            holds_list = []
            self.state_dict[i] = []
            self.state_dict[i].append(request_list)
            self.state_dict[i].append(holds_list)

    def set_view(self, view):
        self.view = view

    def next_step(self):
        if self.current_statement_counter >= len(self.statement_list):
            print('finished')
        else:
            self.parse_statement(self.current_statement_counter)
            self.current_statement_counter += 1

        self.view.set_state_dict(self.state_dict)
        #self.view.display(self.state_dict, self.num_processes, self.num_resources)

    def request_resource(self, process_num, resource_num):
        self.state_dict[process_num][1].append(resource_num)
        self.request_dict[resource_num].append(process_num)

    def take_resource(self, process_num, resource_num):
        self.state_dict[process_num][0].append(resource_num)
        if resource_num in self.state_dict[process_num][1]:
            self.state_dict[process_num][1].remove(resource_num)

    def request_check(self, process_num, resource_num):
        was_found = False

        for k, v in self.state_dict.items():
            if k == process_num:
                continue
            else:
                if resource_num in v[0]:
                    was_found = True
                    continue
                else:
                    continue

        if was_found is False:
            self.take_resource(process_num, resource_num)
            return 0
        else:
            self.request_resource(process_num, resource_num)

            return -1

    def release(self, process_num, resource_num):
        self.state_dict[process_num][0].remove(resource_num)
        #print('request dict ', self.request_dict)
        #print(resource_num)
        #print(process_num)
        if self.request_dict[resource_num]:
            #print(self.request_dict)
            #print('process num found', self.request_dict[resource_num][0])
            if self.request_check(self.request_dict[resource_num][0], resource_num) == 0:
                self.request_dict[resource_num].pop()
            else:
                pass #problem above

        else:
            pass

    def parse_statement(self, current_statement_counter):
        statement = self.statement_list[current_statement_counter]
        split_statement = statement.split()

        process_num = int(split_statement[0][1:])
        keyword = split_statement[1]
        resource_num = int(split_statement[2][1:])

        print(process_num, keyword, resource_num)

        if keyword == 'releases':
            self.release(process_num, resource_num)
        else:
            #print(process_num, resource_num)
            self.request_check(process_num, resource_num)

"""
    def draw_graph(self, state_dict):
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
        print('p', processes)
        print('r', resources)
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
        for k,v in state_dict.items():
            for num in v[0]:
                print(k,num)
                edge_list_1.append((num+self.num_processes, k))

            for num2 in v[1]:
                edge_list_2.append((k, num2 + self.num_processes))

        nx.draw_networkx_edges(G, pos,
                               edgelist=edge_list_1,
                               width=1, alpha=1, arrows=True, arrowstyle='->', arrowsize=20)
        nx.draw_networkx_edges(G, pos,
                               edgelist=edge_list_2,
                               width=1, alpha=1, arrows=True, arrowstyle='->', arrowsize=20)
        nx.draw_networkx_labels(G, pos, labels, font_size=16)
        plt.axis('off')
        plt.show()
"""

if __name__ == '__main__':

    import sys
    app = QApplication(sys.argv)
    app.aboutToQuit.connect(app.deleteLater)
    app.setStyle(QStyleFactory.create("gtk"))
    model = Model()
    view = View(model)
    model.set_view(view)
    #screen = view
    #screen.show()
    sys.exit(app.exec_())


"""
a = Model()
a.draw_graph(a.state_dict)

print(a.state_dict)
print()
a.next_step()
a.draw_graph(a.state_dict)
print(a.state_dict)
print()
a.next_step()
a.draw_graph(a.state_dict)
print(a.state_dict)
print()
a.next_step()
a.draw_graph(a.state_dict)
print(a.state_dict)
print()
a.next_step()
a.draw_graph(a.state_dict)
print(a.state_dict)
print()
a.next_step()
a.draw_graph(a.state_dict)
print(a.state_dict)
print()
a.next_step()
a.draw_graph(a.state_dict)
print(a.state_dict)
print()
a.next_step()
a.draw_graph(a.state_dict)
print(a.state_dict)
print()
a.next_step()
a.draw_graph(a.state_dict)
print(a.state_dict)
print()
a.next_step()
a.draw_graph(a.state_dict)
print(a.state_dict)
print()
a.next_step()
a.draw_graph(a.state_dict)
print(a.state_dict)
print()
a.next_step()
a.draw_graph(a.state_dict)
print(a.state_dict)
print()
a.next_step()
a.draw_graph(a.state_dict)
print(a.state_dict)
print()
a.next_step()
a.draw_graph(a.state_dict)
print(a.state_dict)
print()

a.next_step()
print(a.state_dict)
print()
print(a.request_dict)

a.draw_graph(a.state_dict)
"""

