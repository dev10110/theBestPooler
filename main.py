
import argparse
import theBestPooler as tbp



def main(riders_file, drivers_file, verbosity=1, no_header=False):

  riders  = tbp.read_riders_csv (riders_file, no_header=no_header)
  drivers = tbp.read_drivers_csv(drivers_file, no_header=no_header)

  print("# Successfully loaded riders and drivers file") if verbosity > 1 else None

  tbp.allocate(riders, drivers, verbosity=verbosity)


if __name__ == "__main__":

  parser = argparse.ArgumentParser(description=
    """simple carpool allocation script
    
    pass in riders.csv and drivers.csv. Each column is as follows:
    <Name>, <Seats> <Location>

    In the case of riders.csv,  "Seats" = number of total required seats.
    In the case of drivers.csv, "Seats" = number of available seats, EXCLUDING driver.
    """, formatter_class=argparse.RawTextHelpFormatter)

  parser.add_argument("riders_filepath", help="filepath to riders.csv")
  parser.add_argument("drivers_filepath", help="filepath to drivers.csv")
  parser.add_argument("-n", "--no_header", action="store_true", help="if -n is passed in, assumes the csv files dont include the header row. Default: dont pass in -n and I will assume there is a header row in the csv files")
  parser.add_argument("-v", "--verbosity", help="verbosity, 0: no printing, 1: print summary and allocations, 2,3...: debug. Default = 1", type=int, default=1)
  # riders_file = "riders.csv"
  # drivers_file = "drivers.csv"

  args = parser.parse_args()

  print("#### STARTING #### ") if args.verbosity > 1 else None

  main(args.riders_filepath, args.drivers_filepath, verbosity=args.verbosity, no_header=args.no_header)