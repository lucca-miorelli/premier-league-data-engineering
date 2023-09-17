SELECT
    t."team_name",
    COALESCE(SUM(CASE
        WHEN ms."awayteam_score" ~ E'^\\d+$' THEN CAST(ms."awayteam_score" AS INT)
        ELSE 0
    END), 0) AS "goals"
FROM
    "teams" t
LEFT JOIN
    "match_scores" ms ON t."team_id" = ms."awayteam_id"
GROUP BY
    t."team_name"
ORDER BY
    "goals" DESC,
    t."team_name";
