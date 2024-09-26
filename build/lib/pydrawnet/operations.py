# Copyright (c) 2024, Nathan Hansen
# All rights reserved.

# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

from matplotlib.collections import PatchCollection, LineCollection
from matplotlib.patches import Rectangle, Circle, Polygon
from matplotlib.text import Text
from enum import Enum
from math import sin, cos, pi

# text_kwargs: https://matplotlib.org/stable/api/text_api.html#matplotlib.text.Text


# TODO: keep?
class Edges(Enum):
    TL = 0  # Top-Left
    TR = 1  # Top-Right
    BR = 2  # Bottom-Right
    BL = 3  # Bottom-Left


def make_arrow(X, Y, W, H, rotation=0):
    """
    Returns the line segment coordinates for a simple rotatable arrow

    Parameters
    ----------
    X : float
        The horizontal position of the arrow center
    Y : float
        The vertical position of the arrow center
    W : float
        The width of the arrow
    H : float
        The height of the arrow
    rotation : float
        The angle of the arrow in degrees
    """
    segments = [
        (W / 2, 0),
        (-W / 2, H / 2),
        (-W / 2, -H / 2),
        (W / 2, 0),
    ]
    if rotation != 0:
        rot = rotation * pi / 180
        new_segments = []
        for x, y in segments:
            new_segments.append(
                (
                    x * cos(rot) - y * sin(rot),
                    x * sin(rot) + y * cos(rot),
                )
            )
        return [(x + X, y + Y) for x, y in new_segments]
    else:
        return [(x + X, y + Y) for x, y in segments]


class Conv2dOp:
    """For plotting kernel operation visualizations between layers"""

    def __init__(
        self,
        kernel: tuple = (4, 4),
        stride: int = 2,
        reverse: bool = False,
        label: str = "Conv2d",
        label_only: bool = False,
        loc: str = "below",
        kernel_color: tuple = (0.1, 0.1, 0.1),
        line_kwargs: dict | None = None,
        text_kwargs: dict | None = None,
    ) -> None:
        """
        Parameters
        ----------
        kernel : tuple (int, int)
            The size of the kernel in the convolution operation
        stride : int
            The size of the stride in the convolution operation
        reverse : bool
            Whether to show downsampling (False) or upsampling (True)
        label : str
            A brief description of the operation
        label_only : bool
            Whether to include kernel and stride info with the label
        loc : str
            The location of the label, either 'above' or 'below'
        kernel_color : tuple (float, float, float)
            The RGB fill color of the kernel rectangle
        line_kwargs : dict | None
            Keyword arguments to be passed to the LineCollection
        text_kwargs : dict | None
            Keyword arguments to be passed to matplotlib Text object
        """

        assert len(kernel) == 2, "Must be a 2D kernel"

        self.kernel = kernel
        self.reverse = reverse
        if label_only:
            self.text = label
        else:
            self.text = f"{label}\n{kernel[0]}x{kernel[1]} Kernel\nStride {stride}"
        self.loc = loc
        self.kernel_color = kernel_color
        self.line_kwargs = line_kwargs
        self.text_kwargs = text_kwargs

    def make_collection(self, objA, objB):
        """Generates a PatchCollection and LineCollection containing all graphics to be drawn other than text

        objA : BaseLayer
            The left-side object being connected
        objB : BaseLayer
            The right-side object being connected
        """
        kw, kh = self.kernel

        if self.reverse:
            assert (
                kw <= objB.width and kh <= objB.height
            ), f"Kernel dimensions {(self.kernel)} can't be larger than layer dimensions {objB.width, objB.height}"

            # TL, TR, BL, BR
            _, _, _, BR = objA.get_corners()
            X1 = BR[0] - 0.1 * objA.width
            Y1 = BR[1] + 0.1 * objA.height

            # TL, TR, BL, BR
            _, _, _, BR = objB.get_corners()
            X2 = BR[0] - max(0.9 * objB.width, kw)
            Y2 = BR[1] + max(0.9 * objB.height-kh, 0)

            colors = [self.kernel_color, self.kernel_color]
            patches = [
                Rectangle((X1, Y1), 1, 1),
                Rectangle((X2, Y2), *self.kernel),
            ]
            pcol = PatchCollection(patches, ec="k", fc=colors)

            segments = [
                [(X1 + 1, Y1 + 1), (X2, Y2 + kh)],
                [(X1 + 1, Y1), (X2, Y2)],
            ]

            self.text_X = (X1 + kw + X2) / 2

            return pcol, LineCollection(
                segments,
                ec="k",
                **self.line_kwargs if self.line_kwargs is not None else {},
            )
        else:
            assert (
                kw <= objA.width and kh <= objA.height
            ), f"Kernel dimensions {(self.kernel)} can't be larger than layer dimensions {objA.width, objA.height}"

            # TL, TR, BL, BR
            _, _, _, BR = objA.get_corners()
            X1 = BR[0] - min(objA.width, 0.1 * objA.width + kw)
            Y1 = BR[1] + min(objA.height - kh, 0.1 * objA.height)

            # TL, TR, BL, BR
            _, _, _, BR = objB.get_corners()
            X2 = BR[0] - 0.9 * objB.width
            Y2 = BR[1] + 0.9 * objB.height - 1

            colors = [self.kernel_color, self.kernel_color]
            patches = [
                Rectangle((X1, Y1), *self.kernel),
                Rectangle((X2, Y2), 1, 1),
            ]
            pcol = PatchCollection(patches, ec="k", fc=colors)

            segments = [
                [(X1 + kw, Y1 + kh), (X2, Y2 + 1)],
                [(X1 + kw, Y1), (X2, Y2)],
            ]

            self.text_X = (X1 + kw + X2) / 2

            return pcol, LineCollection(
                segments,
                ec="k",
                **self.line_kwargs if self.line_kwargs is not None else {},
            )


