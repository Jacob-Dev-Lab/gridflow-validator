import os

def ensure_dir(path: str):
    if not os.path.exists(path):
        os.makedirs(path)


def get_latest_file(directory: str):
    files = os.listdir(directory)

    if not files:
        return None

    files.sort(key=lambda f: os.path.getmtime(os.path.join(directory, f)), reverse=True)
    return os.path.join(directory, files[0])