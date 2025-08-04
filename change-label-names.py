import os

folder_path = r"D:\hackathon\yolo\label"  
old_class = "0"
new_class = "8"

for filename in os.listdir(folder_path):
    if filename.endswith(".txt"):
        file_path = os.path.join(folder_path, filename)
        new_lines = []

        with open(file_path, "r") as f:
            for line in f:
                parts = line.strip().split()
                if parts and parts[0] == old_class:
                    parts[0] = new_class  
                new_lines.append(" ".join(parts))

        with open(file_path, "w") as f:
            for line in new_lines:
                f.write(line + "\n")

        print(f"Updated classes in: {filename}")
