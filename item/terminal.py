import time
import os
import os
from prettytable import PrettyTable
from item.filter_information import getInfo, info
from item.tool import buyer
import os

# Lấy đường dẫn thư mục hiện tại


import json



animation = [
"[       ] L",
"[=      ] LO",
"[===    ] LOA",
"[====   ] LOAD",
"[=====  ] LOADI",
"[====== ] LOADIN",
"[=======] LOADING",
"[=======] LOADING .",
"[ ======] LOADING",
"[  =====] LOADIN",
"[   ====] LOADI",
"[    ===] LOAD",
"[     ==] LOA",
"[      =] LO",
"[       ] L",
]
class Effect:
    def load(time_wait):
        notcomplete = True
        i = 0

        while notcomplete:
            print(animation[i % len(animation)], end='\r')
            time.sleep(.1)
            i += 1
            if i == time_wait / 0.1:
                break
    def Print(data):
        print("=" * 60)
        print("\n")
        print(f"{data:^60}")
        print("\n")
        print("=" * 60)

class Table:
    """
    Lớp này tạo và hiển thị bảng dữ liệu.
    """

    def __init__(self):
        """
        Khởi tạo bảng với các cột.
        """
        self.table = PrettyTable(['ID', 'Name', 'Username', 'Robux(ATAX)', 'Money',"Time", 'Status'])

    def add_row(self, id, name, username, robux, money,time,status, ):
        """
        Thêm một hàng dữ liệu vào bảng
        """
        self.table.add_row([id, name, username, robux, money, time, status])


    def show_table(self):
        """
        Hiển thị bảng dữ liệu.
        """
        print(self.table)

    def clear_screen(self):
        """
        Xóa màn hình.
        """
        os.system('cls')
    def table_footer(tbl, text, dc):
        res = f"{tbl._vertical_char} {text}{' ' * (tbl._widths[0] - len(text))} {tbl._vertical_char}"

        for idx, item in enumerate(tbl.field_names):
            if idx == 0:
                continue
            if not item in dc.keys():
                res += f"{' ' * (tbl._widths[idx] + 1)} {tbl._vertical_char}"
            else:
                res += f"{' ' * (tbl._widths[idx] - len(str(dc[item])))} {dc[item]} {tbl._vertical_char}"

        res += f"\n{tbl._hrule}"
        return res

class Account:
    def CheckAccount():
        table = PrettyTable(['ID', 'Name', 'Username','Password', 'Robux(ATAX)', 'Money', 'Time', 'Status'])

        with open("..\data.txt", "r", encoding="utf-8") as file:
            lines = file.readlines()
        a = 0
        for line in lines:
            i = getInfo(line)
            table.add_row([i.id, i.name, i.username, i.password, i.robux, i.money, i.time, "LOADING OK"])
            a += int(i.robux)
        print(table)
        print(Table.table_footer(table, "Total", {'Robux(ATAX)': a}))
        
    def CheckRobux():
        table = PrettyTable(["Count", "Username", "Password", "Robux Left"])
        with open("..\input.txt", "r", encoding="utf-8") as file:
            lines = file.readlines()
            
        i = 0
        robuxs = 0
        for line in lines:
            removeSpace = line.strip()
            data = removeSpace.split("/")  

            if len(data) == 3:  # Kiểm tra độ dài của data
                robux = buyer(data[2]).get_robux_amount()
                table.add_row([i, data[0], data[1], robux])
                i += 1
                if isinstance(robux, int):
                    robuxs += robux
                else:
                    print("SAI fromat")
            else:
                print("Thiếu thành phần trong dòng dữ liệu TK/MK/COOKIE")  # Thông báo lỗi


        print(table)
        print(Table.table_footer(table, "Total", {'Robux Left': robuxs}))

    def ChangeAccount():
        with open("..\input.txt", "r", encoding="utf-8") as file:
            lines = file.readlines()
        for line in lines:
            removeSpace = line.strip()
            data = removeSpace.split("/")
            robux = buyer(data[2]).get_robux_amount()
            if robux == 0:
                return False

