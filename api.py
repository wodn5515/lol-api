import pandas as pd
import requests

API_KEY = "API_KEY"

# 소환사 리스트 가져오기
'''
r = requests.get(url+API_KEY)
league_df = pd.DataFrame(r.json())
league_dic = {}
for i, summoner in enumerate(league_df.entries):
    league_dic[i] = pd.Series(summoner)

league_df = pd.DataFrame(league_dic).T
return league_df
'''


# 유저목록 가져오기
'''
api_url_challenger = "https://kr.api.riotgames.com/lol/league/v4/challengerleagues/by-queue/RANKED_SOLO_5x5?api_key="
api_url_grandmaster = "https://kr.api.riotgames.com/lol/league/v4/grandmasterleagues/by-queue/RANKED_SOLO_5x5?api_key="
api_url_master = "https://kr.api.riotgames.com/lol/league/v4/masterleagues/by-queue/RANKED_SOLO_5x5?api_key="

users_df = pd.concat([get_users(api_url_challenger), get_users(api_url_grandmaster), get_users(api_url_master)], ignore_index=True)
users_df.reset_index(inplace=True)
users_df = users_df.drop(["index", "leaguePoints", "rank", "wins", "losses", "veteran", "inactive", "freshBlood", "hotStreak"], axis=1)
print("done")
return users_df
'''


# SummonerId 를 이용하여 accountId 가져오기
# 파일로 관리
'''user_df = get_user_list()
user_df["accountId"] = np.nan
payload = {"api_key": API_KEY}
for i, summoner_id in enumerate(user_df["summonerId"]):
    api_url_account_id = "https://kr.api.riotgames.com/lol/summoner/v4/summoners/" + summoner_id
    r = requests.get(api_url_account_id, params=payload)
    # 에러 발생시 5초 지연후 재실행
    while r.status_code != 200:
        print(r.status_code)
        time.sleep(10)
        r = requests.get(api_url_account_id, params=payload)
    account_id = r.json()["accountId"]
    user_df.iloc[i,-1] = account_id
    print(i)
user_df.to_csv("summoner.csv")
'''

# Summmoner list 불러오기
'''user_df = pd.read_csv("summoner.csv", index_col=0)'''

# 매치리스트 가져오기
# 파일로 관리
'''match_list_df = pd.DataFrame()
cnt = 0
for account_id in user_df["accountId"]:
    api_url_matches_list = "https://kr.api.riotgames.com/lol/match/v4/matchlists/by-account/" + account_id + "?queue=420&api_key=" + API_KEY
    r = requests.get(api_url_matches_list)
    while r.status_code != 200:
        print(r.status_code)
        time.sleep(30)
        r = requests.get(api_url_matches_list)
    match_list_df = pd.concat([match_list_df, pd.DataFrame(r.json()["matches"])], ignore_index=True)
    cnt += 1
    print(cnt)
'''

# 불필요한 columns 제거
'''
match_list_df = match_list_df.drop(["platformId", "gameId", "queue", "season", "timestamp"], axis=1)
match_list_df.to_csv("matches_list.csv", index=False)
'''
