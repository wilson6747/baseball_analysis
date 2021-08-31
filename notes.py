# %%
import pandas as pd 
import altair as alt
import numpy as np 
import datadotworld as dw
# %%
import datadotworld as dw
con = 'byuidss/cse-250-baseball-database'
results = dw.query('byuidss/cse-250-baseball-database', 
    'SELECT * FROM batting LIMIT 5')
batting5 = results.dataframe
# %%
# query text
qt = """
SELECT playerid, yearid, r, ab, r / ab as runs_atbat
FROM batting
LIMIT 5
"""
dat = dw.query(con, qt).dataframe
# %%
# For seasons after 1999, which year had the most 
# players selected as All Stars but didn't play in 
# the All Star game?
qt = """
SELECT yearid, count(*)
FROM AllstarFull
WHERE gp != 1 
    AND yearid > 1999
GROUP BY yearid
ORDER BY yearid
"""
dat = dw.query(con, qt).dataframe
dat
# %%
dw.query(con, 
    'SELECT * FROM battingpost LIMIT 5').dataframe
# %%
# Provide a summary of how many games, hits, and 
# at bats occurred by those players had in 
# that years post season.
qt = """
-- Not sure this is right. This is a comment.
SELECT 
    bp.yearid, 
    bp.playerid,
    sum(bp.g) as games,
    sum(bp.h) as hits,
    sum(bp.ab) as atbats
FROM battingpost as bp
    JOIN AllstarFull as asf
    ON bp.playerid = asf.playerid
        AND bp.yearid = asf.yearid
WHERE asf.gp != 1 
    AND bp.yearid > 1999
GROUP BY bp.yearid
ORDER BY bp.yearid
"""
dat = dw.query(con, qt).dataframe
dat

# %%
# Day 2, Gets Data
import pandas as pd 
import altair as alt
import numpy as np
import sqlite3

# %%
sqlite_file = 'lahmansbaseballdb.sqlite'
con = sqlite3.connect(sqlite_file)
# %%
# See the tables in the database
table = pd.read_sql_query(
    "SELECT * FROM sqlite_master WHERE type='table'",
    con)
print(table.filter(['name']))
print('\n\n')
# 8 is collegeplaying
print(table.sql[8])

# %%
# finds out what data is in teams
teams = pd.read_sql_query("""
SELECT *
FROM teams
LIMIT 5
""", con
)
teams
# %%
# finds each of the data types
teams.dtypes

# %%
salaries = pd.read_sql_query("""
SELECT *
FROM salaries
LIMIT 5
""", con
)
salaries

# %%
batting = pd.read_sql_query("""
SELECT yearID, H, AB, playerID
FROM Batting
WHERE playerid = 'addybo01'
group by yearID

""", con
)
batting

# %%