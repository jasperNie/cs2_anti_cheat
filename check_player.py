import sqlite3
import tensorflow as tf
import requests
import os
import json
import sys
import shutil
import numpy as np

def get_profile_json(steamId):
    info_url = "https://api.leetify.com/api/profile/" + steamId
    info = requests.get(info_url).json()
    return info

def find_player_by_steamId(player_stats_list, steamId):
    index = 0
    for player in player_stats_list:
        if player.get("steam64Id") == steamId:
            return player
        index += 1
    return None

def create_directory(steamId):
    path = os.path.join(os.getcwd(), steamId)
    path2 = os.path.join(path,"game_files")
    try:  
        os.mkdir(path)
        os.mkdir(path2)
    except OSError:  
        print("Directory Already Exists")
        return False
    return path

def get_game_data(gameId, directory):
    api_url = f"https://api.leetify.com/api/games/{gameId}"
    game_data = requests.get(api_url)
    opening_duels = requests.get(api_url+'/opening-duels')
    
    try:
        path = os.path.join(directory, "game_files", gameId)
        os.mkdir(path)
        game_file_name = os.path.join(path, gameId)
        opening_duels_file_name = os.path.join(path, gameId)
        with open(f"{game_file_name}_game_info.json", "w") as file:
            json.dump(game_data.json(), file, indent=4)
        with open(f"{opening_duels_file_name}_opening_duels.json", "w") as file:
            json.dump(opening_duels.json(), file, indent=4)
    except OSError as e:
        print("Game File Already Exists")

