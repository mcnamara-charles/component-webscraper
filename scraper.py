#Import necessary attchments for script
from datetime import datetime
from glob import glob
import requests, email, smtplib, ssl
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep
import random
import progressbar
#Import NORD headers
from nordvpn_connect import initialize_vpn, rotate_VPN, close_vpn_connection
#Import necessary attchments for email
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import winsound

from colorama import init
init()

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    Magenta = "\033[35m"
    Yellow = "\033[33m"


#Imports Complete -----------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------

print('\nStarting Script\n\n')
print(f'{bcolors.OKGREEN}Modules Imported')
data_blocked = False
CHANGED_PRODUCTS = 0
times_tried = 0
frequency = 750
duration = 150
#Introduced Files -----------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------

# http://www.networkinghowtos.com/howto/common-user-agent-list/
generic_headers = ({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})

amazon_headers = ({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5',
            'authority': 'www.amazon.com',
            'method': 'GET'})

newegg_headers = ({'authority': 'www.newegg.com',
'method': 'GET',
'path': '/api/RolloverMenu?CountryCode=USA&from=www.newegg.com',
'scheme': 'https',
'accept': 'application/json, text/plain, */*',
'accept-encoding': 'gzip, deflate, br',
'accept-language': 'en-US,en;q=0.9',
'cache-control': 'no-cache',
'pragma': 'no-cache',
'sec-fetch-dest': 'empty',
'sec-fetch-mode': 'cors',
'sec-fetch-site': 'same-origin',
'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36'})

print("Headers Set")
print("Functions Defined")

#Introduced Headers ---------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------

print('Starting VPN: ')
vpn_settings = initialize_vpn("United States")
close_vpn_connection(vpn_settings)
print('Connecting to VPN Server: ')
vpn_settings = initialize_vpn("United States")
rotate_VPN(vpn_settings)

#VPN Initialized ------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------

def send_email(date_time, flag):
    smtp_port = 465 # SSL Port
    smtp_server = "smtp.gmail.com"
    sender_email = "data.scaper.api@gmail.com"
    receiver_email = "data.scaper.api@gmail.com"
    password = "xmlhttp198"
    if flag in ('Amazon', 'Newegg'):
        subject = f'{flag} is Blocking Data'
        body = f'{flag} has detected Webscraper API as a potential bot. Consider adding more devices to central server or adding random pauses to code. Email will contain last retrieved data. File contains latest data. Please update your records with the latest product data and XLXS files. This Email account is not monitored, do not reply'
    elif flag == "Empty":
        subject = f"Prices Haven't Changed"
        body = f"Don't worry be happy! Webscraper confirms all products are up to date and that no website flagged our data scraper. Email will contain last retrieved data. This Email account is not monitored, do not reply"
    else:
        subject = f"New Data: {date_time}"
        body = f"File contains latest data. Please update your records with the latest product data and XLXS files"

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message["Bcc"] = receiver_email

    message.attach(MIMEText(body, "plain"))

    filename = glob('C:/webscraper-master/search_history/*.xlsx')[-1]
    filename_csv = glob('C:/webscraper-master/trackers/*.xlsx')[-1]

    with open(filename, "rb") as attachment:
        # Add file as application/octet-stream
        # Email client can usually download this automatically as attachment
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    with open(filename_csv, "rb") as attachment_csv:
        # Add file as application/octet-stream
        # Email client can usually download this automatically as attachment
        part_csv = MIMEBase("application", "octet-stream")
        part_csv.set_payload(attachment_csv.read())

    encoders.encode_base64(part)
    encoders.encode_base64(part_csv)

    # Add header as key/value pair to attachment part
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {filename}",
    )

    part_csv.add_header(
        "Content-Disposition",
        f"attachment; filename= {filename_csv}",
    )

    message.attach(part)
    message.attach(part_csv)

    text = message.as_string()

    # Log in to server using secure context and send email
    smtp_context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", smtp_port, context=smtp_context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)

#Email Function Written -----------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------

