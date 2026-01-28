import json
import random
import re

from faker import Faker
from vllm import LLM, SamplingParams

fake = Faker()


class Player:
    # model_name = "google/gemma-3-4b-it"
    model_name = "google/gemma-3-12b-it"

    llm = LLM(
        model=model_name,
        quantization="bitsandbytes",
        load_format="bitsandbytes",
        max_model_len=4096,
        gpu_memory_utilization=0.90,
        enforce_eager=True
    )
    sampling_params = SamplingParams(temperature=0.8, top_p=0.95, max_tokens=100)

    def __init__(self, game, distretto="1", is_leader=False):
        self.game = game
        self.is_leader = is_leader
        self.name = fake.name()
        self.distretto = distretto

        self.life_points = random.randrange(15, 20)
        self.attack_power = random.randrange(3, 5)
        self.weapon = []
        self.operazioni_effettuate = []
        self.zone = "Cornucopia"

    def get_name(self):
        return f"{self.name} del distretto {self.distretto}"

    def get_prompt(self, targets):
        target_info = ", ".join([f"Player {t.get_name()}" for t in targets])
        can_attack = len(targets) > 0

        return f"""You are a professionist player of hunger games. You have to answer ONLY in JSON with just the next operation to do. DO not put other words. Do not type your thoughts.

                Game Status:

                Available weapon: {self.game.weapons}

                Player status:
                Life points: {self.life_points}
                Inventory: {self.weapon}
                Current attack power: {self.attack_power}
                Zone: {self.zone}
                Other players in this zone: {target_info if target_info else "None"}

                Give the code of the next operation:
                {"1 - Attack other player" if can_attack else ""}
                {"2 - Get a weapon if there is" if len(self.game.weapons) > 0 else ""}
                3 - Move to another zone (may heal, die, or damaged)

                Example of valid answer:
                {{"op": 1}}
                Answer in JSON with only the op code, DO NOT ADD ANY DETAILS, JUST GIVE THE CODE, GIVE JUST ONE LINE OF CODE:
                """

    def get_leader_election_prompt(self, submitted):
        submitted = [t.name for t in submitted]

        return f"""You are a professionist player of hunger games. You have to answer ONLY in JSON with just the next operation to do. DO not put other words. Do not type your thoughts.

                        Now you have to choose who is the leader in your group. The leader will have an attack multiplier.
                        This is the election phase where you can submit the apply to become the leader. Only two can be now nominated.

                        Player that have submitted the application:
                        {submitted}

                        Give the code of the next operation:
                        1 - Apply
                        2 - Not apply

                        Example of valid answer:
                        {{"op": 1}}
                        Answer in JSON with only the op code, DO NOT ADD ANY DETAILS, JUST GIVE THE CODE, GIVE JUST ONE LINE OF CODE:
                        """

    def get_next_leader_election(self, submitted):
        pr = self.get_leader_election_prompt(submitted)
        # print(pr)
        outputs = self.llm.generate(pr, self.sampling_params)
        return self.handle_leader_election(outputs[0].outputs[0].text)

    def handle_leader_election(self, j):
        cl = j.replace("```json", "").replace("```", "").strip()
        cl = re.findall(r'\{.*?\}', cl)
        cl = cl[0]

        try:
            data = json.loads(cl)
            op = data.get("op")
            print(f"Giocatore {self.get_name()} sceglie op durante la leader election: {op}")

            if op == 1:
                return True
            elif op == 2:
                return False
            else:
                return False

        except Exception as e:
            print("error")
            print(e)
            print(cl)
            return False

    def get_vote_prompt(self, c1, c2):
        return f"""You are a professionist player of hunger games. You have to answer ONLY in JSON with just the next operation to do. DO not put other words. Do not type your thoughts.

                        Now you have to vote for the leader in your group.
                        Candidates:
                        1 - {c1.name}
                        2 - {c2.name}

                        Give the code of the candidate you want to vote for:
                        1 - Vote for {c1.name}
                        2 - Vote for {c2.name}

                        Example of valid answer:
                        {{"op": 1}}
                        Answer in JSON with only the op code, DO NOT ADD ANY DETAILS, JUST GIVE THE CODE, GIVE JUST ONE LINE OF CODE:
                        """

    def get_vote(self, c1, c2):
        pr = self.get_vote_prompt(c1, c2)
        outputs = self.llm.generate(pr, self.sampling_params)
        return self.handle_vote(outputs[0].outputs[0].text)

    def handle_vote(self, j):
        cl = j.replace("```json", "").replace("```", "").strip()
        cl = re.findall(r'\{.*?\}', cl)

        try:
            if not cl:
                return random.choice([1, 2])
            cl = cl[0]
            data = json.loads(cl)
            op = data.get("op")
            print(f"Giocatore {self.get_name()} vota per opzione: {op}")

            if op == 1:
                return 1
            elif op == 2:
                return 2
            else:
                return random.choice([1, 2])

        except Exception as e:
            print("error voting")
            print(e)
            return random.choice([1, 2])

    def attack_player(self, p):
        weapon_attack = 0
        if len(self.weapon) > 0:
            weapon_attack = self.weapon[0].get('attack', 0)

        mul = 1.2 if self.is_leader else 1

        p.life_points -= max(self.attack_power, weapon_attack) * mul
        if p.life_points <= 0:
            p.life_points = 0

        if (p.life_points == 0):
            print(f"Parte un colpo di cannone per la morte del player {p.get_name()}")

    def get_weapon(self):
        random.shuffle(self.game.weapons)
        self.weapon.append(self.game.weapons.pop())

    def move_zone(self, all_players):
        if random.random() < 0.03:
            self.life_points = 0
            print(
                f"Sfortuna nera! Parte un colpo di cannone: il player {self.get_name()} è morto per cause naturali spostandosi.")
            return

        available_zones = [z for z in self.game.zones if z != self.zone]
        if available_zones:
            self.zone = random.choice(available_zones)

            # Controlla chi altro c'è nella nuova zona
            others = [p for p in all_players if p.zone == self.zone and p != self and p.life_points > 0]

            if not others:
                # 10% di possibilità di curarsi di 1 se da solo
                if random.random() < 0.10:
                    self.life_points += 1
                    print(
                        f"Il player {self.get_name()} ha trovato un momento di pace in {self.zone} e recupera 1 LP (LP: {self.life_points})")
            else:
                # 20% di possibilità di essere attaccato se c'è gente
                if random.random() < 0.20:
                    attacker = random.choice(others)
                    print(f"Imboscata! {self.get_name()} è stato sorpreso da {attacker.get_name()} in {self.zone}!")
                    attacker.attack_player(self)

    def handle_op(self, j, all_players):
        cl = j.replace("```json", "").replace("```", "").strip()
        cl = re.findall(r'\{.*?\}', cl)
        cl = cl[0]

        try:
            data = json.loads(cl)
            op = data.get("op")
            print(f"Giocatore {self.get_name()} in {self.zone} sceglie op: {op}")

            if op == 1:
                targets = [p for p in all_players if p.zone == self.zone and p != self and p.life_points > 0]
                if targets:
                    target = random.choice(targets)
                    self.attack_player(target)
                    print(
                        f"Player {self.get_name()} ha attaccato il player {target.get_name()}, vita rimanente: {target.life_points}")
                else:
                    print(f"Player {self.get_name()} ha provato ad attaccare ma non c'è nessuno in {self.zone}")
            elif op == 2:
                if self.game.weapons:
                    self.get_weapon()
                    print(f"Player {self.get_name()} ha raccolto {self.weapon[-1]}")
                else:
                    print(f"Player {self.nmome} voleva un'arma ma sono finite")
            elif op == 3:
                self.move_zone(all_players)
                print(f"{self.get_name()} si è spostato in {self.zone}")
            else:
                print("non vale ", op)

            return True
        except Exception as e:
            print("error")
            print(e)
            print(cl)
            return False

    def get_next_operation(self, all_players):
        targets = [p for p in all_players if p.zone == self.zone and p != self and p.life_points > 0]
        for _ in range(5):
            pr = self.get_prompt(targets)
            # print(pr)
            outputs = self.llm.generate(pr, self.sampling_params)
            if self.handle_op(outputs[0].outputs[0].text, all_players):
                break

    def __str__(self):
        return self.weapon.__str__()
