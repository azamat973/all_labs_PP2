import json
def connection():
    str='''Interface Status
================================================================================
DN                                                 Description           Speed    MTU'''
    print(str)
    with open(r"C:\Users\Huawei\OneDrive\Рабочий стол\new_folder_2\labs\lab4\json\sample-data.json", "r", encoding="utf-8") as file:

        fromFile=json.load(file)
        array=fromFile["imdata"]
        for i in array:
            tn=i["l1PhysIf"]["attributes"]["dn"]
            description=i["l1PhysIf"]["attributes"]["descr"]
            speed=i["l1PhysIf"]["attributes"]["speed"]
            mtu=i["l1PhysIf"]["attributes"]["mtu"]
            print(f"{tn}                   {description}            {speed}      {mtu}")
        file.close()
connection()
