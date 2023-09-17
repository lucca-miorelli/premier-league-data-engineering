################################################################################
##                                  LIBRARIES                                 ##
################################################################################

################
##  EXTERNAL  ##
################

import pandas as pd


################################################################################
##                                  FUNCTIONS                                 ##
################################################################################


def process_goalscorers(goalscorers_df):
    # Create separate dataframes for home and away goals
    home_goals = goalscorers_df[goalscorers_df['home_scorer_id'].notna() & (goalscorers_df['home_scorer_id'] != '')].copy()
    home_goals.rename(columns={'home_scorer': 'scorer', 'home_scorer_id': 'scorer_id', 'home_assist': 'assist', 'home_assist_id': 'assist_id'}, inplace=True)
    home_goals['home_away'] = 'home'

    away_goals = goalscorers_df[goalscorers_df['away_scorer_id'].notna() & (goalscorers_df['away_scorer_id'] != '')].copy()
    away_goals.rename(columns={'away_scorer': 'scorer', 'away_scorer_id': 'scorer_id', 'away_assist': 'assist', 'away_assist_id': 'assist_id'}, inplace=True)
    away_goals['home_away'] = 'away'

    # Append the two dataframes together and sort by match_id and time
    all_goals = pd.concat([home_goals, away_goals])
    all_goals = all_goals.sort_values(by=['match_id', 'time']).reset_index(drop=True)

    #  Select the columns of interest
    all_goals = all_goals[['time', 'scorer', 'scorer_id', 'assist', 'assist_id', 'score', 'info', 'score_info_time', 'match_id', 'home_away']]

    return all_goals


def process_cards(cards_df):
    # Create separate dataframes for home and away cards
    home_cards = cards_df[cards_df['home_player_id'].notna() & (cards_df['home_player_id'] != '')].copy()
    home_cards.rename(columns={'home_fault': 'player', 'home_player_id': 'player_id'}, inplace=True)
    home_cards['home_away'] = 'home'

    away_cards = cards_df[cards_df['away_player_id'].notna() & (cards_df['away_player_id'] != '')].copy()
    away_cards.rename(columns={'away_fault': 'player', 'away_player_id': 'player_id'}, inplace=True)
    away_cards['home_away'] = 'away'

    # Combine the two dataframes together and sort by match_id and time
    all_cards = pd.concat([home_cards, away_cards])
    all_cards = all_cards.sort_values(by=['match_id', 'time']).reset_index(drop=True)

    # Select the columns of interest
    all_cards = all_cards[['time', 'player', 'player_id', 'card', 'info', 'score_info_time', 'match_id', 'home_away']]

    return all_cards


def process_substitutions(substitutions_df):

    # Process rows where 'substitution' column contains ' | '
    substitution_contains_splitter = substitutions_df['substitution'].str.contains('|', regex=False)

    substitution_with_split = substitutions_df[substitution_contains_splitter].copy()
    substitution_without_split = substitutions_df[~substitution_contains_splitter].copy()

    # Split 'substitution' into 'player_out' and 'player_in'
    substitution_with_split[['player_out', 'player_in']] = substitution_with_split['substitution'].str.split('|', expand=True)

    # Split 'substitution_player_id' into 'player_out_id' and 'player_in_id'
    substitution_with_split[['player_out_id', 'player_in_id']] = substitution_with_split['substitution_player_id'].str.split('|', expand=True)

    # The rows without '|' can be processed separately depending on the requirement

    # Concatenate rows with and without splits
    substitutions_df = pd.concat([substitution_with_split, substitution_without_split], ignore_index=True)

    # Drop the original 'substitution' and 'substitution_player_id' columns
    substitutions_df = substitutions_df.drop(columns=['substitution', 'substitution_player_id'])

    return substitutions_df

def process_teams(teams_df, matches_df):
    
    badge_team_id = matches_df[["match_hometeam_id", "team_home_badge"]].drop_duplicates()
    # Merge badge_team_id with teams_df
    teams_df = teams_df.merge(badge_team_id, how="left", left_on="team_id", right_on="match_hometeam_id")
    teams_df.drop(columns=["match_hometeam_id"], inplace=True)
    teams_df.rename(columns={"team_home_badge": "team_badge"}, inplace=True)
    
    return teams_df


def process_matches(matches_df):
    
    # Remove match_ prefix from columns
    matches_df.columns = matches_df.columns.str.replace("match_", "")
    
    # Drop badges columns from matches_df
    matches_df.drop(columns=["team_home_badge", "team_away_badge"], inplace=True)

    # Drop unused columns
    matches_df.drop(
        columns=[
            "league_id",
            "league_name",
            "country_id",
            "country_name",
            "league_logo",
            "country_logo",
            "league_year",
            "fk_stage_key",
            "stage_name",
            "hometeam_name",
            "awayteam_name",
            "live",
        ]
    )

    return matches_df

def process_matches_normalize(matches_df):

    match_details_df = \
        matches_df[[
            "id",
            "date",
            "time",
            "status",
            "round",
            "stadium",
            "referee",
            "hometeam_halftime_score",
            "awayteam_halftime_score",
            "hometeam_extra_score",
            "awayteam_extra_score",
            "hometeam_penalty_score",
            "awayteam_penalty_score",
            "hometeam_ft_score",
            "awayteam_ft_score",
            "hometeam_system",
            "awayteam_system"
        ]]

    match_scores_df = \
        matches_df[[
            "id",
            "hometeam_id",
            "hometeam_score",
            "awayteam_id",
            "awayteam_score",
        ]]

    return match_details_df, match_scores_df