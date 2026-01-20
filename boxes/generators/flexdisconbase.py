# Copyright (C) 2013-2014 Florian Festi
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

import math

from boxes import *


class FlexDiscOnBase(Boxes):
    """A ring of flexible/bendy wood mounted on a circular base"""

    ui_group = "Part"

    def __init__(self) -> None:
        Boxes.__init__(self)
        self.addSettingsArgs(edges.FlexSettings)
        self.addSettingsArgs(edges.FingerJointSettings)
        self.argparser.add_argument(
            "--diameter", action="store", type=float, default=100.0,
            help="Diameter of the circular base in mm")
        self.argparser.add_argument(
            "--h", action="store", type=float, default=50.0,
            help="Height of the flexible wall in mm")
        self.argparser.add_argument(
            "--hole_diameter", action="store", type=float, default=0.0,
            help="Diameter of the center hole in the base (0 for no hole)")
        self.argparser.add_argument(
            "--gap_angle", action="store", type=float, default=0.0,
            help="Gap angle in degrees for the wall (0 for complete ring)")

    def render(self):
        d = self.diameter
        h = self.h
        t = self.thickness
        r = d / 2.0
        hole_d = self.hole_diameter
        gap_angle = self.gap_angle

        # Calculate wall circumference accounting for gap
        arc_angle = 360.0 - gap_angle
        c = d * math.pi * (arc_angle / 360.0)
        c_stretched = c / self.edges["X"].settings.stretch

        # Draw base disc with optional center hole
        self.parts.disc(d, hole=hole_d, move="right")

        # Draw flexible wall strip
        self.moveTo(0, 5)
        self.edges["X"](c_stretched, h)
        self.corner(90)
        self.edge(h)
        self.corner(90)
        self.edge(c_stretched)
        self.corner(90)
        self.edge(h)
        self.corner(90)