class LinearOp:
    """For plotting simple diagonal lines between layers"""

    def __init__(
        self,
        label: str = "Linear",
        loc: str = "below",
        line_kwargs: dict | None = None,
        text_kwargs: dict | None = None,
    ) -> None:
        """
        Parameters
        ----------
        label : str
            A brief description of the operation
        loc : str
            The location of the label, either 'above' or 'below'
        line_kwargs : dict | None
            Keyword arguments to be passed to the LineCollection
        text_kwargs : dict | None
            Keyword arguments to be passed to matplotlib Text object
        """
        self.text = label
        self.loc = loc
        self.line_kwargs = line_kwargs
        self.text_kwargs = text_kwargs

    def make_collection(self, objA, objB):
        """Generates a LineCollection containing all graphics to be drawn other than text

        objA : BaseLayer
            The left-side object being connected
        objB : BaseLayer
            The right-side object being connected
        """

        # TL, TR, BL, BR
        _, (X1, Y1), _, (X1_2, Y1_2) = objA.get_corners()
        (X2, Y2), _, (X2_2, Y2_2), _ = objB.get_corners()

        segments = [
            [(X1, Y1), (X2, Y2)],
            [(X1_2, Y1_2), (X2_2, Y2_2)],
        ]
        self.text_X = (X1_2 + X2_2) / 2

        return LineCollection(
            segments,
            ec="k",
            **self.line_kwargs if self.line_kwargs is not None else {},
        )


