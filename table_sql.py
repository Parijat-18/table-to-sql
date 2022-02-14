"""""
IMPORT THIS PROGRAM TO A SEPERATE PYTHON FILE\TERMINAL WINDOW OR PREFERABLY JUPYTER NOTEBOOK.
AFTER CONVERTING THE TABLE TO TEXT FILE USING '.img_to_txt' METHOD, CLEAN THE TEXT FILE MANUALLY TO CORRECT ANY
IRREGULARITIES OR ADDITION OF SPECIAL CHARACTERS BEFORE CONVERTING TO DICTIONARY.
"""""

import cv2 as cv
import pytesseract
import os
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe' # copy paste the tesseract exe path here.

class table_to_sql:
    def __init__(self ,table_name ,  img_path):
        self.table_name = table_name #name of the table
        self.img_path = img_path #location of the table image
        self.txt_path = f"{os.path.split(self.img_path)[1][:-4]}.txt"
        self.create_str= None
        self.rows = []

    def img_to_txt(self , img_path = None): 
        if img_path != None: self.img_path = img_path
        img = cv.imread(self.img_path)
        img = cv.cvtColor(img , cv.COLOR_BGR2RGB)
        txt = pytesseract.image_to_string(img)
        with open(self.txt_path , 'w') as f:
            f.write(txt)

    def txt_preprocess(self , sep= None , txtpath=None): #txtpath= if you already have the table in a text file.
        # sep = add seperators to in case the values have characters like "|" "," seperating the values in the text file.
        if txtpath != None:
            self.txt_path = txtpath
        with open(self.txt_path , 'r') as f:
            txt = f.read()
        self.rows = txt.split('\n')
        self.rows = [row for row in self.rows if row != '']
        for idx , x in enumerate(self.rows):
            if sep != None:
                for s in sep: 
                    x = x.replace(s , '')
            self.rows[idx] = x.split(' ')
            for i , val in enumerate(self.rows[idx]): 
                if val == '': self.rows[idx].pop(i)

    def sql_create(self):
        if(len(self.rows) == 0):
            print("no table/txt is loaded")
            return
        else:
            for idx , column_name in enumerate(self.rows[0]):
                constraint = input(f"\tconstraints/datatype for {column_name}: ")
                self.rows[0][idx] = f"{column_name} {constraint}"
                print(f"{column_name} {constraint}")
            self.create_str = f"CREATE TABLE {self.table_name}("
            self.create_str += " ".join([f"\n\t{col}," for col in self.rows[0]])
            self.create_str = self.create_str[:-1] + ");"
            print(self.create_str)

    def sql_insert(self):
        self.insert_string_arr = []
        if(len(self.rows) == 0):
            print("no table/txt is loaded")
            return
        for row in self.rows[1:]:
            if row != '':
                self.insert_str = f"INSERT INTO {self.table_name} VALUES("
                for value in row:
                    if not value.isdigit():
                        self.insert_str += f"'{value}', "
                    else: self.insert_str += f"{value}, "
                self.insert_str = self.insert_str[:-2] +  ");"
                self.insert_string_arr.append(self.insert_str)
                print(self.insert_str)
        self.insert_str = self.insert_string_arr


if __name__ == "__main__":
    pass