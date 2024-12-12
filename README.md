# 4 Gewinnt – Python-basiertes Spiel

Dieses Projekt implementiert das beliebte Spiel **4 Gewinnt** in Python. Es bietet mehrere Spielmodi, darunter lokale Spiele (Hotseat) und Remote-Spiele, sowie Unterstützung für verschiedene Eingabemethoden (Konsole oder Sense HAT).

## Übersicht

### Features
- **Lokaler Modus**: Spieler treten abwechselnd auf demselben Gerät an.
- **Remote-Modus**: Spiele können über ein Netzwerk gehostet und gespielt werden.
- **Multiplattform-Unterstützung**: Konsole und Sense HAT.
- **Visualisierung**: Das Spielfeld wird entweder in der Konsole oder auf dem Sense HAT angezeigt.
- **Robuste Spiel-Logik**: Enthält Mechanismen zur Validierung von Zügen und zur Überprüfung von Gewinnbedingungen.

## Verzeichnisstruktur

- `game_logic.py`: Kernlogik des Spiels, einschließlich Spielfeldverwaltung, Spielstatus und Gewinnbedingungen.
- `game_logic_server.py`: Flask-basierter Server für Remote-Spiele.
- `game_logic_client.py`: Client für die Kommunikation mit dem Server.
- `player_coordinator.py`: Koordiniert den Spielablauf, wählt Modi und Eingabemethoden.
- `player_console.py`: Implementiert einen Spieler mit Konsoleneingabe.
- `player_sensehat.py`: Implementiert einen Spieler mit Sense HAT-Joystick und Display.
- `input_console.py`: Handhabung von Tastatureingaben in der Konsole.
- `input_sensehat.py`: Handhabung von Joystick-Eingaben über Sense HAT.
- `display_console.py`: Darstellung des Spielfelds in der Konsole.
- `display_sensehat.py`: Darstellung des Spielfelds auf dem Sense HAT.

## Installation

1. Klonen Sie das Repository:
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. Installieren Sie die Abhängigkeiten:
   ```bash
   pip install -r requirements.txt
   ```

3. (Optional) Installieren Sie den Sense HAT Emulator, falls kein physischer Sense HAT vorhanden ist:
    ```bash
    sudo apt-get install sense-emu
    ```

## Nutzung

### Lokales Spiel

1. Starten Sie das Spiel:
    ```bash
    python player_coordinator.py
    ```

2. Wählen Sie "Lokal" und Ihre bevorzugten Eingabemethoden.

### Remote-Spiel

1. Starten Sie den Server:
    ```bash
    python game_logic_server.py
    ```

2. Verbinden Sie sich mit dem Server:
    ```bash
    python player_coordinator.py
    ```

3. Wählen Sie "Remote" und geben Sie die Serveradresse ein.

## Anforderungen

- **Python 3.8+**
- Abhängigkeiten aus `requirements.txt`
- Sense HAT (optional)

## Weiterentwicklung

Dieses Projekt kann erweitert werden durch:
- Verbesserte Benutzeroberflächen.
- Unterstützung für KI-gesteuerte Gegner.
- Mehrsprachige Unterstützung.

## Lizenz

Dieses Projekt steht unter der [MIT-Lizenz](LICENSE).
