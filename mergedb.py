import json
import sqlite3
import os

json_file_path = "databases.json"

with open(json_file_path, "r") as json_file:
    file_paths_data = json.load(json_file)
    
merged_db_conn = sqlite3.connect("all_players_data.db")
merged_db_cursor = merged_db_conn.cursor()

merged_db_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = merged_db_cursor.fetchall()
for table in tables:
    merged_db_cursor.execute(f"DROP TABLE {table[0]}")

create_table_query = """
    CREATE TABLE IF NOT EXISTS all_player_stats (
        gameId STRING,
        steamId STRING,
        isCheating INTEGER,
        wonGame INTEGER,
        teamScores_0 INTEGER,
        teamScores_1 INTEGER,
        mpMaxrounds INTEGER,
        preaim REAL,
        reactionTime REAL,
        accuracy REAL,
        accuracyEnemySpotted REAL,
        accuracyHead REAL,
        shotsFiredEnemySpotted INTEGER,
        shotsFired INTEGER,
        shotsHitEnemySpotted INTEGER,
        shotsHitFriend INTEGER,
        shotsHitFriendHead INTEGER,
        shotsHitFoe INTEGER,
        shotsHitFoeHead INTEGER,
        utilityOnDeathAvg REAL,
        heFoesDamageAvg REAL,
        heFriendsDamageAvg REAL,
        heThrown INTEGER,
        molotovThrown INTEGER,
        smokeThrown INTEGER,
        smokeThrownCT INTEGER,
        smokeThrownCTGood INTEGER,
        smokeThrownCTGoodRatio INTEGER,
        smokeThrownCTFoes INTEGER,
        counterStrafingShotsAll INTEGER,
        counterStrafingShotsBad INTEGER,
        counterStrafingShotsGood INTEGER,
        counterStrafingShotsGoodRatio REAL,
        flashbangHitFoe INTEGER,
        flashbangLeadingToKill INTEGER,
        flashbangHitFoeAvgDuration REAL,
        flashbangHitFriend INTEGER,
        flashbangThrown INTEGER,
        flashAssist INTEGER,
        score INTEGER,
        initialTeamNumber INTEGER,
        mvps INTEGER,
        ctRoundsWon INTEGER,
        ctRoundsLost INTEGER,
        tRoundsWon INTEGER,
        tRoundsLost INTEGER,
        sprayAccuracy REAL,
        totalKills INTEGER,
        totalDeaths INTEGER,
        kdRatio REAL,
        multi2k INTEGER,
        multi3k INTEGER,
        multi4k INTEGER,
        multi5k INTEGER,
        hltvRating REAL,
        hsp REAL,
        roundsSurvived INTEGER,
        roundsSurvivedPercentage REAL,
        dpr REAL,
        totalAssists INTEGER,
        totalDamage INTEGER,
        tradeKillOpportunities INTEGER,
        tradeKillAttempts INTEGER,
        tradeKillsSucceeded INTEGER,
        tradeKillAttemptsPercentage REAL,
        tradeKillsSuccessPercentage REAL,
        tradeKillOpportunitiesPerRound REAL,
        tradedDeathOpportunities INTEGER,
        tradedDeathAttempts INTEGER,
        tradedDeathAttemptsPercentage REAL,
        tradedDeathsSucceeded INTEGER,
        tradedDeathsSuccessPercentage REAL,
        tradedDeathsOpportunitiesPerRound REAL,
        leetifyRating REAL,
        personalPerformanceRating REAL,
        ctLeetifyRating REAL,
        tLeetifyRating REAL,
        openingDuels INTEGER
    );
"""

merged_db_cursor.execute(create_table_query)
merged_db_conn.commit()

for db_file_path in file_paths_data["databases"]:
    if os.path.exists(db_file_path):
        db_conn = sqlite3.connect(db_file_path)
        db_cursor = db_conn.cursor()
        
        db_cursor.execute("SELECT * FROM player_stats")
        data_to_merge = db_cursor.fetchall()
        
        merged_db_cursor.executemany("INSERT INTO all_player_stats VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", data_to_merge)
        merged_db_conn.commit()
        db_conn.close()

merged_db_conn.close()