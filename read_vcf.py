#Script for reading VCF files and outputting a more user friendly table
#written in python 2.7
#Anne Sonnenschein
#10-30-2018

def main():
    info_list = read_VCF("Challenge_data.vcf")
    print_output(info_list, "Challenge_output.csv")
    

def read_VCF(filename):
    VCFfile = open(filename)
    header = VCFfile.readline()
    if "VCFv4.1" not in header:
        print "This script is written for VCFv4.1, and may not work as intendend"
    list_of_variants = []
    for line in VCFfile:
        if line[0] == "#":
            pass
        else:
            info_list = line_parse(line)
            list_of_variants.append(info_list)
    VCFfile.close()
    return(list_of_variants)

def line_parse(inline):
    myline = inline.split("\t")
    chromosome = myline[0]
    position = myline[1]
    ref = myline[3]
    alt = myline[4]
    if "," in alt:
        alt = alt.replace(",",":")
    info = myline[7]
    info_list = info.split(";")
    type = info_list[-1].split("=")[-1]
    if "ins" in type:
        type = "indel"
    elif "del" in type:
        type = "indel"
    #if "complex" in info_list[-1]:
    #    print ref, alt, info_list[-1]
    coverage_info = myline[9]
    depth = coverage_info.split(":")[2]
    ref_count = float(coverage_info.split(":")[4])
    alt_count = coverage_info.split(":")[6]
    if "," in alt_count:
        alt_list = alt_count.split(",")
        alt_count = sum([float(i) for i in alt_list])
    else:
        alt_count = float(coverage_info.split(":")[6])    
    ref_percent = str(100* ref_count/(ref_count + alt_count))[0:4]
    alt_percent = str(100* alt_count/(ref_count + alt_count))[0:4]
    return_line = [chromosome, position, ref, alt, type, depth,ref_percent,alt_percent]
    return(return_line)


def print_output(VCF_info, outfilename):
    outfile = open(outfilename, "w")
    outfile.write("Chromosome,Position,Reference_allele,Alternate_alleles,Variant_type,Depth_coverage,Percent_reads_supporting_reference,Percent_reads_supporting_variants\r\n")
    for each_var in VCF_info:
        outstring = ",".join(each_var)
        outfile.write(outstring)
        outfile.write("\r\n")
    outfile.close()

main()