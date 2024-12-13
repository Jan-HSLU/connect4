from drop_state import DropState
from game_token import GameToken
from game_state import GameState
from game_logic_base import GameLogicBase

class GameLogic(GameLogicBase):
    """
    Implementierung der Spiel-Logik für ein Connect Four-ähnliches Spiel.
    """

    def __init__(self) -> None:
        """
        Initialisiert das Spielfeld, den Spielstatus und die Gewinn-Koordinaten.
        """
        # Initialisiere Board
        self._board: list = [[GameToken.EMPTY for _ in range(7)] for _ in range(6)]

        # Initialisiere Zustand zu Spielbeginn. Standardmässig beginnt Rot
        self._game_state: GameState = GameState.TURN_RED

    def get_board(self) -> list:
        """
        Gibt das aktuelle Spielfeld zurück.

        :return: Das Spielfeld als Liste von Listen (2D-Array)
        """
        return self._board

    def get_state(self) -> GameState:
        """
        Prüft, ob ein Spieler gewonnen hat oder das Spiel unentschieden ist,
        und gibt den aktuellen Spielstatus zurück.

        :return: Der aktuelle Spielstatus als Instanz der GameState-Enum
        """

        def check_win(player: GameToken) -> bool:
            """
            Prüft, ob der angegebene Spieler gewonnen hat.

            :param player: Der Spieler (GameToken.RED oder GameToken.YELLOW)
            :return: True, wenn der Spieler gewonnen hat, sonst False
            """
            # Horizontale Prüfung
            for row in range(6):
                for col in range(4):
                    if all(self._board[row][col + i] == player for i in range(4)):
                        return True

            # Vertikale Prüfung
            for col in range(7):
                for row in range(3):
                    if all(self._board[row + i][col] == player for i in range(4)):
                        return True

            # Diagonale Prüfung (links unten nach rechts oben)
            for row in range(3):
                for col in range(4):
                    if all(self._board[row + i][col + i] == player for i in range(4)):
                        return True

            # Diagonale Prüfung (rechts unten nach links oben)
            for row in range(3):
                for col in range(3, 7):
                    if all(self._board[row + i][col - i] == player for i in range(4)):
                        return True

            return False

        # Prüfen, ob ein Spieler gewonnen hat
        if check_win(GameToken.RED):
            return GameState.WON_RED
        elif check_win(GameToken.YELLOW):
            return GameState.WON_YELLOW

        # Prüfen, ob das Spielfeld voll ist (Unentschieden)
        if all(cell != GameToken.EMPTY for row in self._board for cell in row):
            return GameState.DRAW

        # Andernfalls: Spiel läuft weiter, wer ist dran?
        return self._game_state

    def drop_token(self, player: GameToken, column: int) -> DropState:
        """
        Führt die Aktion des Spielers aus, einen Spielstein in eine Spalte zu werfen.

        :param player: Der Spieler (GameToken.RED oder GameToken.YELLOW)
        :param column: Die Spalte, in die der Spielstein geworfen werden soll
        :return: Der Status der Aktion als Instanz der DropState-Enum
        """
        # Prüfen, ob die Spalte gültig ist
        if not (0 <= column < 7):
            return DropState.COLUMN_INVALID

        # Stein setzen, wenn die Spalte noch Platz hat
        for row in reversed(range(6)):
            if self._board[row][column] == GameToken.EMPTY:
                if player == GameToken.RED:
                    self._board[row][column] = GameToken.RED
                    self._game_state = GameState.TURN_YELLOW
                elif player == GameToken.YELLOW:
                    self._board[row][column] = GameToken.YELLOW
                    self._game_state = GameState.TURN_RED
                return DropState.DROP_OK

        # Wenn die Spalte voll ist
        return DropState.COLUMN_FULL
