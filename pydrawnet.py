import matplotlib.pyplot as plt

import layers
import operations

# For <text_kwargs> options see: https://matplotlib.org/stable/users/explain/text/text_props.html


class SeqRenderer:
    """Builds and renders a sequential visualization of the network"""

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

    def add_layer(self, layer):
        self.collections.append(layer)

    def add_operation(self, operation):
        self.operations.append(operation)

    def get_limits(self, xmargin=0.05, ymargin=0.3):
        """Calculate the overall size of the model, with margins"""
        xmin = None
        xmax = None
        ymin = None
        ymax = None

        for c in self.collections:
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

    def make_figure(self):
        self.fig, ax = plt.subplots()
        self.axs = self.fig.axes[0]

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
                        if not isinstance(c, layers.Layer1DDiagonal):
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
                        if not isinstance(c, layers.Layer1DDiagonal):
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
                            if not isinstance(
                                self.collections[i], layers.Layer1DDiagonal
                            ):
                                Y += self.collections[i].height

                            Y2 = (
                                self.collections[i + 1].Y
                                - self.collections[i + 1].tot_height
                            )
                            if not isinstance(
                                self.collections[i + 1], layers.Layer1DDiagonal
                            ):
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
                            if not isinstance(
                                self.collections[i], layers.Layer1DDiagonal
                            ):
                                Y += self.collections[i].height

                            Y2 = self.collections[i + 1].Y
                            if not isinstance(
                                self.collections[i + 1], layers.Layer1DDiagonal
                            ):
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

        assert len(self.operations) < len(
            self.collections
        ), "There must be fewer operations than graphics/layers"

        if self.axs is None:
            self.make_figure()

        self.calculate_spacing(hspace, dspace)

        for c in self.collections:
            self.axs.add_collection(c.make_collection())

        for i, ops in enumerate(self.operations):
            if not isinstance(ops, list) and not isinstance(ops, tuple):
                ops = [ops]

            for op in ops:
                coll = op.make_collection(self.collections[i], self.collections[i + 1])

                if isinstance(coll, tuple) or isinstance(coll, list):
                    for c in coll:
                        self.axs.add_collection(c)
                else:
                    # Account for "blank" ops
                    if coll is not None:
                        self.axs.add_collection(coll)

        XL, XH, YL, YH = self.get_limits(xmargin, ymargin)
        self.axs.set_xlim(XL, XH)
        self.axs.set_ylim(YL, YH)
        self.axs.set_aspect("equal")

        self._plot_labels(YL, YH, text_y_offset, offset_from_limits)

        if hide_axis:
            self.axs.axis("off")

        if show:
            plt.show()
