# COS 226 – Hash Something Out

Kelvin Nana Gyebi

Two hash tables built in Python from 'MOCK_DATA.csv': one of them is keyed by movie title, one the other one is keyed by movie quote. Each run reports wasted space, collisions, and build time.

## How to run

Start by setting the four SETTINGS lines at the top of 'hash_tables.py', then run 'python3 hash_tables.py'.

## Results

\ # | Method         | Hash            | Size   | Title: empty / collisions   | Quote: empty / collisions   | Build time (title / quote) |

| 1 | Linked list    | Sum of chars    | 15,013 | 11,262 (75.0%) / 45,598     | 12,290 (81.9%) / 56,718     | 0.0159 s / 0.0291 s        |
| 2 | Linked list.   | Polynomial ×31  | 15,013 | 7,063 (47.0%) / 12,118      | 5,555 (37.0%) / 7,650       | 0.0262 s / 0.0434 s        |
| 3 | Linear probing | Sum of chars    | 30,011 | 15,011 (50.0%) / 87,842,966 | 15,011 (50.0%) / 92,757,007 | 5.8937 s / 6.3418 s        |
| 4 | Linear probing | FNV-1a          \ 30,011 | 15,011 (50.0%) / 17,290.    | 15,011 (50.0%) / 7,891      | 0.0254 s / 0.0402 s        |
| 5 | Linked list    | FNV-1a          | 11,251 | 4,111 (36.5%) / 14,771      | 2,982 (26.5%) / 10,045      | 0.0277 s / 0.0433 s        |

Screenshots: [1](screenshots/attempt1.png) · [2](screenshots/attempt2.png) · [3](screenshots/attempt3.png) · [4](screenshots/attempt4.png) · [5](screenshots/attempt5.png)

## Reflection

### Attempt 1 – Linked list, poor hash

This served as the baseline, utilizing an intentionally poor hash that sums up the key's character codes. 75.0% of title buckets and 81.9% of quoted buckets remained empty, indicating poor performance on wasted space. Anagrams constantly collide because adding characters disregards their order. Because most keys are short strings of comparable length, their sums fall within a small range of values. Only roughly 3,751 different sums were generated from the 11,309 unique titles, and only roughly 2,723 from the 14,891 unique quotes. This resulted in a limited number of lengthy chains. 

### Attempt 2 – Linked list, good hash

I just updated the hash function to a polynomial rolling hash (h = h * 31 + c), leaving the linked-list table and size unchanged. Collisions decreased by 87% for quotes (56,718 → 7,650) and 73% for titles (45,598 → 12,118). The percentage of wasted space decreased to 37.0% and 47.0%. Because each character's position matters when multiplying by 31 at each stage, similar keys result in wildly different values that are dispersed throughout the whole table. Because 3,700 titles are duplicates that end up in the same bucket as their last copy, the title table still has more empty buckets than the quote table.



### Attempt 3 – Linear probing, poor hash

By far the worst outcome came from switching to linear probing with the poor sum hash: 87,842,966 title collisions, 92,757,007 quote collisions, and almost 6 seconds to generate each table, as opposed to hundredths of a second for every other attempt. Primary clustering is the reason. The majority of keys are sent into the same small range of slots via the sum hash. Construction is O(n^2) since they combine into a single massive run of occupied slots, and each new insert must walk nearly the whole run to find a free slot. The majority of keys still fell into the same band, therefore doubling the table size to 30,011 hardly made a difference. 


### Attempt 4 – Linear probing, good hash

The clustering issue was resolved by simply changing the hash to FNV-1a while maintaining the same probing table. Build time decreased from around 6 seconds to 0.03 seconds, and collisions decreased from roughly 88 million to 17,290 for titles and from roughly 93 million to 7,891 for quotes. Because FNV-1a incorporates all of the input into the output, keys are distributed uniformly and clusters remain brief. The catch is wasted space: 50% of the table is always empty since linear probing requires more slots than records.


### Attempt 5 – Optimized linked list

Of the first four, Attempt 2 had the best balance. It used half the table area and had collisions that were comparable to or less than those in attempt 4. I reduced the table to 11,251 buckets and switched to FNV-1a to further optimize it. A smaller table fills more linked lists than buckets because linked lists can hold more records than buckets, unlike probing. Wasted space decreased by 42% and 46% from attempt 2 to 36.5% for titles and 26.5% for quotes, the lowest of all five tries. Although build time remained relatively constant, the trade-off was an increase in collisions of 22% for titles and 31% for quotes. 


### Comparison and conclusion

The collision approach was less important than the hash function. While the poor hash ranged from bad (attempt 1) to terrible (attempt 3), every attempt with a good hash built in a few hundredths of a second. With linked lists, a bad hash can survive because only the impacted chains grow; however, linear probing turns it into one, massive cluster. Table size becomes the primary trade-off once the hash is good; a larger table results in fewer collisions but more wasted space. Attempt 5 displays the opposite extreme (26.5–36.5% empty, higher collisions) than Attempt 4 (50% empty, low collisions).

Overall, I would prefer attempt 5. It had the least wasted space of any attempt while utilizing the smallest table, and its collisions remained within the same range as the other good-hash attempts, with chains still short enough to keep build time constant. 