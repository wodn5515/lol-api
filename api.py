import pandas as pd
import requests

API_KEY = "API_KEY"

def champ_data():
    # 최신버젼 가져오기
    r = requests.get("https://ddragon.leagueoflegends.com/api/versions.json")
    current_version = r.json()[0]

    # 챔피언 목록 가져오기
    r = requests.get(f"http://ddragon.leagueoflegends.com/cdn/{current_version}/data/ko_KR/champion.json")
    data = r.json()
    data = pd.DataFrame(data)

    # 챔피언별 데이터 정리
    data_dic = {}
    for i, champ in enumerate(data.data):
        data_dic[i] = pd.Series(champ)

    data_df = pd.DataFrame(data_dic).T
    data_df = data_df.drop(["version", "image", "key", "title", "blurb", "info", "image", "tags", "partype", "stats", "id"], axis=1)
    data_df.loc[:, "no"] = pd.Series([x for x in range(154)], index=data_df.index)

    # 챔피언별 라인 선호도 데이터 합치기
    lane_df = pd.DataFrame({
        "TOP": [0 for x in range(154)],
        "JG": [0 for x in range(154)],
        "MID": [0 for x in range(154)],
        "ADC": [0 for x in range(154)],
        "SUP": [0 for x in range(154)]
    })
    champ_df = pd.concat([data_df, lane_df], axis=1)

    return champ_df