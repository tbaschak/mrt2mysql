# mrt2mysql
takes output from bgpscanner and converts it into mysql inserts

## Usage

This shell script loops through a large list of ASNs and pipes them into the script:

```
for as in `cat ca-asn-latest.txt`; do
 echo "$as\$"
 bgpscanner -p "$as\$" latest-bview | ./mrt2mysql-single.py
done
```

Mysql basic config (edit the .py you use to use these values as well)

```mysql
create user 'mrt'@'localhost' IDENTIFIED BY 'pw';
create database mrtdb;
GRANT ALL PRIVILEGES ON mrtdb.* TO 'mrt'@'localhost';
FLUSH PRIVILEGES;
use mrtdb;
create table mrt2mysql (eventtime datetime, prefix varchar(255), aspath varchar(255), sourceasn int);
```


