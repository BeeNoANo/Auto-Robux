import requests
import time
import re
import pandas as pd
from colorama import Style, Fore
import os


data = []

useragent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36"
authurl = 'https://auth.roblox.com/v2/logout'

class info:
    def get_user_id(cookie):
        url="https://users.roblox.com/v1/users/authenticated"
        req=requests.get(url,headers=info.get_headers(cookie),cookies=info.get_cookies(cookie))
        return req.json()['id']
    def get_info_request_url(type:str,id:int):
        if type=="gamepass":
            return f"https://apis.roblox.com/game-passes/v1/game-passes/{id}/product-info"
        elif type=="asset":
            return f"https://economy.roblox.com/v2/assets/{id}/details"
    def get_info(id:int,type:str):
        url=info.get_info_request_url(type,id)
        req=requests.get(url)
        list=[]
        list.append(req.json()['ProductId'])
        list.append(req.json()['Creator']['Id'])
        list.append(req.json()['PriceInRobux'])
        return list
    def getXsrf(cookie):
        xsrfRequest = requests.post(authurl, headers={'User-Agent': useragent}, cookies=info.get_cookies(cookie))
        if xsrfRequest.headers['x-csrf-token']:
            return xsrfRequest.headers['x-csrf-token']
        else:
            return ''
    def get_headers(cookie):
        return {"X-CSRF-TOKEN":info.getXsrf(cookie)}
    def get_cookies(cookie):
        return {".ROBLOSECURITY":cookie}
    def getUserId(username):
        API_ENDPOINT = "https://users.roblox.com/v1/usernames/users"
        payload={'usernames':[username],}
        req=requests.post(API_ENDPOINT,json=payload)
        return req.json()['data'][0]['id']
    def get_gamepasses(username):
        url=f"https://games.roblox.com/v2/users/{info.getUserId(username)}/games?accessFilter=Public&limit=50"
        req=requests.get(url)
        ids=[]
        for game in req.json()['data']:
            ids.append(game['id'])
        gamepasses=[]
        for universe in ids:
            url=f'https://games.roblox.com/v1/games/{universe}/game-passes?limit=100&sortOrder=Asc'
            otherequest=requests.get(url)
            for gamepass in otherequest.json()['data']:
                a=[]
                if not gamepass['price']==None:
                    a.append(gamepass['id'])
                    a.append(gamepass['price'])
                    gamepasses.append(a)
        return gamepasses
    def getUniverseId(cookie):
        ID = info.get_user_id(cookie)
        Id=requests.get(f"https://games.roblox.com/v2/users/{ID}/games?accessFilter=2&limit=10&sortOrder=Asc")
        game_id = Id.json()['data'][0]['id']
        return game_id


class getInfo:
    """
    Lớp này lưu trữ thông tin chi tiết từ một dòng trong file dữ liệu.
    """

    def __init__(self, datas):
        """
        Khởi tạo đối tượng với thông tin chi tiết.

        Args:
            datas: Chuỗi chứa thông tin được tách biệt bằng dấu tab.

        Raises:
            ValueError: Nếu chuỗi dữ liệu không có đủ thành phần.
        """
        data = datas.split("\t")
        # if len(data) < 10:  # Điều kiện tối thiểu 10 thành phần
        #     raise ValueError("Invalid data format")

        # Tìm kiếm số Robux chưa thuế

        self.id = data[0] 
        self.name = data[1] 
        self.uid = data[2]
        self.username = data[3]
        self.password = data[4]
        self.service = data[5]
        self.money = data[8]
        self.time = data[9]
        self.robux = None

        match = re.search(r"\d+", data[6])
        if self.service == "ROBUX 120H":
            if match:
                robuxAferTax = int(match.group())
                robuxBeforeTax = robuxAferTax / 70 * 100
                self.robux = int(robuxBeforeTax)
            else:
                print("Lỗi: Không có số Robux")
                self.robux = 0
                return
        else:
            print("Chỉ duyệt được robux 120H")
            self.robux = 0
            return
        

# Uid, Username, Password, Service , Money, Time, Robux


class GruopItem:
    """
    Lớp này lưu trữ thông tin chi tiết từ một dòng trong file dữ liệu.
    """

    def __init__(self, datas):
        """
        Khởi tạo đối tượng với thông tin chi tiết.

        Args:
            datas: Chuỗi chứa thông tin được tách biệt bằng dấu tab.

        Raises:
            ValueError: Nếu chuỗi dữ liệu không có đủ thành phần.
        """
        data = datas.split("\t")
        if len(data) < 10:  # Điều kiện tối thiểu 10 thành phần
            raise ValueError("Invalid data format")

        # Tìm kiếm số Robux chưa thuế

        self.id = data[0]
        self.name = data[1]
        self.uid = data[2]
        self.username = data[3]
        self.password = data[4]
        self.service = data[5]
        self.money = data[8]
        self.time = data[9]
        self.robux = None

        match = re.search(r"\d+", data[6])
        if self.service == "ROBUX 120H":
            if match:
                self.robux = int(match.group())

            else:
                print("Lỗi: Không có số Robux")
        else:
            print("Chỉ duyệt được robux 120H")
            return

        



class Gruop:
    def G():
        df = pd.DataFrame(data, columns=["ID", "Name", "UID", "Username", "Password", "Service", "Robux", "FailCount", "Money", "Time"])

    # Xác định username trùng
        df_duplicates = df.loc[df["Username"].duplicated(keep="last")].reset_index(drop=True)

        # Xóa username trùng
        df = df.drop_duplicates(subset="Username", keep="last")

        # Cộng dồn Robux cho username trùng
        for index in df_duplicates.index.to_list():  
            username = df_duplicates.loc[index, "Username"]
            robux = df_duplicates.loc[index, "Robux"]
            df.loc[df["Username"] == username, "Robux"] += robux
        return df

    def CheckWord(line):
        if "thuế" in line.lower():
            return True
        else:
            return False
    def PrintG():
        with open("..\data.txt", "r", encoding="utf-8") as f:
            for line in f:       
                    i = GruopItem(line)
                    parts = [i.id, i.name, i.uid, i.username, i.password, i.service, i.robux, "0", i.money, i.time]
                    # Lưu trữ các phần
                    data.append(parts)
            Gruop.G().to_csv("..\data.txt", sep="\t", index=False, header=False)  # Xuất ra file 'output.txt'






