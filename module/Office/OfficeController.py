from module.EventHandler import EventHandler
from module.Office.Backroom import Backroom
from module.Office.Door import Door
from module.Office.MiniGame import MiniGame
from module.Office.Office import Office


class Office_controller:
    def __init__(self, screen, event_handler: EventHandler) -> None:
        self.screen = screen
        self.event_handler = event_handler

        self.office = Office()
        self.door = Door()
        self.backroom = Backroom()
        self.minigame = MiniGame()

        self.state = "Office"
        self.run_animation = True

        self.door_animation = False

    def render(self):
        if self.state == "Office":
            self.office.render(self.screen)
            self.door.render(self.screen)
            self.door._run_animation(not self.event_handler.is_door_close)
        elif self.state == "Backroom":
            self.backroom.render(self.screen)
            self.minigame.behavior(self.event_handler.is_pc_on)
            self.minigame.render(self.screen)

    def process(self):
        self.event_handler.update_door()
        self.event_handler.score = self.minigame.logic.score
        if self.event_handler._is_facing_office:
            self.state = "Office"
        else:
            self.state = "Backroom"

        if self.event_handler.is_sumbit:
            self.minigame.logic.Swipe_right()
            self.event_handler.sumbit_order()

    def reset_office(self):
        self.minigame.logic.score = 0
        self.state = "Office"
        self.door._run_animation(self.event_handler.is_door_close)
