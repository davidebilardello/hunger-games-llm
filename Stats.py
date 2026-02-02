class Stats:
    values = {1: 0, 2: 0, 3: 0}
    values_min = {1: 0, 2: 0, 3: 0}
    values_more = {1: 0, 2: 0, 3: 0}

    vote_more_attack = {"both_more": 0, "life_points_more": 0, "attack_power_more": 0, "both_less": 0, "equal": 0}

    def add_op_on_surv(self, op, hp, total_hp):
        self.values[op] += 1

        if hp > total_hp / 2:
            self.values_more[op] += 1
        else:
            self.values_min[op] += 1

    def add_leader_vote(self, pl1, pl2):
        if pl1.life_points > pl2.life_points and pl1.attack_power > pl2.attack_power:
            self.vote_more_attack["both_more"] += 1

        if pl1.life_points > pl2.life_points and pl1.attack_power <= pl2.attack_power:
            self.vote_more_attack["life_points_more"] += 1

        if pl1.life_points <= pl2.life_points and pl1.attack_power > pl2.attack_power:
            self.vote_more_attack["attack_power_more"] += 1

        if pl1.life_points < pl2.life_points and pl1.attack_power < pl2.attack_power:
            self.vote_more_attack["both_less"] += 1

        if pl1.life_points == pl2.life_points and pl1.attack_power == pl2.attack_power:
            self.vote_more_attack["equal"] += 1

    def print(self):
        print("Global operations")
        print(self.values)
        print("Operations with lower hp")
        print(self.values_min)
        print("Operations with higher hp")
        print(self.values_more)

    def print_vote(self):
        print(self.vote_more_attack)
