import sys, os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import numpy as np
import pandas as pd
import requests
from lxml import html
import xml.etree.ElementTree as ET
import requests_cache

from util import scrapper_config as cfg
from util import utils

# Install the requests cache
requests_cache.install_cache('requests_cache', expire_after=600)

###########################################################################
### ValueResearch
###########################################################################

def ParseValueResearchOnline(name, code):
    url = cfg.base_url + code
    page = requests.get(url)
    tree = html.fromstring(page.content)
    l = tree.xpath('//table[@id="fund-snapshot-port-holdings"]//td//text()')
    l = utils.RemoveSpaces(l)
    fname = utils.GetFileByName(name)
    final = np.reshape(np.array(l), (-1, 6))
    pd.DataFrame(final).to_csv(fname, header=cfg.header)
    return fname

###########################################################################
### Moneycontrol
###########################################################################

def Transform(url):
    url = url.replace('/nav','')
    url = url.split('/')
    return '/'.join(url[:-1] + ['portfolio-holdings'] + [url[-1]])

def ExtractLinks(url):
    page = requests.get(url)
    tree = html.fromstring(page.content)
    links = tree.xpath('//table[@class="mctable1" and @id="dataTableId"]//a/@href')
    text = tree.xpath('//table[@class="mctable1" and @id="dataTableId"]//a/text()')
    crisil = tree.xpath('//td[@class="crisil_col"]//text()')
    # To get only the rated funds="and (x[2] in ['1', '2', '3', '4', '5']""
    out = list(filter(lambda x: 'direct' in x[0], zip(links, text, crisil)))
    out = map(lambda x: (Transform(x[0]),x[1],x[2]), out)
    return out

def ParseMoneyControl(url):
    print('url:', url)
    page = requests.get(url)
    tree = html.fromstring(page.content)
    rows = tree.xpath('//table[@id="equityCompleteHoldingTable"]//tr[not(@style)]')
    header = list(filter(lambda y: not y.isspace(), rows[0].xpath('./th//text()')))
    rows = list(map(lambda x: x.xpath('./td'), rows[1:]))
    for i,x in enumerate(rows):
        rows[i] = list(map(lambda y: ' '.join(utils.RemoveSpaces(y.xpath('.//text()'))), x))
        rows[i] = list(map(lambda y: y.replace('%', ''), rows[i]))  # strip % signs
    rows = utils.RemoveSpaces(rows)
    final = np.array([np.array(xi) for xi in rows])

    id = url.split('/')[-3]
    fname = utils.GetFileByName(id.replace(' ', '_') + '.csv')
    pd.DataFrame(final).to_csv(fname, encoding = 'utf-8', header=header)
    return fname

####################################################################################
def main():
    args = utils.ParseCmd(sys.argv)
    if args.clean:
        os.system('rm -rf data/*')
    if args.source is not None:
        if utils.MC in args.source:
            for f in cfg.MCFunds:
                print("Geting funds from ", f)
                links = ExtractLinks(f)
                for x in links:
                    print(ParseMoneyControl(x[0]))
        if utils.VRO in args.source:
            for fund in cfg.mutual_funds_codes:
                print("ParseValueResearchOnline, fund:", fund, "code:", cfg.mutual_funds_codes[fund])
                print("Writing:", ParseValueResearchOnline(fund, cfg.mutual_funds_codes[fund]))
                # break

if __name__ == "__main__":
   main()