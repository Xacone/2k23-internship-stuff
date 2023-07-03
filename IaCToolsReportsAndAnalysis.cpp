import subprocess
import subprocess as sp
import time
import json
import threading
import os
from collections import Counter

terrascan_generated_files_names = []
tfsec_generated_files_names = []


def count_lines_in_directory(directory):
    total_lines = 0
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if os.path.isfile(file_path):
                with open(file_path, 'r') as f:
                    try:
                        if f.name.endswith('.tf'):
                            print(f.name)
                            lines = f.readlines()
                            total_lines += len(lines)
                    except Exception:
                        print("---")
    return total_lines


def perform_terrascan_scan(dir):
    file_name = f"terrascan_{str(dir).replace('/', '_')}.json"
    terrascan_generated_files_names.append(file_name)
    cmd = f"terrascan scan -d {dir} -o json > {file_name}"
    debut_terrascan = time.time() * 1000
    try:
        output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, text=True)
    except Exception:
        print("")
    fin_terrascan = time.time() * 1000
    print("Terrascan a mis ", fin_terrascan - debut_terrascan, " pour ", dir)


def perform_tfsec_scan(dir):
    file_name = f"tfsec_{str(dir).replace('/', '_')}.json"
    tfsec_generated_files_names.append(file_name)
    cmd = f"tfsec {dir} --format json > {file_name}"
    debut_tfsec = time.time() * 1000
    try:
        output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, text=True)
    except Exception:
        print("")
    fin_tfsec = time.time() * 1000
    print("Tfsec a mis ", fin_tfsec - debut_tfsec, " pour ", dir)


def TerraformGoat_complete_analysis(root_dir):
    for root, dirs, files in os.walk(root_dir):
        input()
        for file in files:
            # print(f"{sub_indent}{file}")
            if str(file).endswith('.tf'):
                print("\n\n[*] Scanning ", root)
                print("Nombre de lignes analysées : ", count_lines_in_directory(root))

                """
                perform_terrascan_scan(root)
                with open(terrascan_generated_files_names[-1]) as json_file:
                    report = json.load(json_file)
                    results = report['results']
                    try:
                        if len(results['violations']) > 0:
                            terrascan_vuln_and_severity = {}
                            for result in results['violations']:
                                terrascan_vuln_and_severity[result['rule_id']] = result['severity']
                                print("Description : ", result['description'])
                            print("Nombre de vulnérabilités trouvées par Terrascan : ",
                                  len(terrascan_vuln_and_severity))
                            occurences = Counter(terrascan_vuln_and_severity.values())
                            for val, occ in occurences.items():
                                print(f"{val} : {occ}")
                    except Exception:
                        print(root + " non traité.")
                """

                perform_tfsec_scan(root)
                with open(tfsec_generated_files_names[-1]) as json_file:
                    report = json.load(json_file)
                    results = report['results']
                    tfsec_vuln_and_severity = {}
                    try:
                        if len(results) > 0:
                            for result in results:
                                tfsec_vuln_and_severity[result['rule_id']] = result['severity']
                                print("Description : ", result['description'])
                                print("Impact : ", result['impact'])
                                print("Resolution : ", result['resolution'])
                                print("\n--------------------------------------------------------------------------------------------\n")

                            print("Nombre de vulnérabilités trouvées : ", len(tfsec_vuln_and_severity))
                            occurences = Counter(tfsec_vuln_and_severity.values())
                            for val, occ in occurences.items():
                                print(f"{val} : {occ}")
                    except Exception:
                        print(root + " non traité ! ")

                break


root_directory = '/home/yazid/TerraformGoat/'
TerraformGoat_complete_analysis(root_directory)

# perform_terrascan_scan('~/KaiMonkey/terraform/aws')
# perform_tfsec_scan('~/KaiMonkey/terraform/aws')
