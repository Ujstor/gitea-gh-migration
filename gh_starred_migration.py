import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

#Github
gh_access_token = os.environ['GH_ACCESS_TOKEN']
# Gitea
GITEA_ACCESS_TOKEN = os.environ['GITEA_ACCESS_TOKEN']
GITEA_USERNAME = os.environ['GITEA_USERNAME']
GITEA_PASSWORD = os.environ['GITEA_PASSWORD']
TARGET_HOST = "https://gitea.ujstor.com"
MIGRATE_URI = "/api/v1/repos/migrate"
ENDPOINT = "%s%s" % (TARGET_HOST, MIGRATE_URI)


url = "https://api.github.com/user/starred"

def fetch_paginated_data(url, gh_access_token):
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"Bearer {gh_access_token}",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    data = []

    while url:
        response = requests.get(url, headers=headers, params={"per_page": 100})
        if response.status_code == 200:
            data.extend(response.json())
            if 'Link' in response.headers:
                links = requests.utils.parse_header_links(response.headers['Link'])
                try:
                    next_link = next(link['url'] for link in links if link['rel'] == 'next')
                    url = next_link
                except StopIteration:
                    url = None
            else:
                url = None
        else:
            print("Failed to fetch data:", response.status_code)
            return None

    return data


EXCLUDE = []

starred_repos = fetch_paginated_data(url, gh_access_token)

def getRepos(starred_repos):
    repos = []
    for repo in starred_repos:
        r = {}
        r['name'] = str(repo['name'])
        r['url'] = str(repo['html_url'])
        r['description'] = str(repo['description'])
        repos.append(r)
    return repos

def createRepo(source_url, name, description):
    headers = {"accept": "application/json", "content-type": "application/json"}
    headers["Authorization"] = "token %s" % GITEA_ACCESS_TOKEN

    migrate_data = {"mirror": True, "uid": 1}
    migrate_data["auth_password"] = GITEA_PASSWORD
    migrate_data["auth_username"] = GITEA_USERNAME
    migrate_data["description"] = description
    migrate_data["repo_name"] = name
    migrate_data["private"] = bool(False)
    migrate_data["clone_addr"] = "%s.git" % (source_url.replace("api.", "").replace("github.com/repos", "github.com"))
    migrate_data["repo_owner"] = GITEA_USERNAME
    print(migrate_data)

    try:
        r = requests.post(url=ENDPOINT, data=json.dumps(migrate_data), headers=headers)
        print(r.text)
        if r.status_code != 201:
            return "Non-OK Response: %s" % r.status_code
        else:
            return "Done: %s" % source_url
    except Exception as e:
        return e
    finally:
        pass

def runMigration(r, x):
    exclude_repos = x
    for repo in r:
        if repo['name'] in exclude_repos:
            print("Excluding %s" % repo['name'])
        else:
            print("Working on %s" % repo['name'])
            print(createRepo(repo['url'], repo['name'], repo['description']))

    return "Done"

if __name__ == '__main__':
    repos = getRepos(starred_repos)
    print(runMigration(repos, EXCLUDE))