class DenseOp:
    """For plotting dense connection lines between layers"""

    def __init__(
        self,
        numA: int = 1,
        numB: int = 1,
        label: str = "Dense",
        loc: str = "below",
        limited_ends: int | tuple | None = None,
        line_kwargs: dict | None = None,
        text_kwargs: dict | None = None,
    ) -> None:
        """
        Parameters
        ----------
        numA : int
            Number of connections on the left-side
        numB : int
            Number of connections on the right-side
        label : str
            A brief description of the operation
        loc : str
            The location of the label, either 'above' or 'below'
        limited_ends : int | tuple | None
            If not None, then only add connections for at most the top/bottom
            <limited_ends> # of features
        line_kwargs : dict | None
            Keyword arguments to be passed to the LineCollection
        text_kwargs : dict | None
            Keyword arguments to be passed to matplotlib Text object
        """
        assert numA > 0 and numB > 0

        self.numA = numA
        self.numB = numB
        self.text = label
        self.loc = loc
        self.line_kwargs = line_kwargs
        self.text_kwargs = text_kwargs
        self.limited_ends = limited_ends

    def make_collection(self, objA, objB):
        """Generates a LineCollection containing all graphics to be drawn other than text

        objA : BaseLayer
            The left-side object being connected
        objB : BaseLayer
            The right-side object being connected
        """

        # TL, TR, BL, BR
        _, (X1, Y1), _, (X1_2, Y1_2) = objA.get_corners()
        (X2, Y2), _, (X2_2, Y2_2), _ = objB.get_corners()

        if hasattr(objA, "yival"):
            # Use pre-defined spacing, if available
            ivalAY = objA.yival
            offsetAY = objA.height / 2
        else:
            # Estimate spacing
            ivalAY = abs(Y1_2 - Y1) / self.numA
            offsetAY = ivalAY / 2

        if hasattr(objB, "yival"):
            # Use pre-defined spacing, if available
            ivalBY = objB.yival
            offsetBY = objB.height / 2
        else:
            # Estimate spacing
            ivalBY = abs(Y2_2 - Y2) / self.numB
            offsetBY = ivalBY / 2

        ivalAX = (X1_2 - X1) / self.numA
        ivalBX = (X2_2 - X2) / self.numB

        baseY1 = Y1 - offsetAY
        baseY2 = Y2 - offsetBY
        baseX1 = X1 + ivalAX / 2
        baseX2 = X2 + ivalBX / 2

        if self.limited_ends is None:
            irange = range(self.numA)
            jrange = range(self.numB)
        elif isinstance(self.limited_ends, list) or isinstance(
            self.limited_ends, tuple
        ):
            if self.limited_ends[0] is None:
                irange = range(self.numA)
            else:
                irange = list(range(self.limited_ends[0])) + list(
                    range(self.numA - self.limited_ends[0], self.numA)
                )
            if self.limited_ends[1] is None:
                jrange = range(self.numB)
            else:
                jrange = list(range(self.limited_ends[1])) + list(
                    range(self.numB - self.limited_ends[1], self.numB)
                )
        else:
            irange = list(range(self.limited_ends)) + list(
                range(self.numA - self.limited_ends, self.numA)
            )
            jrange = list(range(self.limited_ends)) + list(
                range(self.numB - self.limited_ends, self.numB)
            )

        segments = []
        for i in irange:
            for j in jrange:
                segments.append(
                    [
                        (baseX1 + ivalAX * i, baseY1 - ivalAY * i),
                        (baseX2 + ivalBX * j, baseY2 - ivalBY * j),
                    ]
                )

        self.text_X = (X1_2 + X2_2) / 2
        return LineCollection(
            segments,
            ec="k",
            **self.line_kwargs if self.line_kwargs is not None else {},
        )


class ArrowOp:
    """For plotting horizontal arrows between layers"""

    def __init__(
        self,
        label: str = "Arrow",
        arrow_size: float = 3,
        arrow_offset: float = 0,
        offset: float = 0,
        draw_lines: bool = True,
        loc: str = "below",
        line_kwargs: dict | None = None,
        text_kwargs: dict | None = None,
    ) -> None:
        """
        Parameters
        ----------
        label : str
            A brief description of the operation
        arrow_size : float
            The scale of the arrow
        arrow_offset : float
            Horizontal offset of the arrow from the midpoint between objects
        offset : float
            Horizontal offset of lines from the edges of the objects
        draw_lines : bool
            Whether to draw the lines on either side of the arrow
        loc : str
            The location of the label, either 'above' or 'below'
        line_kwargs : dict | None
            Keyword arguments to be passed to the LineCollection
        text_kwargs : dict | None
            Keyword arguments to be passed to matplotlib Text object
        """
        self.text = label
        self.arrow_size = arrow_size
        self.arrow_offset = arrow_offset
        self.offset = offset
        self.draw_lines = draw_lines
        self.loc = loc
        self.line_kwargs = line_kwargs
        self.text_kwargs = text_kwargs

    def make_collection(self, objA, objB):
        """Generates a LineCollection containing all graphics to be drawn other than text

        objA : BaseLayer
            The left-side object being connected
        objB : BaseLayer
            The right-side object being connected
        """
        # TL, TR, BL, BR
        _, _, _, (X1, Y1) = objA.get_corners()
        (X2, Y2), _, _, _ = objB.get_corners()

        Y1 += objA.tot_height / 2
        Y2 -= objB.tot_height / 2

        Xmid = (X2 + X1) / 2 + self.arrow_offset
        Ymid = (Y2 + Y1) / 2

        if self.arrow_size > 0:
            segments = [make_arrow(Xmid, Ymid, self.arrow_size, self.arrow_size)]
        else:
            segments = []

        if self.draw_lines:
            segments.extend(
                [
                    [(X1 + self.offset, Y1), (Xmid - self.arrow_size / 2, Ymid)],
                    [(Xmid + self.arrow_size / 2, Ymid), (X2 - self.offset, Y2)],
                ]
            )

        self.text_X = (X1 + X2) / 2

        return LineCollection(
            segments,
            ec="k",
            **self.line_kwargs if self.line_kwargs is not None else {},
        )


