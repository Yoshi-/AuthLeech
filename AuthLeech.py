#This leeches auth codes from pastebin
#Uses some basic regex and other shit. Code checking is disabled (for now)
#Written by Contra
#Check Recoders.org for updates and more

from urlparse import urlparse
from xgoogle.search import GoogleSearch, SearchError
from datetime import date
import time
import urllib2
import time
import csv
import re


codewriter = csv.writer(open('all_codes.csv', 'w'), delimiter=',');
validwriter = csv.writer(open('valid_codes.csv', 'w'), delimiter=',');

scriptnames = csv.reader(open('scriptnames.csv', 'r'), delimiter=',');
auth = {};
for row in scriptnames:
    auth[row[0]] = row[1];

def check_code(code):
    request = urllib2.urlopen('https://impsoft.net/nexus/onstart.php?prodauth=%s&hash=9001'%code);
    html = request.read();
    splitsy = html.split("##");
    #print splitsy[4];
    if("1" in splitsy[4]):
        return True
    else:
        return False

def mk_nice_domain(domain):
    domain = re.sub("^www(\d+)?\.", "", domain)
    return domain

def form_query(script):
    query = 'site:pastebin.com "%s" %s' %(script, date);
    return query;

def get_results(query):
    gs = GoogleSearch(query);
    gs.results_per_page = 9001;
    results = gs.get_results();
    ret = [];
    for idx, res in enumerate(results):
        domain = mk_nice_domain(res.url);
        domain = domain.replace("pastebin.com/", "pastebin.com/raw.php?i=");
        print 'Found codes at %s' % domain;
        ret.append(domain);
    return ret;

def get_name(auth_code):
    auth_code = auth_code.lower().split("xz")[0];
    name = auth.get(auth_code, 'SCRIPTNAME');
    return name;

def grab_codes(results):
    codes = [];
    for url in results:
        total = 0;
        print 'Scanning %s' % url;
        request = urllib2.urlopen(url);
        html = request.read();
        for rest in re.findall('[0-9][0-9]?[0-9][xX][zZ][A-Z0-9]{13}', html):
            codes.append(rest);
            total = total + 1;
            print 'Found code %s' % rest;
        print 'Found %s codes in scan' % total;
    return codes;

def save_codes(allcodes, validcodes):
    for code in allcodes:
        codewriter.writerow([get_name(code), code]);
    for code in validcodes:
        validwriter.writerow([get_name(code), code]);
    return;
        
print 'Beginning AuthLeech v0.2 by Contra';
print 'Visit Recoders.org for Updates and more';

date = raw_input('Date: ')

roots = ['perfecticus', 'autocookerpro', 'autofighterpro', 'autogdkpro', 'autosoulwarspro', 'autogdkpro', 'autoagilitypro'];

urls = [];
for i in roots:
    main_query = form_query(i);
    temp = get_results(main_query);
    for d in temp:
        urls.append(d);
urls = list(set(urls)); #Remove duplicates    
allcodes = list(set(grab_codes(urls))); #Remove duplicates

#print 'Checking Codes...';
validcodes = [];
#for z in allcodes:
#    if check_code(z):
#        print 'Code %s is valid' % z;
#        validcodes.append(z);
#print 'Found %s valid codes!' % len(validcodes);

print 'Found %s codes total!' % len(allcodes);
print 'Saving files...';
save_codes(allcodes, validcodes);
print 'Operation completed.';

