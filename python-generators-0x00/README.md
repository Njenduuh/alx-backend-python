# Python Generators - MySQL Streaming

This project demonstrates how to use **Python generators** with **MySQL** to stream data from a database one row at a time. It includes:

- Setting up a MySQL database and table
- Loading user data from a CSV file
- Inserting the data into the table (avoiding duplicates)
- Querying the database
- (Optional) Using a generator to yield rows lazily

---

## 🔧 Requirements

- Python 3.x
- MySQL Server installed and running
- `mysql-connector-python` package

Install the connector:

```bash
pip install mysql-connector-python
