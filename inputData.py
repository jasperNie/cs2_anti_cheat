import json
import subprocess

def main(input_file):
    with open(input_file, 'r') as json_file:
        data = json.load(json_file)
        
    ids_to_process = [item[0] for item in data]

    for i in ids_to_process:
        subprocess.run(["python", "parseprofile.py", str(i)])
        
    filenames_to_process = [f"{item[0]}\\{item[0]}_info.db" for item in data if item[1] == 1]

    for f in filenames_to_process:
        subprocess.run(["python", "toggleIsCheat.py", f])

    subprocess.run(["python", "mergedb.py"])

if __name__ == "__main__":
    main("input_file.json")
