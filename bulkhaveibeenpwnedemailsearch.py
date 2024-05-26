import requests
import csv
import time

def read_emails_from_file(file_path):
    try:
        with open(file_path, "r") as file:
            return [line.strip() for line in file]
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return []

def check_pwned_accounts(email_list):
    url = "https://haveibeenpwned.com/api/v3/breachedaccount/"
    # Replace with your API key
    headers = {"hibp-api-key": "31337313373133731337313373133731"}

    with open("breach_results.csv", "w", newline="") as csvfile:
        fieldnames = ["Email", "Total Breaches", "Breached Sites"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for email in email_list:
            try:

                response = requests.get(url + email, headers=headers)
                print("Searching for: "+email)
                if response.status_code == 200:
                    breaches = response.json()
                    breached_sites = ", ".join(breach["Name"] for breach in breaches)
                    writer.writerow({"Email": email, "Total Breaches": len(breaches), "Breached Sites": breached_sites})
                elif response.status_code == 404:
                    writer.writerow({"Email": email, "Total Breaches": 0, "Breached Sites": "Not found in any data breaches"})
                else:
                    writer.writerow({"Email": email, "Total Breaches": "Error", "Breached Sites": "Error"})
            except requests.RequestException as e:
                writer.writerow({"Email": email, "Total Breaches": "Error", "Breached Sites": f"Error: {e}"})
            time.sleep(7)

# Replace with the path to your email list file
file_path = "email_list.txt"
emails_to_check = read_emails_from_file(file_path)
if emails_to_check:
    check_pwned_accounts(emails_to_check)
    print("Results saved to breach_results.csv")
else:
    print("No valid email addresses found in the file.")
