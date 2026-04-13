from pathlib import Path

import pandas as pd
import pygame

from module.EventHandler import EventHandler


class Session:
    def __init__(self, eventhandler: EventHandler) -> None:
        self.excel_path = Path.cwd() / "Data.xlsx"
        columns = [
            "Timestamp",
            "Session Time",
            "Event type",
            "Threat Name",
            "Aggro level",
            "Action",
            "Survived",
            "Score",
            "Input Count",
        ]
        self.__df = pd.DataFrame(columns=columns)
        self.__start_sessions = self.__time_stamp()
        self.eventhandler = eventhandler

        self._start_tick: int = pygame.time.get_ticks()
        self._total_inputs: int = 0
        self._prep_start: dict[str, int] = {}
        self._burst_inputs: dict[str, int] = {}

    def create_row(
        self,
        event_type,
        threat,
        aggro,
        action,
        survived,
        score,
        input_count,
    ):
        temp = {
            "Timestamp": self.__time_stamp(),
            "Session Time": self._session_time(),
            "Event type": event_type,
            "Threat Name": threat,
            "Aggro level": aggro,
            "Action": action,
            "Survived": not self.eventhandler.is_game_over,
            "Score": self.eventhandler.score,
            "Input Count": input_count,
        }

        self.__df.loc[len(self.__df)] = temp

    def reset(self):
        self.__df = self.__df.iloc[0:0]
        self._start_tick = pygame.time.get_ticks()
        self.__start_sessions = self.__time_stamp()
        self._total_inputs = 0
        self._prep_start.clear()
        self._burst_inputs.clear()

    def on_action(self, action_type: str):
        self._total_inputs += 1
        for name in self._burst_inputs:
            self._burst_inputs[name] += 1
        action_state = {
            "Mask": self.eventhandler.is_mask_on,
            "Door": self.eventhandler.is_door_close,
            "PC": self.eventhandler.is_pc_on,
            "Submit": self.eventhandler.is_sumbit,
            "TurnLeft": self.eventhandler._is_facing_office,
            "TurnRight": self.eventhandler._is_facing_office,
        }.get(action_type, None)
        row = {
            "Timestamp": self.__time_stamp(),
            "Session Time": self._session_time(),
            "Event type": action_type,
            "Threat Name": None,
            "Aggro level": None,
            "Action": action_state,
            "Survived": None,
            "Score": self.eventhandler.score,
            "Input Count": self._total_inputs,
        }
        self.__df.loc[len(self.__df)] = row

    def on_threat_prep(self, threat_name: str):
        if threat_name not in self._prep_start:
            self._prep_start[threat_name] = pygame.time.get_ticks()
            self._burst_inputs[threat_name] = 0

    def on_attack(self, threat_name: str, survived: bool, score: int, aggro_rate=None):
        burst = None
        if threat_name in self._prep_start:
            self._prep_start.pop(threat_name)
            burst = self._burst_inputs.pop(threat_name, 0)
        row = {
            "Timestamp": self.__time_stamp(),
            "Session Time": self._session_time(),
            "Event type": "Encounter",
            "Threat Name": threat_name,
            "Aggro level": aggro_rate,
            "Action": None,
            "Survived": survived,
            "Score": score,
            "Input Count": burst,
        }
        self.__df.loc[len(self.__df)] = row

    def on_session_end(self, survived: bool, score: int):
        duration_s = round((pygame.time.get_ticks() - self._start_tick) / 1000.0, 3)
        row = {
            "Timestamp": self.__start_sessions,
            "Session Time": duration_s,
            "Event type": "Session",
            "Threat Name": None,
            "Aggro level": None,
            "Action": None,
            "Survived": survived,
            "Score": score,
            "Input Count": self._total_inputs,
        }
        self.__df.loc[len(self.__df)] = row

        self.write_to_excels()

    def write_to_excels(self):
        df_out = self.__df.copy()
        if "Timestamp" in df_out.columns:
            df_out["Timestamp"] = pd.to_datetime(df_out["Timestamp"]).dt.tz_convert(
                None
            )

        if self.excel_path.exists():
            df_existing = pd.read_excel(self.excel_path)
            df_out = pd.concat([df_existing, df_out], ignore_index=True)

        df_out.to_excel(self.excel_path, index=False)

    def _session_time(self) -> float:
        return round((pygame.time.get_ticks() - self._start_tick) / 1000.0, 3)

    def __time_stamp(self) -> pd.Timestamp:
        return pd.Timestamp.now(tz="Asia/Bangkok")
