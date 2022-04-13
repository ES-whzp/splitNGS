import argparse
import csv
import os
import time

from xopen import xopen

def makeDir(path):
    if not os.path.exists(path):
        os.mkdir(path)

def write2fq(readsDic, saveDir):
    for k, v in readsDic.items():
        for RN, data in v.items():
            # fo = xopen(os.path.join(saveDir, '%s_%s_fq.gz'%(k, RN)), mode="a", threads=nThreads, compresslevel=3)
            fo = open(os.path.join(saveDir, '%s_%s.fastq' % (k, RN)), 'a')
            fo.write(''.join(data))
            fo.close()

def compare2Reads(r1Seq, r2Seq, barcodeDic):
    barcodeName = '0'
    for k, v in barcodeDic.items():
        if (v[0] in r1Seq and v[1] in r2Seq) or (v[0] in r2Seq and v[1] in r1Seq):
        # if (r1Seq.startswith(v[0]) and r2Seq.startswith(v[1])) or (r1Seq.startswith(v[1]) and r2Seq.startswith(v[0])):
            barcodeName = k
            break
    return barcodeName


def split(r1Path, r2Path, barcodeCSVPath, saveDir, nThreads):
    start = time.time()
    print('%s splitting NO.%d reads...' % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), 1))

    barcodeDic = {}
    with open(barcodeCSVPath, 'r') as fb:
        fbc = csv.reader(fb)
        for row in fbc:
            barcodeDic[row[0]] = [row[1], row[2]]

    f1 = xopen(r1Path, mode="r", threads=nThreads)
    f2 = xopen(r2Path, mode="r", threads=nThreads)
    n = 0
    readsDic = {}
    while True:
        r1Line = f1.readline()
        r2Line = f2.readline()
        if r1Line == '':
            break
        if n % 4 == 0:
            r1Header, r2Header = r1Line, r2Line
        if n % 4 == 1:
            r1Seq, r2Seq = r1Line, r2Line
            barcodeName = compare2Reads(r1Seq, r2Seq, barcodeDic)
        if n % 4 == 2:
            r1ID, r2ID = r1Line, r2Line
        if n % 4 == 3:
            r1Qual, r2Qual = r1Line, r2Line
            if barcodeName != '0':
                readsDic[barcodeName] = readsDic.get(barcodeName, {'R1':[], 'R2':[]})
                readsDic[barcodeName]['R1'].extend([r1Header, r1Seq, r1ID, r1Qual])
                readsDic[barcodeName]['R2'].extend([r2Header, r2Seq, r2ID, r2Qual])
        n += 1
        if n % 400000 == 0:
            print('%s splitting NO.%d reads...\r' % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), int(n/4)), end='')
            write2fq(readsDic, saveDir)
            readsDic = {}
        # if n > 400000:
        #     break
    write2fq(readsDic, saveDir)
    f1.close()
    f2.close()
    print('%s Split Completely, time consuming: %f seconds' % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), time.time() - start))


parser = argparse.ArgumentParser(description='An easy-to-use tool for splitting the NGS data according to custom barcode', formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument('-r1', '--read1', nargs=1, metavar='', help='read 1 Path', type=str)
parser.add_argument('-r2', '--read2', nargs=1, metavar='', help='read 2 path', type=str)
parser.add_argument('-b', '--barcode', nargs=1, metavar='', help="barcode Path. only support'.csv' format", type=str)
parser.add_argument('-t', '--thread', nargs=1, metavar='', help="thread of process. default is 4", default=4, type=int)
parser.add_argument('-o', '--output', nargs=1, metavar='', help="directory path for storing the split files. directory would be generated automatically if not existed.", type=str)


nThreads = 6
saveDir = r'C:\transfer\NGS\split'
makeDir(saveDir)
barcodeCSVPath = r'C:\transfer\NGS\20220312barcode.csv'
r1Path = r'C:\transfer\NGS\WZP20220305_R1_001.fastq.gz'
r2Path = r'C:\transfer\NGS\WZP20220305_R2_001.fastq.gz'

args = parser.parse_args()
r1Path = args.read1[0]
r2Path = args.read2[0]
barcodeCSVPath = args.barcode[0]
nThreads = args.thread[0]
saveDir = args.output[0]
split(r1Path, r2Path, barcodeCSVPath, saveDir, nThreads)

