import time
import random
import winreg

RESOURCE = {
    'US': 'https://www.amazon.com',
    'AE': 'https://www.amazon.ae',
    'CN': 'https://www.amazon.cn',
    'JP': 'https://www.amazon.co.jp',
    'UK': 'https://www.amazon.co.uk',
    'FR': 'https://www.amazon.fr',
    'DE': 'https://www.amazon.de',
    'ES': 'https://www.amazon.es',
    'IT': 'https://www.amazon.it',
    'CA': 'https://www.amazon.ca',
    'IN': 'https://www.amazon.in',
    'AU': 'https://www.amazon.com.au',
    'GB': 'https://www.amazon.co.uk',
    'MX': 'https://www.amazon.com.mx'
    # 'SG': 'https://www.amazon.com.sg'
}

LANG_CODE = {
    'CN': 'zh_CN',
    'US': 'en_US'
}

FR_MONTH = {
    "janvier": "January",
    "février": "February",
    "mars": "March",
    "avril": "April",
    "mai": "May",
    "juin": "June",
    "juillet": "July",
    "août": "August",
    "septembre": "September",
    "octobre": "October",
    "novembre": "November",
    "décembre": "December"
}

MX_MONTH = ES_MONTH = {
    "enero": "January",
    "febrero": "February",
    "marzo": "March",
    "abril": "April",
    "mayo": "May",
    "junio": "June",
    "julio": "July",
    "agosto": "August",
    "septiembre": "September",
    "octubre": "October",
    "noviembre": "November",
    "diciembre": "December"
}

IT_MONTH = {
    "gennaio": "January",
    "febbraio": "February",
    "marzo": "March",
    "aprile": "April",
    "maggio": "May",
    "giugno": "June",
    "luglio": "July",
    "agosto": "August",
    "settembre": "September",
    "ottobre": "October",
    "novembre": "November",
    "dicembre": "December"
}

DE_MONTH = {
    "Januar": "January",
    "Februar": "February",
    "März": "March",
    "April": "April",
    "Mai": "May",
    "Juni": "June",
    "Juli": "July",
    "August": "August",
    "September": "September",
    "Oktober": "October",
    "November": "November",
    "Dezember": "December"
}

TIME_CODE = {
    'US': {'format': '%B%d,%Y', 'replace': 'Reviewed in the United States on'},
    'AE': '%B%d,%Y',
    'CN': '%Y年%m月%d日',
    'JP': {'format': '%Y年%m月%d日', 'replace': 'に日本でレビュー済み'},
    'UK': {'format': '%d%B%Y', 'replace': 'Reviewed in the United Kingdom on'},
    'FR': {'MapMonth': FR_MONTH, 'format': '%d%B%Y', 'replace': 'Commenté en France le'},
    'DE': {'MapMonth': DE_MONTH, 'format': '%d.%B%Y', 'replace': 'Rezension aus Deutschland vom'},
    'ES': {'MapMonth': ES_MONTH, 'format': '%d%B%Y', 'replace': ['Revisado en España el', 'de']},
    'IT': {'MapMonth': IT_MONTH, 'format': '%d%B%Y', 'replace': 'Recensito in Italia il'},
    'CA': {'format': '%B%d,%Y', 'replace': 'Reviewed in Canada on'},
    'IN': {'format': '%d%B%Y', 'replace': 'Reviewed in India on'},
    'AU': {'format': '%d%B%Y', 'replace': 'Reviewed in Australia on'},
    'GB': {'format': '%d%B%Y', 'replace': 'Reviewed in the United Kingdom on'},
    'MX': {'MapMonth': MX_MONTH, 'format': '%d%B%Y', 'replace': ['Revisado en México el', 'de']}
    # 'SG': 'https://www.amazon.com.sg'
}

STANDARD_TIME = '%d-%b-%y'


def getAmazonDomain(country):
    return RESOURCE[country.upper()]


def getDesktopPath():
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
    return winreg.QueryValueEx(key, "Desktop")[0]


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
    return False


amazon_headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;'
              'q=0.8,application/signed-exchange;v=b3',
    # 'Host': getAmazonDomain(self.Country),
    'referer': '',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'upgrade-insecure-requests': '1',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'Connection': 'keep-alive'
}


def is_robot(selector):
    robot = selector.xpath('//form[@action="/errors/validateCaptcha"]')
    return True if robot else False


def wait():
    random_time = random.randint(1, 3)
    print('等待时间 %s' % random_time)
    time.sleep(random_time)


def request_message(response, mode):
    print(response.status_code)
    if response.status_code != 200:
        return None
    if mode == 'json':
        return response.json()
    elif mode == 'txt':
        return response.text
