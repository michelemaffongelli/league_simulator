
import numpy as np
import pandas as pd
from fifa import *

class Teams():

    list_of_teams = []
    def __init__(self, team: str, overall_normalized: float, club_worth_eur_normalized: float):
        self.team = team
        self.overall_normalized = overall_normalized
        self.club_worth_eur_normalized = club_worth_eur_normalized
        self.points = 0
        self.goalfatti = 0
        self.goalsubiti = 0
        self.partitevinte = 0
        self.partitepareg = 0
        self.partiteperse = 0
        self.probability_of_scoring()
        self.add_team(self)

    @classmethod
    def add_team(cls, team):
        cls.list_of_teams.append(team)
    
    def probability_of_scoring(self):
        base_probabilities = [0.2, 0.33, 0.40, 0.05, 0.01, 0.01]
        modified_probabilities = [p + self.overall_normalized + self.club_worth_eur_normalized for p in base_probabilities]
        total_probability = sum(modified_probabilities)
        self.p = [p / total_probability for p in modified_probabilities]

    def expected_goals(self):
        self.min_goals = 0
        self.max_goals = 5
        values = np.arange(self.min_goals, self.max_goals +1)
        random_goals = np.random.choice(values, p=self.p)
        return random_goals

    def __repr__(self):
        return self.team

    
class League(Teams):
    
    def __init__(self, games_to_play: int):
        self.games_to_play = games_to_play
        self.calendario = []
    

    
    def calendar(self):
        for game in range(self.games_to_play):
            np.random.shuffle(self.list_of_teams)
            self.games = []
            for i in range(len(self.list_of_teams)):
                for j in range(i + 1, len(self.list_of_teams)):
                    if (self.list_of_teams[i], self.list_of_teams[j]) not in self.games and (self.list_of_teams[j], self.list_of_teams[i]) not in self.games:
                        self.games.append((self.list_of_teams[i], self.list_of_teams[j]))
                        self.games.append((self.list_of_teams[j], self.list_of_teams[i]))
        self.calendario.append(self.games)
        return self.calendario


    def __repr__(self):
        output = ""
        for game in self.games:
            output += f"{game[0]} vs {game[1]}\n"
        output += "\n"
        return output
    

class Matches(League, Teams):
    
    def __init__(self, league):
        self.league = league 

    def probability_of_scoring(self):
        base_probabilities = [0.2, 0.33, 0.40, 0.05, 0.01, 0.01]
        modified_probabilities = [p + self.overall_normalized + self.club_worth_eur_normalized for p in base_probabilities]
        total_probability = sum(modified_probabilities)
        self.p = [p / total_probability for p in modified_probabilities]

    def expected_goals(self):
        self.min_goals = 0
        self.max_goals = 5
        values = np.arange(self.min_goals, self.max_goals +1)
        random_goals = np.random.choice(values, p=self.p)
        return random_goals
    
    def match(self):
        for day, games in enumerate(self.league.calendario, start=1):
            for game in games:
                team1, team2 = game
                goalteam1 = team1.expected_goals()
                goalteam2 = team2.expected_goals()
                team1.goalfatti += goalteam1
                team1.goalsubiti += goalteam2
                team2.goalfatti += goalteam2
                team2.goalsubiti += goalteam1
                
                if goalteam1 > goalteam2:
                    team1.points += 3
                    team1.partitevinte += 1
                    team2.partiteperse += 1
                elif goalteam1 == goalteam2:
                    team1.points += 1
                    team2.points += 1
                    team1.partitepareg += 1
                    team2.partitepareg += 1
                elif goalteam1 < goalteam2:
                    team2.points += 3
                    team2.partitevinte += 1
                    team1.partiteperse += 1
                print(f"{team1.team} vs {team2.team}: {goalteam1} - {goalteam2}")

        

        
            
class Stats(Matches):

    def __init__(self):
        pass

    def table(self):
        data = [[team.team, team.points, team.partitevinte, team.partitepareg, team.partiteperse, team.goalfatti , team.goalsubiti] for team in self.list_of_teams]
        table = pd.DataFrame(data, columns=['Teams', 'Punti','V','N', 'P', 'Goal fatti', 'Goal subiti'])
        table = table.sort_values(by='Punti', ascending=False)
        winner = table.iloc[0, table.columns.get_loc('Teams')]
        relegated1 = table.iloc[-1, table.columns.get_loc('Teams')]
        relegated2 = table.iloc[-2, table.columns.get_loc('Teams')]
        relegated3 = table.iloc[-3, table.columns.get_loc('Teams')]
        print(table)
        print(f'The winner of the league is {winner}')
        print(f'The three relegated teams are {relegated1}, {relegated2}, {relegated3}')


class Run(Fifa, Stats):

    def __init__(self, league_id: int, fifa_version: int, games_to_play: int):
        fifa_data = Fifa.load(league_id, fifa_version)
        for _, row in fifa_data.iterrows():
            Teams(team=row['team_name'], overall_normalized= row['overall_normalized'], club_worth_eur_normalized=row['club_worth_eur_normalized'])
        print(Teams.list_of_teams)
        league = League(games_to_play)
        calendarioleague = league.calendar()
        print(calendarioleague)
        matches = Matches(league)
        matches.match()
        classifica = Stats()
        classifica.table()


        



    






    





















