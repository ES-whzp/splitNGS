# splitNGS
usage: splitNGS.py [-h] [-r1] [-r2] [-b] [-t] [-o]

An easy-to-use tool for splitting the NGS data according to custom barcode

optional arguments:

  -h, --help       show this help message and exit
	
  -r1 , --read1    read 1 Path
	
  -r2 , --read2    read 2 path
	
  -b , --barcode   barcode Path. only support'.csv' format
	
  -t , --thread    thread of process. default is 4
	
  -o , --output    directory path for storing the split files. directory would be generated automatically if not existed.
	
