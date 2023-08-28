# -*- coding: utf-8 -*-

import json
import os
import subprocess
import time


def checkov_scan(target, output):
    cmd = f"checkov -d {target} -o json > {output}"
    output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, text=True)

def gothrough(root):
    i = 0
    for root, dirs, files in os.walk(root):
        for file in files:
            if str(file).endswith(".tf"):
                print(root)
                output_name = str(root).replace("\\", "_").replace("/", "_") + "_" + str(file).replace(".tf", ".json")

                time_start = time.time() * 1000
                try:
                    checkov_scan(root, output_name)
                except Exception as e:
                    print(e)
                time_end = (time.time() * 1000) - time_start
                print("A mis : ", time_end, "ms")
                break



"""
def gothrough(root):
    i = 0
    for root, dirs, files in os.walk(root):
        for dir in dirs:
            print(dir)
            i+=1
            file_path = os.path.join(root, dir)
            if os.path.isfile(file_path):
                with open(file_path, 'r') as f:
                    time_start = time.time() * 1000
                    try:
                        if f.name.endswith('.tf'):
                            print("[*] Scanning", file_path)
                            output_name = str(i) + "_" + str(f.name).replace('\\', '_') + ".json"
                            checkov_scan(file_path, output_name)
                    except Exception as e:
                        print("---\n", e)
                    time_end = (time.time() * 1000) - time_start
                    print("A mis :  : ", time_end, "ms")
"""
#TerraformGoat_aliyun_oss_server_side_encryption_no_kms_set_main.json

gothrough("TerraformGoat/aliyun/oss/server_side_encryption_no_kms_set")

