import argparse


class ToManyArgumentsError(BaseException):
    def __init__(self, option):
        self.option = option

    def __str__(self):
        return f'Too many arguments for {self.option} option.'


# Create functions
def min_length(seq: str, minlen):
    if len(seq) < minlen:
        return False
    return True


def gc_bounds(seq: str, gcbound):
    if len(seq) == 0:
        return False
    if len(gcbound) == 1:
        min_gc = int(gcbound[0])  # gc_bound arg
        max_gc = 100
    elif len(gcbound) == 2:
        min_gc = int(gcbound[0])
        max_gc = int(gcbound[1])
    else:
        raise ToManyArgumentsError('gc_bounds')  # raise error if more than 2 args

    GC_content = ((seq.upper().count('G') + seq.upper().count('C')) / len(seq)) * 100
    if GC_content < min_gc or GC_content > max_gc:  # filter by min and max GC%
        return False
    return True


def leading(seq: str, qual: str, LEADING):
    if len(seq) == 0:
        return ['', '']
    qualityPhred = [ord(phredscore) - 33 for phredscore in qual]
    for i in range(len(seq)):
        if qualityPhred[i] >= LEADING:
            break
        elif i == len(seq) - 1:  # если и последний нукл не годится возвращаем пустую последовательность
            return ['', '']
    return [seq[i:], qual[i:]]


def trailing(seq: str, qual: str, TRAILING):
    if len(seq) == 0:
        return ['', '']
    qualityPhred = [ord(phredscore) - 33 for phredscore in qual]
    for i in range(len(seq) - 1, -1, -1):
        if qualityPhred[i] >= TRAILING:
            break
        elif i == 0:  # если и последний нукл не годится возвращаем пустую последовательность
            return ['', '']
    return [seq[:i + 1], qual[:i + 1]]


def crop(seq, qual, CROP):
    if len(seq) == 0:
        return ['', '']
    return [seq[:CROP], qual[:CROP]]


def headcrop(seq, qual, HEADCROP):
    if len(seq) == 0:
        return ['', '']
    return [seq[HEADCROP:], qual[HEADCROP:]]

# мой слайдинг виндоу отрезает все что находится справа от 1го нуклеотида
# который говнякает качество окна ниже трешхолда, триммоматик отрезает больше все время
def slidingwindow(seq, qual, window_size, required_quality):
    if len(seq) == 0:
        return ['', '']
    # если длинна рида меньше чем окно проверяем среднее качество по длинне рида
    qualityPhred = [ord(phredscore) - 33 for phredscore in qual]
    if len(seq) < window_size:
        if sum(qualityPhred) / len(qualityPhred) < required_quality:
            return ['', '']
        return [seq, qual]

    cut = False
    for i in range(window_size, len(seq)+1):
        if (sum(qualityPhred[i - window_size: i]) / window_size) < required_quality:
            cut = True
            break

    if cut and i == window_size:
        return ['', '']  # если первое же окно с плохим качеством кушаем весь рид

    elif cut:
        return [seq[:i - 1], qual[:i - 1]] # если нет обрезаем до последнего окна с хорошим качеством(вкл
    # если вся последовательность хороша:
    else:
        return [seq, qual]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('fastq_file', type=str,
                        help="For input need fastq file")
    parser.add_argument('-m', '--min_length', type=int,
                        help='Min length of reads')
    parser.add_argument('-k', '--keep_filtered', action='store_true',
                        help='Make additional file for failed reads')
    parser.add_argument('-g', '--gc_bounds', nargs='+',
                        help='Take min GC%% or min and max GC%%')
    parser.add_argument('-o', '--output_base_name', type=str,
                        help='Name for output files')
    parser.add_argument('-l', '--leading', type=int,
                        help='Cut bases off the start of a read, if below a threshold quality')
    parser.add_argument('-t', '--trailing', type=int,
                        help='Cut bases off the end of a read, if below a threshold quality')
    parser.add_argument('-c', '--crop', type=int,
                        help='Cut the read to a specified length by removing bases from the end')
    parser.add_argument('-hc', '--headcrop', type=int,
                        help='Cut the specified number of bases from the start of the read')
    parser.add_argument('-s', '--slidingwindow', nargs=2,
                        help="""Performs a sliding window trimming approach.
                             It starts scanning at the 5‟ end and clips the read once
                             the average quality within the window falls below a threshold.""")
    args = parser.parse_args().__dict__

    # work with arguments
    if args['output_base_name'] is None:  # output_base_name arg
        outfile_name = '.'.join(args['fastq_file'].split('.')[:-1])  ##
    else:
        outfile_name = args['output_base_name']
    extension = '.' + args['fastq_file'].split('.')[-1]  ##

    if args['keep_filtered'] is True:  # keep filtered arg
        w_failed = open(outfile_name + '_failed' + extension, 'w')  # save failed reads
    w_passed = open(outfile_name + '_passed' + extension, 'w')

    minlen = args['min_length']
    gcbound = args['gc_bounds']
    lead = args['leading']
    trail = args['trailing']
    crop_num = args['crop']
    headcrop_num = args['headcrop']
    slidewin = args['slidingwindow']
    # open file
    f = open(args['fastq_file'])
    # read fastq file
    eat_count = 0
    ml_block_count = 0
    gc_block_count = 0
    for sequence in f:  # iter our file by samples
        readname = sequence.rstrip()
        seq = next(f).rstrip()  # НЕ ИЗМЕНЯТЬ ИСХОДНЫЕ РЕГИСТР
        plusline = next(f).rstrip()  # often just '+' character line
        quality = next(f).rstrip()

        # modify sequences
        if crop is not None:
            seq, quality = crop(seq, quality, crop_num)
        if headcrop_num is not None:
            seq, quality = headcrop(seq, quality, headcrop_num)
        if lead is not None:
            seq, quality = leading(seq, quality, lead)
        if trail is not None:
            seq, quality = trailing(seq, quality, trail)
        if slidewin is not None:
            window_size, required_quality = map(int, slidewin)
            seq, quality = slidingwindow(seq, quality, window_size, required_quality)
            # break
        if len(seq) == 0:
            eat_count += 1
            continue

        # Check sequences:
        if minlen is not None:
            ml_passed = min_length(seq, minlen)
            ml_block_count += not ml_passed
        else:
            ml_passed = True

        if gcbound is not None:
            gc_passed = gc_bounds(seq, gcbound)
            gc_block_count += not gc_passed
        else:
            gc_passed = True

        passed = [ml_passed, gc_passed]

        if all(passed):  # Writing passed read
            w_passed.write(readname + '\n' +
                           seq + '\n' +
                           plusline + '\n' +
                           quality + '\n')
        elif args['keep_filtered'] is True:  # Writing failed read
            w_failed.write(readname + '\n' +
                           seq + '\n' +
                           plusline + '\n' +
                           quality + '\n')
    # close files
    f.close()
    w_passed.close()
    if args['keep_filtered'] is True:
        w_failed.close()

    # Statistics

    if eat_count > 0:
        print(f'Total reads consumed(length equal zero after trim): {eat_count}')
    if ml_block_count > 0:
        print(f'Total reads dropped by minlength {ml_block_count}')
    if gc_block_count > 0:
        print(f'Total reads dropped by gc_bound {gc_block_count}')
