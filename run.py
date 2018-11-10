import pandas as pd
from flask import Flask, jsonify
import json

app = Flask(__name__)


@app.route("/api/os/<int:id_number>")
def view_results(id_number):
    # read excel file
    xls_file = pd.ExcelFile('cpen_OS_Groups_to_TA.xlsx')
    # drop the header from the file and use declared ones
    headers = ["Student_ID_Number", "Name", "Quiz_1", "Quiz_2", "Quiz_3", "Quiz_4",
               "Lab_1", "Lab_2", "Lab_3", "Quiz_5", "Quiz_6", "Presentation", "Total"]
    data = xls_file.parse('assessment', names=headers)

    try:
        # cast id numbers to int
        data["Student_ID_Number"] = data["Student_ID_Number"].astype(int)
        results = data.loc[data["Student_ID_Number"] == id_number]
        results = (results.to_dict(orient="records"))[0]
        results = json.dumps(results)
        return jsonify({"results": results,
                        "status": "success",
                        "header_information": "All Quizzes are over 10, Labs 1 and 2"
                                              " are over 5 and Lab 3 is over 20."
                                              " Presentation is over 10."})
    except Exception as e:
        return jsonify({"status": "failure",
                        "optional": "Unknown Error during processing.."})

if __name__ == "__main__":
    app.run()
