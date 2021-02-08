import pandas as pd
import numpy as np
import requests
import time


API_KEY = "API_KEY"

# 소환사 리스트 가져오기
def get_users(url):
    r = requests.get(url+API_KEY)
    league_df = pd.DataFrame(r.json())
    league_dic = {}
    for i, summoner in enumerate(league_df.entries):
        league_dic[i] = pd.Series(summoner)

    league_df = pd.DataFrame(league_dic).T
    return league_df


# 유저목록 가져오기
api_url_challenger = "https://kr.api.riotgames.com/lol/league/v4/challengerleagues/by-queue/RANKED_SOLO_5x5?api_key="
api_url_grandmaster = "https://kr.api.riotgames.com/lol/league/v4/grandmasterleagues/by-queue/RANKED_SOLO_5x5?api_key="
api_url_master = "https://kr.api.riotgames.com/lol/league/v4/masterleagues/by-queue/RANKED_SOLO_5x5?api_key="

users_df = pd.concat([get_users(api_url_challenger), get_users(api_url_grandmaster), get_users(api_url_master)], ignore_index=True)
users_df.reset_index(inplace=True)
users_df = users_df.drop(["index", "leaguePoints", "rank", "wins", "losses", "veteran", "inactive", "freshBlood", "hotStreak"], axis=1)


# SummonerId 를 이용하여 accountId 가져오기
# 파일로 관리
users_df["accountId"] = np.nan
payload = {"api_key": API_KEY}
for i, summoner_id in enumerate(users_df["summonerId"]):
    api_url_account_id = "https://kr.api.riotgames.com/lol/summoner/v4/summoners/" + summoner_id
    r = requests.get(api_url_account_id, params=payload)
    # 에러 발생시 30초 지연후 재실행
    while r.status_code != 200:
        print(r.status_code)
        time.sleep(30)
        r = requests.get(api_url_account_id, params=payload)
    account_id = r.json()["accountId"]
    users_df.iloc[i,-1] = account_id
    print(i)
users_df.to_csv("summoner.csv")


# Summmoner list 불러오기
users_df = pd.read_csv("summoner.csv", index_col=0)


# 매치리스트 가져오기
# 파일로 관리
match_list_df = pd.DataFrame()
for account_id in users_df["accountId"]:
    api_url_matches_list = "https://kr.api.riotgames.com/lol/match/v4/matchlists/by-account/" + account_id + "?queue=420&api_key=" + API_KEY
    r = requests.get(api_url_matches_list)
    # 에러 발생시 30초 지연후 재실행
    while r.status_code != 200:
        time.sleep(30)
        r = requests.get(api_url_matches_list)
    match_list_df = pd.concat([match_list_df, pd.DataFrame(r.json()["matches"])], ignore_index=True)


# 불필요한 columns 제거
match_list_df = match_list_df.drop(["platformId", "gameId", "queue", "season", "timestamp"], axis=1)
match_list_df.to_csv("matches_list.csv", index=False)


# 챔프별 라인선호도 데이터 얻기
# 파일로 관리
champ_df = pd.read_csv("champions.csv", index_col=0)
matches_df = pd.read_csv("matches_list.csv", index_col=0)
for index, row in matches_df.iterrows():
    key = row["champion"]
    lane = row["lane"]
    role = row["role"]
    if role == "SOLO":
        if lane == "TOP":
            champ_df.loc[champ_df["key"] == key, "TOP"] += 1
            continue
        elif lane == "MID":
            champ_df.loc[champ_df["key"] == key, "MID"] += 1
            continue
        else:
            continue
    if lane == "BOTTOM":
        if role == "DUO_CARRY":
            champ_df.loc[champ_df["key"] == key, "ADC"] += 1
            continue
        elif role == "DUO_SUPPORT":
            champ_df.loc[champ_df["key"] == key, "SUP"] += 1
            continue
        else:
            continue
    if lane == "JUNGLE":
        if role == "NONE":
            champ_df.loc[champ_df["key"] == key, "JG"] += 1
            continue
        else:
            continue

champ_df.to_csv("champions_lane_preference.csv")
