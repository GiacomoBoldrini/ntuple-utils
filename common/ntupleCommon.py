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
    base = "rwgt"

    ret_d = {}

    #find first  launch
    for idx,line in enumerate(contents):
        if "launch" in line: break

    #if base weight name changed we can retrieve it (not optimally but still)
    for line in contents[:idx]:
        if "change rwgt_dir" in line:
            base = line.split(" ")[-1].strip("\n")


    #cycle through reweights
    count_rwgt = 1
    while(idx < len(contents)):

        current_rwgt = []
        rwgt_name = base + "_" + str(count_rwgt)

        idx += 1
        while(1):
            if idx >= len(contents): break
            if "launch" in contents[idx]: break 
            if contents[idx] == "\n" or contents[idx].startswith("#"): 
                idx += 1
                continue
            
            op_name, op_val = contents[idx].split(" ")[-2], float(contents[idx].split(" ")[-1].strip("\n"))
            if convert_names != None: 
                op_name = convert_names[op_name]
                
            if op_val != 0:
                current_rwgt.append([ op_name, op_val])
            idx += 1

        name = "_".join(i[0] + "_" + str(i[1]).replace("-", "m").replace(".", "p") for i in current_rwgt) #join names of every op turned on e.g. 2 1\n 5 0\n 9 1 -> 2_9
        vals = [i[1] for i in current_rwgt]
        if len(name) == 0: name = "SM"

        if name not in ret_d.keys():
            ret_d[name] = {"wgtName": [rwgt_name], "values": [vals]}
        else:
            ret_d[name]["wgtName"].append(rwgt_name)
            ret_d[name]["values"].append([vals])

        count_rwgt += 1

        


    return ret_d
