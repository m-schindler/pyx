import sys; sys.path.insert(0, "../..")
import math
from pyx import *

a = 1
p = path.curve(-1, 0, 1, a, -1, a, 1, 0)

t = trafo.rotate(30).scaled(5)
x = 0.49

p = p.transformed(t)

c = canvas.canvas()
c.stroke(p)
t = p.normsubpaths[0].trafo([x])[0]
#if t is not path.invalid:
#    c.stroke(path.line(0, 0, 1, 0), [p.normsubpaths[0].trafo([x])[0], deco.earrow.normal, color.rgb.red])

c.text(-6, -5, r"t={:f}".format(x))
c.text(-6, -5.5, r"$x(t)={:f}$".format(2.54/72*p.normsubpaths[0].normsubpathitems[0].x_pt(x)))
c.text(-6, -6, r"$\dot x(t)={:f}$".format(2.54/72*p.normsubpaths[0].normsubpathitems[0].xdot_pt(x)))
c.text(-6, -6.5, r"$\ddot x(t)={:f}$".format(2.54/72*p.normsubpaths[0].normsubpathitems[0].xddot_pt(x)))
c.text(-3, -5.5, r"$y(t)={:f}$".format(2.54/72*p.normsubpaths[0].normsubpathitems[0].y_pt(x)))
c.text(-3, -6, r"$\dot y(t)={:f}$".format(2.54/72*p.normsubpaths[0].normsubpathitems[0].ydot_pt(x)))
c.text(-3, -6.5, r"$\ddot y(t)={:f}$".format(2.54/72*p.normsubpaths[0].normsubpathitems[0].yddot_pt(x)))
c.text(0, -6, r"datan2$(\dot y(t), \dot x(t))={:f}$".format(math.atan2(2.54/72*p.normsubpaths[0].normsubpathitems[0].ydot_pt(x), 2.54/72*p.normsubpaths[0].normsubpathitems[0].xdot_pt(x))*180/math.pi))
c.text(0, -6.5, r"datan2$(\ddot y(t), \ddot x(t))={:f}$".format(math.atan2(2.54/72*p.normsubpaths[0].normsubpathitems[0].yddot_pt(x), 2.54/72*p.normsubpaths[0].normsubpathitems[0].xddot_pt(x))*180/math.pi))

g = c.insert(graph.graphxy(width=10, xpos=-5, ypos=-20, key=graph.key.key(), y=graph.axis.lin(min=-10, max=10)))
g.plot(graph.data.functionxy(lambda t: 2.54/72*p.normsubpaths[0].normsubpathitems[0].y_pt(t), title=r"$y(t)$", min=0, max=1))
g.plot(graph.data.functionxy(lambda t: 2.54/72*p.normsubpaths[0].normsubpathitems[0].ydot_pt(t), title=r"$\dot y(t)$", min=0, max=1))
g.plot(graph.data.functionxy(lambda t: 2.54/72*p.normsubpaths[0].normsubpathitems[0].yddot_pt(t), title=r"$\ddot y(t)$", min=0, max=1))
g.stroke(g.xgridpath(x), [color.rgb.red])
g.stroke(g.ygridpath(0))

g = c.insert(graph.graphxy(width=10, xpos=-5, ypos=0.5+g.ypos+g.height, key=graph.key.key(), x=graph.axis.linkedaxis(g.axes[r"x"]), y=graph.axis.lin(min=-10, max=10)))
g.plot(graph.data.functionxy(lambda t: 2.54/72*p.normsubpaths[0].normsubpathitems[0].x_pt(t), title=r"$x(t)$", min=0, max=1))
g.plot(graph.data.functionxy(lambda t: 2.54/72*p.normsubpaths[0].normsubpathitems[0].xdot_pt(t), title=r"$\dot x(t)$", min=0, max=1))
g.plot(graph.data.functionxy(lambda t: 2.54/72*p.normsubpaths[0].normsubpathitems[0].xddot_pt(t), title=r"$\ddot x(t)$", min=0, max=1))
g.stroke(g.xgridpath(x), [color.rgb.red])
g.stroke(g.ygridpath(0))

c.writeEPSfile(r"cusp")
