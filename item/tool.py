import requests
from item.filter_information import info
import time


class buyer:
    def __init__(self,cookie:str):
        self.cookie=cookie
    def buy(self, delete:bool,id:int,type:str):
        infos=info.get_info(id,type)
        data={"expectedCurrency": 1, "expectedPrice":infos[2] , "expectedSellerId":infos[1]}
        url1=f"https://economy.roblox.com/v1/purchases/products/{infos[0]}"
        data = requests.post(url1,data=data,headers=info.get_headers(self.cookie), cookies=info.get_cookies(self.cookie))
        if delete==True:
            if type=="gamepass":
                deleter(self.cookie).delete_gamepass(id)
            elif type=="asset":
                deleter(self.cookie).delete_asset(id)
    def get_robux_amount(self):
        url=f"https://economy.roblox.com/v1/user/currency"
        try:
            data = requests.get(url,cookies=info.get_cookies(self.cookie))
            return data.json()["robux"]
        except:
            return "ERROR"
    def auto_buy(self,id:int,type:str,amount:int,cooldown_time:int):
        for i in range(amount):
            time.sleep(cooldown_time)
            self.buy(True,id,type)
    def donate(self,username,amount):
        a=0
        for passe in info.get_gamepasses(username):
            if  a+passe[1]<=amount:
                a+=passe[1]
                buyer(self.cookie).buy(True,passe[0],"pass")
        if a==amount:
            return "success"
        else:
            return f"Not found gamepass ,Sended {a} Wanted {amount}"
        
class game_pass:
    def __init__(self,cookie:str):
        self.cookie=cookie
    def do_offsale(self,passid):
        url=f"https://apis.roblox.com/game-passes/v1/game-passes/{passid}/details"
        data={"IsForSale": "false"}
        a=requests.post(url,data=data,headers=info.get_headers(self.cookie),cookies=info.get_cookies(self.cookie))
    def pass_creator(self,amount,universeid):
        url="https://apis.roblox.com/game-passes/v1/game-passes"
        data={"Name": "Gamepass Name",
        "UniverseId": universeid}
        a=requests.post(url,data=data,headers=info.get_headers(self.cookie),cookies=info.get_cookies(self.cookie))
        try:
            passid=a.json()['gamePassId']
            url=f"https://apis.roblox.com/game-passes/v1/game-passes/{passid}/details"
            data={"IsForSale": "true","Price": amount}
            a=requests.post(url,data=data,headers=info.get_headers(self.cookie),cookies=info.get_cookies(self.cookie))
            return str(passid)
        except:
            return "Error"
        

class deleter:
    def __init__(self,cookie:str):
        self.cookie=cookie
    def delete_asset(self,assetid):
        url=f"https://www.roblox.com/asset/delete-from-inventory"
        data={"assetId":assetid}
        requests.post(url,data=data, headers=info.get_headers(self.cookie), cookies=info.get_cookies(self.cookie))
        print("Item Deleted")
    def delete_gamepass(self,passid):
        url=f"https://www.roblox.com/game-pass/revoke"
        data={"id":passid}
        requests.post(url,data=data, headers=info.get_headers(self.cookie), cookies=info.get_cookies(self.cookie))
        print("Gamepass Deleted")
        