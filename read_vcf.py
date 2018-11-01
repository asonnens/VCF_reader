#Script for reading VCF files and outputting a more user friendly table
#written in python 2.7
#Anne Sonnenschein
#11-1-2018

import requests
import json


def read_VCF(filename):
    #checks VCF version number, sends each variant to the function line_parse
    VCFfile = open(filename)
    header = VCFfile.readline()
    print "0% complete"
    if "VCFv4.1" not in header:
        print "This script is written for VCFv4.1, and may not work as intended"
    num_lines = sum(1 for line in open(filename))  #setting a counter because the API step is a little slow
    counter = 0
    list_of_variants = []
    for line in VCFfile:
        counter = counter + 1
        progress = 100 * float(counter)/num_lines
        if (progress > 5) and (progress%5 == 0):
            print progress, "% complete"
        if line[0] == "#":
            pass
        else:
            info_list = line_parse(line)
            list_of_variants.append(info_list)
    VCFfile.close()
    return(list_of_variants)

def line_parse(inline):
    #pulls out relevant information from variant lines
    myline = inline.split("\t")
    chromosome = myline[0]
    position = myline[1]
    coding_status = "error"
    gene = "error"
    ref = myline[3]
    alt = myline[4]
    if "," in alt:                 #checking if multiple variant alleles-- removing commas for future CSV file
        variant_list = alt.split(",")
        exac_info_list = [check_coding(chromosome,position,ref,i) for i in variant_list]
        coding_list = exac_info_list[0]
        gene_list = exac_info_list[1]  
        if "intergenic" in coding_list:
            coding_status = "intergenic"
            gene = "NA"
        else:
            coding_status = ":".join(coding_list)
            gene = gene_list[0]         
        alt = alt.replace(",",":")
    else:
        exac_info_list = check_coding(chromosome,position,ref,alt) 
        coding_status = exac_info_list[0]
        gene = exac_info_list[1]
    info = myline[7]
    info_list = info.split(";")
    type = info_list[-1].split("=")[-1]
    if "," in type:
        type = type.replace(",",":")      #classifying type of multiple variant alleles
    if "ins" in type:             
        type = type.replace("ins","insertion")
    if "del" in type:
        type = type.replace("del","deletion")
    coverage_info = myline[9]
    depth = coverage_info.split(":")[2]
    ref_count = float(coverage_info.split(":")[4])
    alt_count = coverage_info.split(":")[6]
    ref_percent = "error"
    alt_percent = "error"
    if "," in alt_count:                 #if there are multiple alleles, frequency for each separated by ":"
        alt_list = alt_count.split(",")
        alt_sum = sum([float(i) for i in alt_list])
        ref_percent = str(100* ref_count/(ref_count + alt_sum))[0:4]
        alt_percent = [str(100 * (float(i)/(ref_count + alt_sum)))[0:4] for i in alt_list] 
        alt_percent = ":".join(alt_percent)
    else:
        alt_count = float(coverage_info.split(":")[6])
        alt_sum = alt_count  
        alt_percent = str(100* alt_count/(ref_count + alt_sum))[0:4]  
        ref_percent = str(100* ref_count/(ref_count + alt_sum))[0:4]
    return_line = [chromosome,position,gene,type,coding_status,ref,alt,depth,ref_percent,alt_percent]
    return(return_line)

def check_coding(chrom,pos,ref,alt):
    #checks if a variant falls within a coding, intronic, or intergenic region by basically turning the API into a string. 
    more_info = requests.get("http://exac.hms.harvard.edu/rest/variant/" + chrom + "-" + pos + "-" + ref + "-" + alt)
    coding = "error"
    gene = "error"
    if more_info == "FALSE":
        coding = "no_data"
        gene = "no_data"
        print chrom, pos, " no ExAc match"
    else:
        data = more_info.json()
        decoded = json.dumps(data)
        relevant_info =  decoded[0:100]
        if "null" in relevant_info:
            coding = "null_no_gene"
            gene = "null_no_gene"
        else:
            workaround = relevant_info.split(":")[1]
            workaround = workaround.replace("_variant","")
            workaround = workaround.replace('"','')
            workaround = workaround.replace("{","")
            coding = workaround.strip()  
            if "}" in coding:              #?? No gene, consequence, etc. information reported for this variant
                coding = "no_data"
                gene = "no_data" 
            else:
                gene = relevant_info.split(":")[2]
                gene = gene.replace('"','')
                gene = gene.replace("{","")  
                gene = gene.strip()
    return_list = [coding,gene]
    return(return_list)

def print_output(VCF_info, outfilename):
    #prints the output of line_parse to a comma separated text file
    outfile = open(outfilename, "w")
    outfile.write("Chromosome,Position,Gene,Variant_type,Impact,Reference_allele,Alternate_alleles,Depth_coverage,Percent_reads_supporting_reference,Percent_reads_supporting_variants\r\n")
    for each_var in VCF_info:
        outstring = ",".join(each_var)
        outstring.replace(", ",",")
        outfile.write(outstring)
        outfile.write("\r\n")
    outfile.close()

def main():
    info_list = read_VCF("Challenge_data.vcf")
    print_output(info_list, "Challenge_output.csv")
    print "100% complete"
main()