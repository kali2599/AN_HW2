"""
You can write here the data elaboration function/s

You should read all the JSON files containing simulations results and compute
average and std of all the metrics of interest.

You can find the JSON file from the simulations into the data.evaluation_tests folder.
Each JSON file follows the naming convention: simulation-current date-simulation id__seed_drones number_routing algorithm

In this way you can parse the name and properly aggregate the data.

To aggregate data you can use also external libraries such as Pandas!

IMPORTANT: Both averages and stds must be computed over different seeds for the same metric!
"""

import numpy as np
import os
import json
from glob import glob
import pandas as pd
from pandas import DataFrame
import pickle

def compute_data_avg_std(path: str):
    """
    Computes averages and stds from JSON files
    @param path: results folder path
    @return: one or more data structure containing data
    """

    #cg = [0, 0, 0, 0, 0, 0]
    #cr = [0, 0, 0, 0, 0, 0]
    cq = [0, 0, 0, 0, 0, 0]
    #cn = [0, 0, 0, 0, 0, 0]

    #mrg = [0, 0, 0, 0, 0, 0]
    #mrr = [0, 0, 0, 0, 0, 0]
    mrq = [0, 0, 0, 0, 0, 0]
    #mrn = [0, 0, 0, 0, 0, 0]

    #mtg = [0, 0, 0, 0, 0, 0]
    #mtr = [0, 0, 0, 0, 0, 0]
    mtq = [0, 0, 0, 0, 0, 0]
    #mtn = [0, 0, 0, 0, 0, 0]

    #dsrg = [0, 0, 0, 0, 0, 0]
    #dsrr = [0, 0, 0, 0, 0, 0]
    dsrq = [0, 0, 0, 0, 0, 0]
    #dsrn = [0, 0, 0, 0, 0, 0]

    #dstg = [0, 0, 0, 0, 0, 0]
    #dstr = [0, 0, 0, 0, 0, 0]
    dstq = [0, 0, 0, 0, 0, 0]
    #dstn = [0, 0, 0, 0, 0, 0]

    #eqvg = [0, 0, 0, 0, 0, 0]
    #eqvr = [0, 0, 0, 0, 0, 0]
    #eqvq = [0, 0, 0, 0, 0, 0]
    #eqvn = [0, 0, 0, 0, 0, 0]

    #ehg = [0, 0, 0, 0, 0, 0]
    #ehr = [0, 0, 0, 0, 0, 0]
    #ehq = [0, 0, 0, 0, 0, 0]
    #ehn = [0, 0, 0, 0, 0, 0]

    #etg = [0, 0, 0, 0, 0, 0]
    #etr = [0, 0, 0, 0, 0, 0]
    #etq = [0, 0, 0, 0, 0, 0]
    #etn = [0, 0, 0, 0, 0, 0]

    #eg = [0, 0, 0, 0, 0, 0]
    #er = [0, 0, 0, 0, 0, 0]
    #eq = [0, 0, 0, 0, 0, 0]
    #en = [0, 0, 0, 0, 0, 0]

    #mnrg = [0, 0, 0, 0, 0, 0]
    #mnrr = [0, 0, 0, 0, 0, 0]
    mnrq = [0, 0, 0, 0, 0, 0]
    #mnrn = [0, 0, 0, 0, 0, 0]

    #dsnrg = [0, 0, 0, 0, 0, 0]
    #dsnrr = [0, 0, 0, 0, 0, 0]
    dsnrq = [0, 0, 0, 0, 0, 0]
    #dsnrn = [0, 0, 0, 0, 0, 0]



    for filename in path:

        with open(filename) as json_data:
            data = json.load(json_data)

        df = pd.DataFrame(data["mission_setup"])
        ra = df["routing_algorithm"]
        n_seed = df["seed"][0]
        n_drones = df["n_drones"][0]
        ratio = float(pd.DataFrame({data.get("packet_delivery_ratio")})[0])
        dt = float(pd.DataFrame({data.get("packet_mean_delivery_time")})[0])


        #explt_q_values = data["exploitation"]["q_values"]
        #explt_heuristic = data["exploitation"]["heuristic"]
        #explt_total = data["exploitation"]["total"]
        #explr = data["exploration"]

        relay = data["mean_number_of_relays"]

        i = int((n_drones / 5) - 1)
        j = int(n_seed)

        '''if ra[0] == "RoutingAlgorithm.GEO":
            mrg[i] += ratio
            mtg[i] += dt
            eqvg[i] += explt_q_values
            ehg[i] += explt_heuristic
            etg[i] += explt_total
            eg[i] += explr
            mnrg[i] += relay
            cg[i] += 1

        elif ra[0] == "RoutingAlgorithm.RND":
            mrr[i] += ratio
            mtr[i] += dt
            eqvr[i] += explt_q_values
            ehr[i] += explt_heuristic
            etr[i] += explt_total
            er[i] += explr
            mnrr[i] += relay
            cr[i] += 1'''

        if ra[0] == "RoutingAlgorithm.QL":
            mrq[i] += ratio
            mtq[i] += dt
            #eqvq[i] += explt_q_values
            #ehq[i] += explt_heuristic
            #etq[i] += explt_total
            #eq[i] += explr
            mnrq[i] += relay
            cq[i] += 1

        '''elif ra[0] == "RoutingAlgorithm.NQL":
            mrn[i] += ratio
            mtn[i] += dt
            eqvn[i] += explt_q_values
            ehn[i] += explt_heuristic
            etn[i] += explt_total
            en[i] += explr
            mnrn[i] += relay
            cn[i] += 1'''

    for i in range(6):
        '''if mrg[i] > 0:
            mrg[i] = round(mrg[i]/cg[i], 7)
            mtg[i] = round(mtg[i]/cg[i], 7)
            eqvg[i] = round(eqvg[i]/cg[i], 7)
            ehg[i] = round(ehg[i]/cg[i], 7)
            etg[i] = round(etg[i]/cg[i], 7)
            eg[i] = round(eg[i]/cg[i], 7)
            mnrg[i] = round(mnrg[i]/cg[i], 7)
        else:
            mrg[i] = -1
            mtg[i] = -1
            eqvg[i] = -1
            ehg[i] = -1
            etg[i] = -1
            eg[i] = -1
            mnrg[i] = -1

        if mrr[i] > 0:
            mrr[i] = round(mrr[i]/cr[i], 7)
            mtr[i] = round(mtr[i]/cr[i], 7)
            eqvr[i] = round(eqvr[i] / cr[i], 7)
            ehr[i] = round(ehr[i] / cr[i], 7)
            etr[i] = round(etr[i] / cr[i], 7)
            er[i] = round(er[i] / cr[i], 7)
            mnrr[i] = round(mnrr[i] / cr[i], 7)
        else:
            mrr[i] = -1
            mtr[i] = -1
            eqvr[i] = -1
            ehr[i] = -1
            etr[i] = -1
            er[i] = -1
            mnrr[i] = -1'''

        if mrq[i] > 0:
            mrq[i] = round(mrq[i]/cq[i], 7)
            mtq[i] = round(mtq[i]/cq[i], 7)
            #eqvq[i] = round(eqvq[i] / cq[i], 7)
            #ehq[i] = round(ehq[i] / cq[i], 7)
            #etq[i] = round(etq[i] / cq[i], 7)
            #eq[i] = round(eq[i] / cq[i], 7)
            mnrq[i] = round(mnrq[i] / cq[i], 7)
        else:
            mrq[i] = -1
            mtq[i] = -1
            #eqvq[i] = -1
            #ehq[i] = -1
            #etq[i] = -1
            #eq[i] = -1
            mnrq[i] = -1

        '''if mrn[i] > 0:
            mrn[i] = round(mrn[i]/cn[i], 7)
            mtn[i] = round(mtn[i]/cn[i], 7)
            eqvn[i] = round(eqvn[i] / cn[i], 7)
            ehn[i] = round(ehn[i] / cn[i], 7)
            etn[i] = round(etn[i] / cn[i], 7)
            en[i] = round(en[i] / cn[i], 7)
            mnrn[i] = round(mnrn[i] / cn[i], 7)
        else:
            mrn[i] = -1
            mtn[i] = -1
            eqvn[i] = -1
            ehn[i] = -1
            etn[i] = -1
            en[i] = -1
            mnrn[i] = -1'''

    for filename in path:

        with open(filename) as json_data:
            data = json.load(json_data)

        df = pd.DataFrame(data["mission_setup"])
        ra = df["routing_algorithm"]
        n_seed = df["seed"][0]
        n_drones = df["n_drones"][0]
        ratio = float(pd.DataFrame({data.get("packet_delivery_ratio")})[0])
        dt = float(pd.DataFrame({data.get("packet_mean_delivery_time")})[0])

        i = int((n_drones / 5) - 1)
        j = int(n_seed)

        '''if ra[0] == "RoutingAlgorithm.GEO":
            if ratio > 0:
                dsrg[i] += pow((ratio - mrg[i]), 2)
                dstg[i] += pow((dt - mtg[i]), 2)
                dsnrg[i] += pow((relay - mnrg[i]), 2)

        elif ra[0] == "RoutingAlgorithm.RND":
            if ratio > 0:
                dsrr[i] += pow((ratio - mrr[i]), 2)
                dstr[i] += pow((dt - mtr[i]), 2)
                dsnrr[i] += pow((relay - mnrr[i]), 2)'''

        if ra[0] == "RoutingAlgorithm.QL":
            if ratio > 0:
                dsrq[i] += pow((ratio - mrq[i]), 2)
                dstq[i] += pow((dt - mtq[i]), 2)
                dsnrq[i] += pow((relay - mnrq[i]), 2)

        '''elif ra[0] == "RoutingAlgorithm.NQL":
            if ratio > 0:
                dsrn[i] += pow((ratio - mrn[i]), 2)
                dstn[i] += pow((dt - mtn[i]), 2)
                dsnrn[i] += pow((relay - mnrn[i]), 2)'''

    for i in range(6):
        '''if dsrg[i] > 0:
            dsrg[i] = round(pow((dsrg[i]/cg[i]), 1/2), 7)
            dstg[i] = round(pow((dstg[i]/cg[i]), 1/2), 7)
            dsnrg[i] = round(pow((dsnrg[i]/cg[i]), 1/2), 7)
        else:
            dsrg[i] = -1
            dstg[i] = -1
            dsnrg[i] = -1
        if dsrr[i] > 0:
            dsrr[i] = round(pow((dsrr[i]/cr[i]), 1/2), 7)
            dstr[i] = round(pow((dstr[i]/cr[i]), 1/2), 7)
            dsnrr[i] = round(pow((dsnrr[i] / cr[i]), 1 / 2), 7)
        else:
            dsrr[i] = -1
            dstr[i] = -1
            dsnrr[i] = -1'''
        if dsrq[i] > 0:
            dsrq[i] = round(pow((dsrq[i]/cq[i]), 1/2), 7)
            dstq[i] = round(pow((dstq[i]/cq[i]), 1/2), 7)
            dsnrq[i] = round(pow((dsnrq[i] / cq[i]), 1 / 2), 7)
        else:
            dsrq[i] = -1
            dstq[i] = -1
            dsnrq[i] = -1
        '''if dsrn[i] > 0:
            dsrn[i] = round(pow((dsrn[i]/cn[i]), 1/2), 7)
            dstn[i] = round(pow((dstn[i]/cn[i]), 1/2), 7)
            dsnrn[i] = round(pow((dsnrn[i] / cn[i]), 1 / 2), 7)
        else:
            dsrn[i] = -1
            dstn[i] = -1
            dsnrn[i] = -1'''

    '''print("Tabella packet_delivery_ratio con GEO Routing:")
    print(mrg)
    print('.....................................................................................................')
    print("Deviazione standard:")
    print(dsrg)
    print('.....................................................................................................')
    print("Tabella packet_mean_delivery_time con GEO Routing:")
    print(mtg)
    print('.....................................................................................................')
    print("Deviazione standard:")
    print(dstg)
    print('.....................................................................................................')
    print("Exploitation: q_values (GEO Routing)")
    print(eqvg)
    print('.....................................................................................................')
    print("Exploitation: heuristic (GEO Routing")
    print(ehg)
    print('.....................................................................................................')
    print("Exploitation: total (GEO Routing)")
    print(etg)
    print('.....................................................................................................')
    print("Exploration (GEO Routing)")
    print(eg)
    print('.....................................................................................................')
    print("Media mean number of relays (GEO Routing):")
    print(mnrg)
    print('.....................................................................................................')
    print("Deviazione standard:")
    print(dsnrg)
    print('.....................................................................................................')

    print("Tabella packet_delivery_ratio con RND Routing:")
    print(mrr)
    print('.....................................................................................................')
    print("Deviazione standard:")
    print(dsrr)
    print('.....................................................................................................')
    print("Tabella packet_mean_delivery_time con RND Routing:")
    print(mtr)
    print('.....................................................................................................')
    print("Deviazione standard:")
    print(dstr)
    print('.....................................................................................................')
    print("Exploitation: q_values (RND Routing)")
    print(eqvr)
    print('.....................................................................................................')
    print("Exploitation: heuristic (RND Routing")
    print(ehr)
    print('.....................................................................................................')
    print("Exploitation: total (RND Routing)")
    print(etr)
    print('.....................................................................................................')
    print("Exploration (RND Routing)")
    print(er)
    print('.....................................................................................................')
    print("Media mean number of relays (RND Routing):")
    print(mnrr)
    print('.....................................................................................................')
    print("Deviazione standard:")
    print(dsnrr)
    print('.....................................................................................................')
    '''

    print("Tabella packet_delivery_ratio con QL Routing:")
    print(mrq)
    print('.....................................................................................................')
    print("Deviazione standard:")
    print(dsrq)
    print('.....................................................................................................')
    print("Tabella packet_mean_delivery_time con QL Routing:")
    print(mtq)
    print('.....................................................................................................')
    print("Deviazione standard:")
    print(dstq)
    print('.....................................................................................................')
    '''print("Exploitation: q_values (QL Routing)")
    print(eqvq)
    print('.....................................................................................................')
    print("Exploitation: heuristic (QL Routing")
    print(ehq)
    print('.....................................................................................................')
    print("Exploitation: total (QL Routing)")
    print(etq)
    print('.....................................................................................................')
    print("Exploration (QL Routing)")
    print(eq)
    print('.....................................................................................................')'''
    print("Media mean number of relays (QL Routing):")
    print(mnrq)
    print('.....................................................................................................')
    print("Deviazione standard:")
    print(dsnrq)
    print('.....................................................................................................')

    '''print("Tabella packet_delivery_ratio con NQL Routing:")
    print(mrn)
    print('.....................................................................................................')
    print("Deviazione standard:")
    print(dsrn)
    print('.....................................................................................................')
    print("Tabella packet_mean_delivery_time con NQL Routing:")
    print(mtn)
    print('.....................................................................................................')
    print("Deviazione standard:")
    print(dstn)
    print('.....................................................................................................')
    print("Exploitation: q_values (NQL Routing)")
    print(eqvn)
    print('.....................................................................................................')
    print("Exploitation: heuristic (NQL Routing")
    print(ehn)
    print('.....................................................................................................')
    print("Exploitation: total (NQL Routing)")
    print(etn)
    print('.....................................................................................................')
    print("Exploration (NQL Routing)")
    print(en)
    print('.....................................................................................................')
    print("Media mean number of relays (NQL Routing):")
    print(mnrn)
    print('.....................................................................................................')
    print("Deviazione standard:")
    print(dsnrn)'''


    '''out_results = {
                   'mean_packet_delivery_ratio': {'GEO': mrg, 'RND': mrr, 'QL': mrq, 'NQL': mrn},
                   'mean_standard_deviation_ratio': {'GEO': dsrg, 'RND': dsrr, 'QL': dsrq, 'NQL': dsrn},
                   'mean_packet_delivery_time': {'GEO': mtg, 'RND': mtr, 'QL': mtq, 'NQL': mtn},
                   'mean_standard_deviation_packet_delivery_time': {'GEO': dstg, 'RND': dstr, 'QL': dstq, 'NQL': dstn},
                   'mean_number_of_relays': {'GEO': mnrg, 'RND': mnrr, 'QL': mnrq, 'NQL': mnrn},
                   'mean_standard_deviation_relays': {'GEO': dsnrg, 'RND': dsnrr, 'QL': dsnrq, 'NQL': dsnrn},
                   'mean_exploitation_q_values': {'GEO': eqvg, 'RND': eqvr, 'QL': eqvq, 'NQL': eqvn},
                   'mean_exploitation_heuristic': {'GEO': ehg, 'RND': ehr, 'QL': ehq, 'NQL': ehn},
                   'mean_exploitation_total': {'GEO': etg, 'RND': etr, 'QL': etq, 'NQL': etn},
                   'mean_exploration': {'GEO': eg, 'RND': er, 'QL': eq, 'NQL': en}
                   }'''
    out_results = {
        'mean_packet_delivery_ratio': {mrq},
        'mean_standard_deviation_ratio': {dsrq},
        'mean_packet_delivery_time': {mtq},
        'mean_standard_deviation_packet_delivery_time': {dstq},
        'mean_number_of_relays': {mnrq},
        'mean_standard_deviation_relays': {dsnrq}
    }

    with open("output.json", "w") as outfile:
        json.dump(out_results, outfile)





if __name__ == "__main__":
    """
    You can run this file to test your script
    """

    path = "../../../data/evaluation_tests/*.json"
    path = glob(path)
    compute_data_avg_std(path=path)