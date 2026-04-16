import sys; sys.path[:0] = ["../.."]
import io
import pyx
from pyx import *

from pyx.graph.style import _autokeygraph
import pyx.graph.data as datamodule

# these two classes are modified versions of
#   pyx.graph.style._keygraphstyle
#   pyx.graph.style.density
# based on pyx 0.15

class _posneg_keygraphstyle(pyx.graph.style._style):
    """a split keygraph to present positive and negative values independently (on log scales)"""

    autographkey = _autokeygraph

    def __init__(self, colorname="color",
                 gradient_pos=pyx.color.gradient.Grey, coloraxis_pos=None, keygraph_pos=pyx.graph.style._autokeygraph,
                 gradient_neg=pyx.color.gradient.Grey, coloraxis_neg=None, keygraph_neg=pyx.graph.style._autokeygraph,
                 toosmall_pos=None, toolarge_pos=None, toosmall_neg=None, toolarge_neg=None):
        self.colorname = colorname
        self.gradient_pos = gradient_pos
        self.gradient_neg = gradient_neg
        self.toosmall_pos = toosmall_pos
        self.toolarge_pos = toolarge_pos
        self.toosmall_neg = toosmall_neg
        self.toolarge_neg = toolarge_neg
        self.coloraxis_pos = coloraxis_pos
        self.coloraxis_neg = coloraxis_neg
        self.keygraph_pos = keygraph_pos
        self.keygraph_neg = keygraph_neg

        if self.toosmall_pos is None or self.toosmall_pos.colorspacestring() != self.gradient_pos.getcolor(0).colorspacestring():
            self.toosmall_pos = self.gradient_pos.getcolor(0)
        if self.toolarge_pos is None or self.toolarge_pos.colorspacestring() != self.gradient_pos.getcolor(0).colorspacestring():
            self.toolarge_pos = self.gradient_pos.getcolor(1)
        if self.toosmall_neg is None or self.toosmall_neg.colorspacestring() != self.gradient_neg.getcolor(0).colorspacestring():
            self.toosmall_neg = self.gradient_neg.getcolor(1)
        if self.toolarge_neg is None or self.toolarge_neg.colorspacestring() != self.gradient_neg.getcolor(0).colorspacestring():
            self.toolarge_neg = self.gradient_neg.getcolor(0)

    def columnnames(self, privatedata, sharedata, graph, columnnames, dataaxisnames):
        return [self.colorname]

    def adjustaxis(self, privatedata, sharedata, graph, plotitem, columnname, data):
        if columnname == self.colorname:
            # do the same thing twice: here for pos
            if self.keygraph_pos is None:
                # we always need a keygraph, but we might not show it
                if self.coloraxis_pos is None:
                    coloraxis_pos = pyx.graph.axis.log()
                else:
                    coloraxis_pos = self.coloraxis_pos
                privatedata.keygraph_pos = graphx(length=4, direction="vertical", x=coloraxis_pos)
            elif self.keygraph_pos is pyx.graph.style._autokeygraph:
                if self.coloraxis_pos is None:
                    coloraxis_pos = pyx.graph.axis.lin(title=plotitem.title)
                    plotitem.title = None # Huui!?
                else:
                    coloraxis_pos = self.coloraxis_pos
                privatedata.keygraph_pos = graphx(x=coloraxis_pos, **graph.autokeygraphattrs())
            else:
                privatedata.keygraph_pos = self.keygraph_pos
            # TODO: we shouldn't have multiple plotitems
            #rom . import data as datamodule
            privatedata.keygraph_pos.plot(datamodule.values(x=data), [pyx.graph.style.gradient(gradient=self.gradient_pos)])

            # do the same thing twice: and here for neg
            if self.keygraph_neg is None:
                # we always need a keygraph, but we might not show it
                if self.coloraxis_neg is None:
                    coloraxis_neg = pyx.graph.axis.log()
                else:
                    coloraxis_neg = self.coloraxis_neg
                privatedata.keygraph_neg = graphx(length=4, direction="vertical", x=coloraxis_neg)
            elif self.keygraph_neg is pyx.graph.style._autokeygraph:
                if self.coloraxis_neg is None:
                    coloraxis_neg = pyx.graph.axis.lin(title=plotitem.title)
                    plotitem.title = None # Huui!?
                else:
                    coloraxis_neg = self.coloraxis_neg
                privatedata.keygraph_neg = graphx(x=coloraxis_neg, **graph.autokeygraphattrs())
            else:
                privatedata.keygraph_neg = self.keygraph_neg
            # TODO: we shouldn't have multiple plotitems
            #rom . import data as datamodule
            privatedata.keygraph_neg.plot(datamodule.values(x=data), [pyx.graph.style.gradient(gradient=self.gradient_neg)])

    def color(self, privatedata, c):
        if c > 0:
            keygraph = privatedata.keygraph_pos
            thegradient = self.gradient_pos
            toosmall = self.toosmall_pos
            toolarge = self.toolarge_pos
        else:
            keygraph = privatedata.keygraph_neg
            thegradient = self.gradient_neg
            toosmall = self.toolarge_neg # notice that we understand "small" and "large"
            toolarge = self.toosmall_neg # as of the absolute value

        vc = keygraph.axes["x"].convert(c)
        if vc < 0:
            return toosmall
            #logger.warning("gradient color range is exceeded (lower bound)")
            #vc = 0
        if vc > 1:
            return toolarge
            #logger.warning("gradient color range is exceeded (upper bound)")
            #vc = 1
        return thegradient.getcolor(vc)

    def donedrawpoints(self, privatedata, sharedata, graph):
        if self.keygraph_pos is pyx.graph.style._autokeygraph:
            graph.layer("key").insert(privatedata.keygraph_pos, [graph.autokeygraphtrafo(privatedata.keygraph_pos)])
        if self.keygraph_neg is pyx.graph.style._autokeygraph:
            graph.layer("key").insert(privatedata.keygraph_neg, [graph.autokeygraphtrafo(privatedata.keygraph_neg)])