def get_input(issue, link, stat_code):
    winsound.Beep(frequency, duration)
    winsound.Beep(frequency, duration)
    winsound.Beep(frequency, duration)
    v = 1
    print(f'\n\n{issue} is causing issues. Please Write a Command\n')
    while v == 1:
        task = input("$: ").lower()
        if (task == "help"):
            print(f"\n\n{bcolors.OKGREEN}POSSIBLE COMMANDS:{bcolors.ENDC}\n{bcolors.OKBLUE}help:{bcolors.ENDC} Displays list of possible commands and relation to program\n{bcolors.OKBLUE}break:{bcolors.ENDC} Causes program to cease and throws {issue} reference code\n{bcolors.OKBLUE}continue: {bcolors.ENDC}Program skips this iteration and continues on. Useful for 404 and unauthorized access\n{bcolors.OKBLUE}rotate:{bcolors.ENDC} Asks VPN to find new server, viable if program is blocked due to anti-spam\n{bcolors.OKBLUE}link:{bcolors.ENDC} Displays active link\n{bcolors.OKBLUE}status:{bcolors.ENDC} Prints status code to ensure no 404's\n{bcolors.OKBLUE}exit:{bcolors.ENDC} Exits input program and resumes normal script execution\n\n")
        elif (task == "rotate"):
            rotate_VPN(vpn_settings)
        elif (task == "link"):
            print(f"Link: {link}")
        elif (task == "exit"):
            return None
        elif task in ("break", "continue"):
            return task
        elif (task == "status"):
            print(f"Status Code: {stat_code}")
        else:
            print("Command not understood. Type help for command list")



def extrapolate_product_data(as_data, ap, au, ns, np, nu, mp, ms, mu):
    ns_no_stock = "Out of stock" in ns
    as_no_stock = "Out of stock" in as_data
    products_zero = (ap == 0.0 and np == 0.0)
    if (ns_no_stock and as_no_stock and products_zero):
        use = "newegg"
    elif (ns_no_stock and as_no_stock and products_zero and (np <= ap)):
        use = "amazon"
    elif (ns_no_stock and as_no_stock and products_zero and (np >= ap)):
        use = "newegg"
    elif (ns_no_stock and as_no_stock and (np <= ap)):
        use = "newegg"
    elif (ns_no_stock and as_no_stock and (np >= ap)):
        use = "amazon"
    elif ns_no_stock:
        use = "amazon"
    elif as_no_stock:
        use = "newegg"
    elif np >= ap:
        use = "amazon"
    elif np <= ap:
        use = "newegg"

    if use == "newegg":
        epd_price = np
        epd_url = nu
        epd_stock = ns
    else:
        epd_price = ap
        epd_url = au
        epd_stock = as_data


    if (mp < epd_price and mp != 0.0) and (ms == 'In stock') or ("Out of stock" in epd_stock) and ("this-page" not in mu):
        epd_price = mp
        epd_url = mu
        epd_stock = ms
    return [epd_price, epd_url, epd_stock]

#Data Extrapolation Function Written ----------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------

