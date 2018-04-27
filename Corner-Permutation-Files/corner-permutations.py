import itertools
one = "(          -43.3658,          -27.7628,          -108.505)\n"
two = "(          40.4625,          -28.3072,          -109.141)\n"
three = "(          -42.6901,          32.66,          -106.815)\n"
four = "(          40.6664,          33.5728,          -109.175)\n"

res = list(itertools.permutations(([one, two, three, four])))

for i in range(0, len(res)):
    file = open("file {}.txt".format(i), "w")
    final = "(0.0186967, -0.0280729, 0.999431), -96.9056\n" + "".join(res[i])
    file.write(final)
