import pandas as pd

pd.set_option('display.max_rows', 22)

class Fifa():

    @staticmethod
    def load( league_id : int , fifa_version : int):
        F = pd.read_csv("male_teams.csv")
        selected_cols = [
            'league_id', 'team_name', 'team_id','fifa_version', 'club_worth_eur', 'overall'
        ]

        target = league_id
        mask = (F['league_id'] == target) & (F['fifa_version'] == fifa_version)
        filtered_F = F.loc[mask, selected_cols].drop_duplicates(subset=['team_id'])
        
        filtered_F['club_worth_eur'] = filtered_F['club_worth_eur'].abs()

        filtered_F['club_worth_eur_normalized'] = filtered_F['club_worth_eur'] / filtered_F['club_worth_eur'].sum()
        filtered_F['overall_normalized'] = filtered_F['overall'] / filtered_F['overall'].sum()

        print(filtered_F)  
        return filtered_F





        















