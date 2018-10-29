
class Model:

    def __init__(self):

        inputfile = open("input.txt", "r")

        firstline = inputfile.readline()
        print(firstline)
        secondline = inputfile.readline()
        print(secondline)
        num_processes = firstline[0]
        num_resources = secondline[0]

        self.num_processes = int(num_processes)
        self.num_resources = int(num_resources)
        self.requestList = []
        self.currentRequest = 0

        for line in inputfile:
            self.requestList.append(line)

        print(self.num_processes)
        print(self.num_resources)
        print(self.requestList)

        self.state_dict = {}

        for i in range(self.num_processes):
            request_list = []
            holds_list = []
            self.state_dict[i] = []
            self.state_dict[i].append(request_list)
            self.state_dict[i].append(holds_list)

    def next_step(self):
        pass

    def request_resource(self, process_num, resource_num):
        self.state_dict[process_num][1].append(resource_num)

    def take_resource(self, process_num, resource_num):
        self.state_dict[process_num][0].append(resource_num)

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

    def parse_statement(self, current_request):
        statement = self.requestList[current_request]
        split_statement = statement.split()

        process_num = split_statement[0][1:]
        keyword = split_statement[1]
        resource_num = split_statement[2][1:]

        print(process_num, keyword, resource_num)


a = Model()
print(a.state_dict)
a.request_check(0, 1)
print(a.state_dict)
a.request_check(1,1)
print(a.state_dict)
a.release(0,1)
print(a.state_dict)
#a.parse_statement(0)
