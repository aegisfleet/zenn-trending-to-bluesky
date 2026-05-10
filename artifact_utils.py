import os

def save_results(models):
    folder_path = "tmp"
    file_path = os.path.join(folder_path, "previous_result.txt")

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # 既存のデータを読み込む
    previous_data = load_previous_results()
    
    # 新しいデータと結合して保存（重複を避ける）
    new_urls = [model[0] for model in models]
    combined_data = list(set(previous_data + new_urls))

    with open(file_path, "w") as file:
        for url in combined_data:
            file.write(f"{url}\n")

def load_previous_results():
    folder_path = "tmp"
    file_path = os.path.join(folder_path, "previous_result.txt")

    try:
        with open(file_path, "r") as file:
            return [line.strip() for line in file]
    except FileNotFoundError:
        return []
