# VCF_reader

Anne Sonnenschein  
11/1/2018

### Purpose
The script read_vcf.py takes information from a VCF file, annotates it using the Broad Institute's ExAc genome browser, and outputs it to a csv file that can be opened in a text editor or spreadsheet.

Each variant is output as a row, with the headers:
Chromosome, Position, Gene, Variant type, Impact, Reference allele, Alternate alleles, Depth coverage, Percent reads supporting reference, Percent reads supporting variants

Variant types include SNPs, MNPs (multiple nucleotide polymorphisms), insertions and deletions. In some cases a variant is labeled as 'complex', which indicates multiple non-consecutive SNPs.

The Impact describes type of mutation if they occur within a transcriptional unit. Categories include, nonsense, missense, synonymous, within the UTR or a splice site, or intronic. 

There are some instances where ExAc identifies the consequence as 'null', but does not report a gene. I originally assumed these were intergenic, but checking a few of these by hand on UCSC suggests that isn't the case. These are recorded as "null no gene" in the output.

When there are multiple variants in the same position, the alleles are reported within the same column, separated by a colon- the percentage of reads supporting each alternate variant allele are also separated by a colon.

### To run:

>python2.7 read_vcf.py

### To use on other VCF files
To change the files that are parsed with this script, or to change the name of the output file, modify lines 126 and 127 of the script, in the main function.


### Additional notes

This script is written in Python 2.7.

This script takes about 5 minutes to run on the original VCF file. While it's running, the terminal output will show progress. In retrospect, this script could probably be sped up by using a batch API command.

**The VCF file and ExAC genome browser are both using the coordinate system for hg19/GRCh37** 

This script was written for VCF format VCFv4.1. It may not be compatible with other VCF file types. 

For other types of VCF files, and additional functionality, the PyVCF Python package, the Broad Institute's GATK tool, VCFTools, and commands within Samtools may be more useful.