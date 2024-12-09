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
    def __init__(self):
        # Initialisiere Spieler (PlayerSimple/PlayerConsole/PlayerSenseHat)
        self._player_red = None  # X
        self._player_yellow = None  # 0
        self._player = None # RemotePlayer

        # Initialisiere GameLogic
        self._game_logic = None
        self._game_mode = None  # "local" oder "remote"

    def run(self):
        # Rufe die interne Setup-Methode auf
        self._set_up()

        # Starte das Spiel basierend auf dem Modus
        if self._game_mode == "local":
            self._run_local()
        elif self._game_mode == "remote":
            self._run_remote()
        else:
            print("Ungültiger Spielmodus. Abbruch.")

    def _set_up(self):
        def print_animiert(message, delay=0.05, end_delay=0.5):
            for char in message:
                sys.stdout.write(char)
                sys.stdout.flush()
                time.sleep(delay)
            print()
            time.sleep(end_delay)

        Ansi.clear_screen()
        print_animiert("Willkommen bei 4Gewinnt!")
        print_animiert("Wie möchtest du spielen?")
        print_animiert("1: Lokal / HotSeat")
        print_animiert("2: Remote")
        print_animiert("Gib 1 oder 2 ein: ")
        game_type = input().strip()


        if game_type == "1":
            self._game_mode = "local"
            self._setup_local_game()
        elif game_type == "2":
            self._game_mode = "remote"
            self._setup_remote_game()

    def _setup_local_game(self):
        Ansi.clear_screen()
        print("HotSeat")
        print("Spieler Rot wähle dein Gerät:")
        print("1: Console")
        print("2: SenseHat")
        player_red_input = input("Gib 1 oder 2 ein: ").strip()

        if player_red_input == "1":
            self._player_red = PlayerConsole(GameToken.RED)
        else:
            self._player_red = PlayerSenseHat(GameToken.RED)

        print("Spieler Gelb wähle dein Gerät:")
        print("1: Console")
        print("2: SenseHat")
        player_yellow_input = input("Gib 1 oder 2 ein: ").strip()

        if player_yellow_input == "1":
            self._player_yellow = PlayerConsole(GameToken.YELLOW)
        else:
            self._player_yellow = PlayerSenseHat(GameToken.YELLOW)

        self._game_logic = GameLogic()

    def _setup_remote_game(self):
        print("Remote")
        print("Wähle deine Farbe:")
        print("1: Rot")
        print("2: Gelb")
        player_colour = input("Gib 1 oder 2 ein: ").strip()

        print("Wähle dein Gerät:")
        print("1: Console")
        print("2: SenseHat")
        player_input = input("Gib 1 oder 2 ein: ").strip()

        if player_colour == "1":
            self._player = PlayerConsole(GameToken.RED) if player_input == "1" else PlayerSenseHat(GameToken.RED)
            self._remote_player_state = GameState.TURN_RED
            self._remote_player_token = GameToken.RED
        else:
            self._player = PlayerConsole(GameToken.YELLOW) if player_input == "1" else PlayerSenseHat(GameToken.YELLOW)
            self._remote_player_state = GameState.TURN_YELLOW
            self._remote_player_token = GameToken.YELLOW

        print("Wähle den Server:")
        print("1: Lokal - 127.0.0.1")
        print("2: Raspi Juri - 10.180.254.67")
        server_ip = input("Gib 1 oder 2 ein: ").strip()

        self._game_logic = GameLogicClient("127.0.0.1" if server_ip == "1" else "10.180.254.67")


    def _run_local(self):
        
        # Schleife bis Spiel gewonnen oder unentschieden
        while (True):
            
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
                    print("Die Spalte ist voll, wähle eine Andere.")


            # Wenn Spieler Gelb am Zug:
            elif state == GameState.TURN_YELLOW:

                # 4. Spieler der am Zug ist, auffordern, seinen nächsten Zug zu bestimmen
                column_to_drop = self._player_yellow.play_turn(state)
        
                # 5. Den Zug an die Logik weiterreichen
                result = self._game_logic.drop_token(GameToken.YELLOW, column_to_drop)
                if result == DropState.COLUMN_FULL:
                    print("Die Spalte ist voll, wähle eine Andere.")


            # Schleifenabbruch bei Spielende (nicht sicher ob hier richtig)
            elif state == GameState.DRAW:
                print("Das Spiel endete Unentschieden.")
                break

            elif state == GameState.WON_RED:
                print("Rot hat gewonnen!")
                break

            elif state == GameState.WON_YELLOW:
                print("Gelb hat gewonnen!")
                break


    def _run_remote(self):
            
        while True:

            # 1. Spiel-Zustand abfragen -> get_state() -> GameLogic -> Return GameState
            state = self._game_logic.get_state()

            # 2. Spielfeld abfragen -> get_board() -> GameLogic -> Return Board as list
            board = self._game_logic.get_board()

            # 3. Spieler auffordern, das Spielfeld neu zu zeichnen
            self._player.draw_board(board, state)

            if state == self._remote_player_state:

                # 4. Spieler der am Zug ist, auffordern, seinen nächsten Zug zu bestimmen
                column_to_drop = self._player.play_turn(state)

                # 5. Den Zug an die Logik weiterreichen
                self._game_logic.drop_token(self._remote_player_token, column_to_drop)

            # Schleifenabbruch bei Spielende (nicht sicher ob hier richtig)
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
        


# Hauptprogramm
if __name__ == '__main__':
    coordinator = PlayerCoordinator()  # Instanziere den Koordinator
    coordinator.run()                  # Starte das Spiel
