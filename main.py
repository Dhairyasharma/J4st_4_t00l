import sys
import argparse
import requests
import re
from bs4 import BeautifulSoup


def banner():
    print(''' 
  @@@@@@  @@@  @@@ @@@  @@@@@@  @@@  @@@      @@@@@@@  @@@@@@@@ @@@@@@@@ @@@      @@@@@@@@ @@@@@@@ 
 @@!  @@@ @@!@!@@@ @@! @@!  @@@ @@!@!@@@      @@!  @@@ @@!      @@!      @@!      @@!      @@!  @@@
 @!@  !@! @!@@!!@! !!@ @!@  !@! @!@@!!@!      @!@@!@!  @!!!:!   @!!!:!   @!!      @!!!:!   @!@!!@! 
 !!:  !!! !!:  !!! !!: !!:  !!! !!:  !!!      !!:      !!:      !!:      !!:      !!:      !!: :!! 
  : :. :  ::    :  :    : :. :  ::    :        :       : :: ::: : :: ::: : ::.: : : :: :::  :   : :
                                                                                                    ''')



def make_request(url,domain):
    
    try:
        #will only do request if domain is in url 
        if f'{domain}' in url:

            response = requests.get(url)
            return response.text
        else:
            return None
    except:
        pass

def url_fetching(url,domain):
    qu=[]
    qu.append(url)
    output =[]
    while True:
        if qu:
            url = qu.pop()
             
            
            if url not in output:
                output.append(url)
                html_document = make_request(url,domain)
                if html_document:
                    soup = BeautifulSoup(html_document, 'html.parser')
                    for link in soup.find_all('a'):
                        
                        if link.get('href') in qu:
                            continue
                        else:
                            qu.append(link.get('href'))
            else:
                continue

        else:
            break
    return output




def check_fi(url):
    file_path = input('\033[92m Enter the wordlist path: \033[00m ')
    if 'Check' in url:
        r = requests.get(url)
        default_len = len(r.text)
        with open(f'{file_path}','rb') as f:
            try:
                while True:
                    param = f.readline().decode('utf-8').rsplit()
                    if param:
                        final_url = url.replace('Check',f'{param[0]}')
                        response = requests.get(final_url)
                        if len(response.text)!= default_len:
                            print(f"\033[91m {response.url}\033[00m")
                        else:
                            continue
                    else:
                        break
            except:
                print('Error')
                sys.exit()
    else:
        print('Check keyword is missing !!')

def get_info(user_name):
    url = f'https://github.com/{user_name}?tab=repositories&q=&type=source&language=&sort='
    
    headers = {'Host': 'github.com',
'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:75.0) Gecko/20100101 Firefox/75.0',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
'Accept-Language': 'en-US,en;q=0.5',
'Accept-Encoding': 'gzip, deflate, br',
'Connection': 'keep-alive'}

    
    try:
        response = requests.get(url,headers=headers)
        if response.text != 'Not Found':
            soup = BeautifulSoup(response.text,'html.parser')
            repo_list = []
            repo = soup.find_all('a')
     
            for link in repo:
                link = link.get("href")
                if link.startswith(f'/{user_name}/'):
                    link = link.split('/')
                    if len(link) == 3:

                        repo_list.append(link[2])
            des = []
            description = soup.find_all(itemprop="description")
            for i in description:
                des.append(i.text.strip())
     
            lang_used =[]
            lang = soup.find_all(itemprop="programmingLanguage")
            for i in lang:
                lang_used.append(i.text.strip())
            name = soup.find(itemprop="name").text.strip()
            if not name:
                name = 'X'
            location = soup.find(itemprop="homeLocation")
            if location:
                location = location.text.strip()
            else:
                location='X'
            twitter = soup.find(itemprop="twitter")
     
            if twitter:
                twitter = twitter.text.strip().split('@')[1]
            else:
                twitter = 'X'

            if name:
                print('*'*40)
                print('\033[92m Name: \033[00m ',name)
            if location:
                print('*'*40)
                print('\033[92m Location: \033[00m ',location)
            if twitter:
                print('*'*40)
                print('\033[92m twitter: \033[00m ',twitter)
            for i in range(len(repo)):
                print('-'*80)
                print(f'\033[92m Repo-name \033[00m -- \033[91m {repo_list[i]} \033[00m \033[92m Description \033[00m -- \033[91m {des[i]} \033[00m \033[92m Langugage used \033[00m --\033[91m {lang_used[i]} \033[00m')

        else:
            print('No profile with given username Found!')
    except:
        pass


if __name__ == '__main__':

    banner()
    while True:

        print('''
        1. Fetch Urls recursively in given domain.
        2. Check for LFI & RFI in given Url.
        3. Git Info
        4. exit
        ''')
        options = input('Select the option: ')


        if options == '1':

            url = input('Please provide url: ')
            domain = url.split('/')[2]
            afurl = url_fetching(url,domain)
            for i in afurl:
                print(f"\033[92m {i}\033[00m")
        
        elif options == '2':
            url = input('\033[92m Please provide url with "Check" to check file inclusion: \033[00m')
            check_fi(url)
    
        elif options == '3':
            user_name = input('Please enter the github username: ')
            get_info(user_name)
    
        elif options == '4':
            exit()
        else:
            print('Please enter a valid no!')
            continue
