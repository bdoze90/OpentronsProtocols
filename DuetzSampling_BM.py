"""This protocol is for taking a Duetz measurement for flow cytometry and OD.  Current functionality allows you
    to pipette a given volume of sample for OD measurement and a given volume for flow cytometry.  Variable volumes
    and volumes connected to the OD reading will be featured in a forthcoming version of this protocol."""

from opentrons import robot, containers, instruments

robot.reset()

p1000rack = containers.load('tiprack-1000ul', 'C2')
p200rack = containers.load('tiprack-200ul', 'E2')
trash200 = containers.load('point', 'E1')
trash1000 = containers.load('point', 'D1')

Duetz_plate = containers.load('96-PCR-flat', 'C1')
microplate = containers.load('384-plate', 'B1')
guava_plate = containers.load('96-PCR-flat', 'A2')

p1000_single = instruments.Pipette(
    axis="b",
    name='p1000',
    max_volume=1000,
    min_volume=100,
    channels=1,
    trash_container=trash1000,
    tip_racks=[p1000rack]
)

p50_multi = instruments.Pipette(
    axis="a",
    name='p50multi',
    max_volume=50,
    min_volume=5,
    channels=8,
    trash_container=trash200,
    tip_racks=[p200rack]
)

# Take samples from all the rows of the Duetz plate and put them in the microplate
for i in range(0, 96, 8):  # This indexing is needed for the multichannel pipette
    p50_multi.distribute(20, Duetz_plate.wells(i), microplate.wells(i*2))
    p50_multi.blow_out((microplate.wells(i*2)))

for item in robot.commands():
    print(item)

robot.simulate()