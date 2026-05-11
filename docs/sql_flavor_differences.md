---
title: Differences between SQL flavors
description: How SQL syntax differs across platforms such as Postgres, SQL Server, BigQuery
icon: material/database-search
---

# Differences between SQL flavors

## What's an SQL flavor?

SQL flavors are different implementations of SQL used by different data platforms. Like various dialects that belong to a single language. The core principles of SQL are the same but syntax, functions, data types, and performance-related features can differ.

Each of the following database / data warehouse uses its own version of SQL:  

- PostgreSQL
- Google BigQuery
- Snowflake
- MySQL
- Microsoft SQL Server (uses T-SQL)
- Oracle Database (uses PL/SQL)
- SQLite 

## What differs?

<div class="grid cards" markdown>

-   :material-database-check-outline:{ .lg .middle } __Concepts common to all flavors__

    ---

    - `SELECT`
    - `WHERE`
    - `JOIN`s
    - `GROUP BY`
    - `HAVING`
    - `ORDER BY`
    - `CASE WHEN`
    - `COALESCE`
    - `CAST`
    - CTEs
    - subqueries
    - window functions

-   :material-swap-horizontal-bold:{ .lg .middle } __Concepts that most differ__

    ---

    - Date functions
    - String functions
    - Quoting & naming tables and columns
    - Data types
    - `LIMIT` / `TOP` / `FETCH` syntax
    - Temporary tables
    - Stored procedures

</div>

### Data types


### Date functions


### Limiting rows


### String concatenation


### Handling null values


### Type casting


### Window functions


### Quoting table and column names


### Full table naming


### `GROUP BY` behavior


### CTEs


## Notes on BigQuery, Snowflake, Postgres

BigQuery: Columnar & cloud-native


