import requests
import json
import os
import time

input_file_path = input("Specify path to input file:\t")

#validate the path to the input file.  If path is invalid, script will exit
if os.path.isfile(input_file_path):
    print("opening input file")
    #open list of email addresses in read mode
    email_addrs = open(input_file_path, "r")
    print("opening report file")
    #open output file for results
    f = open("HIBP_report.txt", "w")
    #open error log file
    el = open("ErrorLog.txt", "w")
    #create header with API key.  This will not work without a valid key
    headers = {"hibp-api-key":"YOUR API KEY GOES HERE"}
    #Column header for report is formatted and written to file
    report_header = "Email\tType\tName\tTitle\tDomain\tDate\tData Classes"
    f.write(report_header + "\r\n")
    f.flush()
    print(report_header)
    #for every email in the list
    for email_addr in email_addrs:
        #remove CRLF
        email_addr = email_addr.replace("\r","")
        email_addr = email_addr.replace("\n","")
        print("Checking:\t" + email_addr)
        #sleep for 2 seconds to avoid the HIBP retry delay of ~1.5 seconds
        time.sleep(2)
        #format the URL for the request with the target email address (Breach Data)
        url = ("https://haveibeenpwned.com/api/v3/breachedaccount/%s?truncateResponse=false") % (str(email_addr))
        try:
            #submit request
            r = requests.get(url, headers=headers)
        except:
            #if error, write to error log
            el.write("*** Error running request ***" + "\t" + url + "\r\n")
            print("*** Error running request ***" + "\t" + url)
        #if data was successfully returned
        if r.status_code == 200:
            #convert to JSON
            data = r.json()
            #for all data in the JSON output
            for d in data:
                #format the output line for the report file and write it
                line = (str(email_addr) + "\tBreach\t" + str(d["Name"]) + "\t" + str(d["Title"]) + "\t" + str(d["Domain"]) + "\t" + str(d["BreachDate"]) + "\t" + str(d["DataClasses"]))
                f.write(line + "\r\n")
                f.flush()
                print(line)
        #if there is no data associated with that email - Do nothing
        elif r.status_code == 404:
            pass
        #if any other return code comes back, write it to the error log and print to the screen
        else:
            el.write(str(r.status_code) + "\t" + url + "\r\n")
            el.flush()
            print("\t" + str(r.status_code) + "\t" + url)
        #sleep for 2 seconds to avoid the HIBP retry delay
        time.sleep(2)
        #format the URL for the request with the target email address (Paste Data)
        url = ("https://haveibeenpwned.com/api/v3/pasteaccount/%s?truncateResponse=false") % (str(email_addr))
        try:
            #submit request
            r = requests.get(url, headers=headers)
        except:
            #if error, write to error log
            el.write("*** Error running request ***" + "\t" + url + "\r\n")
            print("*** Error running request ***" + "\t" + url)
        #if data was successfully returned
        if r.status_code == 200:
            #convert to json
            data = r.json()
            #for all data in the JSON output
            for d in data:
                #format the output line for the report file and write it
                line = (str(email_addr) + "\tPaste\t" + str(d["Source"]) + "\t" + str(d["Title"]) + "\t\t" + str(d["Date"]) + "\t")
                f.write(line + "\r\n")
                f.flush()
                print(line)
        #if there is no data associated with that email - Do nothing
        elif r.status_code == 404:
            pass
        #if any other return code comes back, write it to the error log and print to the screen
        else:
            el.write(str(r.status_code) + "\t" + url + "\r\n")
            el.flush()
            print("\t" + str(r.status_code) + "\t" + url)
    #once all data has been checked, close all file handles
    f.close()
    el.close()
    email_addrs.close()
#if inut file doesn't exist, display below message
else:
    print("Invalid input file.  Check Path")