class posneg_density(_posneg_keygraphstyle):
    """Plot positive and negative values on different color gradients"""

    needsdata = ["values1", "values2", "data12", "data21"]

    def __init__(self, epsilon=1e-10, **kwargs):
        _posneg_keygraphstyle.__init__(self, **kwargs)
        self.epsilon = epsilon

    def initdrawpoints(self, privatedata, sharedata, graph):
        privatedata.colors = {}
        privatedata.vfixed = [None]*len(graph.axesnames)

    def drawpoint(self, privatedata, sharedata, graph, point):
        privatedata.colors.setdefault(sharedata.value1, {})[sharedata.value2] = point[self.colorname]
        if len(privatedata.vfixed) > 2 and sharedata.vposavailable:
            for i, (v1, v2) in enumerate(list(zip(privatedata.vfixed, sharedata.vpos))):
                if i != sharedata.index1 and i != sharedata.index2:
                    if v1 is None:
                        privatedata.vfixed[i] = v2
                    elif abs(v1-v2) > self.epsilon:
                        raise ValueError("data must be in a plane for the density style")

    def donedrawpoints(self, privatedata, sharedata, graph):
        privatedata.keygraph_pos.doaxes()
        privatedata.keygraph_neg.doaxes()

        values1 = sorted(list(sharedata.values1.keys()))
        values2 = sorted(list(sharedata.values2.keys()))
        def equidistant(values):
            l = len(values) - 1
            if l < 1:
                raise ValueError("several data points required by the density style in each dimension")
            range = values[-1] - values[0]
            for i, value in enumerate(values):
                if abs(value - values[0] - i * range / l) > self.epsilon:
                    raise ValueError("data must be equidistant for the density style")
        equidistant(values1)
        equidistant(values2)
        needalpha = False
        for value2 in values2:
            for value1 in values1:
                try:
                    available, valid, v = sharedata.data12[value1][value2]
                except KeyError:
                    needalpha = True
                    break
                if not available:
                    needalpha = True
                    continue
            else:
                continue
            break
        mode = {"/DeviceGray": "L",
                "/DeviceRGB": "RGB",
                "/DeviceCMYK": "CMYK"}[self.gradient_pos.getcolor(0).colorspacestring()]
        # can have only one mode: XXX complain instead of assert!
        assert self.gradient_pos.getcolor(0).colorspacestring() == self.gradient_neg.getcolor(0).colorspacestring()
        if needalpha:
            mode = mode + "A"
        empty = b"\0"*len(mode)
        data = io.BytesIO()
        for value2 in values2:
            for value1 in values1:
                try:
                    available, valid, v = sharedata.data12[value1][value2]
                except KeyError:
                    data.write(empty)
                    continue
                if not available:
                    data.write(empty)
                    continue
                c = privatedata.colors[value1][value2]
                try:
                    c = self.color(privatedata, c)
                except TypeError:
                    data.write(empty)
                    continue

                data.write(c.to8bitbytes())
                if needalpha:
                    data.write(bytes((255,)))
        i = bitmap.image(len(values1), len(values2), mode, data.getvalue())

        v1enlargement = (values1[-1]-values1[0])*0.5/(len(values1)-1)
        v2enlargement = (values2[-1]-values2[0])*0.5/(len(values2)-1)

        privatedata.vfixed[sharedata.index1] = values1[0]-v1enlargement
        privatedata.vfixed[sharedata.index2] = values2[-1]+v2enlargement
        x1_pt, y1_pt = graph.vpos_pt(*privatedata.vfixed)
        privatedata.vfixed[sharedata.index1] = values1[-1]+v1enlargement
        privatedata.vfixed[sharedata.index2] = values2[-1]+v2enlargement
        x2_pt, y2_pt = graph.vpos_pt(*privatedata.vfixed)
        privatedata.vfixed[sharedata.index1] = values1[0]-v1enlargement
        privatedata.vfixed[sharedata.index2] = values2[0]-v2enlargement
        x3_pt, y3_pt = graph.vpos_pt(*privatedata.vfixed)
        t = trafo.trafo_pt(((x2_pt-x1_pt, x3_pt-x1_pt), (y2_pt-y1_pt, y3_pt-y1_pt)), (x1_pt, y1_pt))

        privatedata.vfixed[sharedata.index1] = values1[-1]+v1enlargement
        privatedata.vfixed[sharedata.index2] = values2[0]-v2enlargement
        vx4, vy4 = t.inverse().apply_pt(*graph.vpos_pt(*privatedata.vfixed))
        if abs(vx4 - 1) > self.epsilon or abs(vy4 - 1) > self.epsilon:
            raise ValueError("invalid graph layout for density style (bitmap positioning by affine transformation failed)")

        p = path.path()
        privatedata.vfixed[sharedata.index1] = 0
        privatedata.vfixed[sharedata.index2] = 0
        p.append(path.moveto_pt(*graph.vpos_pt(*privatedata.vfixed)))
        vfixed2 = privatedata.vfixed + privatedata.vfixed
        vfixed2[sharedata.index1] = 0
        vfixed2[sharedata.index2] = 0
        vfixed2[sharedata.index1 + len(graph.axesnames)] = 1
        vfixed2[sharedata.index2 + len(graph.axesnames)] = 0
        p.append(graph.vgeodesic_el(*vfixed2))
        vfixed2[sharedata.index1] = 1
        vfixed2[sharedata.index2] = 0
        vfixed2[sharedata.index1 + len(graph.axesnames)] = 1
        vfixed2[sharedata.index2 + len(graph.axesnames)] = 1
        p.append(graph.vgeodesic_el(*vfixed2))
        vfixed2[sharedata.index1] = 1
        vfixed2[sharedata.index2] = 1
        vfixed2[sharedata.index1 + len(graph.axesnames)] = 0
        vfixed2[sharedata.index2 + len(graph.axesnames)] = 1
        p.append(graph.vgeodesic_el(*vfixed2))
        vfixed2[sharedata.index1] = 0
        vfixed2[sharedata.index2] = 1
        vfixed2[sharedata.index1 + len(graph.axesnames)] = 0
        vfixed2[sharedata.index2 + len(graph.axesnames)] = 0
        p.append(graph.vgeodesic_el(*vfixed2))
        p.append(path.closepath())

        c = canvas.canvas([canvas.clip(p)])
        b = bitmap.bitmap_trafo(t, i)
        c.insert(b)
        graph.layer("filldata").insert(c)

        _posneg_keygraphstyle.donedrawpoints(self, privatedata, sharedata, graph)


