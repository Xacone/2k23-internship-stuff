import docker
import requests as rq
import json
import subprocess

client = docker.from_env()

containers = client.containers.list()
images = client.images.list()

headers = {
    "Authorization": "Bearer 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"
}

docker_files = ['.dockerignore', 'dockerfile', 'Dockerfile', 'docker-compose.yml']
maven_files = ['mvnw.cmd', 'pom.xml', "mvnw"]


def owasp_dependency_check(target_file):
    # ./dependency-check --project /home/yazid/processing-storage-unit/pom.xml --scan . --format XML
    print("todo")


def terraform_scan_img(target):
    print("todo")


def trivy_scan_img(img_name):
    command = f"trivy image --format json --output trivy_report_{img_name.replace('/', '_')}.json {img_name}"
    output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)
    print(output)


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
                    arbre_recursif(link_reformat, repo_content.text, indent + "  ")
                else:
                    if name in docker_files:
                        name += " \033[48;5;117;30m" + " -> Docker 🐋" + "\033[0m"
                    elif name in maven_files:
                        name += " \033[30;48;5;156m" + " -> Maven 🦜" + "\033[0m"
                    print(indent + "📄 " + name)


for container in containers:

    dockerised = False

    container_id = container.id
    container_name = container.name
    container_image = container.image.attrs['RepoTags'][0]
    container_image_location = container.image.attrs['RepoDigests'][0]

    print(f"Container ID: {container_id}")
    print(f"Container Name: {container_name}")
    print(f"Container Image: {container_image}")
    trivy_scan_img(container_image)
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

    print("\n------------------------------------------------------------\n")

"""
Notes :

ghcr.io is a domain used by GitHub Container Registry (GHCR) to host container images. GitHub Container Registry is a feature provided by 
GitHub that allows users to store and manage container images within their GitHub repositories. 
"""
