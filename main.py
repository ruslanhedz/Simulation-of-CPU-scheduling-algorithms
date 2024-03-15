import random
import copy
import csv
import sys

#deklarowanie list, zmiennych potrzebych dla pomiarów
list_of_Processes = list()
amount_of_series = 0
Process_Count = 0
Copy_for_fcfs = list()
Copy_for_sjf_non_preem = list()
Copy_for_sjf_preem = list()
turn_around_times = list()
waiting_times = list()

#ziarno random
random.seed(9191)

#funkcja generator, która generuje randomowe liczby i zapisuje do pliku tekstowego
def generator(Process_count, Arrival_Time_min, Arrival_Time_max, Exec_Time_min, Exec_Time_max,
              amount_of_series):
    file = open("list_Pocesses" + str(Process_count) + ".txt", 'w')
    for i in range(amount_of_series):
        if Arrival_Time_min != Arrival_Time_max:
            for i in range(Process_count):
                file.write(str(random.randint(Arrival_Time_min, Arrival_Time_max)) + ','
                        + str(random.randint(Exec_Time_min, Exec_Time_max)))
                file.write('\n')
        else:
            for i in range(Process_count):
                file.write(str(Arrival_Time_min) + ','
                       + str(random.randint(Exec_Time_min, Exec_Time_max)))
                file.write('\n')
    file.close()

#Klasa Process dla przeprowadzenie symulacji
class Process:
    def __init__(self, ArrivalTime, ExecTime):
        self.ArrivalTime = ArrivalTime
        self.ExecTime = ExecTime
        self.TurnAroundTime = 0
        self.WaitingTime = 0
        self.Execution = 0
        self.Complete = False

#Funkcja która wczystuje dane z pliku tekstowego
def read_the_file(path):
    file = open(path, 'r')
    for i in range(amount_of_series):
        list_of_Processes.append(list())
        for j in range(Process_Count):
            line = file.readline()
            charakteristics = line.split(',')
            process = Process(int(charakteristics[0]), int(charakteristics[1]))
            list_of_Processes[i].append(process)
    file.close()


#Funkcja symulacyjna FCFS
def FCFS(list):
    time = 0
    Queue = []
    while any(process.Complete == False for process in list):
        if Queue:
            if Queue[0].ExecTime == Queue[0].Execution:
                Queue[0].Complete = True
                Queue[0].TurnAroundTime = time - Queue[0].ArrivalTime
                Queue[0].WaitingTime = Queue[0].TurnAroundTime - Queue[0].ExecTime
                print("One process is done!")
                del Queue[0]
        for element in list:
            if element.ArrivalTime == time:
                Queue.append(element)
                print ("Przybył nowy process!!!")
        if Queue:
            Queue[0].Execution += 1
            print("[" + str(time) + "]" + "Executing with proces for "
              + str(Queue[0].Execution) + "time", end="    ")
            print("ExecTime of processes in queue now: [", end='')
            for i in range(len(Queue)):
                if i == len(Queue) - 1:
                    print(Queue[i].ExecTime, end=']')
                    print('\n')
                else:
                    print(Queue[i].ExecTime, end=',')
        else:
            print("[" + str(time) + "]" + "There is no processes now")
        time += 1
    print("The end!!")

#Funkcja symulacyjna SJF Niewywłaszczeniowy
def SJF_Non_Preemtive(List):
    #list.sort(key=lambda x: x.ExecTime)
    time = 0
    Queue = []
    while any(process.Complete == False for process in List):
        if Queue:
            if Queue[0].ExecTime == Queue[0].Execution:
                Queue[0].Complete = True
                Queue[0].TurnAroundTime = time - Queue[0].ArrivalTime
                Queue[0].WaitingTime = Queue[0].TurnAroundTime - Queue[0].ExecTime
                print("One process is done!")
                del Queue[0]
        for element in List:
            if element.ArrivalTime == time:
                Queue.append(element)
                print("Przybył nowy process!!!")
                if len(Queue) >= 3:
                    if Queue[0].Execution != 0:
                        Queue[1:] = sorted(Queue[1:], key=lambda x: x.ExecTime)
                    else:
                        Queue.sort(key=lambda x: x.ExecTime)
        if Queue:
            Queue[0].Execution += 1
            print("[" + str(time) + "]" + "Executing with proces for "
                  + str(Queue[0].Execution) + "time", end="    ")
            print("ExecTime of processes in queue now: [", end='')
            for i in range(len(Queue)):
                if i == len(Queue) - 1:
                    print(Queue[i].ExecTime, end=']')
                    print('\n')
                else:
                    print(Queue[i].ExecTime, end=',')
        else:
            print("[" + str(time) + "]" + "There is no processes now")
        time += 1
    print("The end!!")

