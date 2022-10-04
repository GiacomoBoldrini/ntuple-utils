import ROOT
import argparse
import configparser
from itertools import combinations
from array import array
import sys
import glob
import os
import logging
from common.ntupleCommon import *

def getEventsSM (ntuple, variables, nominal_wgt, rwgt):

    outevents_sm = []

    sum_nominal_weight = 0.
    sum_rwgt_sm = 0.

    leaves = {k: ntuple.GetLeaf(k) for k in variables}
    w = ntuple.GetLeaf(nominal_wgt)
    rwgt0 = ntuple.GetLeaf(rwgt)

    print ('[INFO] reading SM ntuple')
    
    for i in range(0, ntuple.GetEntries()):
        if i % 1000 == 0: print("{}/{} {}%".format(i, ntuple.GetEntries(), 100*float(i)/ntuple.GetEntries()))

        values_sm = []
        ntuple.GetEntry(i)

        sum_nominal_weight += w.GetValue ()
        w_sm = rwgt0.GetValue () 

        sum_rwgt_sm += w_sm

        for key in variables:
            if key == nominal_wgt:
                values_sm.append(w_sm)
            else:
                values_sm.append(float(leaves[key].GetValue ()))
        outevents_sm.append (array('f', values_sm))
    
    print ('[INFO] sum of nominal weights: ' + str(sum_nominal_weight))
    print ('[INFO] sum of new SM nominal weights: ' + str(sum_rwgt_sm))

    resultsDict = {
        'events_sm': outevents_sm,
        'sum_nominal_weight': sum_nominal_weight,
        'sum_rwgt_sm': sum_rwgt_sm
    }

    return resultsDict

def getEventsLinQuad (ntuple, variables, nominal_wgt, rwgt):

    outevents_li = []
    outevents_qu = []

    sum_nominal_weight = 0.
    sum_rwgt_li = 0.
    sum_rwgt_qu = 0.

    quad_null = 0
    quad_neg = 0

    leaves = {k: ntuple.GetLeaf(k) for k in variables}

    w = ntuple.GetLeaf(nominal_wgt)
    rwgt0 = ntuple.GetLeaf(rwgt['0']["wgtName"][0])
    rwgtp1 = ntuple.GetLeaf(rwgt["1"]["wgtName"][0])
    rwgtm1 = ntuple.GetLeaf(rwgt["-1"]["wgtName"][0])

    print ('[INFO] reading SM + LI + QU ntuple')
    
    for i in range(0, ntuple.GetEntries()):
        if i % 1000 == 0: print("{}/{} {}%".format(i, ntuple.GetEntries(), 100*float(i)/ntuple.GetEntries()))

        values_li = []
        values_qu = []

        ntuple.GetEntry(i)

        sum_nominal_weight += w.GetValue ()
        a = rwgtp1.GetValue ()
        b = rwgtm1.GetValue ()
        c = rwgt0.GetValue () 

        #sspeecific case for 0,1,-1 reweighting
        w_li = 0.5 * (a - b)
        w_qu = 0.5 * (a + b - 2 * c)

        sum_rwgt_li += w_li
        sum_rwgt_qu += w_qu
        if w_qu == 0 : quad_null = 1 + quad_null
        if w_qu < 0:
            #w_qu = 0
            quad_neg = 1 + quad_neg

        for key in variables:
            if key == nominal_wgt:
                values_li.append(w_li)
                values_qu.append(w_qu)
            else:
                values_li.append(float(leaves[key].GetValue ()))
                values_qu.append(float(leaves[key].GetValue ()))
        outevents_li.append (array('f', values_li))
        outevents_qu.append (array('f', values_qu))

    print ('[INFO] sum of SM + LI + QU nominal weights: ' + str(sum_nominal_weight))
    print ('[INFO] sum of new LI nominal weights: ' + str(sum_rwgt_li))
    print ('[INFO] sum of new QU nominal weights: ' + str(sum_rwgt_qu))

    resultsDict = {
        'events_li': outevents_li,
        'events_qu': outevents_qu,
        'sum_nominal_weight': sum_nominal_weight,
        'sum_rwgt_li': sum_rwgt_li,
        'sum_rwgt_qu': sum_rwgt_qu,
        'quad_null': quad_null,
        'quad_neg': quad_neg,
    }

    return resultsDict



