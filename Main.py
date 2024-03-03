import simpy
import numpy as np

np.random.seed = 1

num_inst = 100
num_mem = 40

class Proceso:

    def __init__(self, name, env, ram, cpu):
        self.name = name
        self.env = env
        self.ram = ram
        self.cpu = cpu

        self.instrucciones = num_inst # varriabke
        self.memoria = num_mem # variable

        self.hora_inicio = -1
        self.hora_fin = -2


    def run(self):
        # tiempo de inicio
        print(f"{self.env.now} Inicia proceso {self.name}.")

        ram = self.ram_get() # Solicita memoria
        yield ram # espera por memoria

        while self.instrucciones > 0: 
            with self.cpu.request() as cpu_req: # solicita cpu
                self.hora_inicio = self.env.now
                yield cpu_req


    def ram_get(self):
        return self.ram.get(self.memoria)

    def ram_put(self):
        self.ram.put(self.memoria)