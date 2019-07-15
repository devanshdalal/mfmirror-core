import numpy as np
import pandas as pd
import os
from util import mfconfig as cfg
import json
import sys
from util import utils

############################# Helper ######################################

def PrintArgs(csvs, columns = ['instrument', 'weight']):
    print(pd.DataFrame(csvs.items(), columns=columns), file=sys.stderr)

##########################################################################

def WeightedAverage(csvs,
                    columns = ['Stock Invested in', '% of Total Holdings'],
                    to_json = False):
    PrintArgs(csvs)
    print(csvs)

    funds = []
    weights = []
    for file in csvs:
        file_path = utils.GetFileByName(file.split('/')[-1])
        funds.append(pd.read_csv(file_path))
        weights.append(float(csvs[file]))

    combined = {}
    for i, fund in enumerate(funds):
        for org_details in fund.iterrows():
            org_details = org_details[1]
            company = org_details[columns[0]]
            # print org_details[columns[1]], weights[i]
            if company not in combined:
                combined[company] = 0.0
            combined[company] += float(org_details[columns[1]]) * weights[i]

    combined = pd.DataFrame(combined.items(), columns = [columns[0], columns[1]])
    combined = combined.sort_values(by=[columns[1]], ascending=False)
    if to_json:
        return combined.to_json(orient = 'records')
    else: 
        return combined

# WeightedAverage(cfg.VRO, columns=['Company', '% Assets'])
# WeightedAverage(cfg.MC)
def main():
    args = utils.ParseCmd(sys.argv)
    if args.source is not None:
        #############################################################################
        # Moneycontrol specific analysis.
        #############################################################################
        if utils.MC in args.source:
            print(WeightedAverage(cfg.MC))      
        #############################################################################
        # Value research online specific analysis.
        #############################################################################
        if utils.VRO in args.source:
            print(WeightedAverage(cfg.VRO, columns=['Company', '% Assets']))
    elif args.config is not None:
        config = json.loads(args.config)
        print(WeightedAverage(config, to_json = args.to_json))


if __name__ == "__main__":
    # stuff only to run when not called via 'import' here
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
        main()

