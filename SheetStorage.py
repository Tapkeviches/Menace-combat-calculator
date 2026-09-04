import gspread
import csv
import pathlib
import EnemySquad

gc = gspread.service_account("server_creds.json")
balance_file = gc.open('Menace Balance Shenanigans')

class OnlineSheetStorageClass(object):
    def __init__(self):
        self.sheets_storage_dictionary = {}
        self.data_storage_dictionary = {}

    def get_sheet_from_storage(self, key):
        if key in self.sheets_storage_dictionary:
            print("Found sheet with key", key, "in storage")
            sheet = self.sheets_storage_dictionary[key]
        else:
            print("Downloaded sheet with key", key, "from google")
            sheet = OnlineSheetStorageClass.get_sheet_from_google_sheet(key)

        self.sheets_storage_dictionary[key] = sheet
        return sheet

    @staticmethod
    def get_sheet_from_google_sheet(key):
        asked_sheet = balance_file.worksheet(key)
        if key == "WeaponStats":
            sheet_dict = asked_sheet.get_all_records(numericise_ignore=[3,10,19,33,35,38])
        else:
            sheet_dict = asked_sheet.get_all_records()
        return sheet_dict



enemies = []





