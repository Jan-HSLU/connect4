from game_logic import GameLogic
from game_logic_client import GameLogicClient
from player_simple import PlayerSimple
from player_console import PlayerConsole
from game_token import GameToken
from game_state import GameState
from drop_state import DropState
import time

class PlayerCoordinator:
    def __init__(self):

        # Initialisiere Spieler (PlayerSimple/PlayerConsole/PlayerSenseHat)
        self._player = None  


        # Initialisiere GameLogic (GameLogic/GameLogicClient)
        # GameLogic() = lokal
        # GameLogicClient("127.0.0.1") = Server lokal
        # GameLogicClient("10.180.254.67") = Server Raspi Juri
        self._game_logic = GameLogicClient("10.180.254.67")


    def run(self):

        print("Wähle deine Spielerfarbe:")
        print("1: Spieler Rot (X)")
        print("2: Spieler Gelb (O)")

        player_color = input("Gib 1 oder 2 ein: ").strip()

        if player_color == '1':
            self._player = PlayerConsole(GameToken.RED)
            game_state = GameState.TURN_RED
            game_token = GameToken.RED
            
        elif player_color == '2':
            self._player = PlayerConsole(GameToken.YELLOW)
            game_state = GameState.TURN_YELLOW
            game_token = GameToken.YELLOW

        # Schleife bis Spiel gewonnen oder unentschieden
        while (True):

            # 1. Spiel-Zustand abfragen -> get_state() -> GameLogic -> Return GameState
            state = self._game_logic.get_state()


            # 2. Spielfeld abfragen -> get_board() -> GameLogic -> Return Board as list
            board = self._game_logic.get_board()

            self._player.draw_board(board, state)


            if state == GameState.DRAW:
                print("Das Spiel endete Unentschieden.")
                break

            elif state == GameState.WON_RED:
                print("Rot hat gewonnen!")
                break

            elif state == GameState.WON_YELLOW:
                print("Gelb hat gewonnen!")
                break


            # Wenn Spieler Rot am Zug:
            if state == game_state:

                # 4. Spieler der am Zug ist, auffordern, seinen nächsten Zug zu bestimmen
                column_to_drop = self._player.play_turn(state)

                # 5. Den Zug an die Logik weiterreichen
                self._game_logic.drop_token(game_token, column_to_drop)


            
            else:

                time.sleep(3.0)





# start a local game
if __name__ == '__main__':
    coordinator = PlayerCoordinator()
    coordinator.run()


    