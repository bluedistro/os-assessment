import xlrd, csv
import pandas as pd
from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/api/os/<int:id_number>")
def view_results(id_number):
    # read data from excel to csv
    try:
        with xlrd.open_workbook("cpen_OS_Groups_to_TA.xlsx") as wb:
             sh = wb.sheet_by_index(1)
             with open("data.csv", "wb") as f:
                 c = csv.writer(f)
                 for r in range(1, sh.nrows):
                     c.writerow(sh.row_values(r))
    except Exception as e:
        return jsonify({"status": "failure",
                        "optional": "Error occurred during Data Fetching"})

    # main work
    headers = ["Student_ID_Number", "Name", "Quiz_1", "Quiz_2", "Quiz_3", "Quiz_4",
               "Lab_1", "Lab_2", "Lab_3", "Quiz_5", "Quiz_6", "Presentation", "Total"]

    try:
        data = pd.read_csv("data.csv", na_values="NaN", header=None, names=headers)
        # cast id numbers to int
        data["Student_ID_Number"] = data["Student_ID_Number"].astype(int)

        # fetch data given index number
        results = data.loc[data["Student_ID_Number"] == id_number]
        results = (results.to_dict(orient="records"))[0]
        return jsonify({"results": results,
                        "status": "sucess",
                        "optional": ""})
    except Exception as e:
        return jsonify({"status": "failure",
                        "optional": "Unknown Error during processing.."})

if __name__ == "__main__":
    app.run()
