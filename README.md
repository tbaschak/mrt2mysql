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


