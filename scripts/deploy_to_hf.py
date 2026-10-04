import os
from huggingface_hub import HfApi

TOKEN = "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"
REPO_ID = "yeison18/reels-studio"
REPO_TYPE = "space"

api = HfApi(token=TOKEN)

files_to_upload = [
    ("engine/scripts.py", "engine/scripts.py"),
    ("engine/subtitles.py", "engine/subtitles.py"),
    ("engine/video.py", "engine/video.py"),
    ("server.py", "server.py"),
    ("app.py", "app.py"),
    ("static/app.js", "static/app.js"),
    ("static/index.html", "static/index.html"),
    ("static/style.css", "static/style.css"),
    ("requirements.txt", "requirements.txt"),
]

print("Deploying v3.0 to Hugging Face Space...")
for local_path, repo_path in files_to_upload:
    if os.path.exists(local_path):
        print(f"  Uploading {local_path} -> {repo_path}...")
        api.upload_file(
            path_or_fileobj=local_path,
            path_in_repo=repo_path,
            repo_id=REPO_ID,
            repo_type=REPO_TYPE,
            commit_message=f"v3.0: Update {repo_path}"
        )
    else:
        print(f"  WARNING: {local_path} does not exist!")

print("\nAll files uploaded! Checking Space status...")
info = api.get_space_runtime(repo_id=REPO_ID)
print(f"Space Stage: {info.stage}")
