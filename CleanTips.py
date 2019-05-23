"""This protocol is for cleaning tips.  You can select the number of dirty tip boxes that you want to clean.
    It will clean tips able to be attached to the p1000 single channel and the p50 multichannel."""

from opentrons import robot, containers, instruments

class CleanTipsOptions:
    def __init__(self):
        boxes_to_select