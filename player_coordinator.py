from game_logic import GameLogic
from game_logic_client import GameLogicClient
from player_simple import PlayerSimple
from player_console import PlayerConsole
from game_token import GameToken
from game_state import GameState
from drop_state import DropState
class PlayerCoordinator:
    def __init__(self):

        # Initialisiere Spieler (PlayerSimple/PlayerConsole/PlayerSenseHat)
        self._player_red = PlayerConsole(GameToken.RED)  # X
        self._player_yellow = PlayerConsole(GameToken.YELLOW)  # 0

        # Initialisiere GameLogic
        self._game_logic = GameLogicClient("127.0.0.1")


    def run(self):

        # Schleife bis Spiel gewonnen oder unentschieden
        while (True):

            # 1. Spiel-Zustand abfragen -> get_state() -> GameLogic -> Return GameState
            state = self._game_logic.get_state()


            # 2. Spielfeld abfragen -> get_board() -> GameLogic -> Return Board as list
            board = self._game_logic.get_board()


            # Wenn Spieler Rot am Zug:
            if state == GameState.TURN_RED:

                # 3. Spieler, der am Zug ist, auffordern, das Spielfeld neu zu zeichnen
                self._player_red.draw_board(board, state)

                # 4. Spieler der am Zug ist, auffordern, seinen nächsten Zug zu bestimmen
                column_to_drop = self._player_red.play_turn(state)

                # 5. Den Zug an die Logik weiterreichen
                self._game_logic.drop_token(GameToken.RED, column_to_drop)
                if DropState == 2:
                    print("Die Spalte ist voll, wähle eine Andere.")


            # Wenn Spieler Gelb am Zug:
            elif state == GameState.TURN_YELLOW:

                # 3. Spieler, der am Zug ist, auffordern, das Spielfeld neu zu zeichnen
                self._player_yellow.draw_board(board, state)

                # 4. Spieler der am Zug ist, auffordern, seinen nächsten Zug zu bestimmen
                column_to_drop = self._player_yellow.play_turn(state)

                # 5. Den Zug an die Logik weiterreichen
                self._game_logic.drop_token(GameToken.YELLOW, column_to_drop)


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


# start a local game
if __name__ == '__main__':
    coordinator = PlayerCoordinator()
    coordinator.run()


    