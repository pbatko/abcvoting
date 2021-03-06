"""Proposition A.3
from the survey: "Approval-Based Multi-Winner Voting:
Axioms, Algorithms, and Applications"
by Martin Lackner and Piotr Skowron
"""

from __future__ import print_function
import sys
sys.path.insert(0, '..')
from abcvoting import abcrules
from abcvoting.preferences import Profile
from abcvoting import misc


print(misc.header("Proposition A.3", "*"))

num_cand = 8
a, b, c, d, e, f, g, h = list(range(num_cand))  # a = 0, b = 1, c = 2, ...
names = "abcdefgh"

monotonicity_instances = [
    ("seqphrag", 3,  # from Xavier Mora, Maria Oliver (2015)
     [[0, 1]] * 10 + [[2]] * 3 + [[3]] * 12 + [[0, 1, 2]] * 21 + [[2, 3]] * 6,
     True, [0, 1], [[0, 1, 3]], [[0, 2, 3], [1, 2, 3]]),
    ("seqphrag", 3,  # from Xavier Mora, Maria Oliver (2015)
     [[2]] * 7 + [[0, 1]] * 4 + [[0, 1, 2]] + [[0, 1, 3]] * 16 + [[2, 3]] * 4,
     False, [0, 1], [[0, 1, 2]], [[0, 2, 3], [1, 2, 3]]),
    ("rule-x", 3,
     [[1, 3], [0, 1], [1, 3, 4], [0, 4], [2, 3, 4], [2, 4], [2, 3, 4], [0, 2, 4], [1, 2, 3]],
     True, [0], [[0, 3, 4]], [[1, 2, 4]]),
    ("rule-x", 3,
     [[2, 4], [0, 1], [0, 4], [3, 4], [0, 1, 2], [3, 4], [1, 2, 4], [3, 4], [2, 4], [0, 1, 2], [1, 3], [2, 4], [0, 3], [3, 4], [2, 3], [1, 2, 3], [1, 2, 4], [1, 3], [2, 4]],
     False, [1, 3], [[1, 3, 4]], [[2, 3, 4]]),
    ("revseqpav", 3,
     [[0, 4], [1, 2, 3], [3, 4], [2, 4], [1, 3, 4], [2, 4], [0, 1, 2], [2, 3, 4], [0, 3, 4], [1, 3], [0, 4], [0, 3, 4], [0, 1], [0, 3], [0, 1, 3], [2, 4], [1, 2, 3], [1, 2]],
     False, [2, 3], [[2, 3, 4]], [[1, 3, 4]]),
    ("greedy-monroe", 3,
     [[1, 2, 3], [0, 2, 5], [0, 3, 4], [2, 4], [0, 1], [3, 5], [3, 5], [1, 4], [1, 5]],
     True, [4], [[1, 4, 5]], [[1, 2, 3]]),
    ("pav", 4,  # from Sanchez-Fernandez and Fisteus (2019)
     [[0, 1], [0, 1, 2], [4, 5], [4, 5]] + [[0, 4], [1, 4], [2, 4], [0, 5], [1, 5], [2, 5], [0, 6], [1, 6], [2, 6]] * 3 + [[3]] * 100,
     False, [2, 3], [[0, 1, 2, 3]], [[3, 4, 5, 6]]),
    ("cc", 3,  # from Sanchez-Fernandez and Fisteus (2019)
     [[a], [a, d], [a, e], [c, d], [c, e], [b]] * 2 + [[d]],
     False, [b, c], [[a, b, c]], [[a, b, c], [b, d, e]]),
    ("monroe", 4,
     [[a, e]] * 5 + [[a, g]] * 4 + [[b, e]] * 5 + [[b, h]] * 4 + [[c, f]] * 5 + [[c, g]] * 4 + [[d, f]] * 3 + [[d, h]] * 3,
     True, [e], [[e, f, g, h]], [[a, b, c, d], [e, f, g, h]]),
    ("monroe", 3,
     [[a], [a, d], [a, e]] * 2 + [[b], [c, d]] * 4 + [[b, e]] + [[c, e]] * 3,
     False, [b, c], [[a, b, c]], [[a, b, c], [b, d, e]]),
    ("seqpav", 3,
     [[1, 2], [1, 3], [4, 5], [0, 4], [2, 5], [0, 1], [1, 5], [0, 4]],
     False, [4, 5], [[1, 4, 5]], [[0, 1, 5], [1, 4, 5]]),
    ("optphrag", 6,  # from Sanchez-Fernandez and Fisteus (2019)
     [[1, 2, 3, 4, 5]] * 13 + [[0, 6], [0]] * 2 + [[6]] * 1,
     True, [0, 1, 2, 3, 4, 5], [[0, 1, 2, 3, 4, 5], [1, 2, 3, 4, 5, 6]],
     [[0, 1, 2, 3, 4, 6], [0, 1, 2, 3, 5, 6], [0, 1, 2, 4, 5, 6], [0, 1, 3, 4, 5, 6], [0, 2, 3, 4, 5, 6]]),
    ("optphrag", 6,  # from Sanchez-Fernandez and Fisteus (2019)
     [[7]] + [[1, 2, 3, 4, 5]] * 13 + [[0, 6], [0]] * 2 + [[6]] * 1,
     False, [0, 1, 2, 3, 4, 5], [[0, 1, 2, 3, 4, 5], [1, 2, 3, 4, 5, 6]],
     [[0, 1, 2, 3, 4, 6], [0, 1, 2, 3, 5, 6], [0, 1, 2, 4, 5, 6], [0, 1, 3, 4, 5, 6], [0, 2, 3, 4, 5, 6]]),
]