# the example function to plot:
def fct(x, y):
    return (3*x**5*y - 10*x**3*y**3 + 3*x*y**5) / 16.0

xmax = 1.5
xmin = -xmax
w = 8.0
num = 70
xvalues = [xmin + (xmax-xmin)*i/(num-1.0) for i in range(num)]

datapts = []
for i, x in enumerate(xvalues):
    for j, y in enumerate(xvalues):
        value = fct(x, y)
        datapts.append((i,j, x,y, value,
                                  value if value > 0 else None,
                                 -value if value < 0 else None))
mm = max(max(d[4] for d in datapts), -min(d[4] for d in datapts))
mm -= 2.5

databds_pos = (1e-5, mm) # need explicit bounds
databds_neg = (-mm, -1e-5) # need explicit bounds
coltitle = None
xwidth = 10
ywidth = 10
keydist = 0.6
keysep = 0.7
keyheight = None
keywidth = 0.7

assert 0 < databds_pos[0] < databds_pos[1]
assert databds_neg[0] < databds_neg[1] < 0
# define color gradients:
gradient_neg = pyx.color.functiongradient_rgb( # red -> white
    f_r=lambda x: 1-0.7*(1-x)**2,
    f_g=lambda x: x,
    f_b=lambda x: x)
gradient_pos = pyx.color.functiongradient_rgb( # white -> blue
    f_r=lambda x: 1-x,
    f_g=lambda x: 1-x,
    f_b=lambda x: 1-0.7*x**2)
