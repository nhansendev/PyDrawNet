# Copyright (c) 2024, Nathan Hansen
# All rights reserved.

# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.


import matplotlib.pyplot as plt
from matplotlib.artist import Artist
from matplotlib.collections import Collection

from pydrawnet.layers import Layer1DDiagonal

# For <text_kwargs> options see: https://matplotlib.org/stable/users/explain/text/text_props.html
# For <line_kwargs> options see: https://matplotlib.org/stable/api/collections_api.html#matplotlib.collections.LineCollection


class BaseRenderer:
    def __init__(self, axs=None) -> None:
        """
        Parameters
        ----------
        axs : matplotlib axis
            The axis to plot the visualization on.
            If 'None', then a new plot will be created
        """

        self.axs = axs

        self.collections = []
        self.operations = []

    def get_limits(self, xmargin=0.05, ymargin=0.3):
        """Calculate the overall size of the model, with margins"""
        xmin = None
        xmax = None
        ymin = None
        ymax = None

        if isinstance(self.collections, list):
            colls = self.collections
        elif isinstance(self.collections, dict):
            colls = self.collections.values()

        for c in colls:
            XL, XH, YL, YH = c.get_extents()
            if xmin is None:
                xmin = XL
                xmax = XH
                ymin = YL
                ymax = YH
            else:
                xmin = min(xmin, XL)
                xmax = max(xmax, XH)
                ymin = min(ymin, YL)
                ymax = max(ymax, YH)

        xofst = (xmax - xmin) * xmargin
        yofst = (ymax - ymin) * ymargin

        return xmin - xofst, xmax + xofst, ymin - yofst, ymax + yofst

    def make_figure(self):
        self.fig, ax = plt.subplots()
        self.axs = self.fig.axes[0]

    def add_layer(self, layer):
        raise NotImplementedError("Function must be overridden in subclass.")

    def add_operations(self, operation):
        raise NotImplementedError("Function must be overridden in subclass.")

    def render(self):
        raise NotImplementedError("Function must be overridden in subclass.")


