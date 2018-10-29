import xlrd, csv
import json

def update_csv_file():
    # read data from excel to csv
    try:
        with xlrd.open_workbook("cpen_OS_Groups_to_TA.xlsx") as wb:
             sh = wb.sheet_by_index(1)
             with open("data.csv", "wb") as f:
                 c = csv.writer(f)
                 for r in range(1, sh.nrows):
                     c.writerow(sh.row_values(r))
        return "done"
    except Exception as e:
        return "error"

# always run on update
print(update_csv_file())