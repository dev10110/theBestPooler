import pandas as pd

class Rider:
  def __init__(self, name, required_seats, location, allocated=False):
    self.name = name
    self.required_seats = required_seats
    self.location = location.strip().lower()
    self.allocated = allocated

  def __str__(self):
      return f'Rider: {self.name} [Loc: {self.location}, ReqSeats: {self.required_seats}]'
    
  def __repr__(self):
    return f"(Rider) {self.name}"
      

class Driver:
  def __init__(self, name, capacity, location, passengers=[]):
    self.name = name
    self.capacity = capacity
    self.location = location.strip().lower()
    self.passengers = passengers.copy()

  def available_seats(self):
    s = sum(p.required_seats for p in self.passengers)
    return self.capacity - s

  def total_pickups(self):
    return len(self.passengers)

  """ Checks if a passenger can be assigned. If can be assigned, assigns the passenger
  and returns true. Else returns false"""
  def assign(self, passenger, verbosity=0):
    # prevent assigning a passenger that is already allocated
    if passenger.allocated:
      print("    assign failed cause pre-allocated") if verbosity >= 3 else None
      return False

    # prevent reassigning a passenger to a car
    if passenger in self.passengers:
      print("    assign failed cause already in") if verbosity >= 3 else None
      return False
    
    # check availability
    if self.available_seats() < passenger.required_seats:
      print("    assign failed cause not enough seats") if verbosity >= 3 else None
      return False

    # return true if all the checks passed
    passenger.allocated=True
    self.passengers.append(passenger)
    return True

  def __str__(self):
    s = f"Driver: {self.name} [Loc: {self.location}, Cap: {self.capacity}, Avail: {self.available_seats()}] \n"
    for p in self.passengers:
      s += f"  - {p.name} [{p.location}, Req: {p.required_seats}]\n"
    return(s)
  
  def __repr__(self):
    return f"(Driver) {self.name}"



"""
allocates `riders` to `drivers`
`verbosity` specifies how much printing you want
"""
def allocate(riders, drivers, verbosity=1):

  if verbosity >= 1:
    print()
    print("# starting allocations")
    print()

  assert all(isinstance(r, Rider) for r in riders), "All riders must be of type Rider"
  assert all(isinstance(d, Driver) for d in drivers), "All drivers must be of type Driver"
  
  riders.sort(key=lambda r: r.required_seats, reverse=True)
  drivers.sort(key=lambda d: d.available_seats(), reverse=True)

  unallocated_riders = []

  for r in riders:

    if r.allocated:
      print(f"Rider {r.name} is already allocated. Skipping!") if verbosity >= 2 else None
      continue

    print(f"Allocating {r.name}") if verbosity >= 2 else None
    
    # drivers.sort(key=lambda d: d.available_seats(), reverse=True) # prioritise cars with largest number of available seats
    drivers.sort(key=lambda d: d.total_pickups()) # prioritize allocating to people with fewest pickups

    for c in [c for c in drivers if c.location == r.location]:
      print(f"  trying in Car {c.name}") if verbosity >= 2 else None
      if c.assign(r, verbosity):
        print(f"  allocated {r.name} to Car {c.name}") if verbosity >= 2 else None
        print() if verbosity >= 2 else None
        break
    if r.allocated:
      continue

    # print("  oof. No cars in same location work. Trying other locations...")

    for c in [c for c in drivers if c.location != r.location]:
      print(f"  in car {c.name}") if verbosity >= 2 else None
      if c.assign(r, verbosity):
        print(f"  allocated {r.name} to Car {c.name}") if verbosity >= 2 else None
        print() if verbosity >= 2 else None
        break
    
    if r.allocated:
      continue
    
    print(f" ** OOF. Cant find a suitable place in any car for {r.name}\n") if verbosity >= 1 else None
    unallocated_riders.append(r)

  ## Summarise
  if verbosity >= 1:
    print()
    print("# successfully completed allocations")
    print()
    print("#### ALLOCATIONS ####")
    print()
    for d in drivers:
      print(d)
    
    print()
    print("#### UNALLOCATED RIDERS ####")
    print()
    if len(unallocated_riders) == 0:
      print("[none]")
    else:
      for p in unallocated_riders:
        print(f" - {p.name}")

    print()
    print("done.")

  return unallocated_riders


def read_riders_csv(filename, no_header=False):
    if not no_header:
      # file includes header row
      riders_df = pd.read_csv(filename)
    else:
      # file does not include header row
      col_names = ["Name", "Seats", "Location"]
      riders_df = pd.read_csv(filename, header=None, names=col_names)

    riders = []
    for i in range(len(riders_df)):
      n, s, l = riders_df.iloc[i,:]
      rider = Rider(n,s,l)
      riders.append(rider)
    
    return riders

def read_drivers_csv(filename, no_header=False):
    
    if not no_header:
      # file includes header row
      drivers_df = pd.read_csv(filename)
    else:
      # file does not include header row
      col_names = ["Name", "Seats", "Location"]
      drivers_df = pd.read_csv(filename, header=None, names=col_names)

    drivers = []
    for i in range(len(drivers_df)):
      n, s, l = drivers_df.iloc[i,:]
      driver = Driver(n,s,l)
      drivers.append(driver)

    return drivers