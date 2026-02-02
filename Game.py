import random

from Player import Player
from Stats import Stats


class Game:
    weapons = [{"name": "sword", "attack": 6}, {"name": "wooden sword", "attack": 4}, {"name": "knife", "attack": 5}, ]
    zones = ["Cornucopia", "Palude Nebbiosa", "Settore dei Geyser", "La Giungla Elettrica"]

    #zones = ["Cornucopia", "Palude Nebbiosa", ]

    stats= Stats()

    def __init__(self, n_groups=200, players_per_group=10):
        self.groups = {}
        self.n_groups = n_groups
        self.players_per_group = players_per_group
        for i in range(n_groups):
            self.groups[i] = []
            for j in range(players_per_group):
                self.groups[i].append(Player(self, distretto=i))

    def handle_leader_election(self):
        if self.players_per_group < 3:
            return
        i = 0
        for group in self.groups.values():
            sub = []
            found_leader = False
            found_leaders = False
            for n in range(5):
                print(f"Tentativo {n+1} per eleggere il leader del distretto {i}")
                for player in group:
                    s = player.get_next_leader_election(sub)
                    if s:
                        sub.append(player)

                print(f"Per il distretto {i} sono stati nominati {len(sub)} giocatori")

                if len(sub) == 1:
                    sub[0].is_leader = True
                    print(f"{sub[0].get_name()} è il nuovo leader del distretto {i} ")
                    found_leader = True
                    break

                if len(sub) == 2:
                    found_leaders = True
                    print(f"2 persone del distretto {i} sono stati nominati, ora si va alla votazione")
                    c1 = sub[0]
                    c2 = sub[1]
                    elected = False
                    for attempt in range(5):
                        print(f"Votazione {attempt + 1}/5 per il distretto {i}")
                        v1 = 0
                        v2 = 0
                        for p in group:
                            vote = p.get_vote(c1, c2)
                            if vote == 1:
                                v1 += 1
                            else:
                                v2 += 1
                        print(f"Voti: {c1.name}: {v1}, {c2.name}: {v2}")
                        if v1 > v2:
                            self.stats.add_leader_vote(c1,c2)
                            c1.is_leader = True
                            print(f"{c1.get_name()} vince ed è il nuovo leader!")
                            elected = True
                            break
                        elif v2 > v1:
                            self.stats.add_leader_vote(c2, c1)
                            c2.is_leader = True
                            print(f"{c2.get_name()} vince ed è il nuovo leader!")
                            elected = True
                            break
                        else:
                            print("Pareggio.")
                    if not elected:
                        print(f"Nessun leader eletto per il distretto {i} dopo 5 votazioni.")
                    break

            if not found_leader and not found_leaders:
                print(f"Il distretto {i} non avrà leader")

            i += 1
        self.stats.print_vote()

    def loop_game(self):

        all_players = []
        for group in self.groups.values():
            all_players.extend(group)

        while True:

            alive_players = [p for p in all_players if p.life_points > 0]
            if len(alive_players) <= 1:
                break

            random.shuffle(all_players)
            for p in all_players:
                if p.life_points <= 0:
                    continue

                current_alive = [ap for ap in all_players if ap.life_points > 0]
                if len(current_alive) <= 1:
                    break

                p.get_next_operation(current_alive)

        winner = [p for p in all_players if p.life_points > 0]
        if winner:
            print(f"Il vincitore è il giocatore del distretto {winner[0].distretto} {winner[0].name}")
            winner[0].stats.print()
        else:
            print("Non è rimasto nessun sopravvissuto.")
