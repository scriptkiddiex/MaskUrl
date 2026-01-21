import os
import pyshorteners
import re
import sys
import socket
import shutil



def get_center_padding(text_block):
    """Calculates padding to center a multiline block of text based on terminal width."""
    try:

        term_width = shutil.get_terminal_size((80, 20)).columns
    except:
        term_width = 80
    

    lines = text_block.strip("\n").split("\n")
    max_line_len = max(len(line) for line in lines)
    

    return max(0, (term_width - max_line_len) // 2)

def print_centered(text, color=""):
    """Prints each line of a block of text with the calculated center padding."""
    padding = " " * get_center_padding(text)
    reset = "\033[0m"
    for line in text.strip("\n").split("\n"):
        print(f"{padding}{color}{line}{reset}")



def home_logo():
    logo = r"""
 _____ _____ _____ _____ _____ _____ __    
|     |  _  |   __|  |  |  |  | __  |  |   
| | | |     |__   |    -|  |  |    -|  |__ 
|_|_|_|__|__|_____|__|__|_____|__|__|_____|
                                           
    """
    print_centered(logo)

def home_about():
    about_text = (
        "╔════════════════════════════════════════════════════════════╗\n"
        "║  MaskUrl v1.0.2 | Created by ScriptKiddie                  ║\n"
        "║  Licensed under MIT | Copyright (c) 2026                   ║\n"
        "║  Usage: For Educational & Authorized Testing Only          ║\n"
        "╚════════════════════════════════════════════════════════════╝"
    )
    print_centered(about_text)

def validate_url(url):
    url = url.strip().lower()
    if url.startswith(("http://", "https://")):
        return url
    return ""

def validate_domain(domain):
    return bool(re.match(r'^[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$', domain))

def internet_connection():
    try:
        socket.create_connection(("1.1.1.1", 53), timeout=3)
        return True
    except OSError:
        return False

def validate_phishing_keyword(keyword):
    return bool(re.fullmatch(r"[A-Za-z0-9_-]+", keyword))

def shortener_service(url):
    services = {1: "tinyurl", 2: "dagd", 3: "clckru"}
    
    print("\n[1] TinyURL | [2] Da.gd | [3] Clck.ru")
    
    try:
        choice = int(input("\nSelect service [1-3]:  ").strip())
        if choice not in services:
            print("[!]Invalid Selection")
            return "error"

        s = pyshorteners.Shortener()
        short_url = getattr(s, services[choice]).short(url)
        return short_url
    except Exception as e:
        print(f"[!]Shortening Error: {e}")
        return "error"

def combiner(masked_url, domain_name, phishing_keyword):
    prefix, suffix = masked_url.split("://")
    keyword = f"-{phishing_keyword}" if phishing_keyword else ""
    return f"{prefix}://{domain_name}{keyword}@{suffix}"



def urlmask():
    if not internet_connection():
        print("[!]No Internet Connection")
        return

    try:
        print("\n")
        raw_url = input("\n[+]Target URL (e.g., https://site.com): ").strip()
        target_url = validate_url(raw_url)
        
        if not target_url:
            print("[!]Invalid URL format.")
            return

        masked_base = shortener_service(target_url)
        if masked_base == "error": return


        fake_domain = input("\n[+]Masking Domain (e.g., google.com): ").strip().lower()
        if not validate_domain(fake_domain):
            print("[!]Invalid Domain format.")
            return

        phishing_key = input("\n[+]Add phishing keyword? (y/n): ").lower()
        keyword = ""
        if phishing_key == 'y':
            keyword = input("\n[+]Keyword (e.g., login, free): ").strip().lower()
            if not validate_phishing_keyword(keyword):
                print("[!]Invalid Keyword.")
                return


        final_url = combiner(masked_base, fake_domain, keyword)

        print(f"\n[+]Masked URL=> {final_url}\n")

    except KeyboardInterrupt:
        print("[!]Exit")
        sys.exit()

if __name__ == "__main__":

    os.system('cls' if os.name == 'nt' else 'clear')

    home_logo()
    home_about()

    if len(sys.argv) > 1 and sys.argv[1] == "about":
        sys.exit()

    urlmask()

