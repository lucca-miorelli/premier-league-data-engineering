SELECT
    md."referee" AS "referee_name",
    SUM(CASE WHEN c."card" = 'yellow card' THEN 1 ELSE 0 END) +
    SUM(CASE WHEN c."card" = 'red card' THEN 1 ELSE 0 END) AS "cards"
FROM
    "cards" c
INNER JOIN
    "match_details" md ON c."match_id" = md."id"
GROUP BY
    md."referee"
ORDER BY
    "cards" DESC,
    "referee_name" ASC;