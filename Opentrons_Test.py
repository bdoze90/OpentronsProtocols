"""This protocol runs a simple liquid handling where liquid from one 96 well plate is transferred to the other
with a dilution specified by the user.  The dilution buffer is in a general tube rack."""

from opentrons import Robot
from opentrons import instruments, containers


# Enter the user info here.  May eventually want to make an additional GUI for loading User information
class UserInfo:

    def __init__(self):
        self.dilution_factor = 0
        self.well_list = list()
        self.dilution_matrix = {1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                                1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                                1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                                1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                                1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                                1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                                1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                                1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1}

    def set_dilution_factor(self, x):
        self.dilution_factor = x

    def set_well_list(self, mylist):
        self.well_list = mylist

    def modify_dilution_matrix(self,well_index, d_factor):
        self.dilution_matrix[well_index] = d_factor

robot = Robot()
robot.reset()

User = UserInfo()
User.set_dilution_factor(5)

trash = containers.load('point', 'E2')
tiprack = containers.load('tiprack-200ul', 'E1')

big_tubes = containers.load('tube-rack-15_50ml', 'A2')

#this 96-well plate has the samples
samples = containers.load('96-PCR-flat', 'B1')

#this is the plate that we are aiming samples to
dilutions = containers.load('96-PCR-flat', 'C1')

p200 = instruments.Pipette(axis='b', max_volume=200)

# uniform dilution
amount = User.dilution_factor*10
p200.distribute(amount, big_tubes.wells('A4'), dilutions.wells())

#different dilution for each well
for i in range(96):
    p200.transfer(50*(User.dilution_matrix[i]-1), samples.wells(i), dilutions.wells(i), new_tip='always')

#different dilution for each row
for i in range(12):
    p200.transfer(50, samples.rows(i), dilutions.rows(i))

# This part of the protocol adds the dilutions to the requested wells

p200.drop_tip(trash)

for c in robot.commands():
    print(c)
robot.simulate()







