# for outputting to csv -->
# for server side: COPY (SELECT * FROM foo) TO <location> WITH CSV DELIMITER ',' HEADER;
from sqlalchemy import create_engine


def pg_dump():
    db = create_engine('postgresql://postgres:@localhost/practice')
    db.execute("COPY emp to '/tmp/practice2.csv' DELIMITER ',' CSV HEADER;")


def get_intopostgres():
    db = create_engine('postgresql://postgres:@localhost/practice')

    db.execute("CREATE TABLE IF NOT EXISTS temp (name text, yearsofexp int, age int, salary int)")
    db.execute("INSERT INTO temp (name, yearsofexp, age, salary) VALUES ('Doctor Strange', 1, 1, 1)")


get_intopostgres()