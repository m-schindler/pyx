from pyx import *

gridmin, gridmax, gridnum = -1.5, 1.5, 170
gridx = [gridmin + (gridmax-gridmin)*i/(gridnum-1.0) for i in range(gridnum)]
absmin = 1.0e-4
absmax = 1.0
keyheight, keywidth, keydist = 3.5, 0.5, 0.5

def fct(x,y):
    return y*(3*x**2 - y**2)
title = r"$y(3x^2 - y^2)$"

# generate grid data:
dat = []
for x in gridx:
    for y in gridx:
        dat.append((x, y, fct(x,y)))
if absmax is None:
    absmax = max(c for x,y,c in dat)


# define color gradients:
gradient_neg = color.functiongradient_rgb( # red -> white
    f_r=lambda x: 1, #1-0.7*(1-x)**2,
    f_g=lambda x: x,
    f_b=lambda x: x)
gradient_pos = color.functiongradient_rgb( # white -> blue
    f_r=lambda x: 1-x,
    f_g=lambda x: 1-x,
    f_b=lambda x: 1)#1-0.7*x**2)
gradient_toolarge = color.rgb.black  # TODO: want to change this
gradient_toosmall = color.rgb.white  # TODO: want to change this


# all the axes:
texter_pos = graph.axis.texter.default(minusunity="-", plusunity="+")
texter_neg = graph.axis.texter.default(minusunity="-", plusunity="+")
coloraxis_pos = graph.axis.log(min=absmin, max=absmax, title=None, texter=texter_pos)
coloraxis_neg = graph.axis.log(min=-absmax, max=-absmin, title=None, texter=texter_neg)
keygraph_pos = graph.graphx(length=keyheight, size=keywidth, direction="vertical", x=coloraxis_pos)
keygraph_neg = graph.graphx(length=keyheight, size=keywidth, direction="vertical", x=coloraxis_neg)
keygraph_pos.axes["x2"] = graph.axis.linkedaxis(keygraph_pos.axes["x"], painter=graph.axis.painter.regular(innerticklength=None, labelattrs=None, titleattrs=None))
keygraph_neg.axes["x2"] = graph.axis.linkedaxis(keygraph_neg.axes["x"], painter=graph.axis.painter.regular(innerticklength=None, labelattrs=None, titleattrs=None))
density_pos = graph.style.density(coloraxis=coloraxis_pos, keygraph=keygraph_pos, gradient=gradient_pos)
density_neg = graph.style.density(coloraxis=coloraxis_neg, keygraph=keygraph_neg, gradient=gradient_neg)

# the density style:
density_pos_neg = graph.style.density_posneglog(
    gradient_pos=gradient_pos, toosmall_pos=gradient_toosmall, toolarge_pos=gradient_toolarge, coloraxis_pos=coloraxis_pos, keygraph_pos=keygraph_pos,
    gradient_neg=gradient_neg, toosmall_neg=gradient_toosmall, toolarge_neg=gradient_toolarge, coloraxis_neg=coloraxis_neg, keygraph_neg=keygraph_neg)

g = graph.graphxy(width=8, height=8,
   x=graph.axis.linear(min=-gridmin, max=gridmin, title=r"$x$"),
   y=graph.axis.linear(min=-gridmin, max=gridmin, title=r"$y$"))
g.plot(graph.data.points(dat, x=1, y=2, color=3, title=None), [density_pos_neg])
g.finish()
g.insert(keygraph_pos, [trafo.translate(g.width + keydist, g.height - keyheight)])
g.insert(keygraph_neg, [trafo.translate(g.width + keydist, 0)])
g.text(0.5*g.width, g.height+8.0*unit.x_pt, title, [text.halign.center])

g.writeEPSfile("density_double")
g.writePDFfile("density_double")
g.writeSVGfile("density_double")
