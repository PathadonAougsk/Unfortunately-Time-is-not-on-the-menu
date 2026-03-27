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
        if self.event_handler._is_facing_office:
            self.state = "Office"
        else:
            self.state = "Backroom"