class FreeformRenderer(BaseRenderer):
    """Builds and renders a visualization of the network with arbitrary placement"""

    def __init__(self, axs=None) -> None:
        super().__init__(axs)

        self.collections = {}
        self.operations = []

    def add_layer(self, layer, ID, overwrite=False):
        if not overwrite and ID in list(self.collections.keys()):
            raise KeyError(
                f'Entry with ID "{ID}" already exists. Use overwrite to ignore.'
            )

        self.collections[ID] = layer

    def remove_layer(self, ID):
        return self.collections.pop(ID, None)

    def add_operation(self, operation, ID1, ID2):
        self.operations.append([operation, ID1, ID2])

    def _plot_labels(self, YL, YH, text_y_offset=10, offset_from_limits=False):
        for c in self.collections.values():
            # If there is text to plot
            if c.text is not None and len(c.text) > 0:
                if c.loc == "below":
                    if offset_from_limits:
                        Y = YL + text_y_offset
                        va = "bottom"
                    else:
                        Y = c.Y - text_y_offset
                        if not isinstance(c, Layer1DDiagonal):
                            Y += c.height
                        va = "top"

                    self.axs.text(
                        c.X + c.width / 2,
                        Y,
                        c.text,
                        va=va,
                        ha="center",
                        **c.text_kwargs if c.text_kwargs is not None else {},
                    )
                else:
                    if offset_from_limits:
                        Y = YH - text_y_offset
                        va = "top"
                    else:
                        Y = c.Y + text_y_offset
                        if not isinstance(c, Layer1DDiagonal):
                            Y += c.height
                        va = "bottom"

                    self.axs.text(
                        c.X + c.width / 2,
                        Y,
                        c.text,
                        va=va,
                        ha="center",
                        **c.text_kwargs if c.text_kwargs is not None else {},
                    )

        for subset in self.operations:
            ops, ID1, ID2 = subset
            if not isinstance(ops, list) and not isinstance(ops, tuple):
                ops = [ops]

            for op in ops:
                # If there is text to plot
                if op.text is not None and len(op.text) > 0:
                    if op.loc == "below":
                        if offset_from_limits:
                            Ypos = YL + text_y_offset
                            va = "bottom"
                        else:
                            Y = (
                                self.collections[ID1].Y
                                - self.collections[ID1].tot_height
                            )
                            if not isinstance(self.collections[ID1], Layer1DDiagonal):
                                Y += self.collections[ID1].height

                            Y2 = (
                                self.collections[ID2].Y
                                - self.collections[ID2].tot_height
                            )
                            if not isinstance(self.collections[ID2], Layer1DDiagonal):
                                Y2 += self.collections[ID2].height

                            Ypos = min(Y, Y2) - text_y_offset
                            va = "top"

                        self.axs.text(
                            op.text_X,
                            Ypos,
                            op.text,
                            va=va,
                            ha="center",
                            **op.text_kwargs if op.text_kwargs is not None else {},
                        )
                    else:
                        if offset_from_limits:
                            Ypos = YH - text_y_offset
                            va = "top"
                        else:
                            Y = self.collections[ID1].Y
                            if not isinstance(self.collections[ID1], Layer1DDiagonal):
                                Y += self.collections[ID1].height

                            Y2 = self.collections[ID2].Y
                            if not isinstance(self.collections[ID2], Layer1DDiagonal):
                                Y2 += self.collections[ID2].height

                            Ypos = max(Y, Y2) + text_y_offset
                            va = "bottom"

                        self.axs.text(
                            op.text_X,
                            Ypos,
                            op.text,
                            va=va,
                            ha="center",
                            **op.text_kwargs if op.text_kwargs is not None else {},
                        )

    def render(
        self,
        xmargin=0.05,
        ymargin=0.3,
        offset_from_limits=False,
        text_y_offset=10,
        show=True,
        hide_axis=True,
    ):
        def _add_item(item):
            if isinstance(item, Collection):
                self.axs.add_collection(item)
            elif isinstance(item, Artist):
                self.axs.add_artist(item)
            elif item is None:
                pass
            else:
                raise TypeError("Unrecognised object type for rendering")

        if self.axs is None:
            self.make_figure()

        for c in self.collections.values():
            _add_item(c.make_collection())

        for subset in self.operations:
            ops, ID1, ID2 = subset

            if not isinstance(ops, list) and not isinstance(ops, tuple):
                ops = [ops]

            for op in ops:
                coll = op.make_collection(self.collections[ID1], self.collections[ID2])

                if isinstance(coll, tuple) or isinstance(coll, list):
                    for c in coll:
                        _add_item(c)
                else:
                    # Account for "blank" ops
                    if coll is not None:
                        _add_item(coll)

        XL, XH, YL, YH = self.get_limits(xmargin, ymargin)
        self.axs.set_xlim(XL, XH)
        self.axs.set_ylim(YL, YH)
        self.axs.set_aspect("equal")

        self._plot_labels(YL, YH, text_y_offset, offset_from_limits)

        if hide_axis:
            self.axs.axis("off")

        if show:
            plt.show()


