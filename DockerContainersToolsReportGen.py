import subprocess
import subprocess as sp
import time

import docker
import json
import threading

client = docker.from_env()
images = client.images.list()

threads = []

trivy_generated_files_names = []
grype_generated_files_names = []
snyk_generated_files_names = []


def perform_snyk_scan(img_name):
    file_name = f"snyk_{str(img_name).replace('/', '_')}.json"
    snyk_generated_files_names.append(file_name)
    cmd = f"snyk test --docker {img_name} --json > {file_name}"
    debut_snyk = time.time() * 1000
    try:
        output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, text=True)
    except Exception:
        print("Error")
    fin_snyk = time.time() * 1000
    print("Snyk a mis ", fin_snyk - debut_snyk, " pour ", img_name)
    # print(output)

def perform_trivy_scan(img_name):
    file_name = f"trivy_{str(img_name).replace('/', '_')}.json"
    trivy_generated_files_names.append(file_name)
    cmd = f"trivy image --format json --output {file_name} {img_name}"
    debut_trivy = time.time() * 1000
    output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, text=True)
    fin_trivy = time.time() * 1000
    print("Trivy a mis ", fin_trivy - debut_trivy, " pour ", img_name)
    # print(output)


def perform_grype_scan(img_name):
    file_name = f"grype_{str(img_name).replace('/', '_')}.json"
    grype_generated_files_names.append(file_name)
    cmd = f"grype {img_name} --scope all-layers -o json > {file_name}"
    debut_grype = time.time() * 1000
    output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, text=True)
    fin_grype = time.time() * 1000
    print("Grype a mis ", fin_grype - debut_grype, " pour ", img_name)
    # print(output)


def main():
    for img in images:
        if len(img.tags) > 0:
            img_name = img.tags[0]
            if str(img_name).__contains__("ghcr.io"):
                trivy_thread = threading.Thread(target=perform_trivy_scan, args=(img_name,))
                grype_thread = threading.Thread(target=perform_grype_scan, args=(img_name,))
                snyk_thread = threading.Thread(target=perform_snyk_scan, args=(img_name,))
                threads.append(trivy_thread)
                threads.append(grype_thread)
                threads.append(snyk_thread)

                """
                trivy_thread.start()
                trivy_thread.join()

                grype_thread.start()
                grype_thread.join()
                """

                snyk_thread.start()
                snyk_thread.join()

main()

"""
for thread in threads:
    thread.join()
"""

print("[*] Génération finie !")
