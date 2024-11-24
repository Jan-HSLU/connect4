import requests

class GameLogicClient:
    def __init__(self, base_url):
        """
        Initialisiert den Client mit der Basis-URL des Flask-Servers.
        :param base_url: Basis-URL des Flask-Servers, z.B. "http://127.0.0.1:5000"
        """
        self.base_url = base_url

    def get_board(self):
        """
        Holt das aktuelle Spielfeld.
        :return: 2D-Liste, die das Spielfeld darstellt.
        """
        response = requests.get(f"{self.base_url}/board")
        response.raise_for_status()
        return response.json()["board"]

    def get_state(self):
        """
        Holt den aktuellen Spielzustand.
        :return: Spielzustand als String (z. B. "TURN_RED", "WON_YELLOW").
        """
        response = requests.get(f"{self.base_url}/state")
        response.raise_for_status()
        return response.json()["state"]

    def drop_token(self, player, column):
        """
        Setzt einen Token in die angegebene Spalte.
        :param player: Spieler, entweder "RED" oder "YELLOW".
        :param column: Spalte (0-6), in die der Token gesetzt werden soll.
        :return: Ergebnis des Zuges und das aktuelle Spielfeld.
        """
        payload = {"player": player, "column": column}
        response = requests.post(f"{self.base_url}/drop", json=payload)
        response.raise_for_status()
        return response.json()

    def reset_game(self):
        """
        Setzt das Spiel zurück.
        :return: Nachricht und das leere Spielfeld.
        """
        response = requests.post(f"{self.base_url}/reset")
        response.raise_for_status()
        return response.json()
