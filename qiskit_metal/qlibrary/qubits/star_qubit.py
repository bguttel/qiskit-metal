# -*- coding: utf-8 -*-

# This code is part of Qiskit.
#
# (C) Copyright IBM 2017, 2021.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.
"""This is the CircleCaterpillar module."""

from qiskit_metal import draw, Dict  # , QComponent
from qiskit_metal.qlibrary.core import QComponent
from shapely.geometry import CAP_STYLE
import numpy as np


class StarQubit(QComponent):
    """A single configurable circle.

    Inherits QComponent class.

    Default Options:
        * radius: '300um'
        * pos_x: '0um'
        * pos_y: '0um'
        * resolution: '16'
        * cap_style: 'round' -- Valid options are 'round', 'flat', 'square'
        * subtract: 'False'
        * helper: 'False'
        * chip: 'main'
        * layer: '1'
    """

    default_options = dict(
        radius='300um', # radius of the circle defining the star shape
        center_radius='100um', # Measure of how thick the central island is
        gap_couplers='25um', # Gap between the star and the coupling resonator
        gap_readout='10um', # Gap between the star and the readout resonator
        connector_length='75um', # Length of the rectangular part of the connector
        trap_offset='20um', #The offset between coordinates of the trpezoid to define the side wall angle
        junc_h = '30um', # junction height  
        rotation1 = '0.0', # rotation for one of the coupling resonators '36.0', '0.0',
        rotation2 = '72.0', # rotation for the readout resonator '108.0','72.0',
        rotation3 = '144.0', # rotation for one of the coupling resonators '180.0','144.0',
        rotation4 = '216.0', # rotation for one of the coupling resonators'252.0','216.0',
        rotation5 = '288.0', # rotation for one of the coupling resonators '324.0','288.0',
        pos_x='0um',
        pos_y='0um',
        number_of_connectors='1', # Total number of coupling resonators
        resolution='16',
        cap_style='round',  # round, flat, square
        # join_style = 'round', # round, mitre, bevel
        # Connections
        # General
        subtract='False',
        helper='False',
        chip='main',
        layer='1'
    )
    """Default drawing options"""

    def make(self):
        """The make function implements the logic that creates the geoemtry
        (poly, path, etc.) from the qcomponent.options dictionary of
        parameters, and the adds them to the design, using
        qcomponent.add_qgeometry(...), adding in extra needed information, such
        as layer, subtract, etc."""
        p = self.p  # p for parsed parameters. Access to the parsed options.

        # Extracting coordinated from the user input values
        y1 = -p.center_radius # y-coordinate of the trapezoid to subtract from circle
        y2 = -p.radius # y-coordinate of the trapezoid to subtract from circle
        x1 = -p.center_radius/2 # x-coordinate of the trapezoid to subtract from circle
        x2 = p.center_radius/2 # x-coordinate of the trapezoid to subtract from circle
        x3 = p.center_radius + p.trap_offset # x-coordinate of the trapezoid to subtract from circle
        x4 = -(p.center_radius + p.trap_offset) # x-coordinate of the trapezoid to subtract from circle
        a1 = -(p.center_radius+p.gap_couplers) # y-coordinate of the polygon defining the coupling resonator
        a2 = -p.radius # y-coordinate of the polygon defining the coupling resonator
        a3 = p.radius # y-coordinate of the polygon defining the coupling resonator
        b1 = -(p.center_radius/4) # x-coordinate of the polygon defining the coupling resonator
        b2 = (p.center_radius/4) # x-coordinate of the polygon defining the coupling resonator
        b3 = (p.center_radius-(p.gap_couplers)) # x-coordinate of the polygon defining the coupling resonator
        b4 = -(p.center_radius-(p.gap_couplers)) # x-coordinate of the polygon defining the coupling resonator
        b5 = -p.radius # x-coordinate of the polygon defining the coupling resonator
        b6 = p.radius # x-coordinate of the polygon defining the coupling resonator   
        c1 = -(p.center_radius+p.gap_readout) # y-coordinate of the polygon defining the readout resonator
        c2 = -p.radius # y-coordinate of the polygon defining the readout resonator
        c3 = p.radius # y-coordinate of the polygon defining the readout resonator
        d1 = -(p.center_radius/2 - p.gap_readout) # x-coordinate of the polygon defining the readout resonator
        d2 =  p.center_radius/2- p.gap_readout # x-coordinate of the polygon defining the readout resonator
        d3 = p.center_radius # x-coordinate of the polygon defining the readout resonator
        d4 = -p.center_radius # x-coordinate of the polygon defining the readout resonator
        d5 = -p.radius # x-coordinate of the polygon defining the readout resonator
        d6 = p.radius # x-coordinate of the polygon defining the readout resonator
        pocket_w= p.connector_length  # connector pocket width
        pocket_h=p.connector_length*2  # connector pocket height    
        pocket_w1=p.gap_couplers  # Connector to the JJ
        pocket_h1=p.center_radius # Connector to the JJ

        # create a circle
        circle = draw.Point(p.pos_x, p.pos_y).buffer(
            p.radius,
            resolution=int(p.resolution),
            cap_style=getattr(CAP_STYLE, p.cap_style)
        )

        circle_outer = draw.Point(p.pos_x, p.pos_y).buffer(
            p.radius*(1+(p.connector_length/p.radius)),
            resolution=int(p.resolution),
            cap_style=getattr(CAP_STYLE, p.cap_style)
        )
        #join_style = getattr(JOIN_STYLE, p.join_style)
        # create the trapezoids
        coords1 = [((x1 + p.pos_x),(y1 + p.pos_y)),((x2 + p.pos_x),(y1 + p.pos_y)),((x3 + p.pos_x),(y2 + p.pos_y)),((x4 + p.pos_x),(y2 + p.pos_y))]
        trap_0 = draw.Polygon(coords1)
        trap_1 = draw.rotate(trap_0, p.rotation1, origin=(p.pos_x, p.pos_y))
        trap_2 = draw.rotate(trap_0, p.rotation2, origin=(p.pos_x, p.pos_y))
        trap_3 = draw.rotate(trap_0, p.rotation3, origin=(p.pos_x, p.pos_y))
        trap_4 = draw.rotate(trap_0, p.rotation4, origin=(p.pos_x, p.pos_y))
        trap_5 = draw.rotate(trap_0, p.rotation5, origin=(p.pos_x, p.pos_y))

        # Define the connectors
        coords_coupling_resonator = [((b1 + p.pos_x),(a1 + p.pos_y)),((b2 + p.pos_x),(a1 + p.pos_y)),((b3 + p.pos_x),(a2 + p.pos_y)),((b6 + p.pos_x),(a2 + p.pos_y)),((b6 + p.pos_x),(a3 + p.pos_y)),((b5 + p.pos_x),(a3 + p.pos_y)),((b5 + p.pos_x),(a2 + p.pos_y)),((b4 + p.pos_x),(a2 + p.pos_y))]
        trap_z = draw.Polygon(coords_coupling_resonator)
        trap_a = draw.rotate(trap_z, p.rotation1, origin=(p.pos_x, p.pos_y))
        trap_b = draw.rotate(trap_z, p.rotation2, origin=(p.pos_x, p.pos_y))
        trap_d = draw.rotate(trap_z, p.rotation4, origin=(p.pos_x, p.pos_y))
        trap_e = draw.rotate(trap_z, p.rotation5, origin=(p.pos_x, p.pos_y))
        coords_readout = [((d1 + p.pos_x),(c1 + p.pos_y)),((d2 + p.pos_x),(c1 + p.pos_y)),((d3 + p.pos_x),(c2 + p.pos_y)),((d6 + p.pos_x),(c2 + p.pos_y)),((d6 + p.pos_x),(c3 + p.pos_y)),((d5 + p.pos_x),(c3 + p.pos_y)),((d5 + p.pos_x),(c2 + p.pos_y)),((d4 + p.pos_x),(c2 + p.pos_y))]
        trap_c = draw.Polygon(coords_readout)
        trap_c = draw.rotate(trap_c, p.rotation3, origin=(p.pos_x, p.pos_y))
        rect1 = draw.rectangle(pocket_w1, pocket_h1)
        rect1 = draw.translate(rect1, xoff=p.pos_x + b2*1.1, yoff=p.radius)
        rect1 = draw.rotate(rect1, p.rotation1, origin=(p.pos_x, p.pos_y))
        rect2 = draw.rectangle(pocket_w1, pocket_h1)
        rect2 = draw.translate(rect2, xoff=p.pos_x + b1*1.1, yoff=p.radius)
        rect2 = draw.rotate(rect2, p.rotation1, origin=(p.pos_x, p.pos_y))


        # Define contacts
        pocket0 = draw.rectangle(pocket_w, pocket_h)
        pocket0 = draw.translate(pocket0, xoff=p.pos_x, yoff=(y2 + p.pos_y))
        pocket1 = draw.rotate(pocket0, p.rotation1, origin=(p.pos_x, p.pos_y))
        pocket2 = draw.rotate(pocket0, p.rotation2, origin=(p.pos_x, p.pos_y))
        pocket3 = draw.rotate(pocket0, p.rotation3, origin=(p.pos_x, p.pos_y))
        pocket4 = draw.rotate(pocket0, p.rotation4, origin=(p.pos_x, p.pos_y))
        pocket5 = draw.rotate(pocket0, p.rotation5, origin=(p.pos_x, p.pos_y))

        #Connectors for the ground plane
        pocketZ = draw.rectangle(pocket_w*1.4, pocket_h)
        pocketZ = draw.translate(pocketZ, xoff=p.pos_x, yoff=(y2 + p.pos_y))
        pocketA = draw.rotate(pocketZ, p.rotation1, origin=(p.pos_x, p.pos_y))
        pocketB = draw.rotate(pocketZ, p.rotation2, origin=(p.pos_x, p.pos_y))
        pocketC = draw.rotate(pocketZ, p.rotation3, origin=(p.pos_x, p.pos_y))
        pocketD = draw.rotate(pocketZ, p.rotation4, origin=(p.pos_x, p.pos_y))
        pocketE = draw.rotate(pocketZ, p.rotation5, origin=(p.pos_x, p.pos_y))
        if (p.number_of_connectors) ==0:
            circle_outer = draw.union(circle_outer,pocketC)
        elif (p.number_of_connectors) ==1:
            circle_outer = draw.union(circle_outer,pocketA,pocketC)
        elif (p.number_of_connectors) ==2:
            circle_outer = draw.union(circle_outer,pocketA,pocketB,pocketC)
        elif (p.number_of_connectors) ==3:
            circle_outer = draw.union(circle_outer,pocketA,pocketB,pocketC,pocketD)
        elif (p.number_of_connectors) ==4:
            circle_outer = draw.union(circle_outer,pocketA,pocketB,pocketC,pocketD,pocketE)

        #junction
        pocket6 = draw.LineString([[p.pos_x+b1-(pocket_h1/2), p.pos_y], [p.pos_x+b2+(pocket_h1/2), p.pos_y]])
        pocket6 = draw.translate(pocket6, yoff=(p.pos_y + 1.15*(p.radius)))
        pocket6 = draw.rotate(pocket6, p.rotation1, origin=(p.pos_x, p.pos_y))

        # Define the final structure based on use input on how many connectors are needed
        if (p.number_of_connectors) ==0:
            traps = trap_3
        elif (p.number_of_connectors) ==1:
            traps = draw.union(trap_1, trap_3)
        elif (p.number_of_connectors) ==2:
            traps = draw.union(trap_1, trap_2, trap_3)
        elif (p.number_of_connectors) ==3:
            traps = draw.union(trap_1, trap_2, trap_3, trap_4)
        elif (p.number_of_connectors) ==4:
            traps = draw.union(trap_1, trap_2, trap_3, trap_4, trap_5)

        # Subtract
        total1 = draw.subtract(circle, traps)
        # Add connection to the junction
        total = draw.union(total1, rect1, rect2)

        contact1 = draw.subtract(circle,trap_a)
        contact1 = draw.union(contact1,pocket1)
        contact2 = draw.subtract(circle,trap_b)
        contact2 = draw.union(contact2,pocket2)
        contact3 = draw.subtract(circle,trap_c)
        contact3 = draw.union(contact3,pocket3)
        contact4 = draw.subtract(circle,trap_d)
        contact4 = draw.union(contact4,pocket4)
        contact5 = draw.subtract(circle,trap_e)
        contact5 = draw.union(contact5,pocket5)

        #########################################################################################
        # Add geometry and Qpin connections
        p_in=(p.pos_y,(p.pos_y + p.radius))
        p_out=(p.pos_y,1.25*(p.pos_y + p.radius))
        pins=draw.LineString([p_in, p_out])
        pins1=draw.rotate(pins, p.rotation1, origin=(p.pos_x, p.pos_y))
        pins2=draw.rotate(pins, p.rotation2, origin=(p.pos_x, p.pos_y))
        pins3=draw.rotate(pins, p.rotation3, origin=(p.pos_x, p.pos_y))
        pins4=draw.rotate(pins, p.rotation4, origin=(p.pos_x, p.pos_y))
        pins5=draw.rotate(pins, p.rotation5, origin=(p.pos_x, p.pos_y))

        self.add_qgeometry('poly', {'circle1': total},
                           subtract=p.subtract,
                           helper=p.helper,
                           layer=p.layer,
                           chip=p.chip)
        if (p.number_of_connectors) ==0:
            self.add_qgeometry('poly', {'contact3': contact3},
                            subtract=p.subtract,
                            helper=p.helper,
                            layer=p.layer,
                            chip=p.chip)

            self.add_pin('pin3',
                     pins3.coords,
                     width=0.01,
                     input_as_norm=True)
        
        elif (p.number_of_connectors) ==1:
            self.add_qgeometry('poly', {'contact1': contact1},
                            subtract=p.subtract,
                            helper=p.helper,
                            layer=p.layer,
                            chip=p.chip)
            self.add_qgeometry('poly', {'contact3': contact3},
                            subtract=p.subtract,
                            helper=p.helper,
                            layer=p.layer,
                            chip=p.chip)
            # Add pin connections
            self.add_pin('pin1',
                     pins1.coords,
                     width=0.01,
                     input_as_norm=True)

            self.add_pin('pin3',
                     pins3.coords,
                     width=0.01,
                     input_as_norm=True)


        elif (p.number_of_connectors) ==2:
            self.add_qgeometry('poly', {'contact1': contact1},
                            subtract=p.subtract,
                            helper=p.helper,
                            layer=p.layer,
                            chip=p.chip)
            self.add_qgeometry('poly', {'contact2': contact2},
                            subtract=p.subtract,
                            helper=p.helper,
                            layer=p.layer,
                            chip=p.chip)
            self.add_qgeometry('poly', {'contact3': contact3},
                            subtract=p.subtract,
                            helper=p.helper,
                            layer=p.layer,
                            chip=p.chip)
            # Add pin connections
            self.add_pin('pin1',
                     pins1.coords,
                     width=0.01,
                     input_as_norm=True)

            # Define second pin
            
            self.add_pin('pin2',
                        pins2.coords,
                        width=0.01,
                        input_as_norm=True)

            # Define third pin
            self.add_pin('pin3',
                        pins3.coords,
                        width=0.01,
                        input_as_norm=True)

        elif (p.number_of_connectors) ==3:
            self.add_qgeometry('poly', {'contact1': contact1},
                            subtract=p.subtract,
                            helper=p.helper,
                            layer=p.layer,
                            chip=p.chip)
            self.add_qgeometry('poly', {'contact2': contact2},
                            subtract=p.subtract,
                            helper=p.helper,
                            layer=p.layer,
                            chip=p.chip)
            self.add_qgeometry('poly', {'contact3': contact3},
                            subtract=p.subtract,
                            helper=p.helper,
                            layer=p.layer,
                            chip=p.chip)
            self.add_qgeometry('poly', {'contact4': contact4},
                            subtract=p.subtract,
                            helper=p.helper,
                            layer=p.layer,
                            chip=p.chip)
            # Add pin connections
            self.add_pin('pin1',
                     pins1.coords,
                     width=0.01,
                     input_as_norm=True)

            # Define second pin
            self.add_pin('pin2',
                        pins2.coords,
                        width=0.01,
                        input_as_norm=True)

            # Define third pin
            self.add_pin('pin3',
                        pins3.coords,
                        width=0.01,
                        input_as_norm=True)

            # Define fourth pin
            self.add_pin('pin4',
                        pins4.coords,
                        width=0.01,
                        input_as_norm=True)

        elif (p.number_of_connectors) ==4:
            self.add_qgeometry('poly', {'contact1': contact1},
                            subtract=p.subtract,
                            helper=p.helper,
                            layer=p.layer,
                            chip=p.chip)
            self.add_qgeometry('poly', {'contact2': contact2},
                            subtract=p.subtract,
                            helper=p.helper,
                            layer=p.layer,
                            chip=p.chip)
            self.add_qgeometry('poly', {'contact3': contact3},
                            subtract=p.subtract,
                            helper=p.helper,
                            layer=p.layer,
                            chip=p.chip)
            self.add_qgeometry('poly', {'contact4': contact4},
                            subtract=p.subtract,
                            helper=p.helper,
                            layer=p.layer,
                            chip=p.chip)
            self.add_qgeometry('poly', {'contact5': contact5},
                            subtract=p.subtract,
                            helper=p.helper,
                            layer=p.layer,
                            chip=p.chip)   
            # Add pin connections
            self.add_pin('pin1',
                     pins1.coords,
                     width=0.01,
                     input_as_norm=True)

            # Define second pin
            self.add_pin('pin2',
                        pins2.coords,
                        width=0.01,
                        input_as_norm=True)

            # Define third pin
            self.add_pin('pin3',
                        pins3.coords,
                        width=0.01,
                        input_as_norm=True)

            # Define fourth pin
            self.add_pin('pin4',
                        pins4.coords,
                        width=0.01,
                        input_as_norm=True)

            # Define fifth pin
            
            self.add_pin('pin5',
                        pins5.coords,
                        width=0.01,
                        input_as_norm=True)
                        
        self.add_qgeometry('junction', {'poly': pocket6},
                           subtract=p.subtract,
                           helper=p.helper,
                           layer=p.layer,
                           chip=p.chip,
                           width=p.junc_h)
        self.add_qgeometry('poly', {'circle2': circle_outer},
                           subtract=True,
                           helper=p.helper,
                           layer=p.layer,
                           chip=p.chip)