#!/usr/bin/env python3
import pyx
from pyx import *
from pyx.path import *
import math

def testarrow(c):
    c.stroke(path(moveto(10,20),
                curveto(12,16,14,15,12,19),
                rcurveto(-3,2,3,3,-2,4)),
             [deco.barrow.small, deco.earrow.normal,
              deco.arrow(pos=0.5),
              deco.arrow(pos=0.7, reversed=1)])

    c.stroke(path(arc(8,15,4,10,70)), [deco.barrow.small, deco.earrow.normal])
    c.stroke(path(arc(8,15,3,10,70)), [deco.barrow.small, deco.earrow.normal])
    c.stroke(path(arc(8,15,2,10,70)), [deco.barrow.small, deco.earrow.normal])
    c.stroke(path(arc(8,15,1,10,70)), [deco.barrow.small, deco.earrow.normal])
    c.stroke(path(arc(8,15,0.5,10,70)), [deco.barrow.small, deco.earrow.normal])

    base = 2

    pal = color.lineargradient_rgb(color.rgb.red, color.rgb.blue)

    c.stroke(path(moveto(5,10), rlineto(5,0)),
           [#deco.barrow(size=base/math.sqrt(8)*unit.t_pt, constriction=1),
            deco.earrow.SMall,
            deco.colorgradient(pal),
            deco.text("start", arclenfrombegin=0, angle=90)])
    c.stroke(path(moveto(5,10.5), rlineto(5,0)),
           [deco.barrow(size=base/math.sqrt(4)*unit.t_pt, constriction=1),
            deco.earrow.Small,
            deco.colorgradient(pal),
            deco.text("start+1", arclenfrombegin=1, angle=90)])
    c.stroke(path(moveto(5,11), rlineto(5,0)),
           [deco.barrow(size=base/math.sqrt(2)*unit.t_pt, constriction=1),
            deco.earrow.small,
            deco.colorgradient(pal),
            deco.text("center", angle=90)])
    c.stroke(path(moveto(5,11.5), rlineto(5,0)),
           [deco.barrow(size=base/math.sqrt(1)*unit.t_pt, constriction=1),
            deco.earrow.normal,
            deco.colorgradient(pal),
            deco.text("end-1", arclenfromend=1, angle=90)])
    c.stroke(path(moveto(5,12), rlineto(5,0)),
           [deco.barrow(size=base*math.sqrt(2)*unit.t_pt, constriction=1),
            deco.earrow.large,
            deco.text("end", arclenfromend=0, angle=90)])
    c.stroke(path(moveto(5,12.5), rlineto(5,0)),
           [deco.barrow(size=base*math.sqrt(4)*unit.t_pt, constriction=1),
            deco.earrow.Large])
    c.stroke(path(moveto(5,13), rlineto(5,0)),
           [deco.barrow(size=base*math.sqrt(8)*unit.t_pt, constriction=1),
            deco.earrow.LArge])
    c.stroke(path(moveto(5,13.5), rlineto(5,0)),
           [deco.barrow(size=base*math.sqrt(16)*unit.t_pt, constriction=1),
            deco.earrow.LARge])

    lt = style.linewidth.THick

    c.stroke(path(moveto(11,10), rlineto(5,0)),
           [lt,
            deco.barrow(size=base/math.sqrt(8)*unit.t_pt, constriction=1),
            deco.earrow.SMall,
            deco.colorgradient(pal, [style.linewidth.THIN])])
    c.stroke(path(moveto(11,10.5), rlineto(5,0)),
           [lt,
            deco.barrow(size=base/math.sqrt(4)*unit.t_pt, constriction=1),
            deco.earrow.Small])
    c.stroke(path(moveto(11,11), rlineto(5,0)),
           [lt,
            deco.barrow(size=base/math.sqrt(2)*unit.t_pt, constriction=1),
            deco.earrow.small])
    c.stroke(path(moveto(11,11.5), rlineto(5,0)),
           [lt,
            deco.barrow(size=base/math.sqrt(1)*unit.t_pt, constriction=1),
            deco.earrow.normal])
    c.stroke(path(moveto(11,12), rlineto(5,0)),
           [lt,
            deco.barrow(size=base*math.sqrt(2)*unit.t_pt, constriction=1),
            deco.earrow.large])
    c.stroke(path(moveto(11,12.5), rlineto(5,0)),
           [lt,
            deco.barrow(size=base*math.sqrt(4)*unit.t_pt, constriction=1),
            deco.earrow.Large(attrs=[deco.stroked([style.linestyle.dashed]), deco.filled.clear])])
    c.stroke(path(moveto(11,13), rlineto(5,0)),
           [lt,
            deco.barrow(size=base*math.sqrt(8)*unit.t_pt, constriction=1),
            deco.earrow.LArge(attrs=[style.linestyle.dashed, color.rgb.green])])
    c.stroke(path(moveto(11,13.5), rlineto(5,0)),
           [lt,
            deco.barrow(size=base*math.sqrt(16)*unit.t_pt, constriction=1),
            deco.earrow.LARge(attrs=[color.rgb.red,
                                     deco.stroked([style.linejoin.round]),
                                     deco.filled([color.rgb.blue])])])

def linehatched(c):
    p = rect(0, 0, 5, 0.5).transformed(trafo.rotate(60))
    c.draw(p, [deco.linehatched45.normal])
    c.fill(p, [trafo.translate(2,0), deco.linehatched(0.1, 60, cross=1)]) # should not be filled, but hatched
    c.stroke(p, [trafo.translate(4,0), deco.linehatched90.normal])
    c.draw(p, [trafo.translate(6,0), deco.linehatched(0.1, 30, strokestyles=[color.rgb.red, style.linewidth.normal], cross=1)])

def testbrace(c):
    p = line(0, 0, 5, 0).transformed(trafo.rotate(60))
    c.stroke(p, [deco.brace(dist=-0.1, stretch=1.1), deco.text(r"hallo", textdist=20*unit.x_pt, relangle=-90), trafo.translate(8,0)])

    tr = trafo.translate(12, 0)
    c.draw(line(0,0,0,4), [deco.leftbrace, tr])
    c.draw(line(4,0,4,4), [deco.rightbrace, tr])
    c.draw(line(0,0,4,0), [deco.belowbrace, tr])
    c.stroke(line(0,4,4,4), [deco.abovebrace, tr, style.linewidth.THin])

    tr = trafo.translate(12.5, 0.5)
    c.stroke(line(0,0,3,0), [deco.straightbrace, tr, color.rgb.red])
    c.draw(line(3,0,3,3), [deco.straightbrace(fillattrs=[color.rgb.blue]), tr])
    c.draw(line(3,3,0,3), [deco.straightbrace, tr])
    c.draw(line(0,3,0,0), [deco.straightbrace, tr])

c = canvas.canvas()
testarrow(c)
linehatched(c)
testbrace(c)
c.writeEPSfile("test_arrow", page_paperformat=document.paperformat.A4, page_rotated=0, page_fittosize=1)
c.writePDFfile("test_arrow", page_paperformat=document.paperformat.A4)
c.writeSVGfile("test_arrow", page_paperformat=document.paperformat.A4)