#Funkcja symulacyjna SJF Wywłaszczeniowy
def SJF_Preemtive(List):
    time = 0
    Queue = []
    while any(process.Complete == False for process in List):
        if Queue:
            if Queue[0].ExecTime == Queue[0].Execution:
                Queue[0].Complete = True
                Queue[0].TurnAroundTime = time - Queue[0].ArrivalTime
                Queue[0].WaitingTime = Queue[0].TurnAroundTime - Queue[0].ExecTime
                print("One process is done!")
                del Queue[0]
        Queue.sort(key=lambda x: x.ExecTime - x.Execution)
        for element in List:
            if element.ArrivalTime == time:
                Queue.append(element)
                print("Przybył nowy process!!!")
                Queue.sort(key=lambda x: x.ExecTime - x.Execution)

        if Queue:
            Queue[0].Execution += 1
            print("[" + str(time) + "]" + "Executing with proces for "
                  + str(Queue[0].Execution) + "time", end="    ")
            print("ExecTime of processes in queue now: [", end='')
            for i in range(len(Queue)):
                if i == len(Queue) - 1:
                    print(Queue[i].ExecTime, end=']')
                    print('\n')
                else:
                    print(Queue[i].ExecTime, end=',')
        else:
            print("[" + str(time) + "]" + "There is no processes now")
        time += 1
    print("The end!!")


#Funckja która wpisuje wyniki eksperymentów do plików csv
def write_to_scv(path, algoritm, List, Serie):
    file = open(path, 'w', newline='')
    header = ["Index", "Arrival Time", "Execution Time", "Turn Around Time", "Waiting Time"]
    csv_writer = csv.writer(file)
    csv_writer.writerow([algoritm])

    for i in range(Serie):
        csv_writer.writerow(["Seria", i+1])
        csv_writer.writerow(header)
        id = 0
        for process in List[i]:
            id += 1
            csv_writer.writerow(["P" + str(id), process.ArrivalTime, process.ExecTime, process.TurnAroundTime, process.WaitingTime])

    file.close()

#Program główny
if __name__=="__main__":
    while True:
        Process_Count = int(input("Wpisz ilość procesów: "))
        Arrival_Time_Min = int(input("Wpisz czas nadejścia minimalny: "))
        Arrival_Time_Max = int(input("Wpisz czas nadejścia maksymalny: "))
        Exec_Time_Min = int(input("Wpisz minimalny czas wykonania: "))
        Exec_Time_Max = int(input("Wpisz maksymalny czas wykonania: "))
        amount_of_series = int(input("Wpisz ilość serii testów: "))
        generator(Process_Count, Arrival_Time_Min, Arrival_Time_Max, Exec_Time_Min, Exec_Time_Max, amount_of_series)
        read_the_file("list_Pocesses" + str(Process_Count) + ".txt")
        Copy_for_fcfs = copy.deepcopy(list_of_Processes)
        Copy_for_sjf_non_preem = copy.deepcopy(list_of_Processes)
        Copy_for_sjf_preem = copy.deepcopy(list_of_Processes)
        sys.stdout = open("output" + str(Process_Count) + ".txt", 'w')
        print("_________________________________FCFS____________________________________")
        for i in range(amount_of_series):
            print("Seria: " + str(i+1))
            FCFS(Copy_for_fcfs[i])
        print("____________________________SJF Non Preemtive_____________________________")
        for i in range(amount_of_series):
            print("Seria: " + str(i + 1))
            SJF_Non_Preemtive(Copy_for_sjf_non_preem[i])
        print("_____________________________SJF Preemtive________________________________")
        for i in range(amount_of_series):
            print("Seria: " + str(i + 1))
            SJF_Preemtive(Copy_for_sjf_preem[i])
        sys.stdout.close()
        sys.stdout = sys.__stdout__
        write_to_scv("Wyniki " + "FCFS" + str(Process_Count) + ".csv", "FCFS", Copy_for_fcfs, amount_of_series)
        write_to_scv("Wyniki " + "SJFNon" + str(Process_Count) + ".csv", "SJF Non Preemtive", Copy_for_sjf_non_preem, amount_of_series)
        write_to_scv("Wyniki " + "SJF" + str(Process_Count) + ".csv", "SJF Preemtive", Copy_for_sjf_preem, amount_of_series)

        list_of_Processes.clear()
        Copy_for_fcfs.clear()
        Copy_for_sjf_non_preem.clear()
        Copy_for_sjf_preem.clear()