class BlankOp:
    """For use when no operation should be shown between layers"""

    def __init__(
        self,
        label: str = "Blank",
        loc: str = "below",
        text_kwargs: dict | None = None,
    ) -> None:
        """
        Parameters
        ----------
        label : str
            A brief description of the operation
        loc : str
            The location of the label, either 'above' or 'below'
        text_kwargs : dict | None
            Keyword arguments to be passed to matplotlib Text object
        """
        self.text = label
        self.loc = loc
        self.text_kwargs = text_kwargs

    def make_collection(self, objA, objB):
        """Since no graphics are drawn only the text X position is calculated

        objA : BaseLayer
            The left-side object being connected
        objB : BaseLayer
            The right-side object being connected
        """
        # TL, TR, BL, BR
        _, _, _, (X1, Y1) = objA.get_corners()
        _, _, (X2, Y2), _ = objB.get_corners()
        self.text_X = (X1 + X2) / 2
        return None


class ResidualOp:
    """For plotting residual arrows between layers"""

    def __init__(
        self,
        label: str = "Residual",
        arrow_size: float = 3,
        xoffset: float = 3,
        yoffset: float = -10,
        show_vert_arrows: bool = False,
        show_hori_segments: bool = False,
        connection_radius: float = 1,
        loc: str = "below",
        line_kwargs: dict | None = None,
        text_kwargs: dict | None = None,
    ) -> None:
        """
        Parameters
        ----------
        label : str
            A brief description of the operation
        arrow_size : float
            The scale of the arrow
        xoffset : float | tuple (float, float)
            Horizontal offset from the edges of the objects
        yoffset : float | tuple (float, float)
            Vertical offset from the edges of the objects
        show_vert_arrows : bool
            Whether to draw arrows on the vertical portions of the graphic
        show_hori_segments : bool
            Whether to draw the short horizontal segments connecting
            the vertical segments to the objects
        connection_radius : float
            The radii of dots marking the horizontal segment connection point
            Set to zero to disable
        loc : str
            The location of the label, either 'above' or 'below'
        line_kwargs : dict | None
            Keyword arguments to be passed to the LineCollection
        text_kwargs : dict | None
            Keyword arguments to be passed to matplotlib Text object
        """
        self.text = label
        self.arrow_size = arrow_size
        self.xoffset = xoffset
        self.yoffset = yoffset
        self.show_vert_arrows = show_vert_arrows
        self.show_hori_segments = show_hori_segments
        self.connection_radius = connection_radius
        self.loc = loc
        self.line_kwargs = line_kwargs
        self.text_kwargs = text_kwargs

    def make_collection(self, objA, objB):
        """Generates a LineCollection containing all graphics to be drawn other than text

        objA : BaseLayer
            The left-side object being connected
        objB : BaseLayer
            The right-side object being connected
        """
        # TL, TR, BL, BR
        _, _, _, (X1, Y1) = objA.get_corners()
        (X2, Y2), _, _, _ = objB.get_corners()

        Y1 += objA.tot_height / 2
        Y2 -= objB.tot_height / 2

        Xmid = (X1 + X2) / 2
        Ymid = (Y2 + Y1) / 2 + self.yoffset

        segments = []

        if self.show_hori_segments:
            segments.append(
                [
                    (X1, Y1),
                    (X1 + self.xoffset, Y1),
                    (X1 + self.xoffset, Y1 + self.yoffset),
                    (Xmid - self.arrow_size / 2, Ymid),
                ]
            )
            segments.append(
                [
                    (Xmid + self.arrow_size / 2, Ymid),
                    (X2 - self.xoffset, Y2 + self.yoffset),
                    (X2 - self.xoffset, Y2),
                    (X2, Y2),
                ]
            )
        else:
            segments.append(
                [
                    (X1 + self.xoffset, Y1),
                    (X1 + self.xoffset, Y1 + self.yoffset),
                    (Xmid - self.arrow_size / 2, Ymid),
                ]
            )
            segments.append(
                [
                    (Xmid + self.arrow_size / 2, Ymid),
                    (X2 - self.xoffset, Y2 + self.yoffset),
                    (X2 - self.xoffset, Y2),
                ]
            )

        segments.append(make_arrow(Xmid, Ymid, self.arrow_size, self.arrow_size))

        if self.show_vert_arrows:
            segments.append(
                make_arrow(
                    X1 + self.xoffset,
                    Y1 + self.yoffset / 2,
                    self.arrow_size,
                    self.arrow_size,
                    rotation=-90,
                )
            )
            segments.append(
                make_arrow(
                    X2 - self.xoffset,
                    Y2 + self.yoffset / 2,
                    self.arrow_size,
                    self.arrow_size,
                    rotation=90,
                )
            )

        self.text_X = (X1 + X2) / 2

        out = [
            LineCollection(
                segments,
                ec="k",
                **self.line_kwargs if self.line_kwargs is not None else {},
                zorder=-10,
            )
        ]

        if self.connection_radius > 0:
            circles = [
                Circle((X1 + self.xoffset, Y1), self.connection_radius),
                Circle((X2 - self.xoffset, Y2), self.connection_radius),
            ]
            out.append(PatchCollection(circles, ec="k", fc="k"))

        return out


