from game_token import GameToken
from game_state import GameState
from player_base import PlayerBase

class PlayerSimple(PlayerBase):
    def __init__(self, player: GameToken):  # Red or Yellow player
        self._player = player

    def play_turn(self) -> int:

        while True:
            try:
                column_to_drop = int(input(f"Spieler {self._player}: Wo möchtest du spielen? "))
                return column_to_drop  # Gib die Spalte zurück, wenn die Eingabe gültig ist.
            except ValueError:
                print("Ungültige Eingabe. Bitte eine ganze Zahl eingeben.")

        
    def draw_board(self, board: list, state: GameState) -> None:
        
        print("-" * 29)
        for row in board:
           print("|" + "|".join(f" {cell} " for cell in row) + "|")
           print("-" * 29)

        # Spielstatus anzeigen
        if state == GameState.WON_RED:
            print("Red wins!")
        elif state == GameState.WON_YELLOW:
            print("Yellow wins!")
        elif state == GameState.DRAW:
            print("It's a draw!")
        elif state == GameState.TURN_RED:
            print("Red's turn!")
        elif state == GameState.TURN_YELLOW:
            print("Yellow's turn!")

        return #Zeichne das Board in der Konsole
    

    

if __name__ == '__main__':
    Player = PlayerSimple(GameToken.YELLOW)
    Player.play_turn()
