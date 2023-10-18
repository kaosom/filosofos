from threading import Thread, Semaphore
import random
import time

class DiningPhilosophers:
    '''
    P - Pensando 
    E - Esperando 
    C - Comiendo 
    F - Finalizado
    '''
    def __init__(self, number_of_philosophers, meal_size=1):
        self.meals = [meal_size for _ in range(number_of_philosophers)]
        self.chopsticks = [Semaphore(value=1) for _ in range(number_of_philosophers)]
        self.status = ['   U' for _ in range(number_of_philosophers)]
        self.chopstick_holders = ['     ' for _ in range(number_of_philosophers)]
        self.number_of_philosophers = number_of_philosophers

    def philosopher(self, i):
        j = (i + 1) % self.number_of_philosophers
        while self.meals[i] > 0:
            self.status[i] = '   P'
            time.sleep(random.random())
            self.status[i] = '   E'
            first_chopstick = i 
            second_chopstick = j 
            # Seleccionar el primer tenedor disponible
            if self.chopsticks[i]._value > 0: 
                if self.chopsticks[first_chopstick].acquire(timeout=1):
                    self.chopstick_holders[i] = ' ↙️  '
                    
                    # Intentar adquirir el segundo tenedor (derecho)
                    if self.chopsticks[second_chopstick].acquire(timeout=1):
                        self.chopstick_holders[i] =' ↙️ ↘️'
                        self.status[i] = '   C'
                        time.sleep(random.random())
                        self.meals[i] -= 1
                        self.chopsticks[second_chopstick].release()
                        self.chopstick_holders[i] =  ' ↙️  '
                    self.chopsticks[first_chopstick].release()
                    self.chopstick_holders[i] =  '    '   
                    self.status[i] = '   P'
            else: 
                if self.chopsticks[second_chopstick].acquire(timeout =1): 
                    self.chopstick_holders[i] = '   ↘️'
                    time.sleep(random.random())
                    if self.chopsticks[first_chopstick].acquire(timeout=1):
                        self.chopstick_holders[i] =' ↙️ ↘️'
                        self.status[i] = '   C'
                        time.sleep(random.random())
                        self.meals[i] -= 1
                        self.chopsticks[second_chopstick].release()
                        self.chopstick_holders[i] =  '   ↘️'
                    self.chopsticks[first_chopstick].release()
                    self.chopstick_holders[i] =  '    '
                    self.status[i] = '   P'
            self.status[i] = '   F'

    def print_status(self):
        header = "=" * (self.number_of_philosophers * 7)
        status_str = " ".join(self.status)
        holders_str = " ".join(self.chopstick_holders)
        total_meals = str(sum(self.meals))
        holders = [f"{i}   " if i != 5 else "0   " for i in range(self.number_of_philosophers + 1)]


        print(header.center(len(header)))
        print(status_str.center(len(status_str)))
        print(holders_str.center(len(holders_str)))
        holders_chop = " ".join(holders) 
        print(holders_chop.center(len(holders_chop)))
        print(f"Comidas totales: {total_meals}".center(len(header)))

def main():
    n = 5
    dining_philosophers = DiningPhilosophers(n)
    philosophers = [Thread(target=dining_philosophers.philosopher, args=(i,)) for i in range(n)]

    for philosopher in philosophers:
        philosopher.start()

    while sum(dining_philosophers.meals) > 0:
        dining_philosophers.print_status()
        time.sleep(0.1)
    dining_philosophers.print_status()

    for philosopher in philosophers:
        philosopher.join()

if __name__ == "__main__":
    main()