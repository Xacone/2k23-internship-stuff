import subprocess
import subprocess as sp
import time
from collections import Counter

import docker
import json
import threading
import os

dpcheck_generated_files_names = []
snyk_generated_files_names = []

dpcheck_vuln_and_severity = {}
dpcheck_cwe = {}

snyk_vuln_and_severity = {}
snyk_cve = {}
snyk_cwe = {}


def perform_dpcheck_scan(dir):
    number_of_deps = 0
    number_of_vuln_deps = 0
    total_triggered_cwes = 0
    file_name = f"dpcheck_{str(dir).replace('/', '_').replace('~', '_')}.json"
    dpcheck_generated_files_names.append(file_name)
    cmd = f"/home/yazid/Downloads/dependency-check/bin/dependency-check -s {dir} -n -f JSON -o {file_name}"
    debut_dpcheck = time.time() * 1000
    output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, text=True)

    fin_dpcheck = time.time() * 1000
    print("Dpcheck a mis : ", fin_dpcheck - debut_dpcheck, " pour ", dir)

    with open(dpcheck_generated_files_names[-1]) as json_file:
        report = json.load(json_file)
        results = report['dependencies']
        for result in results:
            number_of_deps += 1
            try:
                if result['vulnerabilities'] and len(result['vulnerabilities']) > 0:
                    # print(result, "\n")
                    number_of_vuln_deps += 1
                    for vuln in result['vulnerabilities']:
                        dpcheck_vuln_and_severity[vuln['name']] = vuln['severity']
                        if len(vuln['cwes']) > 0:
                            for cwe in vuln['cwes']:
                                dpcheck_cwe[cwe] = 'cwe'
                        print("in : ", result['fileName'])
                        print("\t", vuln, "\n")
            except KeyError:
                print("clé n'existe pas pour ", result)
    print("Nombre de dépendances total : ", number_of_deps)
    print("Nombre de dépendances vulnérables : ", number_of_vuln_deps)
    print("Nombre de vulnérabilités trouvées : ", len(dpcheck_vuln_and_severity))
    print("Nombre de CWEs détectés : ", len(dpcheck_cwe))
    occurences = Counter(dpcheck_vuln_and_severity.values())
    for val, occ in occurences.items():
        print(f"{val} : {occ}")


def perform_snyk_scan(dir):

    vulnerable_packages = {}
    found_vuln = 0

    file_name = f"snyk_{str(dir).replace('/', '_').replace('~', '_')}.json"
    snyk_generated_files_names.append(file_name)
    cmd = f"snyk test {dir} --json > {file_name}"
    debut_snyk = time.time() * 1000
    try :
        output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, text=True)
    except Exception:
        print("exit")
    fin_snyk = time.time() * 1000
    print("Snyk a mis : ", fin_snyk - debut_snyk, " pour ", dir)
    with open(snyk_generated_files_names[-1]) as json_file:
        report = json.load(json_file)
        vulnerabilities = report['vulnerabilities']
        for vuln in vulnerabilities:
            snyk_vuln_and_severity[vuln['id']] = vuln['severity']
            for cve in vuln['identifiers']['CVE']:
                snyk_cve[cve] = 'present'
            for cwe in vuln['identifiers']['CWE']:
                snyk_cwe[cwe] = 'present'
            vulnerable_packages[vuln['moduleName']] = 'vulnerable'
            found_vuln += 1

    print(vulnerable_packages)
    print("Nombre de vulnérabilités total : ", len(snyk_vuln_and_severity))
    print("Nombre de CVE : ", len(snyk_cve))
    print("Nombre de CWE : ", len(snyk_cwe))
    print("Packages vulnérables : ", len(vulnerable_packages))
    occurences = Counter(snyk_vuln_and_severity.values())
    for val, occ in occurences.items():
        print(f"{val} : {occ}")


def main():
    dir = "/home/yazid/poc-88/"
    perform_dpcheck_scan("/home/yazid/poc-88/")
    perform_snyk_scan(dir)


main()
