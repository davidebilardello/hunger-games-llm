from Player import Player


class Game:
    weapons = [{"name": "sword", "attack": 6}, {"name": "wooden sword", "attack": 4}, {"name": "knife", "attack": 5}, ]
    zones = ["Cornucopia", "Palude Nebbiosa", "Settore dei Geyser", "La Giungla Elettrica"]

    # zones = ["Cornucopia", "Palude Nebbiosa", ]

    def __init__(self, nGroups=10, groupPerPlayer=1):
        self.groups = {}
        for i in range(nGroups):
            self.groups[i] = []
            for j in range(groupPerPlayer):
                self.groups[i].append(Player(self, distretto=i))

    def loop_game(self):

        all_players = []
        for group in self.groups.values():
            all_players.extend(group)

        while True:

            alive_players = [p for p in all_players if p.life_points > 0]
            if len(alive_players) <= 1:
                break

            for p in all_players:
                if p.life_points <= 0:
                    continue

                current_alive = [ap for ap in all_players if ap.life_points > 0]
                if len(current_alive) <= 1:
                    break

                p.get_next_operation(current_alive)

        winner = [p for p in all_players if p.life_points > 0]
        if winner:
            print(f"Il vincitore è il giocatore del distretto {winner[0].distretto}")
        else:
            print("Non è rimasto nessun sopravvissuto.")
