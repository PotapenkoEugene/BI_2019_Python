
class ToManyArgumentsError(BaseException):
    def __init__(self, option):
        self.option = option
    def __str__(self):
        return f'Too many arguments for {self.option} option.'

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('fastq_file', type=str, help="for input need fastq file")
parser.add_argument('--min_length', nargs=1, type=int, help='min length of reads')
parser.add_argument('--keep_filtered', action='store_true', help='Make additional file for failed reads')
parser.add_argument('--gc_bounds', nargs='+',
                    help='Take min GC%% or min and max GC%%')  # берутся только первые два значения
parser.add_argument('--output_base_name', type=str, help='Name for output files')
args = parser.parse_args().__dict__

if args['output_base_name'] is None:  # output_base_name arg
    filename = args['fastq_file'].split('.')[0]
else:
    filename = args['output_base_name']

if args['keep_filtered'] is True:  # keep filtered arg
    w_failed = open(filename + '__failed', 'w')  # save failed reads
w_passed = open(filename + '__passed', 'w')

gc_bound = 0  # number of given gc_bound arguments
if args['gc_bounds'] is not None:
    if len(args['gc_bounds']) == 1:
        gc_bound = 1
        min_gc = int(args['gc_bounds'][0])  # gc_bound arg
    elif len(args['gc_bounds']) == 2:
        gc_bound = 2
        min_gc = int(args['gc_bounds'][0])
        max_gc = int(args['gc_bounds'][1])
    else:
        raise ToManyArgumentsError('gc_bounds') # raise error if more than 2 args

with open(args['fastq_file']) as f:
    for sequence in f:  # iter our file by samples
        readname = sequence.rstrip()
        seq = next(f).rstrip().upper()
        plusline = next(f).rstrip()  # often just '+' character line
        quality = next(f).rstrip().upper()
        qualityPhred = [ord(phredscore)-33 for phredscore in quality]  # get Sanger Phred scores of seq
        passed = True

        if args['min_length'] is not None:  # check length
            if len(seq) < args['min_length'][0]:
                passed = False

        if gc_bound != 0:  # check gc_bound
            for nucleotide in seq:
                GC_content = ((seq.count('G') + seq.count('C')) / len(seq)) * 100
                if gc_bound == 1:
                    if GC_content < min_gc:  # filter by min GC%
                        passed = False
                elif gc_bound == 2:
                    if GC_content < min_gc or GC_content > max_gc:  # filter by min and max GC%
                        passed = False

        if passed is True:  # Writing passed read
            w_passed.write(readname + '\n' +
                           seq + '\n' +
                           plusline + '\n' +
                           quality + '\n')
        if passed is False and args['keep_filtered'] is True:  # Writing failed read
            w_failed.write(readname + '\n' +
                           seq + '\n' +
                           plusline + '\n' +
                           quality + '\n')

w_passed.close()  # close files
if args['keep_filtered'] is True:
    w_failed.close()