def populate_table(directory, steamId):
    games = os.listdir(os.path.join(directory,"game_files"))
    player_info = []
    
    for g in games:
        game_info = []
        game_file_path = os.path.join(os.path.join(directory,"game_files"), g, g+"_game_info.json")
        game_file = open(game_file_path,"r")
        stats = json.load(game_file)
        game_file.close()
        
        opening_duels_file_path = os.path.join(os.path.join(directory,"game_files"), g, g+"_opening_duels.json")
        open_file = open(opening_duels_file_path, "r")
        opening_stats = json.load(open_file)
        open_file.close()
        
        invalid = False
        player = find_player_by_steamId(stats["playerStats"], steamId)
        
        if "id" in list(stats.keys()):
            game_info.append(stats["id"])
        else: 
            invalid = True
        
        if stats["teamScores"] is not None:
            if len(stats["teamScores"]) == 0:
                invalid = True
        else:
            invalid = True
        
        game_info.append(steamId)
        game_info.append(0)
        
        with open('variables.json', 'r') as json_file:
            variables = json.load(json_file)
            
        noMissingVariables = all(variable in player for variable in variables)
        
        if noMissingVariables and player["tRoundsWon"] is not None and player["ctRoundsWon"] is not None and player["tRoundsLost"] is not None and player["ctRoundsLost"] is not None and invalid is not True and stats["isCs2"] is True:
            roundsWon = player["tRoundsWon"] + player["ctRoundsWon"]
            roundsLost = player["tRoundsLost"] + player["ctRoundsLost"]
        
            if roundsLost > roundsWon:
                game_info.append(0)
            else:
                game_info.append(1)
                
            game_info.append(stats["teamScores"][0])
            game_info.append(stats["teamScores"][1])
            if stats["details"]:
                game_info.append(stats["details"]["mpMaxrounds"])
            else:
                game_info.append(30)
            
            game_info.append(player["preaim"])
            game_info.append(player["reactionTime"])
            game_info.append(player["accuracy"])
            game_info.append(player["accuracyEnemySpotted"])
            game_info.append(player["accuracyHead"])
            game_info.append(player["shotsFiredEnemySpotted"])
            game_info.append(player["shotsFired"])
            game_info.append(player["shotsHitEnemySpotted"])
            game_info.append(player["shotsHitFriend"])
            game_info.append(player["shotsHitFriendHead"])
            game_info.append(player["shotsHitFoe"])
            game_info.append(player["shotsHitFoeHead"])
            game_info.append(player["utilityOnDeathAvg"])
            game_info.append(player["heFoesDamageAvg"])
            game_info.append(player["heFriendsDamageAvg"])
            game_info.append(player["heThrown"])
            game_info.append(player["molotovThrown"])
            game_info.append(player["smokeThrown"])
            game_info.append(player["smokeThrownCT"])
            game_info.append(player["smokeThrownCTGood"])
            game_info.append(player["smokeThrownCTGoodRatio"])
            game_info.append(player["smokeThrownCTFoes"])
            game_info.append(player["counterStrafingShotsAll"])
            game_info.append(player["counterStrafingShotsBad"])
            game_info.append(player["counterStrafingShotsGood"])
            game_info.append(player["counterStrafingShotsGoodRatio"])
            game_info.append(player["flashbangHitFoe"])
            game_info.append(player["flashbangLeadingToKill"])
            game_info.append(player["flashbangHitFoeAvgDuration"])
            game_info.append(player["flashbangHitFriend"])
            game_info.append(player["flashbangThrown"])
            game_info.append(player["flashAssist"])
            game_info.append(player["score"])
            game_info.append(player["initialTeamNumber"])
            game_info.append(player["mvps"])
            game_info.append(player["ctRoundsWon"])
            game_info.append(player["ctRoundsLost"])
            game_info.append(player["tRoundsWon"])
            game_info.append(player["tRoundsLost"])
            game_info.append(player["sprayAccuracy"])
            game_info.append(player["totalKills"])
            game_info.append(player["totalDeaths"])
            game_info.append(player["kdRatio"])
            game_info.append(player["multi2k"])
            game_info.append(player["multi3k"])
            game_info.append(player["multi4k"])
            game_info.append(player["multi5k"])
            game_info.append(player["hltvRating"])
            game_info.append(player["hsp"])
            game_info.append(player["roundsSurvived"])
            game_info.append(player["roundsSurvivedPercentage"])
            game_info.append(player["dpr"])
            game_info.append(player["totalAssists"])
            game_info.append(player["totalDamage"])
            game_info.append(player["tradeKillOpportunities"])
            game_info.append(player["tradeKillAttempts"])
            game_info.append(player["tradeKillsSucceeded"])
            game_info.append(player["tradeKillAttemptsPercentage"])
            game_info.append(player["tradeKillsSuccessPercentage"])
            game_info.append(player["tradeKillOpportunitiesPerRound"])
            game_info.append(player["tradedDeathOpportunities"])
            game_info.append(player["tradedDeathAttempts"])
            game_info.append(player["tradedDeathAttemptsPercentage"])
            game_info.append(player["tradedDeathsSucceeded"])
            game_info.append(player["tradedDeathsSuccessPercentage"])
            game_info.append(player["tradedDeathsOpportunitiesPerRound"])
            game_info.append(player["leetifyRating"])
            game_info.append(player["personalPerformanceRating"])
            game_info.append(player["ctLeetifyRating"])
            game_info.append(player["tLeetifyRating"])
            
            counter = 0
            for i in opening_stats:
                if i["attackerSteam64Id"] == steamId:
                    counter += 1
            game_info.append(counter)
            
            info = tuple(game_info)
            info = tuple(0 if value is None else value for value in info)
        else:
            invalid = True
        if invalid == False:
            player_info.append(info)
     
    return player_info

def main(steamId):
    player_profile_info = get_profile_json(steamId)
    directory = create_directory(steamId)
    
    if directory:
        counter = 0
        for i in player_profile_info["games"]:
            if counter == 100:
                break
            get_game_data(i["gameId"], directory)
            counter += 1
         
        data = populate_table(directory, steamId)
        database_path = directory + "/" + steamId+"_info.db"
        
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()
        
        create_table_query = """
        CREATE TABLE IF NOT EXISTS player_stats (
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
        cursor.execute(create_table_query)
        
        insert_query = """INSERT INTO player_stats VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        cursor.executemany(insert_query, data)
        conn.commit()
        conn.close()
        
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM player_stats')
        data = cursor.fetchall()
        conn.close()
        
        X = np.array([row[3:] for row in data])
        games = np.array([row[0] for row in data])
        loaded_model = tf.keras.models.load_model('cs2_anti_cheat_model.h5')
        predictions = loaded_model.predict(X)
        
        counter = 0
        for i in range(len(predictions)):
            if predictions[i] > 0.89:
                print("This player was likely cheating in this game: https://leetify.com/app/match-details/{}/overview".format(games[i]))
                counter += 1
        
        print("Out of the {} game(s) found, this player was likely cheating in {} of them".format(len(games), counter))
                
        shutil.rmtree(directory)
        
        
if __name__ == "__main__":
    player_url = sys.argv[1]
    main(player_url)