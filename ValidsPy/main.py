import requests
from requests import Timeout
from multiprocessing import JoinableQueue as Queue
import threading
import os
from threading import Thread
import random
import ctypes
import time
from time import sleep
import socks
import webbrowser
import time
from os import path


from static.menu import threads, timeout, proxy_type, logs, colors, main_menu, work_input
from static.proxies import requests_proxy, load_proxy, scrape_proxies
from static.wordlists import load_wordlist, vail_wordlists


class results:
    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
    
    def valid(self):
        results_path = f"./Results/{work}/{results.timestamp}"
        file_name = "Valid.txt"
        if not os.path.exists(results_path):
            os.makedirs(results_path)
        file_path = path.join(results_path,file_name)
        with open(file_path,"a+",errors="ingore") as f:
            f.write(self + "\n")

    def invalid(self):
        results_path = f"./Results/{work}/{results.timestamp}"
        file_name = "Invalid.txt"
        if not os.path.exists(results_path):
            os.makedirs(results_path)
        file_path = path.join(results_path,file_name)
        with open(file_path,"a+",errors="ingore") as f:
            f.write(self + "\n")

class status:
    valid = 0
    invalid = 0
    errors = 0
    wordlist = 0
    loaded_wordlist = 0

class cpm:
    def __init__(self,start_timestamp):
        self.start_timestamp = start_timestamp
    
    def cpm(self):
        cpm = 0.0
        seconds = int(time.time()) - self.start_timestamp
        try:
            cpm = status.wordlist / seconds * 60
        except:
            pass
        return cpm
global cpm_counter
cpm_counter = cpm(int(time.time()))


def print_logs(arg):
    lock = threading.Lock()
    lock.acquire()
    print(arg)
    lock.release()


def check_version():
    try:
        getversion = requests.get("https://raw.githubusercontent.com/Stainpy/ValidsPy/main/version.json")
        data = getversion.json()
        current_version = data['version']
        url = data['link']
        if version != current_version:
            main_menu()
            while 1:
                inp = input(colors.yellow + f" New update available!\n Your current version is {version}, latest version is {current_version}\n [1]: Download now\n [2]: Skip\n > ")
                if inp.isdigit():
                    inp = int(inp)
                    if inp == 1:
                        link = webbrowser.open(url)
                        time.sleep(1)
                        os.system('cls')
                        return link
                    elif inp == 2:
                        time.sleep(1)
                        os.system('cls')
                        break
                    else:
                        print(colors.red + " Error!! Please choose one of available modes.")
                        pass
                else:
                    print(colors.red + " Error!! Please enter a digit.")
    except Exception as e:
        main_menu()
        print(colors.red + " Something went wrong while checking for updates!")
        # os.system('pause>nul')
        time.sleep(3)
        os.system('cls')


def updateTitle():
    meow = int(cpm_counter.cpm())
    ctypes.windll.kernel32.SetConsoleTitleW(f"{work} Valid Email | [Status] {status.wordlist}/{status.loaded_wordlist} [Errors] {status.errors} [CPM] {meow} | [Valid] {status.valid} [Invalid] {status.invalid}")
    pass


def Origin(q,proxies,log,proxy_type):
    while True:
        goodAttempt = False
        item = q.get()

        if (item==None):
            return False
        
        while not (goodAttempt):
            username = item[0]
            try:
                password = item[1]
            except:
                password = ""

            def login_function(username,password,proxy,proxy_type):
                sess = requests.session()

                url = ""
                agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36"
                headers = {"Content-Type":"application/json", "User-Agent":agent, "Pragma":"no-cache", "Accept":"*/*"}

                if proxy != None:
                    proxy = requests_proxy(proxy, proxy_type)

                rsp = ""

                try:
                    rsp = sess.get(url, headers=headers, proxies=proxy, timeout=timeout)
                except requests.ConnectionError:
                    status.errors += 1
                    return False
                except requests.Timeout:
                    status.errors += 1
                    return False
                except:
                    status.errors += 1
                    return False

                try:
                    data = rsp.json()
                except:
                    return False

                try:
                    if data['message'] == "register_email_not_existed":
                        if log == 1:
                            print_logs(colors.red + f" [Invalid] {username}")
                            if len(item) == 2:
                                results.invalid(f"{username}:{password}")
                            elif len(item) == 1:
                                results.invalid(f"{username}")
                            status.invalid += 1
                            if status.invalid == 1 and results.timestamp == None:
                                results.timestamp 
                        return True

                    elif data['message'] == "register_email_existed":
                        print_logs(colors.green + f" [Valid] {username}")
                        if len(item) == 2:
                            results.valid(f"{username}:{password}")
                        elif len(item) == 1:
                            results.valid(f"{username}")
                        status.valid += 1
                        if status.valid == 1 and results.timestamp == None:
                            results.timestamp                    
                        updateTitle()                    
                        return True

                    else:
                        pass
                except:
                    if log == 1:
                        print_logs(colors.normal + f" [Error] {username}")

            proxy = None
            if proxies:
                proxy = random.choice(proxies)
            goodAttempt = login_function(username,password,proxy,proxy_type)
            if goodAttempt == False:
                if log == 1:
                    print_logs(colors.normal + f" [Error] {username}")
                    updateTitle()

        else:
            status.wordlist +=1
            updateTitle()
            q.task_done()

