import random, time
ai_elective = {"192311001", "192311004", "192311007", "192311009"}
iot_elective = {"192311002", "192311004", "192311009", "192311010"}
all_students = {f"1923110{i:02d}" for i in range(1, 11)}
# TODO 1 (operators)
both = ai_elective & iot_elective
exactly_one = ai_elective ^ iot_elective
neither = all_students - (ai_elective | iot_elective)
print("clash:", sorted(both))
print("exactly one:", sorted(exactly_one))
print("neither:", sorted(neither))
# Same result using methods
both_m = ai_elective.intersection(iot_elective)
exactly_one_m = ai_elective.symmetric_difference(iot_elective)
neither_m = all_students.difference(ai_elective.union(iot_elective))
print("methods agree:", both == both_m, exactly_one == exactly_one_m, neither == neither_m)
print("only AI:", sorted(ai_elective - iot_elective), "| only IoT:", sorted(iot_elective - ai_elective))
print("union:", len(ai_elective | iot_elective))
print("\n--- duplicates removed ---")
regs = ["192311001", "192311004", "192311001", "192311004", "192311007"]
print(regs, "->", sorted(set(regs)))
print("\n--- edge cases ---")
empty = set()
print("empty & AI :", empty & ai_elective, "| empty | AI size:", len(empty | ai_elective))
print("AI & AI    :", len(ai_elective & ai_elective), "| AI ^ AI:", ai_elective ^ ai_elective)
print("sets of lists:", end=" ")
try:
    {[1, 2]}
except TypeError as e:
    print("TypeError:", e)
print("set of tuples:", {(1, 2), (1, 2), (3, 4)})
def best(f, k=3):
    m = 1e9
    for _ in range(k):
        t = time.perf_counter(); f(); m = min(m, time.perf_counter() - t)
    return m
print("\n--- membership: x in list vs x in set (worst case, 200 lookups of last item) ---")
print(f"{'n':>9} {'list (s)':>12} {'set (s)':>12}")
for n in (10_000, 100_000, 1_000_000):
    L = list(range(n)); S = set(L); x = n - 1
    tl = best(lambda: [x in L for _ in range(200)], 1)
    ts = best(lambda: [x in S for _ in range(200)])
    print(f"{n:>9} {tl:>12.5f} {ts:>12.6f}")
print("\n--- common students: nested loops vs & ---")
print(f"{'n':>7} {'nested (s)':>12} {'& (s)':>10} {'same':>6}")
random.seed(3)
for n in (1000, 3000, 10_000):
    A = random.sample(range(5 * n), n); B = random.sample(range(5 * n), n)
    def nested():
        out = []
        for a in A:
            for b in B:
                if a == b:
                    out.append(a); break
        return out
    t1 = best(nested, 1)
    t2 = best(lambda: set(A) & set(B))
    print(f"{n:>7} {t1:>12.4f} {t2:>10.6f} {set(nested()) == set(A) & set(B)!s:>6}")
print("\n--- sorted merge walk (O(n log n + m log m)) ---")
def common_sorted(A, B):
    A, B = sorted(A), sorted(B)
    i = j = 0; out = []
    while i < len(A) and j < len(B):
        if A[i] == B[j]: out.append(A[i]); i += 1; j += 1
        elif A[i] < B[j]: i += 1
        else: j += 1
    return out
n = 100_000
A = random.sample(range(5 * n), n); B = random.sample(range(5 * n), n)
print("n=100000 sorted-walk:", round(best(lambda: common_sorted(A, B)), 4), "s | set &:", round(best(lambda: set(A) & set(B)), 4), "s")
print("\n--- hand check on small case ---")
X, Y = {1, 2, 3}, {2, 3, 4}
print("X&Y", X & Y, "X|Y", X | Y, "X-Y", X - Y, "X^Y", X ^ Y)
