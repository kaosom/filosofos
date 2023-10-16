import threading
import time

# Definimos una clase llamada "Philosopher" que representa a un filósofo.
class Philosopher(threading.Thread):
    def __init__(self, id, left, right, butler):  # Cada filósofo tiene un número de identificación y dos palillos (izquierdo y derecho).
        threading.Thread.__init__(self)
        self.id = id  # Guardamos el número de identificación del filósofo.
        self.left = left  # Guardamos el palillo izquierdo.
        self.right = right  # Guardamos el palillo derecho.
        self.butler = butler  # Usamos un "butler" (mayordomo) para controlar el acceso de los filósofos a la mesa.

    def run(self):  # Esta función representa lo que hace un filósofo cuando comienza a "pensar" y "comer."
        for _ in range(1):  # Cada filósofo "piensa" y "come" 1 vez.
            self.butler.acquire()  # El filósofo adquiere el permiso del mayordomo para sentarse en la mesa.
            print(f"Filosofo {self.id} está pensando\n")  # Mostramos un mensaje de que el filósofo está pensando.
            time.sleep(2)  # Esperamos un poquito (0.1 segundos) para simular el pensamiento.
            self.left.acquire()  # El filósofo adquiere el palillo izquierdo.
            print(f"El filósofo {self.id} tomó el tenedor izquierdo.\n")
            time.sleep(2)  # Esperamos otro poquito para simular el proceso de tomar el palillo.
            self.right.acquire()  # El filósofo adquiere el palillo derecho.
            print(f"El filósofo {self.id} tomó el tenedor derecho.\n")
            print(f"Filosofo {self.id} está comiendo")  # Mostramos un mensaje de que el filósofo está comiendo.
            time.sleep(2)  # Esperamos un poquito para simular la comida.
            self.right.release()  # El filósofo libera el palillo derecho.
            self.left.release()  # El filósofo libera el palillo izquierdo.
            self.butler.release()  # El filósofo libera el permiso del mayordomo para que otro pueda sentarse a la mesa.
        print(f"El filósofo {self.id} ha terminado de pensar y comer\n")  # Mostramos un mensaje cuando el filósofo termina.

def main():
    num_philosophers = 5  # Hay 5 filósofos en la mesa.
    butler = threading.Semaphore(num_philosophers - 1)  # Creamos un semáforo que controla el acceso de los filósofos.
    chopsticks = [threading.Semaphore(1) for _ in range(num_philosophers)]  # Creamos los palillos con semáforos para que los usen los filósofos.
    philosophers = [Philosopher(i, chopsticks[i], chopsticks[(i + 1) % num_philosophers], butler) for i in range(num_philosophers)]  # Creamos a los filósofos y les damos los palillos y el mayordomo.

    for philosopher in philosophers:
        philosopher.start()  # Hacemos que los filósofos empiecen a "pensar" y "comer."

if __name__ == '__main__':
    main()  # Iniciamos el programa llamando a la función "main."