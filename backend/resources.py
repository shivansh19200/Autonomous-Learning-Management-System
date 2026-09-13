RESOURCE_STORE = [
 {"title":"DP Foundations — Tabulation patterns","topic":"Dynamic Programming","type":"Interactive lesson","minutes":60,"level":"intermediate","url":"https://cp-algorithms.com/dynamic_programming/intro-to-dp.html"},
 {"title":"0/1 Knapsack practice set","topic":"Dynamic Programming","type":"Question bank","minutes":75,"level":"intermediate","url":"https://atcoder.jp/contests/dp/tasks"},
 {"title":"Dijkstra & Bellman-Ford","topic":"Advanced Graph Algorithms","type":"Concept lesson","minutes":60,"level":"intermediate","url":"https://cp-algorithms.com/graph/dijkstra.html"},
 {"title":"Graph shortest paths quiz","topic":"Advanced Graph Algorithms","type":"Adaptive quiz","minutes":35,"level":"intermediate","url":"https://cp-algorithms.com/graph/bellman_ford.html"},
 {"title":"Fenwick Trees / BIT","topic":"Segment Trees / Fenwick Trees","type":"Concept lesson","minutes":55,"level":"intermediate","url":"https://cp-algorithms.com/data_structures/fenwick.html"},
 {"title":"KMP & Z-function patterns","topic":"String Algorithms","type":"Concept lesson","minutes":50,"level":"intermediate","url":"https://cp-algorithms.com/string/prefix-function.html"}
]

def retrieve(topic, max_items=2):
    exact = [r for r in RESOURCE_STORE if r['topic'].lower() == topic.lower()]
    return exact[:max_items] or RESOURCE_STORE[:max_items]
