#Script for reading VCF files and outputting a more user friendly table
#written in python 2.7
#Anne Sonnenschein
#10-30-2018

def main():
    info_list = read_VCF("Challenge_data.vcf")
    print_output(info_list, "Challenge_output.csv")
    

def read_VCF(filename):
    #checks VCF version number, sends each variant to the function line_parse
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
    #pulls out relevant information from variant lines
    myline = inline.split("\t")
    chromosome = myline[0]
    position = myline[1]
    ref = myline[3]
    alt = myline[4]
    if "," in alt:                 #checking if multiple variant alleles-- removing commas for future CSV file
        alt = alt.replace(",",":")
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
    if "," in alt_count:                 #if there's multiple alleles, reporting frequency for each separated by ":"
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