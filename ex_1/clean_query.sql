
-- Reformatting the query to be more readable

-- First CTE
WITH most_recent_filing_id AS (
    SELECT 
        filer_committee_id_number
        ,coverage_from_date
        ,coverage_through_date 
        ,MAX(fec_report_id) AS report_id 
    FROM f3x_fecfile 
    WHERE 
        filer_committee_id_number = 'C00401224'
        AND coverage_from_date BETWEEN '2020-01-01' AND '2020-03-31'
    GROUP BY filer_committee_id_number, coverage_from_date, coverage_through_date --Renamed to be more explicit
),
-- Second CTE
FEC_Committee_Data_2020 AS (
    SELECT * 
    FROM fec_committees 
    WHERE bg_cycle = 2020
)
SELECT 
     sa.fec_report_id
    ,sa.date_report_received
    ,sa.form_type
    ,sa.filer_committee_id_number
    ,sa.transaction_id
    ,sa.entity_type
    ,sa.contributor_last_name
    ,sa.contributor_first_name 
    ,sa.contributor_street_1
    ,sa.contributor_city
    ,sa.contributor_state
    ,sa.contributor_zip_code
    ,sa.contribution_date
    ,sa.contribution_amount::text
    ,sa.contribution_aggregate::text 
    ,sa.contribution_purpose_descrip
    ,sa.contributor_employer
    ,sa.contributor_occupation
    ,sa.memo_text_description
FROM sa_fecfile sa
-- adding table name to join
JOIN most_recent_filing_id lr ON sa.fec_report_id = lr.report_id
WHERE UPPER(sa.form_type) = 'SA11AI'
ORDER BY random()
LIMIT 1600000;



-- Second Query
WITH FEC_Committee_Data_2020 AS (
    SELECT *
    FROM fec_committees
    WHERE bg_cycle = 2020
),
Contributions AS (
    SELECT
        a.filer_committee_id_number,
        a.contributor_state,
        SUM(a.contribution_aggregate) AS total
    FROM DS_technical_112221 a
    GROUP BY 1, 2
),
CommitteeContributions AS (
    SELECT
        c.cmte_nm,
        c.cmte_st,
        b.contributor_state,
        c.cmte_st = b.contributor_state AS instate,
        b.total
    FROM Contributions b
    JOIN FEC_Committee_Data_2020 c ON b.filer_committee_id_number = c.cmte_nm
)
SELECT
    cmte_nm,
    SUM(CASE WHEN instate THEN total END) AS instate,
    SUM(CASE WHEN NOT instate THEN total END) AS outofstate,
    SUM(CASE WHEN instate THEN total END)::NUMERIC / SUM(total)::NUMERIC AS instate_pct
FROM CommitteeContributions
GROUP BY 1
HAVING cmte_nm = 'ACTBLUE';
