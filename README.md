# Hunger Games LLM Simulation

This project is a text-based simulator of "Hunger Games" where each participant is an autonomous agent controlled by a Large Language Model (LLM). The game manages districts, elections, combat, and strategic movements until only one survivor remains.

## 🧠 Artificial Intelligence

The core of the project lies in `Player.py`. Each player uses **vLLM** to generate real-time decisions.
- **Model used**: `google/gemma-3-12b-it` (quantized bitsandbytes).
- **Decision Making**: Agents are provided with a structured JSON prompt containing their status (health, inventory, zone, enemies present) and must choose the best action among those available.

## 🎮 How the Game Works

The main logic is contained in `Game.py`.

### 1. Initialization
The game creates `n_groups` (Districts), each populated by a defined number of players. Each player has:
- **Name**: Randomly generated (Faker).
- **Health Points (HP)**: Random between 15 and 20.
- **Attack Power**: Random between 3 and 5.
- **Starting Zone**: Cornucopia.

### 2. Leader Election Phase (`handle_leader_election`)
Before the massacre begins, each district must attempt to elect a leader.
1. **Candidacy**: The LLM decides if the player wants to run for leader.
2. **Voting**:
   - If there is only one candidate, they are elected automatically.
   - If there are two candidates, the other district members vote (via LLM) for their preference.
   - If no agreement is reached after 5 attempts, the district remains without a leader.

**Leader Bonus**: The leader gets a damage multiplier of **1.2x**.

### 3. The Game Loop (`loop_game`)
Players act in turns until only one remains alive. Each turn, the LLM analyzes the situation and chooses one of the following actions:

#### A. Attack (`op: 1`)
- Possible only if there are other players in the same zone.
- Damage is calculated as: `max(base_strength, weapon_damage) * leader_multiplier`.
- If health points drop to 0, the player dies and a cannon shot is announced.

#### B. Pick up a weapon (`op: 2`)
- The player draws a weapon from the global pool (if available).
- **Available weapons**:
  - Sword (Attacco: 6)
  - Wooden sword (Attacco: 4)
  - Knife (Attacco: 5)

#### C. Move to another zone (`op: 3`)
- The player changes zone among the available ones: *Cornucopia, Palude Nebbiosa, Settore dei Geyser, La Giungla Elettrica*.
- **Random events during movement**:
  - **Accidental death (3%)**: The player dies from natural causes.
  - **Healing (10%)**: If the player is alone in the new zone, they recover 1 HP.
  - **Ambush (20%)**: If there are enemies in the new zone, one of them immediately attacks the newly arrived player.

## 🛠️ Technical Requirements

The project requires an environment with GPU support to run the local LLM model.

- Python 3.x
- `vllm`
- `faker`
- `torch` (con supporto CUDA)

### Environment Variables
The `main.py` file automatically configures PyTorch memory management:
```python
os.environ["PYTORCH_ALLOC_CONF"] = "expandable_segments:True"
```
È necessario aver effettuato il login a Hugging Face (`huggingface-cli login`) per scaricare il modello Gemma.

## 🚀 Esecuzione

Per avviare la simulazione:

```bash
python main.py
```

## Struttura dei File

- **`main.py`**: Entry point. Inizializza il gioco e avvia il loop principale.
- **`Game.py`**: Gestisce lo stato globale, i distretti, le armi e il flusso dei turni.
- **`Player.py`**: Definisce la classe Giocatore, gestisce l'interazione con l'LLM (prompting e parsing JSON) e le azioni individuali.

---
*Progetto sviluppato per sperimentare con agenti autonomi basati su LLM in un contesto competitivo.*