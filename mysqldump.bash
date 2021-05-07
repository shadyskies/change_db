DBNAME='emp'
TABLE='EMPLOYEE'

FNAME=/var/lib/mysql-files/$(date +%Y.%m.%d)-$DBNAME.csv

#(1)creates empty file and sets up column names using the information_schema
mysql -u 'django_projects' -p 'django_projects_pwd' $DBNAME -B -e "SELECT * FROM information_schema.COLUMNS C WHERE table_name = '$TABLE';" | awk '{print $1}' | grep -iv ^COLUMN_NAME$ | sed 's/^/"/g;s/$/"/g' | tr '\n' ',' > $FNAME

#(2)appends newline to mark beginning of data vs. column titles
echo "" >> $FNAME

#(3)dumps data from DB into /var/mysql/tempfile.csv
mysql -u 'django_projects' -p 'django_projects_pwd' $DBNAME -B -e "SELECT * INTO OUTFILE '/var/mysql-files/tempfile.csv' FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '\"' FROM $TABLE;"

#(4)merges data file and file w/ column names
cat /var/lib/mysql-files/tempfile.csv >> $FNAME

#(5)deletes tempfile
#rm -rf /var/mysql/tempfile.csv