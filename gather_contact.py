import argparse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
from datetime import datetime
import os
import re

def sanitize_filename(name):
    return re.sub(r'[^a-zA-Z0-9_-]', '_', name)

def gather_contacts(company, domain, chrome_driver_path):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    service = Service(executable_path=chrome_driver_path)
    browser = webdriver.Chrome(service=service, options=chrome_options)

    all_results = []

    for site in ["linkedin.com/in/", f"rocketreach.co @ {domain}"]:
        browser.get('https://www.google.com')
        time.sleep(1)

        search_box = browser.find_element(By.NAME, 'q')
        search_box.send_keys(f'site:{site} {company}')
        search_box.submit()

        names_with_designation = []
        page_num = 1

        while True:
            print(f"Scraping {site} page {page_num}")

            last_height = browser.execute_script("return document.body.scrollHeight")
            while True:
                browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(1)  # Reduce the sleep time for faster scrolling
                new_height = browser.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height

            results = browser.find_elements(By.CSS_SELECTOR, "h3")
            for result in results:
                data = result.text.split('-')
                if len(data) > 1 and company.lower() in data[-1].lower():
                    full_name_and_designation = data[0].strip()
                    if full_name_and_designation not in names_with_designation:
                        names_with_designation.append(full_name_and_designation)

            try:
                next_button = browser.find_element(By.ID, "pnnext")
                next_button.click()
                page_num += 1
                time.sleep(1)  # Reduce the sleep time between page loads
            except:
                try:
                    more_results_button = browser.find_element(By.CSS_SELECTOR, "a[aria-label='More results']")
                    more_results_button.click()
                    page_num += 1
                    time.sleep(1)  # Reduce the sleep time after clicking "More results"
                except:
                    print(f"No more pages found for {site}.")
                    break

        all_results.extend(names_with_designation)

    browser.close()
    return all_results

def create_emails(names_with_designation, domain_name, format_option):
    emails = []

    format_options = {
        1: lambda first, last: f"{first[0]}{last}@{domain_name}",
        2: lambda first, last: f"{first}.{last}@{domain_name}",
        3: lambda first, last: f"{last}{first[0]}@{domain_name}",
        4: lambda first, last: f"{first}{last[0]}@{domain_name}",
    }

    for name_with_designation in names_with_designation:
        parts = name_with_designation.split()
        first_name = re.sub(r'[^a-zA-Z]', '', parts[0]).lower()
        last_name = re.sub(r'[^a-zA-Z]', '', parts[1]).lower() if len(parts) > 1 else ''

        emails.append(format_options[format_option](first_name, last_name))

    return emails

def write_to_file(company_name, data_list, file_type, output_directory):
    if data_list:
        sanitized_company_name = sanitize_filename(company_name)
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        file_name = os.path.join(output_directory, f"{sanitized_company_name}_{timestamp}_{file_type}.txt")

        try:
            with open(file_name, 'w') as file:
                for data in data_list:
                    file.write(f"{data}\n")

            print(f"Data written to {file_name}")

            if file_type == 'names':
                sorted_file_name = os.path.join(output_directory, f"sorted_{sanitized_company_name}_{timestamp}_{file_type}.txt")
                os.system(f"sort {file_name} | uniq > {sorted_file_name}")
                print(f"Data sorted and duplicates removed. Check '{sorted_file_name}'.")

        except Exception as e:
            print(f"An error occurred while writing to the file: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description="Gather LinkedIn and RocketReach profiles and create email addresses.")
    parser.add_argument("company", help="The company name for Google dork query", nargs='+')
    parser.add_argument("--domain", "-d", help="The domain (e.g., company.com) for email creation", required=True)
    parser.add_argument("--email_format", "-ef", help="Email format (1, 2, 3, or 4). Examples: 1. flastname@domain.com, 2. firstname.lastname@domain.com, 3. lastnamef@domain.com, 4. firstnamel@domain.com", type=int, choices=[1, 2, 3, 4], default=2)
    parser.add_argument("--output_directory", "-o", help="The output directory", default=".")
    parser.add_argument("--chrome_driver_path", "-cdp", help="The path to the ChromeDriver executable", default="/usr/local/bin/chromedriver")
    args = parser.parse_args()

    company_name = " ".join(args.company)
    output_directory = os.path.join(args.output_directory, sanitize_filename(company_name))

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    print(f"Gathering contacts for company: {company_name}")

    names_with_designation = gather_contacts(company_name, args.domain, args.chrome_driver_path)
    emails = create_emails(names_with_designation, args.domain, args.email_format)

    print(f"Found {len(names_with_designation)} contacts.")
    print(f"Creating emails using format {args.email_format}")

    write_to_file(company_name, names_with_designation, "names", output_directory)
    write_to_file(company_name, emails, "emails", output_directory)

    print(f"\nScript executed successfully. All data saved to the directory: {output_directory}")

if __name__ == "__main__":
    main()