def SoundCloud(q,proxies,log,proxy_type):
    while True:
        goodAttempt = False
        item = q.get()

        if (item==None):
            return False
        
        while not (goodAttempt):
            username = item[0]
            try:
                password = item[1]
            except:
                password = ""

            def login_function(username,password,proxy,proxy_type):
                sess = requests.session()

                url = ""
                agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36"
                headers = {"Content-Type":"application/json", "User-Agent":agent, "Pragma":"no-cache", "Accept":"*/*"}

                if proxy != None:
                    proxy = requests_proxy(proxy, proxy_type)

                rsp = ""

                try:
                    rsp = sess.get(url, headers=headers, proxies=proxy, timeout=timeout)
                except requests.ConnectionError:
                    status.errors += 1
                    return False
                except requests.Timeout:
                    status.errors += 1
                    return False
                except:
                    status.errors += 1
                    return False

                try:
                    data = rsp.json()
                except:
                    return False

                try:
                    if data['status'] == "available":
                        if log == 1:
                            print_logs(colors.red + f" [Invalid] {username}")
                            if len(item) == 2:
                                results.invalid(f"{username}:{password}")
                            elif len(item) == 1:
                                results.invalid(f"{username}")
                            status.invalid += 1
                            if status.invalid == 1 and results.timestamp == None:
                                results.timestamp 
                        return True

                    elif data['status'] == "in_use":
                        print_logs(colors.green + f" [Valid] {username}")
                        if len(item) == 2:
                            results.valid(f"{username}:{password}")
                        elif len(item) == 1:
                            results.valid(f"{username}")
                        status.valid += 1
                        if status.valid == 1 and results.timestamp == None:
                            results.timestamp                    
                        updateTitle()                    
                        return True

                    else:
                        pass
                except:
                    if log == 1:
                        print_logs(colors.normal + f" [Error] {username}")

            proxy = None
            if proxies:
                proxy = random.choice(proxies)
            goodAttempt = login_function(username,password,proxy,proxy_type)
            if goodAttempt == False:
                if log == 1:
                    print_logs(colors.normal + f" [Error] {username}")
                    updateTitle()

        else:
            status.wordlist +=1
            updateTitle()
            q.task_done()

