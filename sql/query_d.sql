WITH GoalScorers AS (
    SELECT
        p."player" AS "player_name",
        t."team_name",
        COUNT(gs."scorer_id") AS "goals"
    FROM
        "players" p
    LEFT JOIN
        "goalscorers" gs ON p."player_id" = gs."scorer_id"
    LEFT JOIN
        "teams" t ON (
            t."team_id" = gs."home_away" AND gs."home_away" = 'home'
            OR
            t."team_id" = gs."home_away" AND gs."home_away" = 'away'
        )
    INNER JOIN
        "match_details" md ON gs."match_id" = md."id"
    WHERE
        CAST(md."round" AS INTEGER) <= 38
    GROUP BY
        p."player", t."team_name"
)
SELECT
    "player_name",
    "team_name",
    "goals"
FROM
    GoalScorers
ORDER BY
    "goals" DESC,
    "player_name" ASC
LIMIT 3;
