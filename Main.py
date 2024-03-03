import simpy
import numpy as np

np.random.seed = 1

num_inst = 100
num_mem = 40

intervalo = 10

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
                yield self.env.timeout(1)

                for i in range(min(3, self.instrucciones)): # ejecuta sus instrucciones, el total es el numero de instrucciones, el numero de segundos
                    if self.instrucciones == 0:
                        break
                    else:
                        self.instrucciones -= 1
                        print(self.name, self.instrucciones)
                yield self.env.timeout(np.random.expovariate(1.0 / intervalo))


    def ram_get(self):
        return self.ram.get(self.memoria)

    def ram_put(self):
        self.ram.put(self.memoria)

def crear_procesos(env, ram, cpu, max_num = 25, freq = 1):
    for i in range(max_num):
        print(f"{env.now} -- {i}")