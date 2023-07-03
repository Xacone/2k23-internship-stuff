import json
import os
from collections import Counter
import time
import matplotlib

trivy_generated_files_names = []
grype_generated_files_names = []
snyk_generated_files_names = []
terrascan_generated_files_names = []
tfsec_generated_files_names = []

trivy_cves_and_criticities = {}
grype_cves_and_criticities = {}
snyk_cves_and_criticities = {}
terrascan_problems_and_criticities = {}
tfsec_problems_and_criticities = {}

trivy_number_of_vulns_per_file = {}
grype_number_of_vulns_per_file = {}
snyk_number_of_vulns_per_file = {}
tfsec_numnber_of_vulns_per_file = {}

repertoire_courat = os.getcwd()

for file in os.listdir(repertoire_courat):
    if file.startswith('grype'):
        grype_generated_files_names.append(file)
    if file.startswith('trivy'):
        trivy_generated_files_names.append(file)
    if file.startswith('snyk'):
        snyk_generated_files_names.append(file)



def grype_files_analysis():
    for grype_file in grype_generated_files_names:
        print("[*] Analyse de ", grype_file)
        with open(grype_file) as json_file:
            report = json.load(json_file)
            matches = report['matches']
            vulns_found = 0
            for match in matches:
                grype_cves_and_criticities[match['vulnerability']['id']] = match['vulnerability']['severity']
                vulns_found += 1
            grype_number_of_vulns_per_file[grype_file] = vulns_found


def trivy_files_analysis():
    for trivy_file in trivy_generated_files_names:
        print("[*] Analyse de ", trivy_file)
        with open(trivy_file) as json_file:
            report = json.load(json_file)
            vulnerabilities = report['Results'][0]['Vulnerabilities']
            vulns_found = 0
            for vuln in vulnerabilities:
                trivy_cves_and_criticities[vuln['VulnerabilityID']] = vuln['Severity']
                vulns_found += 1
            trivy_number_of_vulns_per_file[trivy_file] = vulns_found
    # print(trivy_cves_and_criticities)


def snyk_files_analysis():
    for snyk_file in snyk_generated_files_names:
        print("[*] Analyse de ", snyk_file)
        with open(snyk_file) as json_file:
            report = json.load(json_file)
            vulnerabilities = report['vulnerabilities']
            vulns_found = 0
            for vuln in vulnerabilities:
                if len(vuln['identifiers']['CVE']) > 0:
                    snyk_cves_and_criticities[vuln['identifiers']['CVE'][0]] = vuln['nvdSeverity']
                    vulns_found += 1
            snyk_number_of_vulns_per_file[snyk_file] = vulns_found


def main():
    print("\n----------------------------------------------------------------\n")

    grype_files_analysis()
    for key, val in grype_number_of_vulns_per_file.items():
        print(key, " : ", val)
    print("\nNombre total de CVE uniques trouvées par Grype: ", len(grype_cves_and_criticities))
    occurences = Counter(grype_cves_and_criticities.values())
    for val, occ in occurences.items():
        print(f"Niveau {val} : {occ} fois")

    print("\n----------------------------------------------------------------\n")

    trivy_files_analysis()
    for key, val in trivy_number_of_vulns_per_file.items():
        print(key, " : ", val)
    print("\nNombre total de CVE uniques trouvées par Trivy: ", len(trivy_cves_and_criticities))
    occurences = Counter(trivy_cves_and_criticities.values())
    for val, occ in occurences.items():
        print(f"Niveau {val} : {occ} fois")

    print("\n----------------------------------------------------------------\n")

    snyk_files_analysis()
    for key, val in snyk_number_of_vulns_per_file.items():
        print(key, " : ", val)
    print("\nNombre total de CVE uniques trouvées par Snyk: ", len(grype_cves_and_criticities))
    occurences = Counter(snyk_cves_and_criticities.values())
    for val, occ in occurences.items():
        print(f"Niveau {val} : {occ} fois")


main()