def getEventsIn (ntuple, variables, nominal_wgt, rwgt):

    outevents_in = []

    sum_nominal_weight = 0.
    sum_rwgt_in = 0.

    leaves = {k: ntuple.GetLeaf(k) for k in variables}
    w = ntuple.GetLeaf(nominal_wgt)
    rwgt11 = ntuple.GetLeaf(rwgt['11']["wgtName"][0])
    rwgt00 = ntuple.GetLeaf(rwgt['00']["wgtName"][0])
    rwgt01 = ntuple.GetLeaf(rwgt['01']["wgtName"][0])
    rwgt10 = ntuple.GetLeaf(rwgt['10']["wgtName"][0])

    print ('[INFO] reading SM + LI + QU + IN ntuple')
    
    for i in range(0, ntuple.GetEntries()):
        if i % 1000 == 0: print("{}/{} {}%".format(i, ntuple.GetEntries(), 100*float(i)/ntuple.GetEntries()))
        values_in = []

        ntuple.GetEntry(i)

        sum_nominal_weight += w.GetValue ()
        r11 = rwgt11.GetValue ()
        r00 = rwgt00.GetValue ()
        r01 = rwgt01.GetValue ()
        r10 = rwgt10.GetValue ()

        w_in = r11 + r00 - r01 - r10

        sum_rwgt_in += w_in

        for key in variables:
            if key == nominal_wgt:
                values_in.append(w_in)
            else:
                values_in.append(float(leaves[key].GetValue ()))
        outevents_in.append (array('f', values_in))

    print ('[INFO] sum of SM + LI + QU + IN nominal weights: ' + str(sum_nominal_weight))
    print ('[INFO] sum of new IN nominal weights: ' + str(sum_rwgt_in))

    resultsDict = {
        'events_in': outevents_in,
        'sum_nominal_weight': sum_nominal_weight,
        'sum_rwgt_in': sum_rwgt_in,
    }

    return resultsDict

