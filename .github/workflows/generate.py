# *******************************************************************************
# Copyright (c) 2023 Eclipse Foundation and others.
# This program and the accompanying materials are made available
# under the terms of the MIT License
# which is available at https://spdx.org/licenses/MIT.html
# SPDX-License-Identifier: MIT
# *******************************************************************************

import re
import requests


def generate():

    page = 1
    projects = []

    while True:
        print(f"Getting page {page} from Eclipse API")
        response = requests.get(f"https://projects.eclipse.org/api/projects?github_only=1&pagesize=100&page={page}")
        if response.status_code == 200:
            new_projects = response.json()
            if len(new_projects) > 0:
                projects.extend(new_projects)
                page += 1
            else:
                break
        else:
            break

    OUTPUT = './docs/projects.csv'

    with open(OUTPUT, "w") as out:
        out.write("| Project name | Eclipse Project | GitHub organization |\n")
        out.write("| :----------- | :-------------- | :------------------ |\n")

        for project in projects:
            name = escape(project["name"])
            project_id = escape(project["project_id"])
            github_id = project["github"]["org"]

            if not github_id:
                for repo in project["github_repos"]:
                    m = re.search(r"https://github.com/([^/]+)/.*", repo["url"])
                    if m is not None:
                        github_id = m.group(1)
                        break

            out.write(f"| {name} "
                      f"| [{project_id}](https://projects.eclipse.org/projects/{project_id}) "
                      f"| [{github_id}](https://github.com/{github_id}) |\n")


def escape(s: str) -> str:
    return s.replace("|", "&#9;")


if __name__ == "__main__":
    generate()
    exit(0)
