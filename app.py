################################################################################
##                                  LIBRARIES                                 ##
################################################################################

################
##  EXTERNAL  ##
################

import os
import json
import pandas as pd


################
##  INTERNAL  ##
################

from etl.extract import get_events
from etl.transform import (
    process_cards,
    process_goalscorers,
    process_substitutions,
    process_matches,
    process_teams,
    process_matches_normalize
)
from etl.load import get_db_engine
from etl.export import export_data
import config


################################################################################
##              ENVIRONMENT VARIABLES, CONFIGURATIONS, & SETTINGS             ##
################################################################################

# Set the API key
API_KEY = config.API_KEY

# Set the base URL
BASE_URL = config.BASE_URL

# Set the base payload
BASE_PAYLOAD = config.BASE_PAYLOAD

# Set the date ranges
DATE_RANGES = config.DATE_RANGES

# Postgres database url
POSTGRESQL_URL = config.POSTGRESQL_URL
    

################################################################################
##                                    MAIN                                    ##
################################################################################

if __name__ == "__main__":
    # Initialize an empty list of matches
    matches = []

    #################
    ##   EXTRACT   ##
    #################

    # Loop over each date range
    for date_range in DATE_RANGES:
        # Get matches_list
        matches_list = get_events(url=BASE_URL, params={
                                  **BASE_PAYLOAD, **date_range})

        # Extend the main list with this list of matches
        matches.extend(matches_list)

    # Save the list of matches to an auxiliary JSON file
    with open('utils/matches.json', 'w') as matches_file:
        json.dump(matches, matches_file)

    #################
    ##  TRANSFORM  ##
    #################

    # Empty lists to store data for each table
    matches_list = []
    teams_list = []
    goalscorers_list = []
    cards_list = []
    substitutions_list = []
    lineups_list = []
    statistics_list = []

    # Loop over each match in the data list
    for match in matches:
        # Add match data to matches list
        matches_list.append(match)

        # Add team data to teams list
        teams_list.extend([
            {'team_id': match['match_hometeam_id'],
                'team_name': match['match_hometeam_name']},
            {'team_id': match['match_awayteam_id'],
                'team_name': match['match_awayteam_name']}
        ])

        for scorer in match['goalscorer']:
            scorer.update({'match_id': match['match_id']})
            goalscorers_list.append(scorer)

        for card in match['cards']:
            card.update({'match_id': match['match_id']})
            cards_list.append(card)

        for sub in match['substitutions']['home']:
            sub.update(
                {'match_id': match['match_id'], 'team_id': match['match_hometeam_id']})
            substitutions_list.append(sub)

        for sub in match['substitutions']['away']:
            sub.update(
                {'match_id': match['match_id'], 'team_id': match['match_awayteam_id']})
            substitutions_list.append(sub)

        for lineup in match['lineup']['home']['starting_lineups']:
            lineup.update(
                {'match_id': match['match_id'], 'team_id': match['match_hometeam_id'], "lineup_type": "starting", "home": 1})
            lineups_list.append(lineup)

        for lineup in match['lineup']['away']['starting_lineups']:
            lineup.update(
                {'match_id': match['match_id'], 'team_id': match['match_awayteam_id'], "lineup_type": "starting", "home": 0})
            lineups_list.append(lineup)

        for lineup in match['lineup']['home']['substitutes']:
            lineup.update(
                {'match_id': match['match_id'], 'team_id': match['match_hometeam_id'], "lineup_type": "substitute", "home": 1})
            lineups_list.append(lineup)

        for lineup in match['lineup']['away']['substitutes']:
            lineup.update(
                {'match_id': match['match_id'], 'team_id': match['match_awayteam_id'], "lineup_type": "substitute", "home": 0})
            lineups_list.append(lineup)

        for lineup in match['lineup']['home']['missing_players']:
            lineup.update(
                {'match_id': match['match_id'], 'team_id': match['match_hometeam_id'], "lineup_type": "missing", "home": 1})
            lineups_list.append(lineup)

        for lineup in match['lineup']['away']['missing_players']:
            lineup.update(
                {'match_id': match['match_id'], 'team_id': match['match_awayteam_id'], "lineup_type": "missing", "home": 0})
            lineups_list.append(lineup)

        for statistic in match['statistics']:
            statistic.update({'match_id': match['match_id'], 'fulltime': 1})
            statistics_list.append(statistic)

        for statistic in match['statistics_1half']:
            statistic.update({'match_id': match['match_id'], 'fulltime': 0})
            statistics_list.append(statistic)

    # Convert lists to pandas DataFrame
    matches_df = pd.DataFrame(matches_list).drop(columns=[
        "cards", "substitutions", "goalscorer", "lineup", "statistics", "statistics_1half"])
    teams_df = pd.DataFrame(teams_list).drop_duplicates(
        subset=["team_id"]).reset_index(drop=True)
    goalscorers_df = pd.DataFrame(goalscorers_list)
    cards_df = pd.DataFrame(cards_list)
    substitutions_df = pd.DataFrame(substitutions_list)
    lineups_df = pd.DataFrame(lineups_list)
    statistics_df = pd.DataFrame(statistics_list)

    # Create players dataframe from lineups_df
    players_df = lineups_df[['lineup_player', 'player_key']].drop_duplicates(
        subset=['player_key']).reset_index(drop=True)
    players_df.rename(
        columns={'lineup_player': 'player', 'player_key': 'player_id'}, inplace=True)

    # Process goalscorers
    goalscorers_df = process_goalscorers(goalscorers_df)
    # Process cards
    cards_df = process_cards(cards_df)
    # Process substitutions
    substitutions_df = process_substitutions(substitutions_df)
    # Process teams
    teams_df = process_teams(teams_df, matches_df)
    # Process matches
    matches_df = process_matches(matches_df)
    # Process matches_normalize
    match_details_df, match_scores_df = process_matches_normalize(matches_df)
    

    #################
    ##   LOAD      ##
    #################
    
    # Get database engine
    engine = get_db_engine(POSTGRESQL_URL)

    # Load match_details_df to database
    match_details_df.to_sql(name='match_details', con=engine, if_exists='append', index=False)

    # Load match_scores_df to database
    match_scores_df.to_sql(name='match_scores', con=engine, if_exists='append', index=False)

    # Load teams_df to database
    teams_df.to_sql(name='teams', con=engine, if_exists='append', index=False)

    # Load players_df to database
    players_df.to_sql(name='players', con=engine, if_exists='append', index=False)

    # Load goalscorers_df to database
    goalscorers_df.to_sql(name='goalscorers', con=engine, if_exists='append', index=False)

    # Load cards_df to database
    cards_df.to_sql(name='cards', con=engine, if_exists='append', index=False)

    # Load substitutions_df to database
    substitutions_df.to_sql(name='substitutions', con=engine, if_exists='append', index=False)

    # Load lineups_df to database
    lineups_df.to_sql(name='lineups', con=engine, if_exists='append', index=False)

    # Load statistics_df to database
    statistics_df.to_sql(name='statistics', con=engine, if_exists='append', index=False)


    #################
    ##   EXPORT    ##
    #################

    # Export data to CSV
    export_data(
        db_params={
            "host": "premier-league-postgres",
            "database": "premierleague",
            "user": os.environ["POSTGRES_USER"],
            "password": os.environ["POSTGRES_PASSWORD"]
        }
    )