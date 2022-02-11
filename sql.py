import cv2 as cv
import pytesseract
import os
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

class table_to_sql:
    def __init__(self ,table_name ,  img_path):
        self.table_name = table_name
        self.img_path = img_path
        self.txt_path = f"{os.path.split(self.img_path)[1][:-4]}.txt"
        self.csv_dict = {}

    def img_to_txt(self , img_path = None):
        if img_path != None: self.img_path = img_path
        img = cv.imread(self.img_path)
        img = cv.cvtColor(img , cv.COLOR_BGR2RGB)
        txt = pytesseract.image_to_string(img)
        with open(self.txt_path , 'w') as f:
            f.write(txt)

    def txt_to_csv(self , sep):
        with open(self.txt_path , 'r') as f:
            txt = f.read()
        arr = txt.split('\n')
        for idx , x in enumerate(arr):
            if(x == ''): arr.pop(idx)
            for s in sep:
                x = x.replace(s , "")
            arr[idx] = x.split(' ')
        csv_dict = {}
        for idx in range(len(arr[0])):
            csv_dict[arr[0][idx]] = [x[idx] for x in arr[1:]]
        self.csv_dict = csv_dict

    def sql_create(self):
        if(len(self.csv_dict.keys()) == 0):
            print("no table/txt is loaded")
            return
        new_csv_dict = {}
        for column_name in self.csv_dict.keys():
            constraints = input(f"\tconstraints/datatype for {column_name}: ")
            new_csv_dict[f"{column_name} {constraints}"] = self.csv_dict[column_name]
            print(f"{column_name} {constraints}")
        self.csv_dict = new_csv_dict
        create_str = f"CREATE TABLE {self.table_name}("
        create_str += " ".join([f"\n\t{col}," for col in self.csv_dict.keys()])
        create_str = create_str[:-1] + ");"
        print(create_str)

    def sql_insert(self):
        cols = list(self.csv_dict.values())
        for idx , _ in enumerate(cols):
            insert_str = f"INSERT INTO {self.table_name} VALUES("
            row = [x[idx] for x in cols]
            for value in row:
                if not value.isdigit():
                    insert_str += f"'{value}', "
                else: insert_str += f"{value}, "
            insert_str = insert_str[:-2] +  ");"
            print(insert_str)


if __name__ == "__main__":
    pass