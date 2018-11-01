# VCF_reader

Anne Sonnenschein  
11/1/2018

###Purpose
The script read_vcf.py takes information from a VCF file, annotates it using the ExAc genome browser.

Each variant is output as a row, with the headers:
Chromosome,Position,Gene,Variant_type,Impact,Reference_allele,Alternate_alleles,Depth_coverage,Percent_reads_supporting_reference,Percent_reads_supporting_variants


###To run:

python2.7 read_vcf.py

###To use on other VCF files
To change the files that are parsed with this script, or to change the name of the output file, modify lines 10 and 11 of the script, in the main function.



###Additional notes

This script is written in Python 2.7.

This script takes about 15 minutes to run on the original VCF file. While it's running, the terminal output will show progress. In retrospect, this script could probably be sped up by using a batch API command.

**The VCF file and ExAC genome browser are both using the coordinate system for hg19/GRCh37** 

This script was written for VCF format VCFv4.1. It may not be compatible with other VCF file types. 

For other types of VCF files, and additional functionality, the PyVCF Python package, VCFTools, and commands within Samtools may be more useful.