from numpy.random.mtrand import randint

from module.Corountine import Corountine


class AnimatonicSystem:
    def __init__(self, aggro_rate, seconds) -> None:
        self.aggro_rate = aggro_rate
        self.current_sprite = ""

        self.__aggro = 0
        self.__state, self.__max_state = 0, 5
        self.__corountine = Corountine(self.__will_move, seconds)

    def start(self):
        self.__corountine.start()

    def stop(self):
        self.__corountine.stop()

    def get_sprite_for_state(self):
        pass

    def __will_move(self):
        chosen_number = randint(1, 10)
        if chosen_number >= (7 - self.__aggro):
            self.__changing_state()
            self.__aggro = 0
            return

        self.__aggro += 1 * self.aggro_rate
        print("Failed to move!")

    def __changing_state(self):
        if self.__state == self.__max_state:
            self.__prepare_attack()
            self.__state = 0
            return

        self.__state += 1

    def __prepare_attack(self):
        print("Gonna Attack!")
