"""An Opentrons protocol using the OT-One Hood for transforming one (or two with a selected option) in yeast.
    This protocol uses the 96 well transformation protocol developed by the Gietz Lab in 2007.  See the Trinh Lab
    protocols on LabArchives for details on this method."""

from Opentrons import robot, containers, instruments

# Run to run changed information.  This is contained in a Class where it can be changed each time you run.
class TransformationSettings:
    def __init__(self):
        self.number_of_transformations = 1
        self.wells = list()
        self.selected_rows = list()
        self.locations_of_DNA = list()

TS = TransformationSettings()

# ---Initializing all the tools and the containers you will need ---#
# CONTAINERS ON MAP INITIALIZATION #
p200rack = containers.load('tiprack-200ul', 'A2')
p1000rack = containers.load('tiprack-1000ul', 'B2')
trash_200 = containers.load('tiprack-200ul', 'E2')
trash_1000 = containers.load('tiprack-1000ul', 'D2')
tube_rack = containers.load('tube-rack-2ml', 'C2')
big_tubes_rack = containers.load('tube-rack-15_50ml', 'D1')

PEG_bottle = containers.load('point', 'C1')
transformation_plate = containers.load('96-deep-well','B1')
DNA_plate = containers.load('96-PCR-flat', 'A1')

# PIPETTE INITIALIZATION #
p1000_single = instruments.Pipette(
    axis="b",
    name='p1000',
    max_volume=900,
    min_volume=100,
    channels=1,
    trash_container=trash_1000,
    tip_racks=[p1000rack],
    aspirate_speed=180,
    dispense_speed=500
)

p50_multi = instruments.Pipette(
    axis="a",
    name="p50multi",
    max_volume=50,
    min_volume=5,
    channels=8,
    trash_container=trash_200,
    tip_racks=[p200rack]
)

# --- BEGINNING OF PROTOCOL RUN ---#
# Add transformation cell cocktail to each of the desired wells
for well in TS.wells:
    # set up the number of iterations for the cocktail
    p1000_single.pick_up_tip(p1000rack.wells(well))
    p1000_single.aspirate(410, tube_rack.well('A1'))
    p1000_single.dispense(50, transformation_plate.wells(well))
    p1000_single.blow_out(tube_rack.well('E6'))  # blow out tip into a 'trash tube'
    p1000_single.return_tip(trash_1000.wells(well))

# Get the DNA from the DNA plate
for row in TS.selected_rows:
    p50_multi.pick_up_tip(trash_1000.rows(row))
    p50_multi.transfer(12, DNA_plate.rows(row), transformation_plate.rows(row))
    p50_multi.return_tip(trash_200.rows(row))

# Pause for shaking the deep well plate
p50_multi.delay(minutes=1, seconds=15)

# Add the PEG to all the wells
for well in TS.wells:
    p1000_single.pick_up_tip(p1000rack.wells(well+len(TS.wells)))
    p1000_single.aspirate(300, PEG_bottle)
    p1000_single.dispense(300, transformation_plate.wells(well))
    p1000_single.return_tip(trash_1000.wells(well+len(TS.wells)))

# Pause for shaking and innoculation
p1000_single.delay(minutes=32)

# Add the DMSO to all of the wells and mix with pipette
for well in TS.wells:
    p1000_single.distribute(40, big_tubes_rack.well('A4'), transformation_plate.wells(well))

# Pause for heat shock and spindown
p1000_single.delay(minutes=20)

# Transfer selective medium to the transformation plate
for well in TS.wells:
    p1000_single.distribute(900, big_tubes_rack.well('B4'), transformation_plate.wells(well))





