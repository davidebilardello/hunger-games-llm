# Hunger Games LLM Simulation

This project is a simulator of "Hunger Games" where each participant is an autonomous agent controlled by a LLM. The
game manages districts, elections, combat, and strategic movements until only one survivor remains.

## The game

Each player generate real-time decisions.

- **Model used**: `google/gemma-3-12b-it` (quantized).
- **Decision Making**: Agents are provided with a prompt containing their status (health, inventory,
  zone, enemies present) and must choose the best action among those available.

## How the Game Works

The main logic is contained in `Game.py`.

### 1. Initialization

The game creates `n_groups` (Districts), each populated by a defined number of players. Each player has:

- **Name**.
- **Health Points (HP)**: Random between 15 and 20.
- **Attack Power**: Random between 3 and 5.
- **Starting Zone**: Cornucopia.

### 2. Leader Election Phase

Before the massacre begins, each district must attempt to elect a leader.

1. **Candidacy**: The LLM decides if the player wants to run for leader.
2. **Voting**:
    - If there is only one candidate, they are elected automatically.
    - If there are two candidates, the other district members vote for their preference.
    - If no agreement is reached after 5 attempts, the district remains without a leader.

**Leader Bonus**: The leader gets a damage multiplier of **1.2x**.

### 3. The Game Loop

Players act in turns until only one remains alive. Each turn, the LLM analyzes the situation and chooses one of the
following actions:

#### A. Attack (`op: 1`)

- Possible only if there are other players in the same zone.
- Damage is calculated as: `max(base_strength, weapon_damage) * leader_multiplier`.
- If health points drop to 0, the player dies and a cannon shot is announced.

#### B. Pick up a weapon (`op: 2`)

- The player draws a weapon from the global pool (if available).

#### C. Move to another zone (`op: 3`)

- The player changes zone among the available ones.
- **Random events during movement**:
    - **Accidental death (3%)**: The player dies from natural causes.
    - **Healing (10%)**: If the player is alone in the new zone, they recover 1 HP.
    - **Attacked (20%)**: If there are enemies in the new zone, one of them immediately attacks the newly arrived player.

## Technical Requirements

The project requires an environment with GPU support to run the local LLM model.

- Python 3.x
- `vllm`
- `faker`
- `torch` (with CUDA support)


Run (`huggingface-cli login`) to download Gemma3 model.