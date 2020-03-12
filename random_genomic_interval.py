#!/usr/bin/env python3
import random


def random_genomic_interval(rng, fai, cum_weights, length):
    """
    Returns a `length` sized genomic interval.

    The chromosome is drawn from available chromosomes listed in `fai`,
    in proportion to their size. The position is drawn uniformly from the
    chromosome.
    """
    chrom, size = rng.choices(fai, cum_weights=cum_weights)[0]
    assert size > length
    pos = rng.randrange(0, size - length)
    return chrom, pos, pos+length


def simple_chrom_name(chrom):
    if chrom.startswith("chr"):
        chrom = chrom[3:]
    return chrom.lower()


def parse_fai(fn, min_length=1000, exclude={"x", "y", "m", "mt"}):
    fai = []
    with open(fn) as f:
        for line in f:
            fields = line.split()
            chrom = fields[0]
            size = int(fields[1])
            if simple_chrom_name(chrom) in exclude:
                continue
            if size < min_length:
                continue
            fai.append((chrom, size))

    if len(fai) == 0:
        raise RuntimeError(
                f"{fn}: no chromosomes found "
                f"(min_length={min_length}, exclude={exclude}).")

    # Sort the list by size. This makes random chromosome selection slightly
    # faster, as our distribution function (the cumulative weights) has more
    # mass at the start of the array.
    fai.sort(key=lambda a: a[1])

    cum_weights = []
    for i, (chrom, size) in enumerate(fai):
        cum_weights.append(size if i == 0 else size + cum_weights[i-1])

    return fai, cum_weights


def parse_args():
    import argparse
    parser = argparse.ArgumentParser(
            description="Randomly sample genomic intervals.")

    def length(arg, parser=parser):
        x = 1
        if arg[-1] == "k":
            x = 1000
            arg = arg[:-1]
        elif arg[-1] == "m":
            x = 1000 * 1000
            arg = arg[:-1]
        try:
            arg = int(arg)
        except ValueError:
            parser.error(
                    "Length must be an integer, with optional suffix 'k' or 'm'.")
        return x * arg

    parser.add_argument(
            "-n", type=int, default=1,
            help="Number of intervals to print.")
    parser.add_argument(
            "-s", "--seed", type=int, default=None,
            help="Seed for the random number generator.")
    parser.add_argument(
            "fai_file", metavar="ref.fai",
            help="Fast index for the genome reference.")
    parser.add_argument(
            "length", type=length,
            help="Length of the desired genomic interval.")

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    fai, cum_weights = parse_fai(args.fai_file, min_length=args.length)
    rng = random.Random(args.seed)
    for _ in range(args.n):
        chrom, start, end = random_genomic_interval(
                rng, fai, cum_weights, args.length)
        print(f"{chrom}:{start}-{end}")
