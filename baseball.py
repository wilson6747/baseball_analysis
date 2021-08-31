# %%
# imports libraries
import pandas as pd 
import altair as alt
import numpy as np 
import datadotworld as dw
import sqlite3

# %%
# imports data for baseball
sqlite_file = 'lahmansbaseballdb.sqlite'
con = sqlite3.connect(sqlite_file)

# %%
# 1 - queries database for baseball players who went to BYUI
# creates dataframe of data
baseball_byui = pd.read_sql_query("""
SELECT DISTINCT CollegePlaying.playerid, CollegePlaying.schoolid,
Salaries.salary, CollegePlaying.yearid, Salaries.teamid
FROM Collegeplaying
    LEFT JOIN Salaries
    ON Collegeplaying.playerid = Salaries.playerid
WHERE schoolID = 'idbyuid'
ORDER BY salary DESC
""", con
)
baseball_byui

# %%
# 1 - prints byui table to markdown
print(baseball_byui.to_markdown)

# %%
# 2-a lists players with at least one at bat, limit to 5
at_least_one_at_bat = pd.read_sql_query("""
SELECT playerid, yearid,
ROUND((CAST (h AS FLOAT (18,4))) / (CAST (ab AS FLOAT (18,4))),3) AS 'batting average'
FROM Batting
WHERE ab > 1
ORDER BY ROUND((CAST (h AS FLOAT (18,4))) / (CAST (ab AS FLOAT (18,4))),3) DESC
LIMIT 5
""", con
)
at_least_one_at_bat

# %%
# 2-a prints at_least_one_at_bat to markdown
print(at_least_one_at_bat.to_markdown())

# %%
# 2-b lists players with at least ten at bat, limit to 5
at_least_ten_at_bat = pd.read_sql_query("""
SELECT playerid, yearid,
ROUND((CAST (h AS FLOAT (18,4))) / (CAST (ab AS FLOAT (18,4))),3) AS 'batting average'
FROM Batting
WHERE ab > 10
ORDER BY ROUND((CAST (h AS FLOAT (18,4))) / (CAST (ab AS FLOAT (18,4))),3) DESC
LIMIT 5
""", con
)
at_least_ten_at_bat

# %%
# 2-b prints at_least_ten_at_bat to markdown
print(at_least_ten_at_bat.to_markdown())

# %%
# 2-c group by players and include only people who have at least 100 at bats
group_at_least_100_at_bat = pd.read_sql_query("""
SELECT playerid, yearid,
ROUND((CAST (h AS FLOAT (18,4))) / (CAST (ab AS FLOAT (18,4))),3) AS 'batting average'
FROM Batting
GROUP BY playerid
HAVING ab > 100
ORDER BY ROUND((CAST (h AS FLOAT (18,4))) / (CAST (ab AS FLOAT (18,4))),3) DESC
LIMIT 5
""", con
)
group_at_least_100_at_bat

# %%
# 2-c print group_at_least_100_at_bat to markdown
print(group_at_least_100_at_bat.to_markdown())

# %%
# 3 - creates dataframe comparing batting average for the two teams
batting_average_team_compare = pd.read_sql_query("""
SELECT teamid, name,
ROUND((CAST (sum(h) AS FLOAT (30,4))) / (CAST (sum(ab) AS FLOAT (30,4))),4) AS 'batting average'
FROM Teams
GROUP BY name
HAVING name = 'Boston Red Sox' OR name = 'New York Yankees'
ORDER BY ROUND((CAST (sum(h) AS FLOAT (30,4))) / (CAST (sum(ab) AS FLOAT (30,4))),4)
""", con
)
batting_average_team_compare

# %%
# 3 - print batting_average_team_compare to markdown
print(batting_average_team_compare.to_markdown())

# %%
# 3 - creates dataframe comaring wins to loses
win_loss_team_compare = pd.read_sql_query("""
SELECT teamid, name,
ROUND((CAST (sum(w) AS FLOAT (30,4))) / (CAST (sum(l) AS FLOAT (30,4))),4) AS 'win to loss ratio'
FROM Teams
GROUP BY name
HAVING name = 'Boston Red Sox' OR name = 'New York Yankees'
ORDER BY ROUND((CAST (sum(w) AS FLOAT (30,4))) / (CAST (sum(l) AS FLOAT (30,4))),4)
""", con
)
win_loss_team_compare

# %%
# 3 - prints win_loss_team_compare to markdown
print(win_loss_team_compare.to_markdown())

# %%
# graphs win to loss ratio comparing new york yankees and boston red soxs
alt.Chart(win_loss_team_compare, 
title = 'Red Soxs vs Yankees Win to Loss Ratios').encode(
    alt.X('win to loss ratio', title = 'win to loss ratio'),
    alt.Y('name', title = None),
    alt.Color('name'),
).mark_bar().properties(width=500, height=150).save('win_loss_team_compare.png')


# %%
