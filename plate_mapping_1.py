from opentrons import robot, containers, instruments

# This protocol is a test for the p1000 to make sure the robot runs correctly on axis b

p1000rack = containers.load('tiprack-1000ul', 'C2')
trash = containers.load('point', 'E1')

plate1 = containers.load('96-PCR-flat', 'A2')
plate2 = containers.load('96-PCR-flat', 'A1')

p1000_single = instruments.Pipette(
    axis="b",
    name='p1000',
    max_volume=1000,
    min_volume=100,
    channels=1,
    trash_container=trash,
    tip_racks=[p1000rack]
)

dest_plate = plate2

# map 300 uL to all odd rows of the destination plate
for i in range(0, 12, 2):
    target_rows = plate2.rows(i)
    p1000_single.distribute(300, plate1.rows(i), target_rows)

# map 150 uL to all even rows of the destination plate
for i in range(1, 12, 2):
    target_rows = plate2.rows(i)
    p1000_single.distribute(150, plate1.rows(i), target_rows)
