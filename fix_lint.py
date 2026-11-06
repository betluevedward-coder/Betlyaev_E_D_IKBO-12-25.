import os

def clean_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    lines = [line.rstrip() + "\n" for line in lines]
    
    while lines and lines[-1] == "\n":
        lines.pop()
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.writelines(lines)

for root_dir in ["src", "tests"]:
    for root, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".py"):
                clean_file(os.path.join(root, file))
print("Все файлы очищены")