for inst in monotonicity_instances:
    (rule_id, committeesize, apprsets,
     addvoter, extravote, commsfirst, commsafter) = inst

    print(misc.header(abcrules.rules[rule_id].longname, "-"))

    profile = Profile(num_cand, names=names)
    profile.add_preferences(apprsets)
    origvote = set(apprsets[0])
    print(profile.str_compact())

    # irresolute if possible
    if False in abcrules.rules[rule_id].resolute:
        resolute = False
    else:
        resolute = True

    committees = abcrules.compute(
        rule_id, profile, committeesize, resolute=resolute)
    print("original winning committees:\n"
          + misc.str_candsets(committees, names))
    # verify correctness
    assert committees == commsfirst
    some_variant = any(all(c in comm for c in extravote) for comm in commsfirst)
    all_variant = all(all(c in comm for c in extravote) for comm in commsfirst)
    assert some_variant or all_variant
    if all_variant:
        assert not all(all(c in comm for c in extravote) for comm in commsafter)
    else:
        assert not any(all(c in comm for c in extravote) for comm in commsafter)

    if addvoter:
        print("additional voter: " + misc.str_candset(extravote, names))
        apprsets.append(extravote)
    else:
        apprsets[0] = list(set(extravote) | set(apprsets[0]))
        print("change of voter 0: "
              + misc.str_candset(list(origvote), names)
              + " --> "
              + misc.str_candset(apprsets[0], names))

    profile = Profile(num_cand, names=names)
    profile.add_preferences(apprsets)

    committees = abcrules.compute(
        rule_id, profile, committeesize, resolute=resolute)
    print("\nwinning committees after the modification:\n"
          + misc.str_candsets(committees, names))

    # verify correctness
    assert committees == commsafter

    print(abcrules.rules[rule_id].shortname + " fails ", end="")
    if addvoter:
        if len(extravote) == 1:
            print("candidate", end="")
        else:
            print("support", end="")
        print(" monotonicity with additional voters")
    else:
        if len(set(extravote) - origvote) == 1:
            print("candidate", end="")
        else:
            print("support", end="")
        print(" monotonicity without additional voters")
    print()
