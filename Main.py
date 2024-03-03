import simpy
import numpy as np

np.random.seed = 10

num_inst = np.random.randint(1, 11)
num_mem = np.random.randint(1, 11)

intervalo = 10

max_procesos = 25

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
        print(f"{self.env.now} Proceso {self.name} obtiene {self.memoria} unidades de memoria.")

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
                yield self.env.timeout(np.random.exponential(1.0 / intervalo))


                # Al finalizar la ejecución, decide el estado siguiente
                if self.instrucciones == 0:
                    print(f"{self.env.now} Proceso {self.name} Terminado.")
                else:
                    io_decision = np.random.randint(1, 3)
                    if io_decision == 1:
                        print(f"{self.env.now} Proceso {self.name} Esperando por I/O.")
                        yield self.env.process(self.wait_for_io())
                    elif io_decision == 2:
                        print(f"{self.env.now} Proceso {self.name} Listo para continuar.")
                        self.ram_put()

    def ram_get(self):
        return self.ram.get(self.memoria)

    def ram_put(self):
        self.ram.put(self.memoria)


    def wait_for_io(self):
        yield self.env.timeout(np.random.randint(1, 3))
        print(f"{self.env.now} Proceso {self.name} Retorna de I/O y está listo para continuar.")


def crear_procesos(env, ram, cpu, max_procesos, freq=1):
    for i in range(max_procesos):
        proceso = Proceso(f"Proceso_{i}", env, ram, cpu)
        env.process(proceso.run())
        yield env.timeout(freq)

# Configuración de la simulación
env = simpy.Environment()
RAM = simpy.Container(env, init=100, capacity=100)
CPU = simpy.Resource(env, capacity=1)

# Iniciar la simulación
env.process(crear_procesos(env, RAM, CPU, max_procesos))
env.run()
