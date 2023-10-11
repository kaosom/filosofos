import threading 
import time

# Definimos una clase llamada "Semaphore" que nos permite controlar el acceso a recursos compartidos.
class Semaphore:
    def __init__(self, initial):  # Cuando creamos un "Semaphore", necesitamos darle un número inicial.
        self.lock = threading.Condition(threading.Lock())  # Creamos una especie de cerrojo o "lock" que ayuda a mantener el orden.
        self.value = initial  # Guardamos el número inicial de recursos disponibles.

    # Up y Down se usa para aumentar o disminuir el valor del semaforo
    
    def up(self):  # Esta función permite aumentar el número de recursos disponibles.
        with self.lock:  # Usamos el cerrojo para asegurarnos de que nadie más toque los recursos al mismo tiempo.
            self.value += 1  # Agregamos un recurso.
            self.lock.notify()  # Le decimos a otros que un recurso está disponible.

    def down(self):  # Esta función permite tomar un recurso.
        with self.lock:  # Usamos el cerrojo para asegurarnos de que nadie más tome los recursos al mismo tiempo.
            while self.value == 0:  # Si no hay recursos disponibles, esperamos.
                self.lock.wait()
            self.value -= 1  # Tomamos un recurso.
            
# Definimos una clase llamada "Chopstick" que representa un palillo.
class Chopstick:
    def __init__(self, id):  # Cada palillo tiene un número de identificación.
        self.id = id
        self.user = -1  # Inicialmente, ningún filósofo está usando el palillo.
        self.lock = threading.Condition(threading.Lock())  # Al igual que con el "Semaphore," usamos un cerrojo para controlar el acceso.
        self.taken = False  # Inicialmente, el palillo no está siendo usado por nadie. Este es el estado por si alguien lo esta usando. 

    def take(self, user):  # Esta función permite a un filósofo tomar un palillo.
        with self.lock:  # Usamos el cerrojo para asegurarnos de que solo un filósofo tome el palillo a la vez.
            while self.taken:  # Si alguien más está usando el palillo, esperamos.
                self.lock.wait()
            self.user = user  # El filósofo toma el palillo y se convierte en su usuario.
            self.taken = True  # Marcamos el palillo como "tomado."
            print(f"Filosofo {user} toma el palillo {self.id}\n")  # Mostramos un mensaje de que el filósofo ha tomado el palillo.
            self.lock.notify_all()  # Avisamos a otros filósofos que el palillo ha sido tomado.

    def drop(self, user):  # Esta función permite a un filósofo soltar un palillo.
        with self.lock:  # Usamos el cerrojo para asegurarnos de que solo un filósofo suelte el palillo a la vez.
            while not self.taken:  # Si el palillo no está siendo usado, esperamos.
                self.lock.wait()
            self.user = -1  # El filósofo deja de ser el usuario del palillo.
            self.taken = False  # Marcamos el palillo como "no tomado."
            print(f"Filosofo {user} deja el palillo {self.id}\n")  # Mostramos un mensaje de que el filósofo ha soltado el palillo.
            self.lock.notify_all()  # Avisamos a otros filósofos que el palillo ha sido soltado.

# Definimos una clase llamada "Philosopher" que representa a un filósofo.
class Philosopher(threading.Thread):
    def __init__(self, id, left, right, butler):  # Cada filósofo tiene un número de identificación y dos palillos (izquierdo y derecho).
        threading.Thread.__init__(self)
        self.id = id  # Guardamos el número de identificación del filósofo.
        self.left = left  # Guardamos el palillo izquierdo.
        self.right = right  # Guardamos el palillo derecho.
        self.butler = butler  # Usamos un "butler" (mayordomo) para controlar el acceso de los filósofos a la mesa.

    def run(self):  # Esta función representa lo que hace un filósofo cuando comienza a "pensar" y "comer."
        for _ in range(1):  # Cada filósofo "piensa" y "come" 1 vece.
            self.butler.down()  # El filósofo le pide permiso al mayordomo para sentarse en la mesa.
            print(f"Filosofo {self.id} está pensando\n")  # Mostramos un mensaje de que el filósofo está pensando.
            time.sleep(0.1)  # Esperamos un poquito (0.1 segundos) para simular el pensamiento.
            self.left.take(self.id)  # El filósofo toma el palillo izquierdo.
            time.sleep(0.1)  # Esperamos otro poquito para simular el proceso de tomar el palillo.
            self.right.take(self.id)  # El filósofo toma el palillo derecho.
            print(f"Filosofo {self.id} está comiendo")  # Mostramos un mensaje de que el filósofo está comiendo.
            time.sleep(0.1)  # Esperamos un poquito para simular la comida.
            self.right.drop(self.id)  # El filósofo suelta el palillo derecho.
            self.left.drop(self.id)  # El filósofo suelta el palillo izquierdo.
            self.butler.up()  # El filósofo le avisa al mayordomo que ha terminado de comer.
        print(f"El filósofo {self.id} ha terminado de pensar y comer")  # Mostramos un mensaje cuando el filósofo termina.

def main():
    num_philosophers = 5  # Hay 6 filósofos en la mesa.
    butler = Semaphore(num_philosophers - 1)  # Creamos un mayordomo que controla el acceso de los filósofos.
    chopsticks = [Chopstick(i) for i in range(num_philosophers)]  # Creamos los palillos para que los usen los filósofos.
    philosophers = [Philosopher(i, chopsticks[i], chopsticks[(i + 1) % num_philosophers], butler) for i in range(num_philosophers)]  # Creamos a los filósofos y les damos los palillos y el mayordomo.

    for philosopher in philosophers:
        philosopher.start()  # Hacemos que los filósofos empiecen a "pensar" y "comer."

if __name__ == '__main__':
    main()  # Iniciamos el programa llamando a la función "main."
