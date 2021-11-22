# theBestPooler

Simple script to match riders with drivers. 

It's a greedy, unoptimised search, so no guarantees that it works. 
It just seems to work (very quickly) for the few cases Ive tried. 


## Requirements:

python3 [tested on v3.9.7]
pandas [tested on v1.2.5]

## Running 

Put the following files into a single folder:
- `main.py`
- `theBestPooler.py`
- `riders.csv`
- `drivers.csv`

Run
```
python3 main.py riders.csv drivers.csv
```

The allocations will be printed to the console. See `example_output.txt` for an example of the expected output. Any riders that couldnt be allocated will also be listed.

For quick help:
```
python3 main.py -h
```

Optional arguments:
- desired verbosity: `-v <integer>`. 0 for no printing, 1 for printing the summary and the allocations. 2 and higher for debug printing. 
- by default, I assume the csv files contain headers. If they do not contain headers, pass `-n` as an additional argument.
Example:
```
python3 main.py riders.csv drivers.csv -v 2 -n
```
will assume the csv files have no headers, and the verbosity=level 2.


## CSV File Format Details:

Each file contains (exactly) 3 columns:
`<name>, <seats>, <location>`

`<name>` is just any string. preferably unique, but not necessary. Each row is treated as a different person.

For riders, `<seats>` is the number of required seats. Usually this will be 1.
For drivers, `<seats>` is the number of available seats EXCLUDING the driver, i.e. if the number is 2, this driver can pickup 2 passengers

The `<location>` specifies where the driver/riders start/want to be picked up. 
These are assumed to be categorical, so make sure that there are no spelling errors. Insensitive to capitilization: 'north' and 'North' are treated as the same location.

## Algorithm Description

Here is the basic psuedo-code:
```
Sort the riders: those requesting largest number of seats go in front
For each rider:
    Sort the drivers: those with fewest pickups so far go in front
    For each driver in same location:
      if assign(rider, driver) is possible
        assign(rider, driver)
        goto next rider
    For each driver not in same location:
      if assign(rider, driver) is possible
        assign(rider, driver)
        goto next rider
    print(error: cant assign rider to any driver)
print allocations
```

The sorts allow us to encode priority. Here I valued being in the same location most. Next most important is minimising the number of pickups by a driver.

        
        
