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
    CYAN = "\033[96m\033[1m"
    logo = r"""
M   M   A    SSSS K   K U   U RRRR  L     
MM MM  A A  S     K  K  U   U R   R L     
M M M AAAAA  SSS  KKK   U   U RRRR  L     
M   M A   A     S K  K  U   U R  R  L     
M   M A   A SSSS  K   K  UUU  R   R LLLLL 
    """
    print_centered(logo, CYAN)

def home_about():
    CYAN = "\033[96m\033[1m"
    about_text = (
        "╔════════════════════════════════════════════════════════════╗\n"
        "║  MaskUrl v1.0.2 | Created by ScriptKiddie                  ║\n"
        "║  Licensed under MIT | Copyright (c) 2026                   ║\n"
        "║  Usage: For Educational & Authorized Testing Only          ║\n"
        "╚════════════════════════════════════════════════════════════╝"
    )
    print_centered(about_text, CYAN)

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
    
    print("\n\033[94m[1] TinyURL | [2] Da.gd | [3] Clck.ru\033[0m")
    
    try:
        choice = int(input("\nSelect Service> "))
        if choice not in services:
            print("\033[91m(!) Invalid Selection\033[0m")
            return "error"

        s = pyshorteners.Shortener()
        short_url = getattr(s, services[choice]).short(url)
        return short_url
    except Exception as e:
        print(f"\033[91m(!) Shortening Error: {e}\033[0m")
        return "error"

def combiner(masked_url, domain_name, phishing_keyword):
    prefix, suffix = masked_url.split("://")
    keyword = f"-{phishing_keyword}" if phishing_keyword else ""
    return f"{prefix}://{domain_name}{keyword}@{suffix}"



def urlmask():
    if not internet_connection():
        print("\033[91m(!) No Internet Connection\033[0m")
        return

    try:
        print("\n")
        raw_url = input("[?] Target URL (e.g., https://site.com): ").strip()
        target_url = validate_url(raw_url)
        
        if not target_url:
            print("\033[91m[!] Invalid URL format.\033[0m")
            return

        masked_base = shortener_service(target_url)
        if masked_base == "error": return


        fake_domain = input(" [?] Masking Domain (e.g., google.com): ").strip().lower()
        if not validate_domain(fake_domain):
            print("\033[91m[!] Invalid Domain format.\033[0m")
            return

        phishing_key = input("[?]Add phishing keyword? (y/n): ").lower()
        keyword = ""
        if phishing_key == 'y':
            keyword = input("[?]Keyword (e.g., login, free): ").strip().lower()
            if not validate_phishing_keyword(keyword):
                print("\033[91m[!]Invalid Keyword.\033[0m")
                return


        final_url = combiner(masked_base, fake_domain, keyword)
        
        print("\n" + "═"*50)
        print("\033[92mSUCCESSFULLY MASKED\033[0m")
        print(f"\033[97m\033[1m{final_url}\033[0m")
        print("═"*50 + "\n")

    except KeyboardInterrupt:
        print("\n\n [!]Exiting...\n")
        sys.exit()

if __name__ == "__main__":

    os.system('cls' if os.name == 'nt' else 'clear')

    home_logo()
    home_about()

    if len(sys.argv) > 1 and sys.argv[1] == "about":
        sys.exit()

    urlmask()

