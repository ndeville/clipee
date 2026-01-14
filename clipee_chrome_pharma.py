# # Copy URL from Chrome and add to Videotech vendors table

import sys
sys.path.append(f"/Users/nic/Python/indeXee")

from datetime import datetime
from pync import Notifier

import time
import os
import subprocess
import my_utils
import sqlite3
import requests

from dotenv import load_dotenv
load_dotenv()
DB_BTOB = os.getenv("DB_BTOB")
APOLLO_API_KEY = os.getenv("APOLLO_API_KEY")

from DB.tools import select_all_records, update_record, create_record, delete_record

# for pasting
# from pynput.keyboard import Key, Controller
# keyb = Controller()

eu_countries = ['AT', 'BE', 'BG', 'CH', 'CY', 'CZ', 'DE', 'DK', 'EE', 'ES', 'FI', 'FR', 'GR', 'HR', 'HU', 'IE', 'IT', 'LT', 'LU', 'LV', 'ME', 'MT', 'NL', 'PL', 'PT', 'RO', 'SE', 'SI', 'SK', 'UK']

# CLASSES

class CompanyData:
    def __init__(self):
        self.name = None
        self.domain = None
        self.url = None
        self.linkedin = None
        self.country = None
        self.industry = None
        self.employees = None
        self.founded = None
        self.location = None
        self.description = None

    def __str__(self):
        result = "\nApollo CompanyData("
        if self.name is not None:
            result += f"\nname\t\t{self.name}"
        if self.domain is not None:
            result += f"\ndomain\t\t{self.domain}"
        if self.url is not None:
            result += f"\nurl\t\t{self.url}"
        if self.linkedin is not None:
            result += f"\nlinkedin\t{self.linkedin}"
        if self.country is not None:
            result += f"\ncountry\t\t{self.country}"
        if self.industry is not None:
            result += f"\nindustry\t{self.industry}"
        if self.employees is not None:
            result += f"\nemployees\t{self.employees}"
        if self.founded is not None:
            result += f"\nfounded\t\t{self.founded}"
        if self.location is not None:
            result += f"\nlocation\t{self.location}"
        if self.description is not None:
            result += f"\ndescription\t{self.description}"
        result += "\n)"
        return result

    def fetch_data(self, api_key, domain, max_retries=10):
        url = "https://api.apollo.io/v1/organizations/enrich"
        data = {
            "api_key": api_key,
            "domain": domain
        }
        headers = {
            'Cache-Control': 'no-cache',
            'Content-Type': 'application/json'
        }

        retries = 0
        while retries < max_retries:
            try:
                response = requests.post(url, headers=headers, json=data)

                # response_data = response.json().get('organization', {})
                response_data = response.json()

                # pp.pprint(response_data)

                if response.status_code == 429:  # Rate limit exceeded
                    print("\n\n\n=========\n❌ Apollo threshold reached\n=========\n\n\n")
                    print("waiting for API limit reset to resume...")
                    my_utils.wait(3700)
                    retries += 1
                    continue

                self.name = response_data.get('organization', {}).get('name')
                self.domain = response_data.get('organization', {}).get('primary_domain')
                self.url = response_data.get('organization', {}).get('website_url')
                self.linkedin = response_data.get('organization', {}).get('linkedin_url')
                self.annual_revenue = response_data.get('organization', {}).get('annual_revenue')
                self.employees = response_data.get('organization', {}).get('estimated_num_employees')
                self.founded = response_data.get('organization', {}).get('founded_year')
                self.location = response_data.get('organization', {}).get('postal_code')
                self.description = response_data.get('organization', {}).get('seo_description')
                location = response_data.get('organization', {}).get('country')
                if location is not None:
                    self.country = my_utils.country_code_from_location(location)
                self.industry = response_data.get('organization', {}).get('industry')

                # update_company_in_db(self)

                break  # Successfully processed the data, exit the loop

            except Exception as e:
                error_message = str(e)

                if error_message == "Expecting value: line 1 column 1 (char 0)":
                    print("\n\n\n=========\n❌ Apollo threshold reached\n=========\n\n\n")
                    print("waiting for API limit reset to resume...")
                    my_utils.wait(3700)
                    retries += 1
                else:
                    print(f"❌  {e}")
                    break




