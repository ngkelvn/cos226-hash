#Author: Kelvin Nana Gyebi

"""
COS 226 - Hash Something Out

This program builds two hash tables from MOCK_DATA.csv: one keyed by movie title,
the other keyed by movie quote in order to store and retrieve movie records.
It then prints out wasted space, collisions, and  the build time for each table.

The collision methods I'll be implementing:
  chaining - for this, each bucket is a linked list and new records go at the end.
  probing  - linear probing; on a full slot, step to the next one.
A collision is only counted every time a spot we look at is filled or already holds data.
"""


import csv
import os
import time

# SETTINGS: they change for each attempt
ATTEMPT = 1                # which optimization attempt this run represents
METHOD = "chaining"        # "chaining" (linked list) or linear probing
HASH = "sum"               # "sum" (poor), "poly" (good), "fnv" (good)
SIZE = 15013               # number of slots



def sum_hash(key):
    """Poor: add character codes. Order is ignored and values bunch together."""
    total = 0
    for ch in key:
        total += ord(ch)
    return total


def poly_hash(key):
    """Good: h = h*31 + c. Position matters, so values spread out."""
    h = 0
    for ch in key:
        h = (h * 31 + ord(ch)) % 2**32
    return h


def fnv_hash(key):
    """Good: FNV-1a. XOR each byte in, then multiply to mix the bits."""
    h = 2166136261
    for b in key.encode("utf-8"):
        h = ((h ^ b) * 16777619) % 2**32
    return h


HASHES = {"sum": sum_hash, "poly": poly_hash, "fnv": fnv_hash}


class Node:
    def __init__(self, key, record):
        self.key = key
        self.record = record
        self.next = None


def build_chaining(rows, field, hash_fn):
    """Linked list per bucket. Each node walked past = 1 collision."""
    table = [None] * SIZE
    collisions = 0
    for row in rows:
        key = row[field].strip()
        if key == "":
            continue
        i = hash_fn(key) % SIZE
        if table[i] is None:
            table[i] = Node(key, row)
            continue
        node = table[i]
        collisions += 1
        while node.next is not None:
            node = node.next
            collisions += 1
        node.next = Node(key, row)
    return table, collisions


def get_chaining(table, key, hash_fn):
    """Retrieve the record stored under key or None if it isn't there."""
    node = table[hash_fn(key) % SIZE]
    while node is not None:
        if node.key == key:
            return node.record
        node = node.next
    return None


def build_probing(rows, field, hash_fn):
    """One record per slot. Each occupied slot stepped past = 1 collision."""
    table = [None] * SIZE
    collisions = 0
    for row in rows:
        key = row[field].strip()
        if key == "":
            continue
        i = hash_fn(key) % SIZE
        steps = 0
        while table[i] is not None and steps < SIZE:
            collisions += 1
            steps += 1
            i = (i + 1) % SIZE
        if steps < SIZE:
            table[i] = (key, row)
    return table, collisions


def get_probing(table, key, hash_fn):
    """Retrieve the record stored under key, or None if it is not there."""
    i = hash_fn(key) % SIZE
    steps = 0
    while table[i] is not None and steps < SIZE:
        if table[i][0] == key:
            return table[i][1]
        i = (i + 1) % SIZE
        steps += 1
    return None


def main():
    if not os.path.isfile("MOCK_DATA.csv"):
        print("MOCK_DATA.csv not found. Put it next to this script.")
        return
    with open("MOCK_DATA.csv", newline="", encoding="utf-8", errors="replace") as f:
        rows = list(csv.DictReader(f))

    if METHOD == "probing" and SIZE < len(rows):
        print("Linear probing needs SIZE >= number of rows ({})".format(len(rows)))
        return

    build = build_chaining if METHOD == "chaining" else build_probing
    get = get_chaining if METHOD == "chaining" else get_probing
    hash_fn = HASHES[HASH]
    print("Attempt {} | Method: {} | Hash: {} | Size: {:,}\n".format(ATTEMPT, METHOD, HASH, SIZE))

    for field, label in (("movie_title", "Title table"), ("quote", "Quote table")):
        start = time.perf_counter()
        table, collisions = build(rows, field, hash_fn)
        seconds = time.perf_counter() - start
        empty = table.count(None)
        print(label)
        print("  Wasted space: {:,} empty ({:.1f}%)".format(empty, 100 * empty / SIZE))
        print("  Collisions  : {:,}".format(collisions))
        print("  Build time  : {:.4f} s".format(seconds))
        sample = rows[0][field].strip()
        found = get(table, sample, hash_fn) is not None
        print("  Retrieval   : '{}' -> {}\n".format(sample, "found" if found else "NOT found"))


main()
