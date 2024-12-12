from game_logic import GameLogic
from game_logic_client import GameLogicClient
from player_simple import PlayerSimple
from player_console import PlayerConsole
from game_token import GameToken
from game_state import GameState
from drop_state import DropState
from player_sensehat import PlayerSenseHat
from ansi import Ansi
import time
import sys

class PlayerCoordinator:
    """
    Koordiniert das 4Gewinnt-Spiel, indem es die Spielmodi (lokal oder remote) verwaltet
    und die Spieler (Konsole oder SenseHat) steuert.
    """

    def __init__(self):
        """
        Initialisiert die Spieler, die Spiellogik und den Spielmodus.
        """
        self._player_red: PlayerConsole | PlayerSenseHat | None = None  # Spieler Rot (X)
        self._player_yellow: PlayerConsole | PlayerSenseHat | None = None  # Spieler Gelb (O)
        self._player: PlayerConsole | PlayerSenseHat | None = None  # Remote-Spieler

        self._game_logic: GameLogic | GameLogicClient | None = None
        self._game_mode: str | None = None  # "local" oder "remote"

    def run(self) -> None:
        """
        Startet das Spiel, nachdem die Setup-Methode aufgerufen wurde.
        """
        # Rufe die interne Setup-Methode auf
        self._set_up()

        # Starte das Spiel basierend auf dem Modus
        if self._game_mode == "local":
            self._run_local()
        elif self._game_mode == "remote":
            self._run_remote()
        else:
            print("Ungültiger Spielmodus. Abbruch.")

    def _print_animiert(self, message: str, delay: float = 0.05, end_delay: float = 0.5) -> None:
        """
        Gibt eine animierte Nachricht auf der Konsole aus.

        :param message: Die Nachricht, die ausgegeben wird.
        :param delay: Verzögerung zwischen den Zeichen (Standard: 0.05).
        :param end_delay: Verzögerung nach der gesamten Nachricht (Standard: 0.5).
        """
        for char in message:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(delay)
        print()
        time.sleep(end_delay)

    def _get_valid_input(self, prompt: str) -> str:
        """
        Fordert den Benutzer auf, entweder "1" oder "2" einzugeben, und wiederholt die Eingabeaufforderung, falls eine ungültige Eingabe erfolgt.

        :param prompt: Die Eingabeaufforderung für den Benutzer.
        :return: Eine gültige Eingabe ("1" oder "2").
        """
        while True:
            self._print_animiert(prompt)
            user_input = input().strip()
            if user_input in {"1", "2"}:
                return user_input
            self._print_animiert("Ungültige Eingabe. Bitte gib 1 oder 2 ein.")

    def _set_up(self) -> None:
        """
        Konfiguriert das Spiel basierend auf der Benutzereingabe.
        """
        Ansi.clear_screen()
        self._print_animiert("Willkommen bei 4Gewinnt!")
        self._print_animiert("Wie möchtest du spielen?")
        self._print_animiert("1: Lokal / HotSeat")
        self._print_animiert("2: Remote")
        game_type = self._get_valid_input("Gib 1 oder 2 ein: ")

        if game_type == "1":
            self._game_mode = "local"
            self._setup_local_game()
        elif game_type == "2":
            self._game_mode = "remote"
            self._setup_remote_game()

    def _setup_local_game(self) -> None:
        """
        Richtet ein lokales Spiel ein, indem die Spieler und ihre Geräte ausgewählt werden.
        """
        Ansi.clear_screen()
        self._print_animiert("HotSeat")
        self._print_animiert("Spieler Rot wähle dein Gerät:")
        self._print_animiert("1: Console")
        self._print_animiert("2: SenseHat")
        player_red_input = self._get_valid_input("Gib 1 oder 2 ein: ")

        if player_red_input == "1":
            self._player_red = PlayerConsole(GameToken.RED)
        else:
            self._player_red = PlayerSenseHat(GameToken.RED)

        Ansi.clear_screen()
        self._print_animiert("Spieler Gelb wähle dein Gerät:")
        self._print_animiert("1: Console")
        self._print_animiert("2: SenseHat")
        player_yellow_input = self._get_valid_input("Gib 1 oder 2 ein: ")

        if player_yellow_input == "1":
            self._player_yellow = PlayerConsole(GameToken.YELLOW)
        else:
            self._player_yellow = PlayerSenseHat(GameToken.YELLOW)

        self._game_logic = GameLogic()

    def _setup_remote_game(self) -> None:
        """
        Richtet ein Remote-Spiel ein, indem der Spieler seine Farbe, sein Gerät und den Server auswählt.
        """
        Ansi.clear_screen()
        self._print_animiert("Remote")
        self._print_animiert("Wähle deine Farbe:")
        self._print_animiert("1: Rot")
        self._print_animiert("2: Gelb")
        player_colour = self._get_valid_input("Gib 1 oder 2 ein: ")

        Ansi.clear_screen()
        self._print_animiert("Wähle dein Gerät:")
        self._print_animiert("1: Console")
        self._print_animiert("2: SenseHat")
        player_input = self._get_valid_input("Gib 1 oder 2 ein: ")

        if player_colour == "1":
            self._player = PlayerConsole(GameToken.RED) if player_input == "1" else PlayerSenseHat(GameToken.RED)
            self._remote_player_state = GameState.TURN_RED
            self._remote_player_token = GameToken.RED
        else:
            self._player = PlayerConsole(GameToken.YELLOW) if player_input == "1" else PlayerSenseHat(GameToken.YELLOW)
            self._remote_player_state = GameState.TURN_YELLOW
            self._remote_player_token = GameToken.YELLOW

        Ansi.clear_screen()
        self._print_animiert("Wähle den Server:")
        self._print_animiert("1: Lokal - 127.0.0.1")
        self._print_animiert("2: Raspi Juri - 10.180.254.61")
        server_ip = self._get_valid_input("Gib 1 oder 2 ein: ")

        self._game_logic = GameLogicClient("127.0.0.1" if server_ip == "1" else "10.180.254.61")

    def _run_local(self) -> None:
        """
        Führt das lokale Spiel aus, indem die Spielzustände abgefragt und Spieleraktionen ausgeführt werden.
        """

        # Schleife bis Spiel gewonnen oder unentschieden
        while True:

            # 1. Spiel-Zustand abfragen -> get_state() -> GameLogic -> Return GameState
            state = self._game_logic.get_state()

            # 2. Spielfeld abfragen -> get_board() -> GameLogic -> Return Board as list
            board = self._game_logic.get_board()

            # 3. Spieler auffordern, das Spielfeld neu zu zeichnen
            self._player_red.draw_board(board, state)
            self._player_yellow.draw_board(board, state)

            # Wenn Spieler Rot am Zug:
            if state == GameState.TURN_RED:

                # 4. Spieler der am Zug ist, auffordern, seinen nächsten Zug zu bestimmen
                column_to_drop = self._player_red.play_turn(state)

                # 5. Den Zug an die Logik weiterreichen
                result = self._game_logic.drop_token(GameToken.RED, column_to_drop)
                if result == DropState.COLUMN_FULL:
                    Ansi.gotoXY(1, 16)
                    print("Die Spalte ist voll, wähle eine Andere.")
                    time.sleep(1.0)

            # Wenn Spieler Gelb am Zug:
            elif state == GameState.TURN_YELLOW:

                # 4. Spieler der am Zug ist, auffordern, seinen nächsten Zug zu bestimmen
                column_to_drop = self._player_yellow.play_turn(state)

                # 5. Den Zug an die Logik weiterreichen
                result = self._game_logic.drop_token(GameToken.YELLOW, column_to_drop)
                if result == DropState.COLUMN_FULL:
                    Ansi.gotoXY(1, 16)
                    print("Die Spalte ist voll, wähle eine Andere.")
                    time.sleep(1.0)

            # Schleifenabbruch bei Spielende
            elif state == GameState.DRAW:
                print("Das Spiel endete Unentschieden.")
                break

            elif state == GameState.WON_RED:
                print("Rot hat gewonnen!")
                break

            elif state == GameState.WON_YELLOW:
                print("Gelb hat gewonnen!")
                break

    def _run_remote(self) -> None:
        """
        Führt das Remote-Spiel aus, indem die Spielzustände abgefragt und Spieleraktionen synchronisiert werden.
        """

        # Schleife bis Spiel gewonnen oder unentschieden
        while True:

            # 1. Spiel-Zustand abfragen -> get_state() -> GameLogic -> Return GameState
            state = self._game_logic.get_state()

            # 2. Spielfeld abfragen -> get_board() -> GameLogic -> Return Board as list
            board = self._game_logic.get_board()

            self._player.draw_board(board, state)

            if state == self._remote_player_state:

                # 4. Spieler der am Zug ist, auffordern, seinen nächsten Zug zu bestimmen
                column_to_drop = self._player.play_turn(state)

                # 5. Den Zug an die Logik weiterreichen
                result = self._game_logic.drop_token(self._remote_player_token, column_to_drop)
                if result == DropState.COLUMN_FULL:
                    Ansi.gotoXY(1, 16)
                    print("Die Spalte ist voll, wähle eine Andere.")
                    time.sleep(1.0)

            # Schleifenabbruch bei Spielende
            elif state == GameState.DRAW:
                print("Das Spiel endete Unentschieden.")
                break

            elif state == GameState.WON_RED:
                print("Rot hat gewonnen!")
                break

            elif state == GameState.WON_YELLOW:
                print("Gelb hat gewonnen!")
                break

            else:
                time.sleep(1.0)

if __name__ == '__main__':
    coordinator = PlayerCoordinator()
    coordinator.run()
