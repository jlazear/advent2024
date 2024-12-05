from functools import cmp_to_key
from collections import defaultdict

with open("input.txt", 'r') as f:
    rules, updates = f.read().split('\n\n')

lefts = defaultdict(list)
rights = defaultdict(list)

for rule in rules.split():
    left, right = rule.split('|')
    lefts[left].append(right)
    rights[right].append(left)

def cmp(a, b):
    if a in lefts and b in lefts[a]:
        return -1
    elif a in rights and b in rights[a]:
        return 1
    else:
        return 0
key = cmp_to_key(cmp)

s = 0
for update in updates.strip().split('\n'):
    pages = update.split(',')
    sorted_pages = sorted(pages, key=key)
    if pages != sorted_pages:
        mid = int(sorted_pages[len(sorted_pages)//2])
        s += mid

print(s)
