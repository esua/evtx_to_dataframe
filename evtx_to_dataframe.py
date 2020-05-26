import argparse
import Evtx.Evtx as evtx
import pandas as pd
import xmltodict
import re

parser = argparse.ArgumentParser(description="Convert Windows EVTX event log file to DataFrame.")
parser.add_argument("evtx", type=str, help="Path to the Windows EVTX event log file")
args = parser.parse_args()

with evtx.Evtx(args.evtx) as log:
    data_dicts = []
    for record in log.records():
        elem = record.xml()
        elem = re.sub(r'<Data Name="(.+)">(.+)</Data>', r'<\1>\2</\1>', elem)  # Replace contents of EventData
        data_dict = xmltodict.parse(elem)  # convert xml to dict
        data_dicts.append(data_dict)

df = pd.json_normalize(data_dicts)  # convert dict to pd.DataFrame
print(df)
