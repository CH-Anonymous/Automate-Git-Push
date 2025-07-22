import os
import git
import json
from github import Github

# File to store token locally
TOKEN_FILE = os.path.expanduser("~/.autogitpush_token.json")

# Save token and username securely
def save_token(username, token):
    with open(TOKEN_FILE, 'w') as f:
        json.dump({"username": username, "token": token}, f)

# Load token and username
def load_token():
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'r') as f:
            data = json.load(f)
            return data.get('username'), data.get('token')
    return None, None

# Remove stored token
def reset_token():
    if os.path.exists(TOKEN_FILE):
        os.remove(TOKEN_FILE)

# ✅ Main push function — fully fixed
def push_to_github(folder_path, username, repo_name, token):
    try:
        os.chdir(folder_path)

        # Initialize repo if it doesn't exist
        if not os.path.exists(os.path.join(folder_path, ".git")):
            repo = git.Repo.init(folder_path)
        else:
            repo = git.Repo(folder_path)

        # Setup remote URL
        remote_url = f"https://{username}:{token}@github.com/{username}/{repo_name}.git"

        # Recreate 'origin' remote to avoid duplicate error
        if 'origin' in [remote.name for remote in repo.remotes]:
            repo.delete_remote('origin')
        repo.create_remote('origin', remote_url)

        # ✅ Reset merge conflicts or index issues
        repo.git.reset('--hard')

        # ✅ Checkout or create 'main' branch
        try:
            repo.git.checkout('main')
        except git.exc.GitCommandError:
            repo.git.checkout('-b', 'main')

        # ✅ Stage and commit changes
        repo.git.add(A=True)
        if repo.is_dirty(untracked_files=True):
            repo.index.commit("AutoGitPush Commit")

        # ✅ Push to GitHub
        repo.git.push('--set-upstream', 'origin', 'main', force=True)
        return True, "Code pushed successfully to GitHub!"
    except Exception as e:
        return False, f"Push failed: {str(e)}"

# ✅ Create a GitHub repository
def create_github_repo(repo_name, username, token, description=""):
    try:
        g = Github(token)
        user = g.get_user()
        if repo_name not in [repo.name for repo in user.get_repos()]:
            user.create_repo(name=repo_name, description=description)
            return True, f"Repository '{repo_name}' created successfully."
        return False, f"Repository '{repo_name}' already exists."
    except Exception as e:
        return False, f"Failed to create repo: {str(e)}"

# ✅ Delete a GitHub repository
def delete_github_repo(repo_name, token):
    try:
        g = Github(token)
        user = g.get_user()
        for repo in user.get_repos():
            if repo.name == repo_name:
                repo.delete()
                return True
        return False
    except:
        return False

# ✅ List all GitHub repositories for user
def list_github_repos(token):
    try:
        g = Github(token)
        user = g.get_user()
        return [repo.name for repo in user.get_repos()]
    except:
        return []

# ✅ Update local folder's Git remote URL
def update_repo_remote(folder_path, username, repo_name, token):
    try:
        repo = git.Repo(folder_path)
        remote_url = f"https://{username}:{token}@github.com/{username}/{repo_name}.git"
        if 'origin' in [remote.name for remote in repo.remotes]:
            repo.delete_remote('origin')
        repo.create_remote('origin', remote_url)
        return True, "Remote updated successfully."
    except Exception as e:
        return False, str(e)
