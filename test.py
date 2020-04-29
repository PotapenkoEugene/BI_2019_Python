import unittest
import random
import fastq_filter as ff


class TestBadBedTools(unittest.TestCase):
    def test_min_length(self):
        result = True
        for i in range(1000):
            length = random.randint(0, 250)
            seq = 'A' * length
            res = ff.min_length(seq, 50)
            if res:
                if length < 50 or len(seq) == 0:
                    result = False
                    break
        self.assertTrue(result)

    def test_gc_bound(self):
        result = True
        for i in range(1000):
            length = random.randint(0, 250)
            seq = ''.join([random.choice('AT') for i in range(length)])
            gc_length = random.randint(0, 250)
            gc_seq = seq + ('C' * gc_length)
            gc_range = [random.randint(0, 100), random.randint(0, 100)]
            res = ff.gc_bounds(gc_seq, gc_range)
            if gc_length != 0:
                gc_content = (gc_length / len(gc_seq)) * 100
            else:
                gc_content = 0

            if (gc_content < gc_range[0] or
                gc_content > gc_range[1] or
                len(gc_seq) == 0) and res:
                result = False
                break
        self.assertTrue(result)

    def test_leading(self):
        phred33_above_20 = "56789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~"
        phred33_under_20 = '!\"#$%&\'()*+,-./01234'
        result = True
        for i in range(1000):
            norm_qual_length = random.randint(0, 250)
            low_qual_length = random.randint(0, 250)
            seq_length = norm_qual_length + low_qual_length
            seq = ''.join([random.choice('ATGC') for i in range(seq_length)])
            norm_quality = ''.join([random.choice(phred33_above_20) for i in range(norm_qual_length)])
            low_quality = ''.join([random.choice(phred33_under_20) for i in range(low_qual_length)])
            quality = low_quality + norm_quality  # фигачим лоу квалити в начало

            trimmed_seq, trimmed_quality = ff.leading(seq, quality, 20)
            if len(trimmed_seq) != norm_qual_length:
                result = False
        self.assertTrue(result)

    def test_trailing(self):
        phred33_above_20 = "56789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~"
        phred33_under_20 = '!\"#$%&\'()*+,-./01234'
        result = True
        for i in range(1000):
            norm_qual_length = random.randint(0, 250)
            low_qual_length = random.randint(0, 250)
            seq_length = norm_qual_length + low_qual_length
            seq = ''.join([random.choice('ATGC') for i in range(seq_length)])
            norm_quality = ''.join([random.choice(phred33_above_20) for i in range(norm_qual_length)])
            low_quality = ''.join([random.choice(phred33_under_20) for i in range(low_qual_length)])
            quality = norm_quality + low_quality  # фигачим лоу квалити в конец

            trimmed_seq, trimmed_quality = ff.trailing(seq, quality, 20)
            if len(trimmed_seq) != norm_qual_length:
                result = False
        self.assertTrue(result)

    def test_crop(self):
        result = True
        for i in range(1000):
            base_length = random.randint(0, 250)
            base_seq = ''.join([random.choice('ATGC') for i in range(base_length)])
            cut = random.randint(0, 250)
            cut_seq = ''.join(['!' for i in range(cut)])
            full_seq = base_seq + cut_seq
            quality = full_seq  # тут квалити неважно просто создаем строку той же длинны
            crop_seq, crop_qual = ff.crop(full_seq, quality, base_length)  # режем до определенной длинны
            if len(crop_seq) != base_length or \
                    len(crop_qual) != base_length or \
                    '!' in crop_seq:
                result = False
                break
        self.assertTrue(result)

    def test_headcrop(self):
        result = True
        for i in range(1000):
            base_length = random.randint(0, 250)
            base_seq = ''.join([random.choice('ATGC') for i in range(base_length)])
            cut = random.randint(0, 250)
            cut_seq = ''.join(['!' for i in range(cut)])
            full_seq = cut_seq + base_seq
            quality = full_seq  # тут квалити неважно просто создаем строку той же длинны
            crop_seq, crop_qual = ff.headcrop(full_seq, quality, cut)  # отрезаем сначала столько-то
            if len(crop_seq) != base_length or \
                    len(crop_qual) != base_length or \
                    '!' in crop_seq:
                result = False
                break
        self.assertTrue(result)

    def test_slidingwindow(self):
        phred33 = "!\"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~"
        random.seed(11)
        result = True
        for i in range(1000):
            length = random.randint(0, 250)
            seq = ''.join([random.choice('ATGC') for i in range(length)])
            winsize = random.randint(1, 10)
            threshold = random.randint(10, 30)

            # генерим последовательность квалити добавляя по одному случайному символу качества
            quality = []
            first_time = True
            cut_length = length  # по-умолчания весь рид хорош

            if length >= winsize:
                for i in range(0, length):
                    qual = random.choice(phred33)
                    quality.append(qual)

                    if i > winsize - 2:  # -1 поправка на индекс и еще -1 на то что входит [a,b)
                        qualityPhred = [ord(phredscore) - 33 for phredscore in quality[i - winsize + 1:]]
                        if sum(qualityPhred) / winsize < threshold and first_time:
                            if len(quality) > winsize:
                                cut_length = len(quality) - 1  # в прошлом цикле все было ок сохраняем длинну
                            else:
                                cut_length = 0
                            first_time = False
            else:
                quality = [random.choice(phred33) for i in range(length)]
                qualityPhred = [ord(phredscore) - 33 for phredscore in quality]
                if length == 0 or (sum(qualityPhred) / len(quality) < threshold):
                    cut_length = 0

            trim_seq, trim_qual = ff.slidingwindow(seq, quality, winsize, threshold)
            if len(trim_seq) != cut_length:
                result = False

        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
