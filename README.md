```
$ ./random_genomic_interval.py --help
usage: random_genomic_interval.py [-h] [-n N] [-s SEED] ref.fai length

Randomly sample genomic intervals.

positional arguments:
  ref.fai               Fasta index for the genome reference.
  length                Length of the desired genomic interval.

optional arguments:
  -h, --help            show this help message and exit
  -n N                  Number of intervals to print.
  -s SEED, --seed SEED  Seed for the random number generator.
```

Get ten 100k intervals from human reference.
```
$ ./random_genomic_interval.py -n 10 -s 1234 hs37d5.fasta.fai 100k
1:118308257-118408257
17:12165978-12265978
2:216628059-216728059
6:22531996-22631996
18:47598385-47698385
14:4135787-4235787
1:4252131-4352131
11:129988772-130088772
6:39877333-39977333
18:15356248-15456248
```
