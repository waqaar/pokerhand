import collections
import argparse


def check_rank(hand, d):
    if royal_flush(hand):
        return 10
    elif straight_flush(hand, d):
        return 9
    elif four_of_kind(hand, d):
        return 8
    elif full_house(hand, d):
        return 7
    elif flush(hand):
        return 6
    elif straight(hand, d):
        return 5
    elif three_of_kind(hand, d):
        return 4
    elif two_pair(hand, d):
        return 3
    elif pair(hand, d):
        return 2
    else:
        return 1

#  function for different ranks ------------------------


def royal_flush(hand):
    hand_value = [value[0] for value in hand]
    e = [e[1] for e in hand]
    suit = ["T", "J", "Q", "K", "A"]
    if len(set(e)) == 1:
        return all(item in hand_value for item in suit)


def flush(hand):
    hand_value = [value[1] for value in hand]
    if len(set(hand_value)) == 1:
        return True


def straight(hand, d):
    hand_value = [value[0] for value in hand]
    hand_value_key = connect(hand_value, d)
    return sorted(hand_value_key) == list(range(min(hand_value_key), max(hand_value_key)+1))


def straight_flush(hand, d):
    return straight(hand, d) and flush(hand)


def high_card(a, b, d):

    i = set(a).intersection(set(b))
    k1 = list(set(a).difference(i))
    k2 = list(set(b).difference(i))
    if max(k1) > max(k2):
        return 1
    elif max(k1) < max(k2):
        return 2


def two_pair(hand, d):
    hand_value = [value[0] for value in hand]
    hand_value_key = connect(hand_value, d)
    di = di_rep(hand_value_key)
    if sorted(di.values()) == [1, 2, 2]:
        return True


def three_of_kind(hand, d):
    hand_value = [value[0] for value in hand]
    hand_value_key = connect(hand_value, d)
    di = di_rep(hand_value_key)
    if sorted(set(di.values())) == [1, 3]:
        return True


def full_house(hand, d):
    hand_value = [value[0] for value in hand]
    hand_value_key = connect(hand_value, d)
    di = di_rep(hand_value_key)
    if sorted(set(di.values())) == [2, 3]:
        return True


def four_of_kind(hand, d):
    hand_value = [value[0] for value in hand]
    hand_value_key = connect(hand_value, d)
    di = di_rep(hand_value_key)
    if sorted(set(di.values())) == [1, 4]:
        return True


def pair(hand, d):
    hand_value = [value[0] for value in hand]
    hand_value_key = connect(hand_value, d)
    di = di_rep(hand_value_key)
    if sorted(di.values()) == [1, 1, 1, 2]:
        return True

# functions to reassign string value of cards to int value


def connect(l, d):
    hand_value_key = []
    for x in l:
        hand_value_key.append(d[x])
    return hand_value_key


def di_rep(hand_value_key):
    di = collections.defaultdict(lambda: 0)
    for value in hand_value_key:
        di[value] += 1
    return di

# draw function when both player have same rank hand


def draw(h1, h2, d, rank):
    hand1_value = [value[0] for value in h1]
    hand1_value_key = connect(hand1_value, d)
    hand2_value = [value[0] for value in h2]
    hand2_value_key = connect(hand2_value, d)

    di1 = di_rep(hand1_value_key)
    di2 = di_rep(hand2_value_key)
    max_value_key1 = max(di1, key=di1.get)
    max_value_key2 = max(di2, key=di2.get)

    max_value1 = max(di1.values())
    max_value2 = max(di2.values())
    min_value1 = min(di1.values())
    min_value2 = min(di2.values())

    max_keys1 = [k for k, v in di1.items() if v == max_value1]
    max_keys2 = [k for k, v in di2.items() if v == max_value2]

    min_keys1 = [k for k, v in di1.items() if v == min_value1]
    min_keys2 = [k for k, v in di2.items() if v == min_value2]

    if rank == 1:
        return high_card(hand1_value_key, hand2_value_key,d)
    elif rank == 2:
        if max_value_key1 > max_value_key2:
            return 1
        elif max_value_key1 < max_value_key2:
            return 2
        elif max_value_key1 == max_value_key2:
            i = set(hand1_value_key).intersection(set(hand2_value_key))
            k1 = list(set(hand1_value_key).difference(i))
            k2 = list(set(hand2_value_key).difference(i))
            if max(k1) > max(k2):
                return 1
            elif max(k1) < max(k2):
                return 2
    elif rank == 3:
        if max(max_keys1) > max(max_keys2):
            return 1
        elif max(max_keys1) < max(max_keys2):
            return 2
        elif min(max_keys1) > min(max_keys2):
            return 1
        elif min(max_keys1) < min(max_keys2):
            return 2
        elif min_keys1 > min_keys2:
            return 1
        elif min_keys1 < min_keys2:
            return 2

# argument parser used to take input from command line if not required remove three lines below


ap = argparse.ArgumentParser()
ap.add_argument("-i", "--text", required=True, help="Path to the text_file")
args = vars(ap.parse_args())

# input txt file
# when running file from pycharm replace  with "path of txt file" and remove three line of argument parse from above


with open(args["text"]) as f:
    lines = [line.rstrip() for line in f]

d = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "T": 10, "J": 11, "Q": 12, "K": 13, "A": 14}

hand1_score = 0
hand2_score = 0

for h in lines:
    temp = h.split()
    hand1 = temp[0:5]
    hand2 = temp[5:]

    hand1_rank = check_rank(hand1, d)
    hand2_rank = check_rank(hand2, d)

    if hand1_rank > hand2_rank:
        hand1_score += 1
    elif hand1_rank < hand2_rank:
        hand2_score += 1
    elif hand1_rank == hand2_rank:
        res = draw(hand1, hand2, d, hand1_rank)
        if res == 1:
            hand1_score += 1
        elif res == 2:
            hand2_score += 1

print("PLAYER1 SCORE:{}".format(hand1_score))
print("PLAYER2 SCORE:{}".format(hand2_score))