import docker
import requests as rq
import json

client = docker.from_env()

containers = client.containers.list()
images = client.images.list()

headers = {
    "Authorization": "Bearer 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"
}

docker_files = ['.dockerignore', 'dockerfile', 'Dockerfile', 'docker-compose.yml']
maven_files = ['mvnw.cmd', 'pom.xml']

def arbre_recursif(link, root, indent=" "):
    repo_content = json.loads(root)
    for val in repo_content:
        name = val['name']
        if isinstance(val, dict):
            if 'name' in val:
                if val['type'] == 'dir':
                    print(indent + "📂 " + name)
                    link_reformat = link + "/" + val['name']
                    repo_content = rq.get(link_reformat, headers=headers)
                    arbre_recursif(link_reformat, repo_content.text, indent + "   ")
                else :
                    if name in docker_files:
                        name += " -> Docker 🐋"
                    print(indent + "📄 " + name)

for container in containers:
    container_id = container.id
    container_name = container.name
    container_image = container.image.attrs['RepoTags'][0]
    container_image_location = container.image.attrs['RepoDigests'][0]

    print(f"Container ID: {container_id}")
    print(f"Container Name: {container_name}")
    print(f"Container Image: {container_image}")
    print(f"Container Image Location: {container_image_location}")

    splited_img_loc = container_image_location.split("/")

    if splited_img_loc[0] == "ghcr.io":

        author_name = splited_img_loc[1]
        repo_name = splited_img_loc[2]
        target_base = "https://api.github.com/repos/" + author_name + "/" + repo_name[:-72]
        target_languages = target_base + "/languages"
        print(target_languages)
        languages = rq.get(target_languages, headers=headers)
        print(languages.text)

        print("\n")

        repo_content = rq.get(target_base + "/contents", headers=headers)

        arbre_recursif(target_base + "/contents", repo_content.text)

        """
        repo_content = json.loads(repo_content.text)
        for val in repo_content:
            print(val['name'])
        """

    print("\n------------------------------------------------------------\n")

"""
ghcr.io is a domain used by GitHub Container Registry (GHCR) to host container images. GitHub Container Registry is a feature provided by 
GitHub that allows users to store and manage container images within their GitHub repositories. 
"""
