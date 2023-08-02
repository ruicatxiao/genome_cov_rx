import argparse

def read_fai_file(fai_filename):
    chromosome_lengths = {}

    with open(fai_filename, 'r') as fai_file:
        for line in fai_file:
            chromosome, length = line.strip().split('\t')[:2]
            chromosome_lengths[chromosome] = int(length)

    return chromosome_lengths

def calculate_chromosome_coverage(filename, chromosome_lengths, coverage_threshold):
    chromosome_coverages = {}

    with open(filename, 'r') as file:
        for line in file:
            chromosome, start, end, coverage = line.strip().split()
            start, end, coverage = int(start), int(end), int(coverage)
            
            if coverage >= coverage_threshold:
                if chromosome not in chromosome_coverages:
                    chromosome_coverages[chromosome] = 0
                chromosome_coverages[chromosome] += end - start + 1

    return chromosome_coverages

def calculate_total_coverage(chromosome_coverages, chromosome_lengths):
    total_covered_bases = sum(chromosome_coverages.values())
    total_genome_size = sum(chromosome_lengths.values())
    total_coverage_percentage = (total_covered_bases / total_genome_size) * 100
    return total_coverage_percentage

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Calculate chromosome and genome coverage.')
    parser.add_argument('filename', type=str, help='Input bedgraph file')
    parser.add_argument('fai_filename', type=str, help='.fai file with chromosome lengths')
    parser.add_argument('coverage_threshold', type=int, help='Coverage threshold')

    args = parser.parse_args()

    chromosome_lengths = read_fai_file(args.fai_filename)
    chromosome_coverages = calculate_chromosome_coverage(args.filename, chromosome_lengths, args.coverage_threshold)
    total_coverage_percentage = calculate_total_coverage(chromosome_coverages, chromosome_lengths)
    
    print("Chromosome Coverage:")
    for chromosome, covered_bases in chromosome_coverages.items():
        chromosome_coverage_percentage = (covered_bases / chromosome_lengths[chromosome]) * 100
        print(f"{chromosome}: {chromosome_coverage_percentage:.2f}%")

    print(f"\nTotal Genome Coverage: {total_coverage_percentage:.2f}%")