def search_product_list():
    global refs
    global CHANGED_PRODUCTS
    global procedure
    last_link = ''
    prod_tracker = pd.read_excel('trackers/TRACKER_PRODUCTS.xlsx', sheet_name='TRACKER_PRODUCTS')
    print(f'XLSX File Initiated{bcolors.ENDC}')
    print(prod_tracker)
    print('Start Pause to Delay Detection\n')
    amazon_prod_tracker_urls = prod_tracker.amazon_url
    tracker_log = pd.DataFrame()
    now = datetime.now().strftime('%m-%d-%Y %Hh%Mm')
    print("Initializing Progress Bar Module")
    print("Reading Product Data, See Progress Bar for Progress:\n\n\n\n")
    for x in progressbar.progressbar(range(len(prod_tracker)), redirect_stdout=True):
        sleep(1)
        try:
            base_page = requests.get(prod_tracker.base_url[x], headers=generic_headers)
        except:
            rotate_VPN(vpn_settings)
            base_page = requests.get(prod_tracker.base_url[x], headers=generic_headers)
        try:
            amazon_page = requests.get(prod_tracker.amazon_url[x], headers=amazon_headers)
        except:
            rotate_VPN(vpn_settings)
            amazon_page = requests.get(prod_tracker.amazon_url[x], headers=amazon_headers)
        try:
            newegg_page = requests.get(prod_tracker.newegg_url[x], headers=newegg_headers)
        except:
            rotate_VPN(vpn_settings)
            newegg_page = requests.get(prod_tracker.newegg_url[x], headers=newegg_headers)
        try:
            manu_page = requests.get(prod_tracker.man_url[x], headers=generic_headers)
        except:
            rotate_VPN(vpn_settings)
            manu_page = requests.get(prod_tracker.man_url[x], headers=generic_headers)
        base_soup = BeautifulSoup(base_page.content, features="lxml")
        amazon_soup = BeautifulSoup(amazon_page.content, features="lxml")
        newegg_soup = BeautifulSoup(newegg_page.content, features="lxml")
        manu_soup = BeautifulSoup(manu_page.content, features="lxml")

        if prod_tracker.static[x]:
            print("Static Product")
            continue

        #-----------------------------------------------------------------#
        #Place All Debug Script Here
        #-----------------------------------------------------------------#
        #product title
        try:
            title = newegg_soup.find("h1", class_="product-title").get_text()
            refs = ""
        except:
            if (prod_tracker.newegg_url[x] != "https://www.newegg.com"):
                procedure = get_input("newegg", prod_tracker.newegg_url[x], newegg_page)
                if(procedure == "break"):
                    print("Program Stopped Manually")
                    last_link = prod_tracker.newegg_url[x]
                    refs = "Newegg"
                    break
                elif(procedure == "continue"):
                    print("Iteration skipped manually")
                    continue
                else:
                    newegg_page = requests.get(prod_tracker.newegg_url[x], headers=newegg_headers)
                    newegg_soup = BeautifulSoup(newegg_page.content, features="lxml")
                    title = newegg_soup.find("h1", class_="product-title").get_text()
                #print(f'{bcolors.WARNING}Newegg is causing some issues. To Avoid Stopping early, the VPN is rotating to another server. Please hold{bcolors.ENDC}')
                #rotate_VPN(vpn_settings)
                #print("Resuming Script Execution\n\n\n\n")
                #sleep(1)
                #newegg_page = requests.get(prod_tracker.newegg_url[x], headers=newegg_headers)
                #newegg_soup = BeautifulSoup(newegg_page.content, features="lxml")
                #sleep(1)
                #try:
                    #title = newegg_soup.find("h1", class_="product-title").get_text()
                    #refs = ""
                #except:
                    #last_link = prod_tracker.newegg_url[x]
                    #refs = "Newegg"
                    #break

        try:
            a_title = amazon_soup.find(id='productTitle').get_text().strip()
            refs = ""
        except:
            if (prod_tracker.amazon_url[x] != "https://www.amazon.com"):
                procedure = get_input("amazon", prod_tracker.amazon_url[x], amazon_page)

                if(procedure == "break"):
                    print("Program Stopped Manually")
                    last_link = prod_tracker.amazon_url[x]
                    refs = "Amazon"
                    break
                elif(procedure == "continue"):
                    print("Iteration skipped manually")
                    continue
                else:
                    amazon_page = requests.get(prod_tracker.amazon_url[x], headers=amazon_headers)
                    amazon_soup = BeautifulSoup(amazon_page.content, features="lxml")
                    a_title = amazon_soup.find(id='productTitle').get_text().strip()
        # Get Home Site Data
        try:
            base_price = float(base_soup.select('div.summary bdi')[-1].get_text().replace('$', '').replace(',', '').strip())
        except:
            base_price = 0.0
        try:
            base_stock = base_soup.find("p", class_="out-of-stock").get_text().strip()
        except:
            try:
                if base_price == 0.0:
                    base_stock = "Out of stock"
                else:
                    base_stock = "In stock"
            except:
                base_stock = "Unavailable"
        # Get Manufacturer Website Data
        try:
            #Thermaltake Price
            manu_price = float(manu_soup.find("span", class_="price-wrapper").get_text().replace('USD$', '').replace(',', '').strip())
        except:
            try:
                #Corsair Price
                manu_price = float(manu_soup.find("span", class_="product-price").get_text().replace('$', '').replace(',', '').strip())
            except:
                try:
                    manu_price = float(manu_soup.find("span", class_="offer-price").get_text().replace('$', '').replace(',', '').strip())
                except:
                    try:
                        #NZXT Pricing
                        manu_price = float(manu_soup.find("span", class_="current-price").get_text().replace('$', '').replace(',', '').strip())
                    except:
                        try:
                            #EKWB Pricing
                            manu_price = float(manu_soup.find("span", class_="regular-price").get_text().replace('$', '').replace(',', '').strip())
                        except:
                            manu_price = 0.0

        try:
            if manu_soup.find(class_='availability').get_text().strip() == "No stock":
                manu_stock = 'Out of stock'
            elif manu_soup.find(class_='availability').get_text().replace('!','').strip() == "In stock":
                manu_stock = 'In stock'
        except:
            try:
                if manu_soup.find(id='arrival-notification').get_text().strip() == "Notify Me When In Stock":
                    manu_stock = 'Out of stock'
            except:
                try:
                    if manu_soup.find(id='product-addtocart-button').get_text().strip() == "Add to Cart":
                        manu_stock = 'In stock'
                except:
                    try:
                        if manu_soup.find("button", class_="disabled-stock").get_text().strip() == "Sold Out":
                            manu_stock = 'Out of stock'
                    except:
                        try:
                            if manu_soup.find(class_='add-to-cart-btn').get_text().strip() == "Add to cart":
                                manu_stock = 'In stock'
                        except:
                            manu_stock = 'In stock'

        if manu_price == 0.0:
            manu_stock = 'Out of stock'
        try:
            amazon_price = float(amazon_soup.find(id='price_inside_buybox').get_text().replace('$', '').replace(',', '').strip())
        except:
                # this part gets the price in dollars from amazon.com store
            try:
                amazon_price = float(amazon_soup.find(id='priceblock_saleprice').get_text().replace('$', '').replace(',', '').strip())
            except:

                try:
                    amazon_price = float(amazon_soup.find(id='priceblock_ourprice').get_text().replace('$', '').replace(',', '').strip())
                # Other pricing Box possible
                except:
                    try:
                        amazon_price = float(amazon_soup.find(id='newBuyBoxPrice').get_text().replace('$', '').replace(',', '').strip())
                    except:
                        #Other pricing Box possible
                        try:
                            amazon_price = float(amazon_soup.find(id='#aod-price-1').get_text().replace('$', '').replace(',', '').strip())
                        except:
                            amazon_price = 0.00
        try:
            newegg_price = float(newegg_soup.find("li", class_="price-current").get_text().replace('$', '').replace(',', '').strip())
        except:
            newegg_price = 0.00
        # checking if there is "Out of stock"
        try:
            amazon_stock = amazon_soup.select('#availability .a-color-state')[0].get_text().strip()
        except:
            # checking if there is "Out of stock" on a second possible position
            try:
                amazon_stock = amazon_soup.select('#availability .a-color-price')[0].get_text().strip()
            except:
                # if there is any error in the previous try statements, it means the product is available
                amazon_stock = 'In stock'
        #Compare 0.0 price data for STOCK
        if newegg_price == 0.00:
            newegg_stock = "Out of stock"
        else:
            newegg_stock = newegg_soup.find("div", class_="product-inventory").get_text().replace('.', '').strip()
        if amazon_price == 0.00:
            amazon_stock = "unavailable"

        if (amazon_stock in ("unavailable", "In stock on")):
            amazon_stock = "Out of stock"
        else:
            amazon_stock = "In stock"
        if "In stock" in newegg_stock:
            newegg_stock = "In stock"
        else:
            newegg_stock = "Out of stock"


        # Compares Newegg and Amazon Price and Stock Data
        # Notes Made
        # Vital to Algorithm
        product_data_tuple = extrapolate_product_data(amazon_stock, amazon_price, prod_tracker.amazon_url[x], newegg_stock, newegg_price, prod_tracker.newegg_url[x], manu_price, manu_stock, prod_tracker.man_url[x])
        price = product_data_tuple[0]
        url = product_data_tuple[1]
        stock = product_data_tuple[2]
        #----------------------------------------------------------------------------#
        if price <= (base_price*0.95) or price > base_price:
            it_changed = "Price"
            CHANGED_PRODUCTS += 1
        elif stock != base_stock:
            it_changed = "Inventory"
            CHANGED_PRODUCTS += 1
        else:
            continue

        log = pd.DataFrame({'date': now.replace('h',':').replace('m',''),
                            'code': prod_tracker.code[x], # this code comes from the TRACKER_PRODUCTS file
                            'url':  url,
                            'title': title,
                            'price': price,
                            'stock': stock}, index=[x])
        tracker_log = tracker_log.append(log)

    # after the run, checks last search history record, and appends this run results to it, saving a new file
    if (CHANGED_PRODUCTS > 0 and not refs in ('Amazon', 'Newegg')):
        print("Reversing Indexes")
        final_df = tracker_log.reindex(index=tracker_log.index[::-1])
        final_df.to_excel('search_history/SEARCH_HISTORY_{}.xlsx'.format(now), index=False)
        items_changed = f'Items Changed: {CHANGED_PRODUCTS}'
        print(f'{bcolors.OKGREEN}items_changed')
        print(f'Writing Email from Server{bcolors.ENDC}')
        sleep (10)
        send_email(now, "")
    elif refs in ('Amazon', 'Newegg'):
        print(f'{bcolors.FAIL}{refs} has blocked requests for right now. Please check last link\n{bcolors.ENDC}')
        print(last_link)
        final_df = tracker_log.reindex(index=tracker_log.index[::-1])
        final_df.to_excel('search_history/SEARCH_HISTORY_{}.xlsx'.format(now), index=False)
        items_changed = f'Items Changed: {CHANGED_PRODUCTS}'
        print(bcolors.OKGREEN + items_changed)
        data_blocked = True
        send_email(now, refs)
    else:
        print(f'{bcolors.WARNING}No Items Changed, No Data Added{bcolors.ENDC}')
        send_email(now, "Empty")
    print(f'Email Sent{bcolors.ENDC}')
    print("Closing VPN Connection")
    close_vpn_connection(vpn_settings)
    print("Data Collected, refer to email, or XLSX History file for information")
    print(f'{bcolors.WARNING}If this is open in CMD and not Python 3.9 Dialog Box please close this window before attempting to run in a seperate window and before the scheduled task is set to run to prevent exceptions{bcolors.ENDC}')


search_product_list()
