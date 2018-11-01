from flask import Flask, render_template, send_from_directory, request
from pathlib import Path
import os, json
import re
import tkinter as tk
from tkinter import filedialog
from flask_cors import CORS

root = tk.Tk()
root.withdraw()

file_path = filedialog.askdirectory()
print(file_path)
app = Flask(__name__)
CORS(app)
def get_all_files(directory, file_types=[]):
    data = []
    reg_ex = "\.("
    for i in range(len(file_types)):
        reg_ex = reg_ex + file_types[i] 
        if i < len(file_types) - 1:
            reg_ex += "|"
    reg_ex += ")"
    print(reg_ex)
    rx = re.compile(reg_ex) 
        
    for x in os.walk(directory):
        if len(x[2]) > 0:
            root = x[0].replace("\\","/")
            folders = []
            for i in x[1]:
                folders.append(i.replace("\\","/"))
            files = []
            for i in x[2]:
                if rx.search(i):
                    files.append(i)
            if len(files) > 0:
                data.append({"directory": root, "folders": folders, "files": files})
    return data

@app.route("/")
def index():
    data = get_all_files(file_path)
        
    with open("data.json", "w") as file:
        json.dump(data, file)
    return render_template("index.html", data=data)

@app.route("/video", methods=['GET'])
def video():
    directory = request.args.get("dir")
    video_file = request.args.get("file")
    return send_from_directory(directory, video_file)

if __name__ == "__main__":
    app.run(host='0.0.0.0')