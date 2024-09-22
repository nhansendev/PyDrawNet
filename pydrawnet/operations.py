# Copyright (c) 2024, Nathan Hansen
# All rights reserved.

# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

from matplotlib.collections import PatchCollection, LineCollection
from matplotlib.patches import Rectangle


class Conv2dOp:
    """For plotting kernel operation visualizations between layers"""

    def __init__(
        self,
        kernel: tuple = (4, 4),
        stride: int = 2,
        label: str = "Conv2d",
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
        label : str
            A brief description of the operation
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
        loc: str = "below",
        line_kwargs: dict | None = None,
        text_kwargs: dict | None = None,
    ) -> None:
        """
        Parameters
        ----------
        label : str
            A brief description of the operation
        arrow_size : int
            The scale of the arrow
        loc : str
            The location of the label, either 'above' or 'below'
        line_kwargs : dict | None
            Keyword arguments to be passed to the LineCollection
        text_kwargs : dict | None
            Keyword arguments to be passed to matplotlib Text object
        """
        self.text = label
        self.arrow_size = arrow_size
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

        Xoffset = 0.05 * abs(X2 - X1)

        Xmid = (X2 + X1) / 2 + self.arrow_size / 2
        Ymid = (Y2 + Y1) / 2

        segments = [
            [(X1 + Xoffset, Y1), (Xmid - self.arrow_size, Ymid)],
            [(Xmid, Ymid), (X2 - Xoffset, Y2)],
            [
                (Xmid - self.arrow_size, Ymid + self.arrow_size),
                (Xmid, Ymid),
                (Xmid - self.arrow_size, Ymid - self.arrow_size),
                (Xmid - self.arrow_size, Ymid + self.arrow_size),
            ],
        ]
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
        _, (X1, Y1), _, _ = objA.get_corners()
        (X2, Y2), _, _, _ = objB.get_corners()
        self.text_X = (X1 + X2) / 2
        return None