# FUNCTIONS

def get_clipboard_content():
    clipboard_content = subprocess.check_output(['pbpaste']).decode('utf-8')
    return clipboard_content


def get_company_rowid_from_domain(domain):
    with sqlite3.connect(DB_BTOB) as conn:
        cur = conn.cursor()
        cur.execute(f"""
            SELECT rowid FROM ka_pharma WHERE domain = ?
        """, (domain,))
        return cur.fetchone()[0]


def add_to_db(url):

    from DB.tools import create_record
    import my_utils

    if url.startswith('http'):

        domain = my_utils.domain_from_url(url)

        try:

            create_record(DB_BTOB, 'ka_pharma', {
                'website': url,
                'domain': domain,
                'notes': f"manual capture clipee_chrome_pharma.py on {datetime.now().strftime('%Y-%m-%d %H:%M')}",
                'created': f"{datetime.now().strftime('%Y-%m-%d %H:%M')}",
                })
            
            Notifier.notify(
                title='SUCCESS',
                message=f'🟢\ncreated {domain} in ka_pharma table',
            )

            # ENRICH

            rowid = get_company_rowid_from_domain(domain)

            company_update_dict = {
                'rowid': rowid,
                'updated': f"{datetime.now().strftime('%Y-%m-%d %H:%M')}",
                'apollo': 1,
            }

            print(f"\n⚙️    Enriching {domain}...")

            company_data = CompanyData()
            company_data.fetch_data(APOLLO_API_KEY, domain=domain)

            print(f"{company_data}")

            # Update the company fields

            if company_data.name is not None:
                company_update_dict['name'] = company_data.name

            if company_data.country is not None:
                company_update_dict['country'] = company_data.country

                if company_data.country not in eu_countries:
                    company_update_dict['eu'] = 0
                else:
                    company_update_dict['eu'] = 1

            if company_data.industry is not None:
                company_update_dict['industry'] = company_data.industry

            if company_data.employees is not None:
                company_update_dict['ftes'] = company_data.employees

            if company_data.founded is not None:
                company_update_dict['founded'] = company_data.founded

            if company_data.location is not None:
                company_update_dict['location'] = company_data.location

            if company_data.linkedin is not None:
                company_update_dict['linkedin'] = company_data.linkedin

            if company_data.description is not None:
                company_update_dict['description'] = company_data.description

            # Update the company record in the database
            update_record(DB_BTOB, 'ka_pharma', company_update_dict)

            Notifier.notify(
                title='SUCCESS',
                message=f'🟢🟢🟢\nupdated {domain} in ka_pharma table',
            )


        except Exception as e:
            
            Notifier.notify(
                title='FAIL',
                message=f'🔴🔴🔴 ERROR: {e}',
            )



    else:
        
        Notifier.notify(
                title='FAIL',
                message=f'🔴🔴🔴 NOT A URL {url}',
            )



# MAIN

with sqlite3.connect(DB_BTOB) as conn:
    cur = conn.cursor()
    cur.execute("""
        SELECT domain, alt_domains
        FROM ka_pharma 
        WHERE domain IS NOT NULL
    """)
    rows = cur.fetchall()
    
    existing_domains = set()  # Unique
    for domain, alts in rows:
        # Main domain (normalize: lower/strip)
        existing_domains.add(domain.strip().lower())
        
        # Alt domains: split comma, normalize
        if alts and alts.strip():  # Not NULL/empty
            for alt in alts.split(','):
                cleaned_alt = alt.strip().lower()
                if cleaned_alt:  # Skip empty
                    existing_domains.add(cleaned_alt)
    
    existing_domains = sorted(existing_domains)

url = my_utils.get_chrome_active_tab_url()
url = my_utils.clean_url(url)

domain = my_utils.domain_from_url(url)

if domain in existing_domains:
    print(f"\n\n\n=========\nℹ️  {domain} already exists\n=========\n\n\n")
    Notifier.notify(
        title='ℹ️  ALREADY EXISTS',
        message=f'{domain}',
    )
else:
    add_to_db(url)