with most_recent_filing_id as (
select filer_committee_id_number
,coverage_from_date
,coverage_through_date 
,max(fec_report_id) as report_id 
from f3x_fecfile 
where filer_committee_id_number='C00401224'
and coverage_from_date between '2020-01-01' and '2020-03-31'
group by 1,2,3)
select sa.fec_report_id
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
from sa_fecfile sa
join lr on sa.fec_report_id=lr.report_id
where upper(sa.form_type)='SA11AI'
order by random()
limit 1600000
), FEC_Committee_Data_2020 as (
select * from fec_committees where bg_cycle=2020
)
SELECT cmte_nm
    ,sum(case when instate=TRUE then total end) as instate
    ,sum(case when instate=FALSE then total end) as outofstate
    ,sum(case when instate=TRUE then total end)::numeric / sum(total)::numeric as instate_pct
    
from (
SELECT c.cmte_nm
    ,c.cmte_st
    ,b.contributor_state
    ,c.cmte_st = b.contributor_state as instate
    ,b.total
    
from (SELECT a.filer_committee_id_number
    ,a.contributor_state
    ,sum(a.contribution_aggregate) total
from DS_technical_112221 a
group by 1,2) b
    ,FEC_Committee_Data_2020 as c
)
group by 1
having cmte_nm = 'ACTBLUE';




-- FIXED QUERY (I used a bunch of CTEs to keep the query organized, consistent, and easier to read.)
-- First CTE - This CTE is used to filter the f3x_fecfile table to only include records from the most recent filing
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
    GROUP BY filer_committee_id_number, coverage_from_date, coverage_through_date --Renamed to be explicit
),
-- Second CTE
DS_technical_112221 AS ( -- I noticed this name in the 4th CTE query that uses these fields, so I'm assuming that this should be named DS_technical_112221
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
    -- adding table name to join and an inner join (filter sa_fecfile table to only include records from most recent filing)
    INNER JOIN most_recent_filing_id lr ON sa.fec_report_id = lr.report_id
    WHERE UPPER(sa.form_type) = 'SA11AI'
    ORDER BY random()
    LIMIT 1600000
),
-- I removed FEC_Committee_Data_2020 CTE because I was able to include it directly into the 4th CTE, as that was the only place it was referenced. I also removed the SELECT * and replaced it with the specific columns that were used in the query.
-- Third CTE
cmte_state_total AS (
    SELECT 
         filer_committee_id_number
        ,contributor_state
        ,SUM(contribution_aggregate) AS total
    FROM DS_technical_112221 -- used this name for the 2nd CTE
    GROUP BY filer_committee_id_number, contributor_state -- Renamed to be more explicit
),
-- Fourth CTE
contributions AS (
    SELECT
        c.cmte_nm,
        c.cmte_st,
        t.contributor_state,
        c.cmte_st = t.contributor_state AS instate,
        t.total
    FROM cmte_state_total t
    JOIN fec_committees c ON t.filer_committee_id_number = c.cmte_nm
    WHERE bg_cycle = 2020
)

-- Final Query (Results)
SELECT 
     cmte_nm
    ,SUM(CASE WHEN     instate THEN total END)                                AS instate
    ,SUM(CASE WHEN NOT instate THEN total END)                                AS outofstate
    ,SUM(CASE WHEN     instate THEN total END)::numeric / SUM(total)::numeric AS instate_pct
FROM contributions
WHERE cmte_nm = 'ACTBLUE' -- changing HAVING to WHERE because it's filtering on a non-aggregated column. Better performance this way.
GROUP BY cmte_nm;


