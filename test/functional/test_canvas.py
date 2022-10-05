#!/usr/bin/env python3
import sys; sys.path[:0] = ["../.."]

from pyx import *

c = canvas.canvas()

p = ( path.line(10*unit.u_pt, 10*unit.u_pt, 40*unit.u_pt, 40*unit.u_pt) +
      path.line(10*unit.u_pt, 40*unit.u_pt, 40*unit.u_pt, 10*unit.u_pt) )

t1 = trafo.rotate(20)
t2 = trafo.translate(5,0)
t3 = trafo.mirror(10)

sc = canvas.canvas([t1, t2, t3])
c.insert(sc).stroke(p)

c.stroke(c.bbox().rect())

c.stroke(p.transformed(t1*t2*t3), [color.rgb.green, style.linestyle.dashed])

c.stroke(p, [color.rgb.red, style.linestyle.dotted, t3, t2, t1])

c.writeEPSfile("test_canvas", page_paperformat=document.paperformat.A4)
c.writePDFfile("test_canvas", page_paperformat=document.paperformat.A4)
c.writeSVGfile("test_canvas", page_paperformat=document.paperformat.A4)