class SeqRenderer(BaseRenderer):
    """Builds and renders a sequential visualization of the network"""

    def add_layer(self, layer):
        self.collections.append(layer)

    def add_operation(self, operation):
        self.operations.append(operation)

    def calculate_spacing(self, hspace=200, dspace=300):
        """Calculate and update the required X-axis positioning of each layer"""
        X = 0
        b = 0
        lastX = 0
        for i, c in enumerate(self.collections):
            c.calc_overall_sizes()

            if i > 0:
                # Diagonal Spacing
                X = dspace + b - c.Y

            if X > lastX or X + c.tot_width < lastX:
                # Horizontal Spacing
                if c.tot_width < hspace:
                    X = lastX + hspace * 1.5
                else:
                    X = lastX + hspace

            b = X + c.width + c.Y + c.height
            lastX = X + c.tot_width
            c.X = X

    def _plot_labels(self, YL, YH, text_y_offset=10, offset_from_limits=False):
        for c in self.collections:
            # If there is text to plot
            if c.text is not None and len(c.text) > 0:
                if c.loc == "below":
                    if offset_from_limits:
                        Y = YL + text_y_offset
                        va = "bottom"
                    else:
                        Y = c.Y - text_y_offset
                        if not isinstance(c, Layer1DDiagonal):
                            Y += c.height
                        va = "top"

                    self.axs.text(
                        c.X + c.width / 2,
                        Y,
                        c.text,
                        va=va,
                        ha="center",
                        **c.text_kwargs if c.text_kwargs is not None else {},
                    )
                else:
                    if offset_from_limits:
                        Y = YH - text_y_offset
                        va = "top"
                    else:
                        Y = c.Y + text_y_offset
                        if not isinstance(c, Layer1DDiagonal):
                            Y += c.height
                        va = "bottom"

                    self.axs.text(
                        c.X + c.width / 2,
                        Y,
                        c.text,
                        va=va,
                        ha="center",
                        **c.text_kwargs if c.text_kwargs is not None else {},
                    )

        for i, ops in enumerate(self.operations):
            if not isinstance(ops, list) and not isinstance(ops, tuple):
                ops = [ops]

            for op in ops:
                # If there is text to plot
                if op.text is not None and len(op.text) > 0:
                    if op.loc == "below":
                        if offset_from_limits:
                            Ypos = YL + text_y_offset
                            va = "bottom"
                        else:
                            Y = self.collections[i].Y - self.collections[i].tot_height
                            if not isinstance(self.collections[i], Layer1DDiagonal):
                                Y += self.collections[i].height

                            Y2 = (
                                self.collections[i + 1].Y
                                - self.collections[i + 1].tot_height
                            )
                            if not isinstance(self.collections[i + 1], Layer1DDiagonal):
                                Y2 += self.collections[i + 1].height

                            Ypos = min(Y, Y2) - text_y_offset
                            va = "top"

                        self.axs.text(
                            op.text_X,
                            Ypos,
                            op.text,
                            va=va,
                            ha="center",
                            **op.text_kwargs if op.text_kwargs is not None else {},
                        )
                    else:
                        if offset_from_limits:
                            Ypos = YH - text_y_offset
                            va = "top"
                        else:
                            Y = self.collections[i].Y
                            if not isinstance(self.collections[i], Layer1DDiagonal):
                                Y += self.collections[i].height

                            Y2 = self.collections[i + 1].Y
                            if not isinstance(self.collections[i + 1], Layer1DDiagonal):
                                Y2 += self.collections[i + 1].height

                            Ypos = max(Y, Y2) + text_y_offset
                            va = "bottom"

                        self.axs.text(
                            op.text_X,
                            Ypos,
                            op.text,
                            va=va,
                            ha="center",
                            **op.text_kwargs if op.text_kwargs is not None else {},
                        )

    def render(
        self,
        hspace=100,
        dspace=200,
        manual_xpos=None,
        xmargin=0.05,
        ymargin=0.3,
        offset_from_limits=False,
        text_y_offset=10,
        show=True,
        hide_axis=True,
    ):
        """Visualize the model in the order that layers and operations were added

        Parameters
        ----------
        hspace : int
            The horizontal spacing between objects
        dspace : int
            The diagonal spacing between objects, where applicable
        manual_xpos : list of [float, float...] | None
            Allows the X positions to be set manually instead of automatically
        xmargin : float
            The fractional margin of plot width added to the left and right
        ymargin : float
            The fractional margin of plot height added to the top and bottom
        offset_from_limits : bool
            Whether to place text relative to the plot limits, or each layer's height
        show : bool
            Whether to call plt.show()
        hide_axis : bool
            Whether to turn off the axes of the plot
        """

        def _add_item(item):
            if isinstance(item, Collection):
                self.axs.add_collection(item)
            elif isinstance(item, Artist):
                self.axs.add_artist(item)
            elif item is None:
                pass
            else:
                raise TypeError("Unrecognised object type for rendering")

        assert len(self.operations) < len(
            self.collections
        ), "There must be fewer operations than graphics/layers"

        if self.axs is None:
            self.make_figure()

        if manual_xpos is None:
            self.calculate_spacing(hspace, dspace)
        else:
            assert len(self.collections) == len(manual_xpos)
            # Note: a future update may support a mix of manual and automatic
            # For now it must be fully one or the other.
            for i in range(len(self.collections)):
                self.collections[i].X = manual_xpos[i]

        for c in self.collections:
            _add_item(c.make_collection())

        for i, ops in enumerate(self.operations):
            if not isinstance(ops, list) and not isinstance(ops, tuple):
                ops = [ops]

            for op in ops:
                coll = op.make_collection(self.collections[i], self.collections[i + 1])

                if isinstance(coll, tuple) or isinstance(coll, list):
                    for c in coll:
                        _add_item(c)
                else:
                    # Account for "blank" ops
                    if coll is not None:
                        _add_item(coll)

        XL, XH, YL, YH = self.get_limits(xmargin, ymargin)
        self.axs.set_xlim(XL, XH)
        self.axs.set_ylim(YL, YH)
        self.axs.set_aspect("equal")

        self._plot_labels(YL, YH, text_y_offset, offset_from_limits)

        if hide_axis:
            self.axs.axis("off")

        if show:
            plt.show()
