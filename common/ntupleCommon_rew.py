import ROOT


def getTreeName (filepath, conventions):

    if '/' in filepath:
        treeName = filepath.split('/')[1]
    else:
        treeName = filepath
        
    for s in conventions:
        treeName = treeName.replace(s.strip(), '')

    return treeName


def getNtuple (name, title, variables, events):

    ntuple = ROOT.TNtuple (name, title, ':'.join(variables))
    for e in events : ntuple.Fill(e)
    
    return ntuple


def getHisto (name, title, XS, sum_wgt_overall, sum_wgt_passed):

    histo = ROOT.TH1D (name, title, 3, 0, 3)
    histo.SetBinContent(1, XS)
    histo.SetBinContent(2, sum_wgt_overall)
    histo.SetBinContent(3, sum_wgt_passed)
    
    return histo
    

def rwgtObjects (couplingList, nameList, notusedList):

    keys = [rwgt.strip() for rwgt in couplingList]
    used = [rwgt.strip() for rwgt in nameList]
    notused = [rwgt.strip() for rwgt in notusedList]

    if len(keys) == len(used):

        used_dict = dict(zip(keys, used))
        return keys, used, notused, used_dict

    else: raise IndexError ('In config file <name2d> and <coupling2d> have different sizes')

def readReweightCard ( card_path, convert_names=None ):

    print(". . . @ @ @ Reading Reweight Card. {} @ @ @ . . . ".format(card_path))

    f = open(card_path, "r")
    contents = f.readlines()

    ret_d = {}

    #w_names = "cbHIm_cjj11,cbHIm_cjj18,cbHIm_cjj31,cbHIm_cjj38,cbHIm_cll1,cbHIm_ctBRe,cbHIm_ctGIm,cbHIm_ctj1,cbHIm_ctj8,cbHIm_ctWIm,cbHIm_ctWRe,cbHIm,cbHImm1,cHB_cbHIm,cHB_cHbox,cHB_cHbq,cHB_cHd,cHB_cHDD,cHB_cHe,cHB_cHj1,cHB_cHj3,cHB_cHl1,cHB_cHl3,cHB_cHQ1,cHB_cHQ3,cHB_cHtbRe,cHB_cHt,cHB_cHu,cHB_cHWB,cHB_cHW,cHB_cjj11,cHB_cjj18,cHB_cjj31,cHB_cjj38,cHB_cll1,cHB_cQj11,cHB_cQj18,cHB_cQj31,cHB_cQj38,cHB_cQQ1,cHB_cQQ8,cHB_cQt1,cHB_cQt8,cHB_ctBRe,cHB_ctGIm,cHB_ctj1,cHB_ctj8,cHB_ctWIm,cHB_ctWRe,cHB_cW,cHB,cHBm1,cHbox_cbHIm,cHbox_cHbq,cHbox_cHd,cHbox_cHe,cHbox_cHj1,cHbox_cHj3,cHbox_cHl1,cHbox_cHl3,cHbox_cHtbRe,cHbox_cHt,cHbox_cHu,cHbox_cjj11,cHbox_cjj18,cHbox_cjj31,cHbox_cjj38,cHbox_cll1,cHbox_cQj11,cHbox_cQj18,cHbox_cQj31,cHbox_cQj38,cHbox_cQQ1,cHbox_cQQ8,cHbox_cQt1,cHbox_cQt8,cHbox_ctBRe,cHbox_ctGIm,cHbox_ctj1,cHbox_ctj8,cHbox_ctWIm,cHbox_ctWRe,cHbox_cW,cHbox,cHboxm1,cHbq_cbHIm,cHbq_cHd,cHbq_cHe,cHbq_cHj1,cHbq_cHj3,cHbq_cHl1,cHbq_cHl3,cHbq_cHtbRe,cHbq_cHt,cHbq_cHu,cHbq_cjj11,cHbq_cjj18,cHbq_cjj31,cHbq_cjj38,cHbq_cll1,cHbq_cQj11,cHbq_cQj18,cHbq_cQj31,cHbq_cQj38,cHbq_cQQ1,cHbq_cQQ8,cHbq_cQt1,cHbq_cQt8,cHbq_ctBRe,cHbq_ctGIm,cHbq_ctj1,cHbq_ctj8,cHbq_ctWIm,cHbq_ctWRe,cHbq_cW,cHbq,cHbqm1,cHd_cbHIm,cHd_cHe,cHd_cHj1,cHd_cHj3,cHd_cHl1,cHd_cHl3,cHd_cHtbRe,cHd_cHt,cHd_cHu,cHd_cjj11,cHd_cjj18,cHd_cjj31,cHd_cjj38,cHd_cll1,cHd_cQj11,cHd_cQj18,cHd_cQj31,cHd_cQj38,cHd_cQQ1,cHd_cQQ8,cHd_cQt1,cHd_cQt8,cHd_ctBRe,cHd_ctGIm,cHd_ctj1,cHd_ctj8,cHd_ctWIm,cHd_ctWRe,cHd_cW,cHd,cHDD_cbHIm,cHDD_cHbox,cHDD_cHbq,cHDD_cHd,cHDD_cHe,cHDD_cHj1,cHDD_cHj3,cHDD_cHl1,cHDD_cHl3,cHDD_cHQ1,cHDD_cHQ3,cHDD_cHtbRe,cHDD_cHt,cHDD_cHu,cHDD_cHWB,cHDD_cHW,cHDD_cjj11,cHDD_cjj18,cHDD_cjj31,cHDD_cjj38,cHDD_cll1,cHDD_cQj11,cHDD_cQj18,cHDD_cQj31,cHDD_cQj38,cHDD_cQQ1,cHDD_cQQ8,cHDD_cQt1,cHDD_cQt8,cHDD_ctBRe,cHDD_ctGIm,cHDD_ctj1,cHDD_ctj8,cHDD_ctWIm,cHDD_ctWRe,cHDD_cW,cHDD,cHDDm1,cHdm1,cHe_cbHIm,cHe_cHj1,cHe_cHj3,cHe_cHl1,cHe_cHl3,cHe_cHtbRe,cHe_cHt,cHe_cHu,cHe_cjj11,cHe_cjj18,cHe_cjj31,cHe_cjj38,cHe_cll1,cHe_cQj11,cHe_cQj18,cHe_cQj31,cHe_cQj38,cHe_cQQ1,cHe_cQQ8,cHe_cQt1,cHe_cQt8,cHe_ctBRe,cHe_ctGIm,cHe_ctj1,cHe_ctj8,cHe_ctWIm,cHe_ctWRe,cHe_cW,cHe,cHem1,cHj1_cbHIm,cHj1_cHj3,cHj1_cHl1,cHj1_cHl3,cHj1_cHtbRe,cHj1_cHt,cHj1_cHu,cHj1_cjj11,cHj1_cjj18,cHj1_cjj31,cHj1_cjj38,cHj1_cll1,cHj1_cQj11,cHj1_cQj18,cHj1_cQj31,cHj1_cQj38,cHj1_cQQ1,cHj1_cQQ8,cHj1_cQt1,cHj1_cQt8,cHj1_ctBRe,cHj1_ctGIm,cHj1_ctj1,cHj1_ctj8,cHj1_ctWIm,cHj1_ctWRe,cHj1_cW,cHj1,cHj1m1,cHj3_cbHIm,cHj3_cHl1,cHj3_cHl3,cHj3_cHtbRe,cHj3_cHt,cHj3_cHu,cHj3_cjj11,cHj3_cjj18,cHj3_cjj31,cHj3_cjj38,cHj3_cll1,cHj3_cQj11,cHj3_cQj18,cHj3_cQj31,cHj3_cQj38,cHj3_cQQ1,cHj3_cQQ8,cHj3_cQt1,cHj3_cQt8,cHj3_ctBRe,cHj3_ctGIm,cHj3_ctj1,cHj3_ctj8,cHj3_ctWIm,cHj3_ctWRe,cHj3_cW,cHj3,cHj3m1,cHl1_cbHIm,cHl1_cHl3,cHl1_cHtbRe,cHl1_cHt,cHl1_cHu,cHl1_cjj11,cHl1_cjj18,cHl1_cjj31,cHl1_cjj38,cHl1_cll1,cHl1_cQj11,cHl1_cQj18,cHl1_cQj31,cHl1_cQj38,cHl1_cQQ1,cHl1_cQQ8,cHl1_cQt1,cHl1_cQt8,cHl1_ctBRe,cHl1_ctGIm,cHl1_ctj1,cHl1_ctj8,cHl1_ctWIm,cHl1_ctWRe,cHl1_cW,cHl1,cHl1m1,cHl3_cbHIm,cHl3_cHtbRe,cHl3_cHt,cHl3_cHu,cHl3_cjj11,cHl3_cjj18,cHl3_cjj31,cHl3_cjj38,cHl3_cll1,cHl3_cQj11,cHl3_cQj18,cHl3_cQj31,cHl3_cQj38,cHl3_cQQ1,cHl3_cQQ8,cHl3_cQt1,cHl3_cQt8,cHl3_ctBRe,cHl3_ctGIm,cHl3_ctj1,cHl3_ctj8,cHl3_ctWIm,cHl3_ctWRe,cHl3_cW,cHl3,cHl3m1,cHQ1_cbHIm,cHQ1_cHbox,cHQ1_cHbq,cHQ1_cHd,cHQ1_cHe,cHQ1_cHj1,cHQ1_cHj3,cHQ1_cHl1,cHQ1_cHl3,cHQ1_cHQ3,cHQ1_cHtbRe,cHQ1_cHt,cHQ1_cHu,cHQ1_cHWB,cHQ1_cHW,cHQ1_cjj11,cHQ1_cjj18,cHQ1_cjj31,cHQ1_cjj38,cHQ1_cll1,cHQ1_cQj11,cHQ1_cQj18,cHQ1_cQj31,cHQ1_cQj38,cHQ1_cQQ1,cHQ1_cQQ8,cHQ1_cQt1,cHQ1_cQt8,cHQ1_ctBRe,cHQ1_ctGIm,cHQ1_ctj1,cHQ1_ctj8,cHQ1_ctWIm,cHQ1_ctWRe,cHQ1_cW,cHQ1,cHQ1m1,cHQ3_cbHIm,cHQ3_cHbox,cHQ3_cHbq,cHQ3_cHd,cHQ3_cHe,cHQ3_cHj1,cHQ3_cHj3,cHQ3_cHl1,cHQ3_cHl3,cHQ3_cHtbRe,cHQ3_cHt,cHQ3_cHu,cHQ3_cHWB,cHQ3_cHW,cHQ3_cjj11,cHQ3_cjj18,cHQ3_cjj31,cHQ3_cjj38,cHQ3_cll1,cHQ3_cQj11,cHQ3_cQj18,cHQ3_cQj31,cHQ3_cQj38,cHQ3_cQQ1,cHQ3_cQQ8,cHQ3_cQt1,cHQ3_cQt8,cHQ3_ctBRe,cHQ3_ctGIm,cHQ3_ctj1,cHQ3_ctj8,cHQ3_ctWIm,cHQ3_ctWRe,cHQ3_cW,cHQ3,cHQ3m1,cHtbRe_cbHIm,cHtbRe_cHu,cHtbRe_cjj11,cHtbRe_cjj18,cHtbRe_cjj31,cHtbRe_cjj38,cHtbRe_cll1,cHtbRe_cQj11,cHtbRe_cQj18,cHtbRe_cQj31,cHtbRe_cQj38,cHtbRe_cQQ1,cHtbRe_cQQ8,cHtbRe_cQt1,cHtbRe_cQt8,cHtbRe_ctBRe,cHtbRe_ctGIm,cHtbRe_ctj1,cHtbRe_ctj8,cHtbRe_ctWIm,cHtbRe_ctWRe,cHtbRe_cW,cHtbRe,cHtbRem1,cHt_cbHIm,cHt_cHtbRe,cHt_cHu,cHt_cjj11,cHt_cjj18,cHt_cjj31,cHt_cjj38,cHt_cll1,cHt_cQj11,cHt_cQj18,cHt_cQj31,cHt_cQj38,cHt_cQQ1,cHt_cQQ8,cHt_cQt1,cHt_cQt8,cHt_ctBRe,cHt_ctGIm,cHt_ctj1,cHt_ctj8,cHt_ctWIm,cHt_ctWRe,cHt_cW,cHt,cHtm1,cHu_cbHIm,cHu_cjj11,cHu_cjj18,cHu_cjj31,cHu_cjj38,cHu_cll1,cHu_cQj11,cHu_cQj18,cHu_cQj31,cHu_cQj38,cHu_cQQ1,cHu_cQQ8,cHu_cQt1,cHu_cQt8,cHu_ctBRe,cHu_ctGIm,cHu_ctj1,cHu_ctj8,cHu_ctWIm,cHu_ctWRe,cHu_cW,cHu,cHum1,cHWB_cbHIm,cHWB_cHbox,cHWB_cHbq,cHWB_cHd,cHWB_cHe,cHWB_cHj1,cHWB_cHj3,cHWB_cHl1,cHWB_cHl3,cHWB_cHtbRe,cHWB_cHt,cHWB_cHu,cHWB_cjj11,cHWB_cjj18,cHWB_cjj31,cHWB_cjj38,cHWB_cll1,cHWB_cQj11,cHWB_cQj18,cHWB_cQj31,cHWB_cQj38,cHWB_cQQ1,cHWB_cQQ8,cHWB_cQt1,cHWB_cQt8,cHWB_ctBRe,cHWB_ctGIm,cHWB_ctj1,cHWB_ctj8,cHWB_ctWIm,cHWB_ctWRe,cHWB_cW,cHWB,cHWBm1,cHW_cbHIm,cHW_cHbox,cHW_cHbq,cHW_cHd,cHW_cHe,cHW_cHj1,cHW_cHj3,cHW_cHl1,cHW_cHl3,cHW_cHtbRe,cHW_cHt,cHW_cHu,cHW_cHWB,cHW_cjj11,cHW_cjj18,cHW_cjj31,cHW_cjj38,cHW_cll1,cHW_cQj11,cHW_cQj18,cHW_cQj31,cHW_cQj38,cHW_cQQ1,cHW_cQQ8,cHW_cQt1,cHW_cQt8,cHW_ctBRe,cHW_ctGIm,cHW_ctj1,cHW_ctj8,cHW_ctWIm,cHW_ctWRe,cHW_cW,cHW,cHWm1,cjj11_cjj18,cjj11_cjj31,cjj11_cjj38,cjj11_cll1,cjj11_ctBRe,cjj11_ctGIm,cjj11_ctj1,cjj11_ctj8,cjj11_ctWIm,cjj11_ctWRe,cjj11,cjj11m1,cjj18_cjj31,cjj18_cjj38,cjj18_cll1,cjj18_ctBRe,cjj18_ctGIm,cjj18_ctj1,cjj18_ctj8,cjj18_ctWIm,cjj18_ctWRe,cjj18,cjj18m1,cjj31_cjj38,cjj31_cll1,cjj31_ctBRe,cjj31_ctGIm,cjj31_ctj1,cjj31_ctj8,cjj31_ctWIm,cjj31_ctWRe,cjj31,cjj31m1,cjj38_cll1,cjj38_ctBRe,cjj38_ctGIm,cjj38_ctj1,cjj38_ctj8,cjj38_ctWIm,cjj38_ctWRe,cjj38,cjj38m1,cll1_ctBRe,cll1_ctGIm,cll1_ctj1,cll1_ctj8,cll1_ctWIm,cll1_ctWRe,cll1,cll1m1,cQj11_cbHIm,cQj11_cjj11,cQj11_cjj18,cQj11_cjj31,cQj11_cjj38,cQj11_cll1,cQj11_cQj18,cQj11_cQj31,cQj11_cQj38,cQj11_cQt1,cQj11_cQt8,cQj11_ctBRe,cQj11_ctGIm,cQj11_ctj1,cQj11_ctj8,cQj11_ctWIm,cQj11_ctWRe,cQj11_cW,cQj11,cQj11m1,cQj18_cbHIm,cQj18_cjj11,cQj18_cjj18,cQj18_cjj31,cQj18_cjj38,cQj18_cll1,cQj18_cQj31,cQj18_cQj38,cQj18_cQt1,cQj18_cQt8,cQj18_ctBRe,cQj18_ctGIm,cQj18_ctj1,cQj18_ctj8,cQj18_ctWIm,cQj18_ctWRe,cQj18_cW,cQj18,cQj18m1,cQj31_cbHIm,cQj31_cjj11,cQj31_cjj18,cQj31_cjj31,cQj31_cjj38,cQj31_cll1,cQj31_cQj38,cQj31_cQt1,cQj31_cQt8,cQj31_ctBRe,cQj31_ctGIm,cQj31_ctj1,cQj31_ctj8,cQj31_ctWIm,cQj31_ctWRe,cQj31_cW,cQj31,cQj31m1,cQj38_cbHIm,cQj38_cjj11,cQj38_cjj18,cQj38_cjj31,cQj38_cjj38,cQj38_cll1,cQj38_cQt1,cQj38_cQt8,cQj38_ctBRe,cQj38_ctGIm,cQj38_ctj1,cQj38_ctj8,cQj38_ctWIm,cQj38_ctWRe,cQj38_cW,cQj38,cQj38m1,cQQ1_cbHIm,cQQ1_cjj11,cQQ1_cjj18,cQQ1_cjj31,cQQ1_cjj38,cQQ1_cll1,cQQ1_cQj11,cQQ1_cQj18,cQQ1_cQj31,cQQ1_cQj38,cQQ1_cQQ8,cQQ1_cQt1,cQQ1_cQt8,cQQ1_ctBRe,cQQ1_ctGIm,cQQ1_ctj1,cQQ1_ctj8,cQQ1_ctWIm,cQQ1_ctWRe,cQQ1_cW,cQQ1,cQQ1m1,cQQ8_cbHIm,cQQ8_cjj11,cQQ8_cjj18,cQQ8_cjj31,cQQ8_cjj38,cQQ8_cll1,cQQ8_cQj11,cQQ8_cQj18,cQQ8_cQj31,cQQ8_cQj38,cQQ8_cQt1,cQQ8_cQt8,cQQ8_ctBRe,cQQ8_ctGIm,cQQ8_ctj1,cQQ8_ctj8,cQQ8_ctWIm,cQQ8_ctWRe,cQQ8_cW,cQQ8,cQQ8m1,cQt1_cbHIm,cQt1_cjj11,cQt1_cjj18,cQt1_cjj31,cQt1_cjj38,cQt1_cll1,cQt1_cQt8,cQt1_ctBRe,cQt1_ctGIm,cQt1_ctj1,cQt1_ctj8,cQt1_ctWIm,cQt1_ctWRe,cQt1_cW,cQt1,cQt1m1,cQt8_cbHIm,cQt8_cjj11,cQt8_cjj18,cQt8_cjj31,cQt8_cjj38,cQt8_cll1,cQt8_ctBRe,cQt8_ctGIm,cQt8_ctj1,cQt8_ctj8,cQt8_ctWIm,cQt8_ctWRe,cQt8_cW,cQt8,cQt8m1,ctBRe_ctGIm,ctBRe_ctj1,ctBRe_ctj8,ctBRe_ctWIm,ctBRe_ctWRe,ctBRe,ctBRem1,ctGIm_ctj1,ctGIm_ctj8,ctGIm_ctWIm,ctGIm_ctWRe,ctGIm,ctGImm1,ctj1_ctj8,ctj1,ctj1m1,ctj8,ctj8m1,ctWIm_ctj1,ctWIm_ctj8,ctWIm_ctWRe,ctWIm,ctWImm1,ctWRe_ctj1,ctWRe_ctj8,ctWRe,ctWRem1,cW_cbHIm,cW_cjj11,cW_cjj18,cW_cjj31,cW_cjj38,cW_cll1,cW_ctBRe,cW_ctGIm,cW_ctj1,cW_ctj8,cW_ctWIm,cW_ctWRe,cW,cWm1"
    #w_names = w_names.split(",")

    #print(len(w_names))

    #find first  launch
    for line in contents:
        if "launch" in line: 
            weight_name = line.split("--rwgt_name=")[1].split("\n")[0]
            if "m1" in weight_name:
                op = weight_name.split("m1")[0]
                name = op + "_m1p0"
                ret_d[name] = {"wgtName": [weight_name], "values": [[-1.0]]}
                
            elif "_" in weight_name:
                ops = weight_name.split("_")
                name = "{}_1p0_{}_1p0".format(ops[0], ops[1])
                ret_d[name] = {"wgtName": [weight_name], "values": [[1.0, 1.0]]}

            else:
                name = weight_name + "_1p0"
                ret_d[name] = {"wgtName": [weight_name], "values": [[1.0]]}

    ret_d["SM"] = {"wgtName": ["w"], "values": [[0.0]]}

    return ret_d


def define_weights ( ):
  
   print(". . . @ @ @ Creating OP Mapping @ @ @ . . . ")

   
   ret_d = {}