if __name__ == '__main__':

    print("""
 ___________________________________ 
  Extract All components
 ----------------------------------- """)

    parser = argparse.ArgumentParser(description='Command line parser')
    parser.add_argument('--root', dest='root', help='root file ntuple_$proc_SM_LI_QU_IN.root', required=True)
    parser.add_argument('--ops', dest='ops', help='Operator / s to compute the components. If _ in name then it assumes you want the mixed interference', required=True, type=str)
    parser.add_argument('--vars', dest='vars', help='Only store these variables in output tree', required=False, default=[], nargs="+")
    parser.add_argument('--out', dest='out', help='Ouput path where to store ntuples', required=False, default="./")
    parser.add_argument('--sm', dest='smweight', help='How the SM weight is called in the original root file as branch. Default is w', required=False, default="w")
    args = parser.parse_args()


    file_path = args.root 
    tntuple_name  = args.root.split("/")[-1].split("ntuple_")[1].split(".root")[0]
    th_name = tntuple_name + "_nums"

    process = tntuple_name.split("_")[0]

    ops = args.ops
    
    #first extract SM

    w  = "w" #nominal weight

    print ('\n\tNtuple file-in   =  ' + file_path)
    print ('\tTNtuple name-in  =  ' + tntuple_name)
    print ('\tTH1F name-in     =  ' + th_name + '\n')

    f_in = ROOT.TFile (file_path, 'READ')
    t = ROOT.gDirectory.Get (tntuple_name)
    h = ROOT.gDirectory.Get (th_name)
    overallXS = h.GetBinContent(1)

    leaves = t.GetListOfLeaves()
    vars_wrwgt = [leaves.At(i).GetName() for i in range(0, leaves.GetEntries())]

    # variables for final ntuple
    if len(args.vars) == 0:
        vars = [v for v in vars_wrwgt if "rwgt" not in v]
        vars.sort()
    else:
        vars = args.vars + ["w"]


    print(vars)

    print ('[INFO] overall XS: ' + str(overallXS))

    print("""
    #-------------------------------------#
    #-----------     BEGIN    ------------#
    #-------------------------------------#
    """)

    # just counters
    count_filled = 0
    tot_number_of_files = 1 if ("_" in args.ops or args.ops == "SM") else 2

    if args.ops == "SM":
        ntupleFileOut = args.out + "ntuple_" + process + '_SM.root'
        ntupleNameOut = process + '_SM'
        histoNameOut = ntupleNameOut + "_nums"

        events_dictionary = getEventsSM (t, vars, w, args.smweight)

        eventsIN = events_dictionary['events_sm']
        SumWgtOld = events_dictionary['sum_nominal_weight']
        SumWgtIN = events_dictionary['sum_rwgt_sm']

        f_in.Close()
            
        XS = overallXS * SumWgtIN / SumWgtOld

        print ('\n\tNtuple file-out  =  ' + ntupleFileOut)
        print ('\tTNtuple name-out =  ' + ntupleNameOut)
        print ('\tTH1F name-out    =  ' + histoNameOut + '\n')

        t = getNtuple (ntupleNameOut, ntupleNameOut, vars, eventsIN)
        h = getHisto (histoNameOut, "global numbers", XS, SumWgtIN, SumWgtIN)

        f_out = ROOT.TFile (ntupleFileOut, 'RECREATE')

        print ('[INFO] writing ROOT file')
        t.Write()
        h.Write()
            
        f_out.Close()
        count_filled += 1

        print ('\n[INFO] end SM process')
        print("")
        print("# -----------  {}/{}   ----------- # ".format(count_filled, tot_number_of_files))
        print("")

    # if "_" not in op name then we extract linear and quadratic components
    elif "_" not in args.ops:
    #then extract linear and quadratic

        f_in = ROOT.TFile (file_path, 'READ')
        t = ROOT.gDirectory.Get (tntuple_name)
        h = ROOT.gDirectory.Get (th_name)
        overallXS = h.GetBinContent(1)

        #searching weights name from the dict
        rwgt_dict = {}
        rwgt_dict["1"] = {'wgtName': [args.ops], 'values': [[1.0]]}
        rwgt_dict["0"] = {'wgtName': [args.smweight], 'values': [[0.0]]}
        rwgt_dict["-1"] = {'wgtName': [args.ops + "m1"], 'values': [[-1.0]]}

        events_dictionary = getEventsLinQuad (t, vars, w, rwgt_dict)

        eventsLI = events_dictionary['events_li']
        eventsQU = events_dictionary['events_qu']
        SumWgtOld = events_dictionary['sum_nominal_weight']
        SumWgtLI = events_dictionary['sum_rwgt_li']
        SumWgtQU = events_dictionary['sum_rwgt_qu']
        q_null = events_dictionary['quad_null']
        q_neg = events_dictionary['quad_neg']

        f_in.Close()

        if q_null > 0:
            print ('[WARNING] {0}: {1} events give Quad nominal weight = 0'.format(args.ops, q_null))
        if q_neg > 0:
            print ('[WARNING] {0}: {1} events give Quad nominal weight < 0. Setting them to 0'.format(args.ops, q_neg))

        for component in ['LI', 'QU']:

            if component == 'LI':
                eventsExtr = eventsLI
                SumWgtExtr = SumWgtLI
            elif component == 'QU':
                eventsExtr = eventsQU
                SumWgtExtr = SumWgtQU
            
            XS = overallXS * SumWgtExtr / SumWgtOld

            ntupleFileOut = args.out + "ntuple_" + process + '_{}_{}.root'.format(args.ops, component)
            ntupleNameOut = process + '_{}_{}'.format(args.ops, component)
            histoNameOut = ntupleNameOut + "_nums"

            print ('\n\tNtuple file-out  =  ' + ntupleFileOut)
            print ('\tTNtuple name-out =  ' + ntupleNameOut)
            print ('\tTH1F name-out    =  ' + histoNameOut + '\n')
            
            t = getNtuple (ntupleNameOut, ntupleNameOut, vars, eventsExtr)
            h = getHisto (histoNameOut, "global numbers", XS, SumWgtExtr, SumWgtExtr)
            f_out = ROOT.TFile (ntupleFileOut, 'RECREATE')

            print ('[INFO] writing {} {} ROOT file'.format(args.ops, component))
            t.Write()
            h.Write()
            
            f_out.Close()
            
            count_filled += 1
            print("")
            print("# -----------  {}/{}   ----------- # ".format(count_filled, tot_number_of_files))
            print("")


    elif "_" in args.ops:

        ntupleFileOut = args.out + "ntuple_" + process + '_{}_IN.root'.format(args.ops)
        ntupleNameOut = process + '_{}_IN'.format(args.ops)
        histoNameOut = ntupleNameOut + "_nums"

        f_in = ROOT.TFile (file_path, 'READ')
        t = ROOT.gDirectory.Get (tntuple_name)
        h = ROOT.gDirectory.Get (th_name)
        overallXS = h.GetBinContent(1)

        single_ops = args.ops.split("_")
        #searching weights name from the dict
        rwgt_dict = {}
        #00
        rwgt_dict["00"] = {'wgtName': [args.smweight], 'values': [[0.0]]}
        #11
        rwgt_dict["11"] = {'wgtName': [args.ops], 'values': [[1.0,1.0]]}
        #10
        rwgt_dict["10"] = {'wgtName': [single_ops[0]], 'values': [[1.0]]}
        #01
        rwgt_dict["01"] = {'wgtName': [single_ops[1]], 'values': [[1.0]]}

        events_dictionary = getEventsIn (t, vars, w, rwgt_dict)

        eventsIN = events_dictionary['events_in']
        SumWgtOld = events_dictionary['sum_nominal_weight']
        SumWgtIN = events_dictionary['sum_rwgt_in']

        f_in.Close()
            
        XS = overallXS * SumWgtIN / SumWgtOld

        print ('\n\tNtuple file-out  =  ' + ntupleFileOut)
        print ('\tTNtuple name-out =  ' + ntupleNameOut)
        print ('\tTH1F name-out    =  ' + histoNameOut + '\n')

        t = getNtuple (ntupleNameOut, ntupleNameOut, vars, eventsIN)
        h = getHisto (histoNameOut, "global numbers", XS, SumWgtIN, SumWgtIN)

        f_out = ROOT.TFile (ntupleFileOut, 'RECREATE')

        print ('[INFO] writing {} IN ROOT file'.format(args.ops))
        t.Write()
        h.Write()
            
        f_out.Close()

        count_filled += 1
        print("")
        print("# -----------  {}/{}   ----------- # ".format(count_filled, tot_number_of_files))
        print("")

    else:
        print("[ERROR] No valid op name")
        sys.exit(0)
    
