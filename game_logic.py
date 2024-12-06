from drop_state import DropState
from game_token import GameToken
from game_state import GameState
from game_logic_base import GameLogicBase


class GameLogic(GameLogicBase):

    def __init__(self):

        # Initialisiere Board
        self._board = [[GameToken.EMPTY for _ in range(7)] for _ in range(6)]

        # Initialisiere Zustand zu Spielbeginn. Standardmässig beginnt Rot
        self._game_state = GameState.TURN_RED
        self._winning_positions = None

    def get_board(self) -> list:

        return self._board #Board as list
    
    def get_winning_positions(self):
        # Gibt die Gewinn-Koordinaten zurück, falls vorhanden, sonst None
        return self._winning_positions
    
    def get_state(self) -> GameState:
        
        # Prüft, ob ein Spieler gewonnen hat oder das Spiel unentschieden ist.
        # Gibt den aktuellen Spielzustand zurück.
        
        def check_win(player: GameToken) -> bool:

            # Horizontale Prüfung
            for row in range(6):
                for col in range(4):  # Maximaler Startpunkt für 4er-Sequenz
                    if all(self._board[row][col + i] == player for i in range(4)):
                        self._winning_positions = [(row, col+i) for i in range(4)]
                        return True

            # Vertikale Prüfung
            for col in range(7):
                for row in range(3):  # Maximaler Startpunkt für 4er-Sequenz
                    if all(self._board[row + i][col] == player for i in range(4)):
                        self._winning_positions = [(row+i, col) for i in range(4)]
                        return True

            # Diagonale Prüfung (links unten nach rechts oben)
            for row in range(3):
                for col in range(4):
                    if all(self._board[row + i][col + i] == player for i in range(4)):
                        self._winning_positions = [(row+i, col+i) for i in range(4)]
                        return True

            # Diagonale Prüfung (rechts unten nach links oben)
            for row in range(3):
                for col in range(3, 7):
                    if all(self._board[row + i][col - i] == player for i in range(4)):
                        self._winning_positions = [(row+i, col - i) for i in range(4)]
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

        # Prüfen, ob die Spalte möglich ist
        if not (0 <= column < 7):
            return DropState.COLUMN_INVALID
 
        # Stein setzen, wenn die Spalte noch leer ist. Spieler wechseln
        for row in reversed(range(6)):
            if self._board[row][column] == GameToken.EMPTY:
                if player == GameToken.RED:
                    self._board[row][column] = GameToken.RED
                    self._game_state = GameState.TURN_YELLOW
                elif player == GameToken.YELLOW:
                    self._board[row][column] = GameToken.YELLOW
                    self._game_state = GameState.TURN_RED
                return DropState.DROP_OK
            
        # Wenn die Spalte voll ist melden. Zug wird in der Schleife wiederholt
        return DropState.COLUMN_FULL
    


"""
    def drop_token(self, player: GameToken, column: int):
        if column < 0 or column >= len(self._board[0]):
            return DropState.COLUMN_INVALID, -1

        # Prüfen, ob die Spalte voll ist
        if self._board[0][column] != GameToken.EMPTY:
            return DropState.COLUMN_FULL, -1

        # Finde die niedrigste leere Zeile in der Spalte
        for row in reversed(range(len(self._board))):
            if self._board[row][column] == GameToken.EMPTY:
                self._board[row][column] = player
                return DropState.DROP_OK, row  # Zeile zurückgeben
        return DropState.COLUMN_FULL, -1"""