# Gitea & GitHub Repo Migration

This repository contains Gitea docker instance with postgres db and scripts for migrating repositories from GitHub to Gitea, including both normal and starred repositories.


1. Set up your environment variables by creating a `.env` file in the root directory of the repository. Example:

    ```plaintext
    # Github
    GH_ACCESS_TOKEN = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    # Gitea
    GITEA_USERNAME = "xxxxxxxxxxx"
    GITEA_PASSWORD = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

    # User repos
    GITEA_ACCESS_TOKEN = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

    # Gitea & DB env
    POSTGRES_USER = "gitea"
    POSTGRES_PASSWORD = "gitea"
    POSTGRES_DB = "gitea"
    GITEA_PORT = "3030"
    GITEA_SSH_PORT = "2222" 
    ```

2. Run `docker-compose up -d` to start the Gitea server and PostgreSQL database.
3. Run the migration scripts as needed.


## Migrating User Repositories

Run `migration.py` script to migrate user-owned repositories from GitHub to Gitea.

```bash
python gh_repo_migration.py
```

### Migrating Starred Repositories

Run `starred_migrations.py` script to migrate starred repositories from GitHub to Gitea.

```bash
python gh_starred_migrations.py
```

## Note

- Make sure you have appropriate permissions and access tokens set up for both GitHub and Gitea.
- Modify the `EXCLUDE` list in each script to exclude specific repositories from migration.

