WITH TeamStats AS (
    SELECT
        t."team_name",
        COUNT(md."id") AS "matches_played",
        SUM(CASE
            WHEN ms."hometeam_score" > ms."awayteam_score" AND ms."hometeam_id" = t."team_id" THEN 1
            WHEN ms."awayteam_score" > ms."hometeam_score" AND ms."awayteam_id" = t."team_id" THEN 1
            ELSE 0
        END) AS "won",
        SUM(CASE
            WHEN ms."hometeam_score" = ms."awayteam_score" THEN 1
            ELSE 0
        END) AS "draw",
        SUM(CASE
            WHEN ms."hometeam_score" < ms."awayteam_score" AND ms."hometeam_id" = t."team_id" THEN 1
            WHEN ms."awayteam_score" < ms."hometeam_score" AND ms."awayteam_id" = t."team_id" THEN 1
            ELSE 0
        END) AS "lost",
        SUM(CASE
            WHEN ms."hometeam_id" = t."team_id" THEN
                CASE
                    WHEN ms."hometeam_score" ~ E'^\\d+$' THEN CAST(ms."hometeam_score" AS INT)
                    ELSE 0
                END
            ELSE
                CASE
                    WHEN ms."awayteam_score" ~ E'^\\d+$' THEN CAST(ms."awayteam_score" AS INT)
                    ELSE 0
                END
        END) AS "goals_scored",
        SUM(CASE
            WHEN ms."hometeam_id" = t."team_id" THEN
                CASE
                    WHEN ms."awayteam_score" ~ E'^\\d+$' THEN CAST(ms."awayteam_score" AS INT)
                    ELSE 0
                END
            ELSE
                CASE
                    WHEN ms."hometeam_score" ~ E'^\\d+$' THEN CAST(ms."hometeam_score" AS INT)
                    ELSE 0
                END
        END) AS "goals_conceded",
        SUM(CASE
            WHEN ms."hometeam_id" = t."team_id" AND ms."hometeam_score" > ms."awayteam_score" THEN 3
            WHEN ms."awayteam_id" = t."team_id" AND ms."awayteam_score" > ms."hometeam_score" THEN 3
            WHEN ms."hometeam_score" = ms."awayteam_score" THEN 1
            ELSE 0
        END) AS "points"
    FROM
        "teams" t
    LEFT JOIN
        "match_scores" ms ON t."team_id" = ms."hometeam_id" OR t."team_id" = ms."awayteam_id"
    LEFT JOIN
        "match_details" md ON ms."id" = md."id"
    WHERE
        md."status" = 'Finished'
    GROUP BY
        t."team_name", t."team_id"
)
SELECT
    ROW_NUMBER() OVER (ORDER BY "points" DESC, ("goals_scored" - "goals_conceded") DESC, "goals_scored" DESC, "goals_conceded" ASC, "won" DESC) AS "position",
    "team_name",
    "matches_played",
    "won",
    "draw",
    "lost",
    "goals_scored",
    "goals_conceded",
    "points"
FROM
    TeamStats;
