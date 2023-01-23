#!/bin/python3
import os
import json
from datetime import datetime
import requests

headers = {
    'Sec-Ch-Ua': '"Chromium";v="105", "Not)A;Brand";v="8"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"Linux"',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.5195.102 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Sec-Fetch-Dest': 'document',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'close'
}

path_to_dirsearch = "/usr/bin"
domain = input("Enter the domain: ")
url = 'https://crt.sh/?q=' + domain + '&output=json'
directory = domain + "_recon"
if os.path.exists(directory):
    print("Recon directory for " + domain + " already exists.")
else:
    print("Creating directory " + directory + ".")
    os.mkdir(directory)

def dirsearch_scan():
    os.system("touch ./" + directory + "/crt")
    os.system(path_to_dirsearch + "/dirsearch -u " + domain + " --format=simple --output=" + directory + "/dirsearch")
    print("The results of dirsearch scan are stored in " + directory + "/dirsearch.")

def crt_scan():
    os.system("touch ./" + directory + "/dirsearch")
    response = requests.get(url, headers=headers)
    json_response = response.json()
    with open(directory + '/crt', 'w') as f:
        json.dump(json_response, f)
    print("The results of cert parsing is stored in " + directory + "/crt.")

def subdomain_scan():
    os.system("touch ./" + directory + "/subdomains")
    os.system("gobuster dns -t 30 -d " + domain + " -w /usr/share/wordlists/combined_subdomains.txt -o " + directory + "/subdomains")
    print("The results of gobuster are stored in " + directory + "/subdomains.")

def nmap_scan():
    os.system("touch ./" + directory + "/nmap")
    if os.path.exists('./' + directory + '/subdomains'):
        subdomain_array = []
        with open(directory + "/subdomains", "r") as subdomains:
            for line in subdomains:
                subdomain_array.append(line)
        for line in subdomain_array:
            line = line.replace("Found: ", "").replace("\n","")
            os.system("nmap -vv -sV " + line + " >> " + directory + "/nmap")
    else:
        os.system("nmap -vv -sV " + domain + " > " + directory + "/nmap")
    print("The results of nmap scan are stored in " + directory + "/nmap.")

scan_type = input("Enter the scan type (1) nmap only, 2) dirsearch only, 3) crt only, 4) subdomain enumeration only, or hit enter for all): ")

if scan_type == "1":
    nmap_scan()
elif scan_type == "2":
    dirsearch_scan()
elif scan_type == "3":
    crt_scan()
elif scan_type == "4":
    subdomain_scan()
else:
    dirsearch_scan()
    crt_scan()
    subdomain_scan()
    nmap_scan()

print("Generating recon report from output files...")
today = str(datetime.now())
os.system("touch ./" + directory + "/report")
with open(directory + "/report", "w") as report:
    report.write("This scan was created on " + today + "\n")
    report.write("Results for Nmap:\n")
    
    with open(directory + "/nmap") as nmap:
        for line in nmap:
            report.write(line)
    
    with open(directory + "/dirsearch") as dirsearch:
        report.write("Results for Dirsearch:\n")
        for line in dirsearch:
            report.write(line)
    
    with open(directory + "/crt") as crt:
        report.write("Results for crt.sh:\n")
        json_data = json.load(crt)
        for item in json_data:
            with open(directory + "/crt_subdomains") as crt_subdomains:
                crt_subdomains.write(item["name_value"] + "\n")
            report.write(item["name_value"] + "\n")
    with open(directory + "/subdomains") as subdomains:
        report.write("Results for subdomain enumeration:\n")
        for item in subdomains:
            report.write(item)
print("Report located in " + directory + "/report")
    print("The results of gobuster are stored in " + directory + "/subdomains.")

def nmap_scan():
    os.system("touch ./" + directory + "/nmap")
    os.system("nmap -v " + domain + " > " + directory + "/nmap")
    print("The results of nmap scan are stored in " + directory + "/nmap.")

scan_type = input("Enter the scan type (1) nmap only, 2) dirsearch only, 3) crt only, 4) subdomain enumeration only, or hit enter for all): ")

if scan_type == "1":
    nmap_scan()
elif scan_type == "2":
    dirsearch_scan()
elif scan_type == "3":
    crt_scan()
elif scan_type == "4":
    subdomain_scan()
else:
    dirsearch_scan()
    crt_scan()
    subdomain_scan()
    nmap_scan()

print("Generating recon report from output files...")
today = str(datetime.now())
os.system("touch ./" + directory + "/report")
with open(directory + "/report", "w") as report:
    report.write("This scan was created on " + today + "\n")
    report.write("Results for Nmap:\n")
    
    with open(directory + "/nmap") as nmap:
        for line in nmap:
            report.write(line)
    
    with open(directory + "/dirsearch") as dirsearch:
        report.write("Results for Dirsearch:\n")
        for line in dirsearch:
            report.write(line)
    
    with open(directory + "/crt") as crt:
        report.write("Results for crt.sh:\n")
        json_data = json.load(crt)
        for item in json_data:
            report.write(item["name_value"] + "\n")
    with open(directory + "/subdomains") as subdomains:
        report.write("Results for subdomain enumeration:\n")
        for item in subdomains:
            report.write(item)
print("Report located at " + directory + "/report")
