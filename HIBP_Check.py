import requests
import json
import os
import time

input_file_path = input("Specify path to input file:\t")

if os.path.isfile(input_file_path):
    print("opening input file")
    email_addrs = open(input_file_path, "r")
    print("opening report file")
    f = open("HIBP_report.txt", "w")
    el = open("ErrorLog.txt", "w")
    headers = {"hibp-api-key":"YOUR API KEY GOES HERE"}
    report_header = "Email\tType\tName\tTitle\tDomain\tDate\tData Classes"
    f.write(report_header + "\r\n")
    f.flush()
    print(report_header)
    for email_addr in email_addrs:
        email_addr = email_addr.replace("\r","")
        email_addr = email_addr.replace("\n","")
        print("Checking:\t" + email_addr)
        time.sleep(2)
        url = ("https://haveibeenpwned.com/api/v3/breachedaccount/%s?truncateResponse=false") % (str(email_addr))
        try:
            r = requests.get(url, headers=headers)
        except:
            el.write("*** Error running request ***" + "\t" + url + "\r\n")
            print("*** Error running request ***" + "\t" + url)
        if r.status_code == 200:
            data = r.json()
            for d in data:
                line = (str(email_addr) + "\tBreach\t" + str(d["Name"]) + "\t" + str(d["Title"]) + "\t" + str(d["Domain"]) + "\t" + str(d["BreachDate"]) + "\t" + str(d["DataClasses"]))
                f.write(line + "\r\n")
                f.flush()
                print(line)
        elif r.status_code == 404:
            pass
        else:
            el.write(str(r.status_code) + "\t" + url + "\r\n")
            el.flush()
            print("\t" + str(r.status_code) + "\t" + url)

        time.sleep(2)
        url = ("https://haveibeenpwned.com/api/v3/pasteaccount/%s?truncateResponse=false") % (str(email_addr))
        try:
            r = requests.get(url, headers=headers)
        except:
            el.write("*** Error running request ***" + "\t" + url + "\r\n")
            print("*** Error running request ***" + "\t" + url)
        if r.status_code == 200:
            data = r.json()
            for d in data:
                line = (str(email_addr) + "\tPaste\t" + str(d["Source"]) + "\t" + str(d["Title"]) + "\t\t" + str(d["Date"]) + "\t")
                f.write(line + "\r\n")
                f.flush()
                print(line)
        elif r.status_code == 404:
            pass
        else:
            el.write(str(r.status_code) + "\t" + url + "\r\n")
            el.flush()
            print("\t" + str(r.status_code) + "\t" + url)
    f.close()
    el.close()
    email_addrs.close()
else:
    print("Invalid input file.  Check Path")