class CircleOp:
    """For plotting circled symbols between layers"""

    def __init__(
        self,
        label: str = "Circle",
        symbol: str = "+",
        diameter: float = 3,
        symbol_kwargs: dict | None = None,
        fill_color: tuple = (1, 1, 1),
        offset: float = 0,
        loc: str = "below",
        line_kwargs: dict | None = None,
        text_kwargs: dict | None = None,
    ) -> None:
        """
        Parameters
        ----------
        label : str
            A brief description of the operation
        symbol : str
            The symbol to be drawn within a circle
        diameter : float
            The diameter of the circle containing the symbol
        symbol_kwargs : dict | None
            Keyword arguments to be passed to the symbol Text object
        fill_color : RGB tuple (float, float, float)
            The color to fill the circle with
        offset : float
            Horizontal offset from the edges of the objects
        loc : str
            The location of the label, either 'above' or 'below'
        line_kwargs : dict | None
            Keyword arguments to be passed to the LineCollection
        text_kwargs : dict | None
            Keyword arguments to be passed to the label Text object
        """
        self.text = label
        self.symbol = symbol
        self.diameter = diameter
        self.symbol_kwargs = symbol_kwargs
        self.fill_color = fill_color
        self.offset = offset
        self.loc = loc
        self.line_kwargs = line_kwargs
        self.text_kwargs = text_kwargs

    def make_collection(self, objA, objB):
        """Generates a LineCollection containing all graphics to be drawn other than text

        objA : BaseLayer
            The left-side object being connected
        objB : BaseLayer
            The right-side object being connected
        """
        # TL, TR, BL, BR
        _, _, _, (X1, Y1) = objA.get_corners()
        (X2, Y2), _, _, _ = objB.get_corners()

        Y1 += objA.tot_height / 2
        Y2 -= objB.tot_height / 2

        Xmid = (X2 + X1) / 2
        Ymid = (Y2 + Y1) / 2

        segments = [
            [(X1 + self.offset, Y1), (Xmid - self.diameter / 2, Ymid)],
            [(Xmid + self.diameter / 2, Ymid), (X2 - self.offset, Y2)],
        ]

        circle = [Circle((Xmid, Ymid), self.diameter / 2)]

        txt = Text(
            Xmid,
            Ymid,
            self.symbol,
            va="center",
            ha="center",
            **self.symbol_kwargs if self.symbol_kwargs is not None else {},
        )

        self.text_X = (X1 + X2) / 2

        return (
            LineCollection(
                segments,
                ec="k",
                **self.line_kwargs if self.line_kwargs is not None else {},
            ),
            PatchCollection(circle, ec="k", fc=self.fill_color),
            txt,
        )


