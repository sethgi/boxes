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

from boxes import *


class HalfLidBox(Boxes):
    """Box with a removable lid covering half of the top"""

    ui_group = "Box"

    description = """A box where the lid only covers half of the top surface.
The lid slides into place and is held by finger joints on three sides.
The open half provides easy access to the contents."""

    def __init__(self) -> None:
        Boxes.__init__(self)
        self.addSettingsArgs(edges.FingerJointSettings)
        self.buildArgParser("x", "y", "h", "outside")
        self.argparser.add_argument(
            "--lid_side", action="store", type=str, default="y",
            choices=["x", "y"],
            help="which side the lid covers half of (x=front/back, y=left/right)")
        self.argparser.add_argument(
            "--lid_position", action="store", type=str, default="back",
            choices=["front", "back"],
            help="which half has the lid (front or back along the chosen side)")

    def render(self):
        x, y, h = self.x, self.y, self.h

        if self.outside:
            x = self.adjustSize(x)
            y = self.adjustSize(y)
            h = self.adjustSize(h)

        t = self.thickness

        if self.lid_side == "y":
            # Lid covers half of y dimension
            lid_length = y / 2
            lid_width = x

            # Side walls (along y) - these need the divider for the half-lid
            # The top edge has finger joints on the lid half and plain edge on the open half
            if self.lid_position == "back":
                # Lid on back half: finger joint on back, edge on front
                side_top = edges.CompoundEdge(self, "ef", [lid_length, lid_length])
            else:
                # Lid on front half: edge on back, finger joint on front
                side_top = edges.CompoundEdge(self, "fe", [lid_length, lid_length])

            # Four walls in a row
            # Front and back walls (along x)
            # One wall has finger joints on top (connects to lid), other has plain edge (open)
            if self.lid_position == "back":
                self.rectangularWall(x, h, "FFeF", move="right", label="Front")
                self.rectangularWall(x, h, "FFfF", move="right", label="Back")
            else:
                self.rectangularWall(x, h, "FFfF", move="right", label="Front")
                self.rectangularWall(x, h, "FFeF", move="right", label="Back")

            # Side walls
            self.rectangularWall(y, h, ["F", "f", side_top, "f"], move="right", label="Right Side")
            self.rectangularWall(y, h, ["F", "f", side_top, "f"], move="up", label="Left Side")

            # Bottom and lid
            self.rectangularWall(x, y, "ffff", move="left", label="Bottom")

            # Half-lid
            # Edges are: bottom, right, top, left
            # U-shape of finger holes (F) to receive wall fingers (f); one side open (e)
            if self.lid_position == "back":
                # bottom=F (back wall), right=F (short side), top=e (open), left=F (short side)
                self.rectangularWall(x, lid_length, "FFeF", move="left", label="Lid")
            else:
                # bottom=e (open), right=F (short side), top=F (front wall), left=F (short side)
                self.rectangularWall(x, lid_length, "eFFF", move="left", label="Lid")

        else:
            # Lid covers half of x dimension
            lid_length = x / 2
            lid_width = y

            # Front and back walls (along x) - these need the divider
            if self.lid_position == "back":
                front_back_top = edges.CompoundEdge(self, "ef", [lid_length, lid_length])
            else:
                front_back_top = edges.CompoundEdge(self, "fe", [lid_length, lid_length])

            # Four walls in a row
            self.rectangularWall(x, h, ["F", "F", front_back_top, "F"], move="right", label="Front")
            self.rectangularWall(x, h, ["F", "F", front_back_top, "F"], move="right", label="Back")

            # Side walls (along y)
            # One wall has finger joints on top (connects to lid), other has plain edge (open)
            if self.lid_position == "back":
                self.rectangularWall(y, h, "FffF", move="right", label="Right Side")
                self.rectangularWall(y, h, "FfeF", move="up", label="Left Side")
            else:
                self.rectangularWall(y, h, "FfeF", move="right", label="Right Side")
                self.rectangularWall(y, h, "FffF", move="up", label="Left Side")

            # Bottom and lid
            self.rectangularWall(x, y, "ffff", move="left", label="Bottom")

            # Half-lid
            # Edges are: bottom, right, top, left
            # U-shape of finger holes (F) to receive wall fingers (f); one side open (e)
            if self.lid_position == "back":
                # bottom=F (short), right=F (long, side wall), top=F (short), left=e (long, open)
                self.rectangularWall(lid_length, y, "FFFe", move="left", label="Lid")
            else:
                # bottom=F (short), right=e (long, open), top=F (short), left=F (long, side wall)
                self.rectangularWall(lid_length, y, "FeFF", move="left", label="Lid")