gradient_toolarge = pyx.color.rgb.white
gradient_toosmall = pyx.color.rgb.black

# keygraphs
cpd = dict()
#cpd["labeldist"] = 0.1 * unit.u_cm
#cpd["innerticklength"] = 0.3 * keywidth
if keyheight is None:
    keyheight = 0.5*(ywidth - keysep)

# define the coloraxes, keygraphs, density styles:
texter_pos = pyx.graph.axis.texter.default(minusunity="-", plusunity="+")
texter_neg = pyx.graph.axis.texter.default(minusunity="-", plusunity="+")
coloraxis_pos = pyx.graph.axis.log(min=databds_pos[0], max=databds_pos[1], title=coltitle, painter=pyx.graph.axis.painter.regular(**cpd), reverse=False, texter=texter_pos)
coloraxis_neg = pyx.graph.axis.log(min=databds_neg[0], max=databds_neg[1], title=coltitle, painter=pyx.graph.axis.painter.regular(**cpd), reverse=False, texter=texter_neg)
keygraph_pos = graph.graphx(length=keyheight, size=keywidth, direction="vertical", x=coloraxis_pos)
keygraph_neg = graph.graphx(length=keyheight, size=keywidth, direction="vertical", x=coloraxis_neg)
keygraph_pos.axes["x2"] = pyx.graph.axis.linkedaxis(keygraph_pos.axes["x"], painter=pyx.graph.axis.painter.regular(innerticklength=None, labelattrs=None, titleattrs=None))
keygraph_neg.axes["x2"] = pyx.graph.axis.linkedaxis(keygraph_neg.axes["x"], painter=pyx.graph.axis.painter.regular(innerticklength=None, labelattrs=None, titleattrs=None))
density_pos = graph.style.density(coloraxis=coloraxis_pos, keygraph=keygraph_pos, gradient=gradient_pos)
density_neg = graph.style.density(coloraxis=coloraxis_neg, keygraph=keygraph_neg, gradient=gradient_neg)

density_pos_neg = posneg_density(
    gradient_pos=gradient_pos, toosmall_pos=gradient_toosmall, toolarge_pos=gradient_toolarge, coloraxis_pos=coloraxis_pos, keygraph_pos=keygraph_pos,
    gradient_neg=gradient_neg, toosmall_neg=gradient_toosmall, toolarge_neg=gradient_toolarge, coloraxis_neg=coloraxis_neg, keygraph_neg=keygraph_neg)

g = pyx.graph.graphxy(width=xwidth, height=ywidth,
    x=pyx.graph.axis.linear(title=r"x"),
    y=pyx.graph.axis.linear(title=r"y"),
    )

# plot:
g.plot(pyx.graph.data.points(datapts, x=3, y=4, color=5, title=None), [density_pos_neg])

# insert keygraphs
keygraph_pos.finish()
keygraph_neg.finish()
g.insert(keygraph_pos, [trafo.translate(g.width + keydist, g.height - keyheight)])
g.insert(keygraph_neg, [trafo.translate(g.width + keydist, 0)])

g.writeEPSfile()
g.writePDFfile()
g.writeSVGfile()

