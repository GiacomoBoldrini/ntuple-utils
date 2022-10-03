import argparse
import ROOT
import subprocess
import os
import glob
import shutil 
import sys
from itertools import combinations

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-r"    , "--root"         , dest="root", help="Original root file path that stores all the weights" , required=True, type=str)
    parser.add_argument('-b'    , '--doBatch'      , dest="doBatch", help="Run reading jobs on condor", default=False, action="store_true")
    parser.add_argument('-o'    , '--operators'    , dest="operators", help="Space separated list of operators to extract components", default=[], nargs="+")
    parser.add_argument('-sm'   , '--sm-weight'    , dest="smweight", help="The name of the SM weight in the root file, default is w nominal name", default="w")
    parser.add_argument('-v'    , '--vars'         , dest='vars', help='Only store these variables in output tree', required=False, default=[], nargs="+")
    parser.add_argument('-out'  , '--out'          , dest='out', help='Ouput path where to store ntuples', required=False, default="./")
    
    args = parser.parse_args()

    sample_name = args.root.split("/")[-1].split("ntuple_")[1].split(".root")[0]

    # just checks if we have every possible branch:
    weight_branches = args.operators + list(combinations(args.operators,2))

    
    f = ROOT.TFile(args.root)
    t = f.Get(sample_name)
    root_weight_branches = [i.GetName() for i in t.GetListOfBranches()]


    weight_names = []

    ok = True
    for i in weight_branches:
        if isinstance(i, str):
            if i not in root_weight_branches:  print("missing weight {}".format(i))
            else: weight_names.append(i)
            if i + "m1" not in root_weight_branches:  print("missing weight {}".format(i))
            else: weight_names.append(i+ "m1")
        elif isinstance(i, tuple):
            if (i[0] + "_" + i[1] in root_weight_branches): weight_names.append(i[0] + "_" + i[1]) 
            elif (i[1] + "_" + i[0] in root_weight_branches): weight_names.append(i[1] + "_" + i[0]) 
            else: print("missing weight {}".format(i[1] + "_" + i[0]))

    weight_names.append(args.smweight)

    """
    Structure of folders for this script:
    - readLhe.py
    - readLheScript.py
    - lheReaderFolder
        - jobs
            - Sample Name (gp_Zjj_ewk)
                - job_0
                    - config_0.py
                    - submit.jdl
                    ...
        - EFT_LHE
            - gp_ntuples
                - ntuple_sample_name_0.py
                ...
                - ntuple_sample_name.py (the complete one)
    """

    # this folder will contain ntuples from jobs and merged ones
    if os.path.islink("lheComponentFolder/EFT_LHE"):
       try: 
          os.makedirs("lheComponentFolder/EFT_LHE/gp_components")
       except: 
          pass
    else:
        print("You should create a symlink to your eos EFT_LHE inside lheReaderFolder")
        sys.exit(0)
    basefolder = "lheComponentFolder/jobs/"+sample_name
    try:
       os.makedirs(basefolder)
    except:
       pass

    if args.doBatch:
        nJobs = 1 + len(args.operators) * (len(args.operators) + 3) / 2 #both single and mixed interference
        # nJobs = 1
        print("Number of jobs: {}".format(nJobs))  

        shFile =  "#!/bin/bash\n"
        shFile += "export X509_USER_PROXY=/afs/cern.ch/user/g/gboldrin/proxy\n"
        shFile += "cd {} && eval `scramv1 runtime -sh`\n".format(os.path.abspath("."))
        shFile += "mkdir -p lheComponentFolder/jobs/{}/job_\"$1\"\n".format(sample_name)
        shFile += "python extractComponentCondorScript.py --root {} --ops $1 --out {} --vars {} --sm {}\n".format(args.root, args.out, " ".join(i for i in args.vars), args.smweight)
        with open('lheComponentFolder/readLheScript.sh', 'w') as file:
            file.write(shFile)
        process = subprocess.Popen("chmod +x lheComponentFolder/readLheScript.sh", shell=True)
        process.wait()
        

        # print("Submitting files", end='')
        print("Submitting files")

        ### Write .jdl 
        jdl = "Universe = vanilla\n"
        jdl += '+JobFlavour = "espresso"\n'
        jdl += "Executable = readLheScript.sh\n"
        jdl += "Arguments = $(proc)\n"
        jdl += "request_cpus = {}\n".format(2)
        jdl += "should_transfer_files = YES\n"
        jdl += "when_to_transfer_output = ON_EXIT\n"
        jdl += "Log = jobs/{}/job_$(proc)/job.log\n".format(sample_name)
        jdl += "Output = jobs/{}/job_$(proc)/job.out\n".format(sample_name)
        jdl += "Error = jobs/{}/job_$(proc)/job.err\n".format(sample_name)
        jdl += "Queue 1 proc in ({}) \n".format(" ".join(i for i in weight_names if ("m1" not in i and i != args.smweight)) + " SM")

        with open("lheComponentFolder/submit_{}.jdl".format(sample_name),"w") as file:
            file.write(jdl)

        workingPath = os.path.abspath(".")
        os.chdir("lheComponentFolder/")
        process = subprocess.Popen("condor_submit submit_{}.jdl".format(sample_name), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        process.wait()
        os.chdir(workingPath)


        print("\nSubmitted jobs to condor")
        
