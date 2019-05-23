"""This protocol is for prepping different media conditions in a plate (Duetz or otherwise). It relies on
    a list from the Opentrons Protocol Settings protocol to determine the type of media and what wells to
    add it to."""

from opentrons import robot, containers, instruments

robot.reset()

class MediaPrepSettings:
    def __init__(self):
        self.mediadict = dict()  # names of media and their locations

    def add_media(self, name, concentration, location):
        mytuple = (concentration, location, list())
        self.mediadict[name] = mytuple

    def importmediasettings(self):
        f = open('/Users/brianmendoza/PyCharmProjects/OpentronsProtocols/mediasettings.txt')
        medianame = str()
        for line in f:
            ismedia = line.find('media_name:')
            if ismedia != -1:
                medianame = line[ismedia+11:-1]
            else:
                self.mediadict[medianame][2].append(line[:-1])
        f.close()


class Plate:
    def __init__(self):
        self.totalvolume = 500
        self.wellmatrix = dict()
        self.fill_wellmatrix()

    def fill_wellmatrix(self):
        f = open('/Users/brianmendoza/PyCharmProjects/OpentronsProtocols/96welllist.txt')
        for line in f:
            self.wellmatrix[line[:-1]] = 0
        f.close()

    def change_well_volume(self, mywell, amount_added):
        self.wellmatrix[mywell] += amount_added

    def get_well_volume(self, mywell):
        return self.wellmatrix[mywell]


# Initializing the containers and media
p1000rack = containers.load('tiprack-1000ul', 'D2')
trash = containers.load('tiprack-1000ul', 'D1')

DuetzPlate = containers.load('96-deep-well', 'A1')
smalltubes = containers.load('tube-rack-2ml', 'B2')
bigtubes = containers.load('tube-rack-15_50ml', 'C2')

# These are the hardcoded media that will be added via the protocol gui later.
MyMedia = MediaPrepSettings()
Plate1 = Plate()

# Medias
MyMedia.add_media('SC-Leu-Ura',2, bigtubes.wells('A4'))
MyMedia.add_media('Leu', 40, bigtubes.wells('B4'))
MyMedia.add_media('Ura', 50, bigtubes.wells('B2'))
MyMedia.add_media('YPD', 1.11, bigtubes.wells('A2'))

# Carbon Sources
MyMedia.add_media('Galactose', 10, bigtubes.wells('B1'))
MyMedia.add_media('Glucose', 10, bigtubes.wells('A1'))

# Antibiotics
MyMedia.add_media('G418', 10, bigtubes.wells('C1'))
MyMedia.add_media('Amp', 10, bigtubes.wells('C2'))

MyMedia.importmediasettings()


# Initialize the Pipette
p1000_single = instruments.Pipette(
    axis="b",
    name='p1000',
    max_volume=900,
    min_volume=50,
    channels=1,
    trash_container=trash,
    tip_racks=[p1000rack]
)

# ---PROTOCOL--- #

# Distribute every needed media from the list
for media, info in MyMedia.mediadict.items():
    vol = Plate1.totalvolume / info[0]
    p1000_single.distribute(vol, info[1], DuetzPlate.wells(info[2]), disposal_vol=10)
    for well in info[2]:  # Iterates through every well that requires the media and adds media to it
        Plate1.change_well_volume(well, vol)  # reset the volume on the plate tracker

# Determine the appropriate amound of water for each well to get to 500 ul
wells_lists = list()
# Temporary storage:
cum_volume = 0
well_subset = list()
for well in Plate1.wellmatrix:
    vol_water = int(Plate1.totalvolume) - int(Plate1.wellmatrix[well])
    if cum_volume + vol_water >= 800:
        # Consolidate current information:
        wells_lists.append([well_subset, cum_volume])
        # Reset the temporary storage:
        well_subset = []
        cum_volume = 0
    # Add info into temporary storage vectors
    cum_volume += vol_water
    well_subset.append([well, vol_water])
wells_lists.append([well_subset, cum_volume])

# Add the appropriate volume of water to each of the wells
p1000_single.pick_up_tip(p1000rack)
for wells in wells_lists:
    p1000_single.aspirate(wells[1]+10, bigtubes.wells('A3'))
    for awell in wells[0]:
        p1000_single.dispense(awell[1], DuetzPlate.wells(awell[0]))  # index 1 gives volume index 0 is the well name
    p1000_single.blow_out(trash)
p1000_single.drop_tip(trash)

for item in robot.commands():
    print(item)
robot.simulate()
