import os
from pathlib import Path


def create_synthetic_dataset():
    # Clean code sample
    Path("sample_test_repo/clean_code").mkdir(parents=True, exist_ok=True)
    with open("sample_test_repo/clean_code/simple_app.py", "w") as f:
        f.write("""
def greet(name: str):
    return f"Hello, {name}"

def main():
    print(greet("World"))
        """)

    # Bad code samples
    Path("sample_test_repo/bad_code").mkdir(parents=True, exist_ok=True)
    with open("sample_test_repo/bad_code/god_function.py", "w") as f:
        f.write("""
def process_data(data, config, logger, retries, timeout, user, password, host, port, db, table, transform, notify, validate, backup):
    # This function is too long and has too many parameters
    if data and config:
        print("Processing...")
        if retries > 0:
            for i in range(retries):
                if timeout > 10:
                    if user and password:
                        if host and port:
                            if db and table:
                                if transform:
                                    print("All checks passed")
    # ... more code
    a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z = 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26
    # ... many more lines
    print("Done")
        """)
    with open("sample_test_repo/bad_code/deep_nesting.py", "w") as f:
        f.write("""
def deep_nesting(a,b,c):
    if a:
        if b:
            if c:
                for i in range(10):
                    while i > 5:
                        if i % 2 == 0:
                            print("Deep")
def unused_function():
    pass
        """)

    # SQL files
    Path("sample_test_repo/sql_files").mkdir(parents=True, exist_ok=True)
    with open("sample_test_repo/sql_files/queries.sql", "w") as f:
        f.write("""
SELECT * FROM users;
DELETE FROM logs;
UPDATE products SET price = 20 WHERE name = 'Hardcoded';
SELECT name, (SELECT MAX(price) FROM products) AS max_price FROM users;
        """)
