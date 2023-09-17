-- init.sql

CREATE TABLE teams (
    team_id TEXT PRIMARY KEY,
    team_name TEXT,
    team_badge TEXT
);

CREATE TABLE goalscorers (
    "time" TEXT,
    scorer TEXT,
    scorer_id TEXT,
    assist TEXT,
    assist_id TEXT,
    score TEXT,
    info TEXT,
    score_info_time TEXT,
    match_id TEXT,
    home_away TEXT
);

CREATE TABLE cards (
    "time" TEXT,
    player TEXT,
    player_id TEXT,
    "card" TEXT,
    info TEXT,
    score_info_time TEXT,
    match_id TEXT,
    home_away TEXT
);

CREATE TABLE substitutions (
    "time" TEXT,
    match_id TEXT,
    team_id TEXT,
    player_out TEXT,
    player_in TEXT,
    player_out_id TEXT,
    player_in_id TEXT
);

CREATE TABLE lineups (
    lineup_player TEXT,
    lineup_number TEXT,
    lineup_position TEXT,
    player_key TEXT,
    match_id TEXT,
    team_id TEXT,
    lineup_type TEXT,
    home INTEGER
);

CREATE TABLE players (
    player TEXT,
    player_id TEXT PRIMARY KEY
);

CREATE TABLE statistics (
    "type" TEXT,
    home TEXT,
    away TEXT,
    match_id TEXT,
    fulltime INTEGER
);

CREATE TABLE match_details (
    id TEXT,
    "date" TEXT,
    "time" TEXT,
    "status" TEXT,
    round TEXT,
    stadium TEXT,
    referee TEXT,
    hometeam_halftime_score TEXT,
    awayteam_halftime_score TEXT,
    hometeam_extra_score TEXT,
    awayteam_extra_score TEXT,
    hometeam_penalty_score TEXT,
    awayteam_penalty_score TEXT,
    hometeam_ft_score TEXT,
    awayteam_ft_score TEXT,
    hometeam_system TEXT,
    awayteam_system TEXT
);

CREATE TABLE match_scores (
    id TEXT,
    hometeam_id TEXT,
    hometeam_score TEXT,
    awayteam_id TEXT,
    awayteam_score TEXT
);


-- Relationship between match_details and match_scores
-- ALTER TABLE match_scores
-- ADD CONSTRAINT fk_match_scores_match_details
-- FOREIGN KEY (id) REFERENCES match_details (id);

-- -- Relationships between match_scores and teams
-- ALTER TABLE match_scores
-- ADD CONSTRAINT fk_match_scores_hometeam_teams
-- FOREIGN KEY (hometeam_id) REFERENCES teams (team_id);

-- -- Relationships between match_scores and teams
-- ALTER TABLE match_scores
-- ADD CONSTRAINT fk_match_scores_awayteam_teams
-- FOREIGN KEY (awayteam_id) REFERENCES teams (team_id);

-- -- Relationship between match_scores and goalscorers
-- ALTER TABLE goalscorers
-- ADD CONSTRAINT fk_goalscorers_match_scores
-- FOREIGN KEY (match_id) REFERENCES match_scores (id);

-- -- Relationship between match_details and cards
-- ALTER TABLE cards
-- ADD CONSTRAINT fk_cards_match_details
-- FOREIGN KEY (match_id) REFERENCES match_details (id);

-- -- Relationship between match_details and substitutions
-- ALTER TABLE substitutions
-- ADD CONSTRAINT fk_substitutions_match_details
-- FOREIGN KEY (match_id) REFERENCES match_details (id);

-- -- Relationship between match_details and lineups
-- ALTER TABLE lineups
-- ADD CONSTRAINT fk_lineups_match_details
-- FOREIGN KEY (match_id) REFERENCES match_details (id);

-- -- Relationship between match_details and statistics
-- ALTER TABLE statistics
-- ADD CONSTRAINT fk_statistics_match_details
-- FOREIGN KEY (match_id) REFERENCES match_details (id);

-- -- Relationship between goalscorers and players
-- ALTER TABLE goalscorers
-- ADD CONSTRAINT fk_goalscorers_scorer_players
-- FOREIGN KEY (scorer_id) REFERENCES players (player_id);

-- ALTER TABLE goalscorers
-- ADD CONSTRAINT fk_goalscorers_assist_players
-- FOREIGN KEY (assist_id) REFERENCES players (player_id);

-- -- Relationship between substitutions and players
-- ALTER TABLE substitutions
-- ADD CONSTRAINT fk_substitutions_player_in_players
-- FOREIGN KEY (player_in_id) REFERENCES players (player_id);

-- ALTER TABLE substitutions
-- ADD CONSTRAINT fk_substitutions_player_out_players
-- FOREIGN KEY (player_out_id) REFERENCES players (player_id);

-- -- Relationship between substitutions and teams
-- ALTER TABLE substitutions
-- ADD CONSTRAINT fk_substitutions_team_teams
-- FOREIGN KEY (team_id) REFERENCES teams (team_id);

-- -- Relationship between lineups and players
-- ALTER TABLE lineups
-- ADD CONSTRAINT fk_lineups_player_key_players
-- FOREIGN KEY (player_key) REFERENCES players (player_id);

-- -- Relationship between lineups and teams
-- ALTER TABLE lineups
-- ADD CONSTRAINT fk_lineups_team_teams
-- FOREIGN KEY (team_id) REFERENCES teams (team_id);

-- -- Relationship between cards and players
-- ALTER TABLE cards
-- ADD CONSTRAINT fk_cards_player_players
-- FOREIGN KEY (player_id) REFERENCES players (player_id);