def Activision(q,proxies,log,proxy_type):
    while True:
        goodAttempt = False
        item = q.get()

        if (item==None):
            return False
        
        while not (goodAttempt):
            username = item[0]
            try:
                password = item[1]
            except:
                password = ""

            def login_function(username,password,proxy,proxy_type):
                sess = requests.session()

                url = ""
                data = ""
                agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36"
                headers = {"User-Agent":agent, "Pragma":"no-cache", "Accept":"*/*", "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}

                if proxy != None:
                    proxy = requests_proxy(proxy, proxy_type)

                rsp = ""

                try:
                    rsp = sess.post(url, data=data, headers=headers, proxies=proxy, timeout=timeout)
                except requests.ConnectionError:
                    status.errors += 1
                    return False
                except requests.Timeout:
                    status.errors += 1
                    return False
                except:
                    status.errors += 1
                    return False

                try:
                    data = rsp.json()
                except:
                    return False

                try:
                    if data['status'] == "valid":
                        if log == 1:
                            print_logs(colors.red + f" [Invalid] {username}")
                            if len(item) == 2:
                                results.invalid(f"{username}:{password}")
                            elif len(item) == 1:
                                results.invalid(f"{username}")
                            status.invalid += 1
                            if status.invalid == 1 and results.timestamp == None:
                                results.timestamp 
                        return True

                    elif data['status'] == "invalid":
                        print_logs(colors.green + f" [Valid] {username}")
                        if len(item) == 2:
                            results.valid(f"{username}:{password}")
                        elif len(item) == 1:
                            results.valid(f"{username}")
                        status.valid += 1
                        if status.valid == 1 and results.timestamp == None:
                            results.timestamp                    
                        updateTitle()                    
                        return True

                    else:
                        pass
                except:
                    if log == 1:
                        print_logs(colors.normal + f" [Error] {username}")

            proxy = None
            if proxies:
                proxy = random.choice(proxies)
            goodAttempt = login_function(username,password,proxy,proxy_type)
            if goodAttempt == False:
                if log == 1:
                    print_logs(colors.normal + f" [Error] {username}")
                    updateTitle()

        else:
            status.wordlist +=1
            updateTitle()
            q.task_done()

def Discord(q,proxies,log,proxy_type):
    while True:
        goodAttempt = False
        item = q.get()

        if (item==None):
            return False
        
        while not (goodAttempt):
            username = item[0]
            try:
                password = item[1]
            except:
                password = ""

            def login_function(username,password,proxy,proxy_type):
                sess = requests.session()

                url = ""
                data = ""
                agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36"
                headers = {"User-Agent":agent, "Pragma":"no-cache", "Accept":"*/*", "Content-Type": "application/json"}

                if proxy != None:
                    proxy = requests_proxy(proxy, proxy_type)

                rsp = ""

                try:
                    rsp = sess.post(url, json=data, headers=headers, proxies=proxy, timeout=timeout)
                except requests.ConnectionError:
                    status.errors += 1
                    return False
                except requests.Timeout:
                    status.errors += 1
                    return False
                except:
                    status.errors += 1
                    return False

                if "captcha_key" in rsp.text:
                    if log == 1:
                        print_logs(colors.red + f" [Invalid] {username}")
                        if len(item) == 2:
                            results.invalid(f"{username}:{password}")
                        elif len(item) == 1:
                            results.invalid(f"{username}")
                        status.invalid += 1
                        if status.invalid == 1 and results.timestamp == None:
                            results.timestamp 
                    return True

                elif "EMAIL_ALREADY_REGISTERED" in rsp.text:
                    print_logs(colors.green + f" [Valid] {username}")
                    if len(item) == 2:
                        results.valid(f"{username}:{password}")
                    elif len(item) == 1:
                        results.valid(f"{username}")
                    status.valid += 1
                    if status.valid == 1 and results.timestamp == None:
                        results.timestamp                    
                    updateTitle()                    
                    return True

                else:
                    pass

            proxy = None
            if proxies:
                proxy = random.choice(proxies)
            goodAttempt = login_function(username,password,proxy,proxy_type)
            if goodAttempt == False:
                if log == 1:
                    print_logs(colors.normal + f" [Error] {username}")
                    updateTitle()

        else:
            status.wordlist +=1
            updateTitle()
            q.task_done()

def Instagram(q,proxies,log,proxy_type):
    while True:
        goodAttempt = False
        item = q.get()

        if (item==None):
            return False
        
        while not (goodAttempt):
            username = item[0]
            try:
                password = item[1]
            except:
                password = ""

            def login_function(username,password,proxy,proxy_type):
                sess = requests.session()

                url = ""
                data = ""
                agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36"
                headers = {"User-Agent":agent, "Pragma":"no-cache", "Accept":"*/*", "Content-Type": "application/x-www-form-urlencoded"}

                if proxy != None:
                    proxy = requests_proxy(proxy, proxy_type)

                rsp = ""

                try:
                    rsp = sess.post(url, data=data, headers=headers, proxies=proxy, timeout=timeout)
                except requests.ConnectionError:
                    status.errors += 1
                    return False
                except requests.Timeout:
                    status.errors += 1
                    return False
                except:
                    status.errors += 1
                    return False

                try:
                    data = rsp.json()
                except:
                    return False

                try:
                    if data['errors']['email'][0]['message']:
                        print_logs(colors.green + f" [Valid] {username}")
                        if len(item) == 2:
                            results.valid(f"{username}:{password}")
                        elif len(item) == 1:
                            results.valid(f"{username}")
                        status.valid += 1
                        if status.valid == 1 and results.timestamp == None:
                            results.timestamp                    
                        updateTitle()                    
                        return True

                except:
                    if log == 1:
                        print_logs(colors.red + f" [Invalid] {username}")
                        if len(item) == 2:
                            results.invalid(f"{username}:{password}")
                        elif len(item) == 1:
                            results.invalid(f"{username}")
                        status.invalid += 1
                        if status.invalid == 1 and results.timestamp == None:
                            results.timestamp 
                    return True

            proxy = None
            if proxies:
                proxy = random.choice(proxies)
            goodAttempt = login_function(username,password,proxy,proxy_type)
            if goodAttempt == False:
                if log == 1:
                    print_logs(colors.normal + f" [Error] {username}")
                    updateTitle()

        else:
            status.wordlist +=1
            updateTitle()
            q.task_done()

def Viu(q,proxies,log,proxy_type):
    while True:
        goodAttempt = False
        item = q.get()

        if (item==None):
            return False
        
        while not (goodAttempt):
            username = item[0]
            try:
                password = item[1]
            except:
                password = ""

            def login_function(username,password,proxy,proxy_type):
                sess = requests.session()

                url = ""
                agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36"
                headers = {"Content-Type":"application/json", "User-Agent":agent, "Accept":"*/*"}

                if proxy != None:
                    proxy = requests_proxy(proxy, proxy_type)

                rsp = ""

                try:
                    rsp = sess.get(url, headers=headers, proxies=proxy, timeout=timeout)
                except requests.ConnectionError:
                    status.errors += 1
                    return False
                except requests.Timeout:
                    status.errors += 1
                    return False
                except:
                    status.errors += 1
                    return False

                try:
                    data = rsp.json()
                except:
                    return False

                try:
                    if data['exists'] == False:
                        if log == 1:
                            print_logs(colors.red + f" [Invalid] {username}")
                            if len(item) == 2:
                                results.invalid(f"{username}:{password}")
                            elif len(item) == 1:
                                results.invalid(f"{username}")
                            status.invalid += 1
                            if status.invalid == 1 and results.timestamp == None:
                                results.timestamp 
                        return True

                    elif data['exists'] == True:
                        print_logs(colors.green + f" [Valid] {username}")
                        if len(item) == 2:
                            results.valid(f"{username}:{password}")
                        elif len(item) == 1:
                            results.valid(f"{username}")
                        status.valid += 1
                        if status.valid == 1 and results.timestamp == None:
                            results.timestamp                    
                        updateTitle()                    
                        return True

                    else:
                        pass
                except:
                    print_logs(colors.normal + f" [Error] {username}")

            proxy = None
            if proxies:
                proxy = random.choice(proxies)
            goodAttempt = login_function(username,password,proxy,proxy_type)
            if goodAttempt == False:
                if log == 1:
                    print_logs(colors.normal + f" [Error] {username}")
                    updateTitle()

        else:
            status.wordlist +=1
            updateTitle()
            q.task_done()

def Spotify(q,proxies,log,proxy_type):
    while True:
        goodAttempt = False
        item = q.get()

        if (item==None):
            return False
        
        while not (goodAttempt):
            username = item[0]
            try:
                password = item[1]
            except:
                password = ""

            def login_function(username,password,proxy,proxy_type):
                sess = requests.session()

                url = ""
                agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36"
                headers = {"Content-Type":"application/json", "User-Agent":agent, "Pragma":"no-cache", "Accept":"*/*"}

                if proxy != None:
                    proxy = requests_proxy(proxy, proxy_type)

                rsp = ""

                try:
                    rsp = sess.get(url, headers=headers, proxies=proxy, timeout=timeout)
                except requests.ConnectionError:
                    status.errors += 1
                    return False
                except requests.Timeout:
                    status.errors += 1
                    return False
                except:
                    status.errors += 1
                    return False

                try:
                    data = rsp.json()
                except:
                    return False

                try:
                    if data['status'] == 1:
                        if log == 1:
                            print_logs(colors.red + f" [Invalid] {username}")
                            if len(item) == 2:
                                results.invalid(f"{username}:{password}")
                            elif len(item) == 1:
                                results.invalid(f"{username}")
                            status.invalid += 1
                            if status.invalid == 1 and results.timestamp == None:
                                results.timestamp 
                        return True

                    elif data['status'] == 20:
                        print_logs(colors.green + f" [Valid] {username}")
                        if len(item) == 2:
                            results.valid(f"{username}:{password}")
                        elif len(item) == 1:
                            results.valid(f"{username}")
                        status.valid += 1
                        if status.valid == 1 and results.timestamp == None:
                            results.timestamp                    
                        updateTitle()                    
                        return True

                    else:
                        pass
                except:
                    print_logs(colors.normal + f" [Error] {username}")

            proxy = None
            if proxies:
                proxy = random.choice(proxies)
            goodAttempt = login_function(username,password,proxy,proxy_type)
            if goodAttempt == False:
                if log == 1:
                    print_logs(colors.normal + f" [Error] {username}")
                    updateTitle()

        else:
            status.wordlist +=1
            updateTitle()
            q.task_done()

def Uplay(q,proxies,log,proxy_type):
    while True:
        goodAttempt = False
        item = q.get()

        if (item==None):
            return False
        
        while not (goodAttempt):
            username = item[0]
            try:
                password = item[1]
            except:
                password = ""

            def login_function(username,password,proxy,proxy_type):
                sess = requests.session()

                url = ""
                data = ""
                agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36"
                headers = {"Content-Type":"application/json", "User-Agent":agent, "Pragma":"no-cache", "Accept":"*/*"}

                if proxy != None:
                    proxy = requests_proxy(proxy, proxy_type)

                rsp = ""

                try:
                    rsp = sess.post(url, json=data, headers=headers, proxies=proxy, timeout=timeout)
                except requests.ConnectionError:
                    status.errors += 1
                    return False
                except requests.Timeout:
                    status.errors += 1
                    return False
                except:
                    status.errors += 1
                    return False

                try:
                    data = rsp.json()
                except:
                    return False

                try:
                    if data['validationReports'][2]['Message'] == "Email address already registered":
                        print_logs(colors.green + f" [Valid] {username}")
                        if len(item) == 2:
                            results.valid(f"{username}:{password}")
                        elif len(item) == 1:
                            results.valid(f"{username}")
                        status.valid += 1
                        if status.valid == 1 and results.timestamp == None:
                            results.timestamp                    
                        updateTitle()                    
                        return True

                except:
                    if log == 1:
                        print_logs(colors.red + f" [Invalid] {username}")
                        if len(item) == 2:
                            results.invalid(f"{username}:{password}")
                        elif len(item) == 1:
                            results.invalid(f"{username}")
                        status.invalid += 1
                        if status.invalid == 1 and results.timestamp == None:
                            results.timestamp 
                    return True

            proxy = None
            if proxies:
                proxy = random.choice(proxies)
            goodAttempt = login_function(username,password,proxy,proxy_type)
            if goodAttempt == False:
                if log == 1:
                    print_logs(colors.normal + f" [Error] {username}")
                    updateTitle()

        else:
            status.wordlist +=1
            updateTitle()
            q.task_done()

def Godaddy(q,proxies,log,proxy_type):
    while True:
        goodAttempt = False
        item = q.get()

        if (item==None):
            return False
        
        while not (goodAttempt):
            username = item[0]
            try:
                password = item[1]
            except:
                password = ""

            def login_function(username,password,proxy,proxy_type):
                sess = requests.session()

                url = ""
                data = ""
                agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36"
                headers = {"Content-Type":"application/json", "User-Agent":agent, "Pragma":"no-cache", "Accept":"application/json"}

                if proxy != None:
                    proxy = requests_proxy(proxy, proxy_type)

                rsp = ""

                try:
                    rsp = sess.post(url, json=data, headers=headers, proxies=proxy, timeout=timeout)
                except requests.ConnectionError:
                    status.errors += 1
                    return False
                except requests.Timeout:
                    status.errors += 1
                    return False
                except:
                    status.errors += 1
                    return False

                try:
                    data = rsp.json()
                except:
                    return False

                if data['message'] == 'username is available':
                    if log == 1:
                        print_logs(colors.red + f" [Invalid] {username}")
                        if len(item) == 2:
                            results.invalid(f"{username}:{password}")
                        elif len(item) == 1:
                            results.invalid(f"{username}")
                        status.invalid += 1
                        if status.invalid == 1 and results.timestamp == None:
                            results.timestamp 
                    return True

                elif data['message'] == 'username is unavailable':
                    print_logs(colors.green + f" [Valid] {username}")
                    if len(item) == 2:
                        results.valid(f"{username}:{password}")
                    elif len(item) == 1:
                        results.valid(f"{username}")
                    status.valid += 1
                    if status.valid == 1 and results.timestamp == None:
                        results.timestamp                    
                    updateTitle()                    
                    return True

                else:
                    pass

            proxy = None
            if proxies:
                proxy = random.choice(proxies)
            goodAttempt = login_function(username,password,proxy,proxy_type)
            if goodAttempt == False:
                if log == 1:
                    print_logs(colors.normal + f" [Error] {username}")
                    updateTitle()

        else:
            status.wordlist +=1
            updateTitle()
            q.task_done()



if __name__ == "__main__":
    version = 1.0
    os.system(f"title AIO Vaild Email Checker v{version} - By StaiN#9677")
    check_version()
    main_menu()

    open("proxies.txt", "a").close()
    open("wordlists.txt", "a").close()

    work_input()
    while True:
            work_input = input( " > ")
            if work_input.isdigit():
                work_input = int(work_input)
                if work_input == 1:
                    work = "Origin"
                    break
                elif work_input == 2:
                    work = "SoundCloud"
                    break
                elif work_input == 3:
                    work = "Activision"
                    break
                elif work_input == 4:
                    work = "Discord"
                    break
                elif work_input == 5:
                    work = "Instagram"
                    break
                elif work_input == 6:
                    work = "Viu"
                    break
                elif work_input == 7:
                    work = "Spotify"
                    break
                elif work_input == 8:
                    work = "Uplay"
                    break
                elif work_input == 9:
                    work = "Godaddy"
                    break
                else:
                    print(colors.red + " Error!! Please choose one of available modes.")
            else:
                print(colors.red + " Error!! Please enter a digit.")


    while True:
            if work_input in [4, 8]:
                mode = (input(colors.normal + " [1] Load Proxies\n [2] Proxy Scraper\n > "))
            else:
                mode = (input(colors.normal + " [1] Load Proxies\n [2] Proxy Scraper\n [3] Proxyless\n > "))
            if mode.isdigit():
                mode = int(mode)
                if mode == 1:
                    proxy_type = proxy_type()
                    proxies = load_proxy(proxy_type)
                    break
                elif mode == 2:
                    proxy_type = proxy_type()
                    proxies = scrape_proxies(proxy_type)
                    break
                elif mode == 3:
                    proxy_type = 'proxyless'
                    proxies = load_proxy(proxy_type)
                    break
                else:
                    print(colors.red + " Error!! Please choose one of available modes.")
            else:
                print(colors.red + " Error!! Please enter a digit.")

    threads_input = threads()
    timeout = timeout()
    log = logs()

    worldist_array = load_wordlist()
    status.loaded_wordlist = len(worldist_array)
    q = vail_wordlists(worldist_array)
    time.sleep(1)

    os.system('cls')

    if work == "Origin":
        for i in range(threads_input):
            worker = Thread(target=Origin, args=(q, proxies, log, proxy_type))
            worker.setDaemon(True)
            worker.start()

    elif work == "SoundCloud":
        for i in range(threads_input):
            worker = Thread(target=SoundCloud, args=(q, proxies, log, proxy_type))
            worker.setDaemon(True)
            worker.start()

    elif work == "Activision":
        for i in range(threads_input):
            worker = Thread(target=Activision, args=(q, proxies, log, proxy_type))
            worker.setDaemon(True)
            worker.start()

    elif work == "Discord":
        for i in range(threads_input):
            worker = Thread(target=Discord, args=(q, proxies, log, proxy_type))
            worker.setDaemon(True)
            worker.start()

    elif work == "Instagram":
        for i in range(threads_input):
            worker = Thread(target=Instagram, args=(q, proxies, log, proxy_type))
            worker.setDaemon(True)
            worker.start()

    elif work == "Viu":
        for i in range(threads_input):
            worker = Thread(target=Viu, args=(q, proxies, log, proxy_type))
            worker.setDaemon(True)
            worker.start()

    elif work == "Spotify":
        for i in range(threads_input):
            worker = Thread(target=Spotify, args=(q, proxies, log, proxy_type))
            worker.setDaemon(True)
            worker.start()

    elif work == "Uplay":
        for i in range(threads_input):
            worker = Thread(target=Uplay, args=(q, proxies, log, proxy_type))
            worker.setDaemon(True)
            worker.start()

    elif work == "Godaddy":
        for i in range(threads_input):
            worker = Thread(target=Godaddy, args=(q, proxies, log, proxy_type))
            worker.setDaemon(True)
            worker.start()

    q.join()



os.system('pause>nul')