class DiamondOp:
    """For plotting diamond-enclosed symbols between layers"""

    def __init__(
        self,
        label: str = "Diamond",
        symbol: str = "+",
        width: float = 3,
        height: float = 3,
        symbol_kwargs: dict | None = None,
        fill_color: tuple = (1, 1, 1),
        offset: float = 0,
        loc: str = "below",
        line_kwargs: dict | None = None,
        text_kwargs: dict | None = None,
    ) -> None:
        """
        Parameters
        ----------
        label : str
            A brief description of the operation
        symbol : str
            The symbol to be drawn within a diamond
        width : float
            The point-to-point width of the diamond containing the symbol
        height : float
            The point-to-point height of the diamond containing the symbol
        symbol_kwargs : dict | None
            Keyword arguments to be passed to the symbol Text object
        fill_color : RGB tuple (float, float, float)
            The color to fill the diamond with
        offset : float
            Horizontal offset from the edges of the objects
        loc : str
            The location of the label, either 'above' or 'below'
        line_kwargs : dict | None
            Keyword arguments to be passed to the LineCollection
        text_kwargs : dict | None
            Keyword arguments to be passed to the label Text object
        """
        self.text = label
        self.symbol = symbol
        self.width = width
        self.height = height
        self.symbol_kwargs = symbol_kwargs
        self.fill_color = fill_color
        self.offset = offset
        self.loc = loc
        self.line_kwargs = line_kwargs
        self.text_kwargs = text_kwargs

    def make_collection(self, objA, objB):
        """Generates a LineCollection containing all graphics to be drawn other than text

        objA : BaseLayer
            The left-side object being connected
        objB : BaseLayer
            The right-side object being connected
        """
        # TL, TR, BL, BR
        _, _, _, (X1, Y1) = objA.get_corners()
        (X2, Y2), _, _, _ = objB.get_corners()

        Y1 += objA.tot_height / 2
        Y2 -= objB.tot_height / 2

        Xmid = (X2 + X1) / 2
        Ymid = (Y2 + Y1) / 2

        segments = [
            [(X1 + self.offset, Y1), (Xmid - self.width / 2, Ymid)],
            [(Xmid + self.width / 2, Ymid), (X2 - self.offset, Y2)],
        ]

        poly = [
            Polygon(
                [
                    (Xmid - self.width / 2, Ymid),
                    (Xmid, Ymid + self.height / 2),
                    (Xmid + self.width / 2, Ymid),
                    (Xmid, Ymid - self.height / 2),
                ]
            )
        ]

        txt = Text(
            Xmid,
            Ymid,
            self.symbol,
            va="center",
            ha="center",
            **self.symbol_kwargs if self.symbol_kwargs is not None else {},
        )

        self.text_X = (X1 + X2) / 2

        return (
            LineCollection(
                segments,
                ec="k",
                **self.line_kwargs if self.line_kwargs is not None else {},
            ),
            PatchCollection(poly, ec="k", fc=self.fill_color),
            txt,
        )


class EllipsisOp:
    """For plotting ellipsis (...) between layers"""

    def __init__(
        self,
        label: str = "Ellipsis",
        diameter: float = 3,
        fill_color: tuple = (1, 1, 1),
        offset: float | str = "auto",
        loc: str = "below",
        line_kwargs: dict | None = None,
        text_kwargs: dict | None = None,
    ) -> None:
        """
        Parameters
        ----------
        label : str
            A brief description of the operation
        diameter : float
            The diameter of the circles
        fill_color : RGB tuple (float, float, float)
            The color to fill the circle with
        offset : float | str
            The horizontal spacing between circles. Equally spaced
            between objects if set to "auto"
        loc : str
            The location of the label, either 'above' or 'below'
        line_kwargs : dict | None
            Keyword arguments to be passed to the LineCollection
        text_kwargs : dict | None
            Keyword arguments to be passed to the label Text object
        """
        self.text = label
        self.diameter = diameter
        self.fill_color = fill_color
        self.offset = offset
        self.loc = loc
        self.line_kwargs = line_kwargs
        self.text_kwargs = text_kwargs

    def make_collection(self, objA, objB):
        """Generates a LineCollection containing all graphics to be drawn other than text

        objA : BaseLayer
            The left-side object being connected
        objB : BaseLayer
            The right-side object being connected
        """
        # TL, TR, BL, BR
        _, _, _, (X1, Y1) = objA.get_corners()
        (X2, Y2), _, _, _ = objB.get_corners()

        Y1 += objA.tot_height / 2
        Y2 -= objB.tot_height / 2

        Xmid = (X2 + X1) / 2
        Ymid = (Y2 + Y1) / 2

        if self.offset == "auto":
            ival = (X2 - X1) / 4
        else:
            ival = self.offset

        circle = [
            Circle((Xmid - ival, Ymid), self.diameter / 2),
            Circle((Xmid, Ymid), self.diameter / 2),
            Circle((Xmid + ival, Ymid), self.diameter / 2),
        ]

        self.text_X = (X1 + X2) / 2

        return PatchCollection(circle, ec="k", fc=self.fill_color)
