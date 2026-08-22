# 🪟 Understanding Frames in Window Functions

![Topic](https://img.shields.io/badge/Topic-Window%20Functions-4a90d9?style=for-the-badge)
![SQL](https://img.shields.io/badge/SQL-MySQL%208.0-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![Type](https://img.shields.io/badge/Type-Concept%20Doc-f59e0b?style=for-the-badge)

---

### Not just `PARTITION BY` and `ORDER BY` — the part everyone skips until the numbers come out wrong.

*A row-by-row breakdown of how SQL actually decides which rows belong in a window — and why `ROWS` and `RANGE` can return two completely different answers for the same query.*

---

## 📌 Why This Doc Exists

[#-why-this-doc-exists](#-why-this-doc-exists)

Every window function tutorial covers `PARTITION BY` and `ORDER BY`, then quietly moves on. The frame clause — `ROWS BETWEEN ... AND ...` / `RANGE BETWEEN ... AND ...` — is the part that actually decides *which rows the function sees* for each row it computes. Skip understanding it, and a moving average or running total will silently return the wrong numbers the moment two rows tie.

This doc exists so I stop guessing at frame behavior and start reasoning about it.

## 🗂️ Table of Contents

[#️-table-of-contents](#️-table-of-contents)

- [What Is a Window Frame?](#-what-is-a-window-frame)
- [Frame Syntax Breakdown](#-frame-syntax-breakdown)
- [ROWS vs RANGE vs GROUPS](#-rows-vs-range-vs-groups)
- [Default Frame Behavior](#️-default-frame-behavior)
- [Practical Examples](#-practical-examples)
- [Common Pitfalls](#️-common-pitfalls)
- [SQL Quick-Reference Cheatsheet](#-sql-quick-reference-cheatsheet)
- [Concepts Used](#-concepts-used)
- [My Takeaway](#-my-takeaway)

---

## 🪟 What Is a Window Frame?

[#-what-is-a-window-frame](#-what-is-a-window-frame)

A window function operates on a **partition** (`PARTITION BY`), ordered by a column (`ORDER BY`) — but the **frame** is what decides which rows *inside* that partition are actually fed into the calculation for the current row.

> Partition answers "which group am I in?"
> Order answers "what's the sequence?"
> **Frame answers "how far left and right of me do I look?"**

Change only the frame, keep the same `SUM()` / `AVG()` / `FIRST_VALUE()` — the output changes. That's the whole reason frames deserve their own doc instead of a footnote.

## 🧩 Frame Syntax Breakdown

[#-frame-syntax-breakdown](#-frame-syntax-breakdown)

```sql
<window_function>() OVER (
    PARTITION BY <col>
    ORDER BY <col>
    <frame_unit> BETWEEN <frame_start> AND <frame_end>
)
```

| Piece | Options | Meaning |
|---|---|---|
| `frame_unit` | `ROWS`, `RANGE`, `GROUPS` | how the boundary is measured |
| `frame_start` / `frame_end` | `UNBOUNDED PRECEDING`, `N PRECEDING`, `CURRENT ROW`, `N FOLLOWING`, `UNBOUNDED FOLLOWING` | where the window opens and closes, relative to the current row |

If `frame_end` is omitted, it defaults to `CURRENT ROW`. If the whole frame clause is omitted, MySQL falls back to a default frame — covered below, and it's rarely the one you want.

## 📊 ROWS vs RANGE vs GROUPS

[#-rows-vs-range-vs-groups](#-rows-vs-range-vs-groups)

| Frame Unit | Counts by | How ties are handled | Support |
|---|---|---|---|
| `ROWS` | physical row position | each row counted independently, even if values tie | MySQL 8.0+, PostgreSQL, SQL Server |
| `RANGE` | the value in the `ORDER BY` column | all rows with the same value form one peer group and move together | MySQL 8.0+, PostgreSQL, SQL Server |
| `GROUPS` | number of distinct peer groups (each group of tied rows = 1 unit) | peer group treated as one step, but rows within it aren't merged into a single value | PostgreSQL 11+ — **not available in MySQL 8.0** |

The distinction only matters when there are **ties** in the `ORDER BY` column. No ties → `ROWS` and `RANGE` give identical results.

### Ties, side by side

```
id | amount
---+-------
 1 |  500
 2 |  500
 3 |  700
 4 |  900
```

Running total with `ORDER BY amount`:

```sql
-- ROWS: strictly physical, ties still get separate partial sums
SELECT id, amount,
  SUM(amount) OVER (ORDER BY amount ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS rows_total
FROM sales;
```

| id | amount | rows_total |
|---|---|---|
| 1 | 500 | 500 |
| 2 | 500 | **1000** |
| 3 | 700 | 1700 |
| 4 | 900 | 2600 |

```sql
-- RANGE: tied rows are one peer group, both jump to the group total together
SELECT id, amount,
  SUM(amount) OVER (ORDER BY amount RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS range_total
FROM sales;
```

| id | amount | range_total |
|---|---|---|
| 1 | 500 | **1000** |
| 2 | 500 | **1000** |
| 3 | 700 | 1700 |
| 4 | 900 | 2600 |

Same query, same data, different frame unit — row 1 gets `500` under `ROWS` and `1000` under `RANGE`. That gap is the entire reason this doc exists.

## ⚙️ Default Frame Behavior

[#️-default-frame-behavior](#️-default-frame-behavior)

| Situation | Implicit default frame |
|---|---|
| `ORDER BY` present, no frame clause written | `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW` |
| No `ORDER BY` at all | `RANGE BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING` (whole partition) |

This is why a plain `SUM(amount) OVER (ORDER BY sale_date)` quietly behaves like a running total (it's using the first default), while the same function with no `ORDER BY` sums the *entire partition* for every row. Same function, opposite behavior — and nothing in the syntax warns you.

## 💡 Practical Examples

[#-practical-examples](#-practical-examples)

**7-row moving average — always use `ROWS`, never leave it implicit:**

```sql
SELECT sale_date, amount,
  AVG(amount) OVER (
    ORDER BY sale_date
    ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
  ) AS moving_avg_7d
FROM sales;
```

**Running total per employee, reset by partition:**

```sql
SELECT employee_id, sale_date, amount,
  SUM(amount) OVER (
    PARTITION BY employee_id
    ORDER BY sale_date
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
  ) AS running_total
FROM sales;
```

**Centered frame — average of the row before and after:**

```sql
SELECT sale_date, amount,
  AVG(amount) OVER (
    ORDER BY sale_date
    ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING
  ) AS centered_avg
FROM sales;
```

## ⚠️ Common Pitfalls

[#️-common-pitfalls](#️-common-pitfalls)

- **Assuming a running total without an explicit frame.** `SUM() OVER (ORDER BY col)` works only because of the implicit `RANGE ... CURRENT ROW` default — write the frame explicitly so the query survives a refactor.
- **Using `RANGE` for a row-count-based moving average.** `RANGE BETWEEN 6 PRECEDING AND CURRENT ROW` doesn't mean "6 rows back" — it means "rows within 6 units of the current *value*." For a fixed-size window, `ROWS` is almost always what you want.
- **Forgetting `ORDER BY` flips the default frame to the whole partition.** A `SUM()` with no `ORDER BY` isn't a running total — it's the partition total, repeated on every row.
- **Expecting `GROUPS` in MySQL.** It's valid ANSI SQL and works in PostgreSQL, but MySQL 8.0 only implements `ROWS` and `RANGE`.

## 🧠 SQL Quick-Reference Cheatsheet

[#-sql-quick-reference-cheatsheet](#-sql-quick-reference-cheatsheet)

```sql
-- ✅ Fixed-size moving average (last N rows, inclusive)
AVG(amount) OVER (ORDER BY sale_date ROWS BETWEEN N-1 PRECEDING AND CURRENT ROW)

-- ✅ Running total that resets per group
SUM(amount) OVER (PARTITION BY grp ORDER BY dt ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)

-- ✅ Peer-group aware total (ties move together)
SUM(amount) OVER (ORDER BY amount RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)

-- ✅ Whole-partition total on every row (no ORDER BY = default frame is the full partition)
SUM(amount) OVER (PARTITION BY grp)

-- ✅ Centered window
AVG(amount) OVER (ORDER BY dt ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING)
```

## 📌 Concepts Used

[#-concepts-used](#-concepts-used)

`Window Functions` `PARTITION BY` `ORDER BY` `ROWS BETWEEN` `RANGE BETWEEN` `GROUPS` `UNBOUNDED PRECEDING` `CURRENT ROW` `Moving Average` `Running Total`

## 💭 My Takeaway

[#-my-takeaway](#-my-takeaway)

The frame is the actual mechanism, not a stylistic add-on — `PARTITION BY` and `ORDER BY` just set the stage, but `ROWS` vs `RANGE` decides what the function computes. Default to `ROWS` when I mean "a fixed number of rows," and only reach for `RANGE` when ties should genuinely be treated as one unit.

---

[![GitHub](https://img.shields.io/badge/GitHub-Rushit004-181717?style=flat-square&logo=github)](https://github.com/Rushit004)
[![LinkedIn](https://img.shields.io/badge/Let's_connect_on_LinkedIn-0077B5?style=flat-square&logo=linkedin&logoColor=white)](https://linkedin.com/in/rushit-tholiya-605341311)
[![Kaggle](https://img.shields.io/badge/Find_me_on_Kaggle-20BEFF?style=flat-square&logo=kaggle&logoColor=white)](https://www.kaggle.com/rushittholiya)

**If this helped you, a ⭐ keeps it alive.**