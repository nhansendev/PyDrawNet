# Copyright (c) 2024, Nathan Hansen
# All rights reserved.

# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

from matplotlib.collections import PatchCollection
from matplotlib.patches import Rectangle, Circle, Polygon

COLOR_LIGHT = (0.7, 0.7, 0.7)
COLOR_DARK = (0.4, 0.4, 0.4)


class BaseLayer:
    """Base class for adding graphics to the visualization"""

    def __init__(
        self,
        X: float = 0,
        Y: float = "auto",
        width: float = 100,
        height: float = 100,
        loc: str = "above",
        text_kwargs: dict | None = None,
    ) -> None:
        self.X = X
        self.Y = Y

        self.width = width
        self.height = height

        self.loc = loc
        self.text_kwargs = text_kwargs

        self.patches = None
        self.colors = None

    def get_extents(self):
        """Returns the tuple (Xmin, Xmax, Ymin, Ymax) describing the limits of the layer"""
        TL, _, _, BR = self.get_corners()

        # Xmin, Xmax, Ymin, Ymax
        return (TL[0], BR[0], BR[1], TL[1])

    def calc_overall_sizes(self):
        raise NotImplementedError("Function must be overridden in subclass.")

    def get_corners(self):
        raise NotImplementedError("Function must be overridden in subclass.")

    def make_collection(self):
        raise NotImplementedError("Function must be overridden in subclass.")


class Layer2D(BaseLayer):
    """For adding diagonally stacked-rectangle visualizations"""

    def __init__(
        self,
        channels: int = 3,
        width: float = 100,
        height: float = 100,
        label: str = "Features",
        cspace: float = 10,
        limited: int = 0,
        limited_radius: float = 5,
        skip_ival: int = 3,
        end_channels: int = 3,
        loc: str = "above",
        X: float = 0,
        Y: float | str = "auto",
        text_kwargs: dict | None = None,
        color_dark: tuple = COLOR_DARK,
        color_light: tuple = COLOR_LIGHT,
    ) -> None:
        """
        Parameters
        ----------
        channels : int
            How many layers of rectangles will be drawn
        width : float
            Width of the base rectangle
        height : float
            Height of the base rectangle
        label : str
            Briefly describes the graphic
        cspace : float
            The offset between rectangles in (X, Y), should be zero or greater
        limited : int
            If non-zero, then limit the displayed channels to this quantity, represented
            by circles. Some channels may be displayed on each end, set by <end_channels>
        limited_radius : float
            When reducing the number of displayed channels, what size should the
            placeholder circles be
        skip_ival : int
            When reducing the number of displayed channels, at what interval should
            the placeholder circles be drawn (e.g. skip_ival=3 -> show 1 every 3 spaces)
        end_channels : int
            When reducing the number of displayed channels, how many
            should still be shown on the ends
        loc : str
            Where the label text should be placed: "above" or "below" the layer
        X : float
            The location of the leftmost edge of base rectangle, set
            automatically when using NetGraph for rendering
        Y : float (default: 'auto')
            The location of the bottom edge of the base rectangle.
            Specifying 'auto' will place the entire graphic symmetrically
            about 0
        text_kwargs : dict, or None (default)
            Keyword arguments to be passed to matplotlib Text object
        color_dark : RGB tuple(float, float, float)
            Channel colors alternate between dark and light, with color
            defined by a 3-tuple of floats in the range 0-1
        color_light : RGB tuple(float, float, float)
            Channel colors alternate between dark and light, with color
            defined by a 3-tuple of floats in the range 0-1
        """
        super().__init__(X, Y, width, height, loc, text_kwargs)
        assert channels > 0
        assert (
            limited >= 0 and limited < channels
        ), "The channel display limit must be less than the number of channels, or False/0 to disable"
        assert limited_radius >= 0
        assert end_channels >= 0
        assert cspace >= 0, "The diagonal spacing between elements must be zero or more"

        if limited > 0 and end_channels * 2 > limited:
            end_channels = limited // 2

        self.channels = channels
        self.cspace = cspace
        self.limited = limited
        self.limited_radius = limited_radius
        self.skip_ival = skip_ival
        self.end_channels = end_channels
        self.color_dark = color_dark
        self.color_light = color_light

        chn = "Channels" if channels > 1 else "Channel"
        self.text = f"{label}\n{channels} {chn}\n{width}x{height}"

    def calc_overall_sizes(self):
        """Calculates tot_width and tot_height, also Y if not already known"""

        if self.limited > 0:
            num = self.limited - 1
        else:
            num = self.channels - 1

        self.tot_width = self.width + num * self.cspace
        self.tot_height = self.height + num * self.cspace

        if self.Y == "auto":
            self.Y = self.tot_height / 2 - self.height

    def get_corners(self):
        """Used to find attachment points for operation visualizations

        Returns (x, y) coordinates in format: (Top Left, Top Right, Bottom Left, Bottom Right)
        """
        if (
            not hasattr(self, "tot_width")
            or not hasattr(self, "tot_height")
            or isinstance(self.Y, str)
        ):
            raise AttributeError("<self.calc_overall_sizes> must be run first")

        corners = [
            (self.X, self.Y + self.height),
            (self.X + self.width, self.Y + self.height),
            (
                self.X + self.tot_width - self.width,
                self.Y + self.height - self.tot_height,
            ),
            (self.X + self.tot_width, self.Y + self.height - self.tot_height),
        ]
        return corners

    def make_collection(self):
        """Generates a PatchCollection containing all graphics to be drawn other than text"""
        patches = []
        colors = []
        color_toggle = False

        self.calc_overall_sizes()

        if self.limited > 0:
            # Reduce the number of shown channels, only showing some on the ends, if any

            # Add end channels
            for i in range(self.end_channels):
                patches.append(
                    Rectangle(
                        (self.X + self.cspace * i, self.Y - self.cspace * i),
                        self.width,
                        self.height,
                    )
                )
                colors.append(self.color_dark if color_toggle else self.color_light)
                color_toggle = not color_toggle

            # Add placeholders
            ioffset = self.end_channels
            for i in range(self.limited - 2 * self.end_channels):
                if i % self.skip_ival == 0:
                    patches.append(
                        Circle(
                            (
                                self.X + self.cspace * (i + ioffset) + self.width / 2,
                                self.Y - self.cspace * (i + ioffset) + self.height / 2,
                            ),
                            self.limited_radius,
                        )
                    )
                    colors.append((0.1, 0.1, 0.1))

            # Add remaining end channels
            ioffset = self.end_channels + max(0, self.limited - 2 * self.end_channels)
            for i in range(self.end_channels):
                patches.append(
                    Rectangle(
                        (
                            self.X + self.cspace * (i + ioffset),
                            self.Y - self.cspace * (i + ioffset),
                        ),
                        self.width,
                        self.height,
                    )
                )
                colors.append(self.color_dark if color_toggle else self.color_light)
                color_toggle = not color_toggle

        else:
            # Show all channels
            for i in range(self.channels):
                patches.append(
                    Rectangle(
                        (self.X + self.cspace * i, self.Y - self.cspace * i),
                        self.width,
                        self.height,
                    )
                )
                colors.append(self.color_dark if color_toggle else self.color_light)
                color_toggle = not color_toggle

        return PatchCollection(patches, ec="k", fc=colors)


class Layer1D(BaseLayer):
    """For adding vertically-stacked circle visualizations"""

    def __init__(
        self,
        features: int = 9,
        diameter: float = 1,
        label: str = "Features",
        fill_color: tuple = (0.9, 0.9, 0.9),
        limited: int = 0,
        limited_radius: float = 0.25,
        skip_ival: int = 1,
        end_features: int = 5,
        shape_spacing: float = 0,
        loc: str = "above",
        X: float = 0,
        Y: float | str = "auto",
        text_kwargs: dict | None = None,
    ) -> None:
        """
        Parameters
        ----------
        features : int
            How many stacked circles will be drawn
        diameter : float
            Diameter of the base circle
        label : str
            Briefly describes the graphic
        fill_color : RGB tuple(float, float, float)
            RGB color to fill each circle with
        limited : int
            If non-zero, then limit the displayed featres to this quantity, represented
            by small circles. Some features may be displayed on each end, set by <end_features>
        limited_radius : float
            When reducing the number of displayed features, what size should the
            placeholder circles be
        skip_ival : int
            When reducing the number of displayed channels, at what interval should
            the placeholder circles be drawn (e.g. skip_ival=3 -> show 1 every 3 spaces)
        end_features : int
            When reducing the number of displayed features, how many
            should still be shown on the ends
        shape_spacing : float
            The spacing between the stacked circles
        loc : str
            Where the label text should be placed: "above" or "below" the layer
        X : float
            The location of the leftmost edge of base circle, set
            automatically when using NetGraph for rendering
        Y : float (default: 'auto')
            The location of the bottom edge of the base circle.
            Specifying 'auto' will place the entire graphic symmetrically
            about 0
        text_kwargs : dict, or None (default)
            Keyword arguments to be passed to matplotlib Text object
        """
        super().__init__(X, Y, diameter, diameter, loc, text_kwargs)

        assert diameter > 0
        assert (
            limited >= 0 and limited < features
        ), "The feature display limit must be less than the number of features, or False/0 to disable"
        assert limited_radius >= 0
        assert end_features >= 0

        if limited > 0 and end_features * 2 > limited:
            end_features = limited // 2

        self.diameter = diameter
        self.features = features
        self.fill_color = fill_color
        self.limited = limited
        self.limited_radius = limited_radius
        self.skip_ival = skip_ival
        self.end_features = end_features
        self.shape_spacing = shape_spacing
        self.yival = self.diameter + self.shape_spacing

        self.text = f"{label}\n{features}"

        self.tot_width = diameter

    def calc_overall_sizes(self):
        """Calculates tot_height and Y if not already known"""
        if self.limited > 0:
            num_features = self.limited
        else:
            num_features = self.features

        self.tot_height = (
            self.diameter + self.shape_spacing
        ) * num_features - self.shape_spacing
        if self.Y == "auto":
            self.Y = self.tot_height / 2 - self.diameter

    def get_corners(self):
        """Used to find attachment points for operation visualizations

        Returns (x, y) coordinates in format: (Top Left, Top Right, Bottom Left, Bottom Right)
        """
        if (
            not hasattr(self, "tot_width")
            or not hasattr(self, "tot_height")
            or isinstance(self.Y, str)
        ):
            raise AttributeError("<self.calc_overall_sizes> must be run first")

        corners = [
            (self.X, self.Y + self.diameter),
            (self.X + self.diameter, self.Y + self.diameter),
            (self.X, self.Y + self.diameter - self.tot_height),
            (self.X + self.diameter, self.Y + self.diameter - self.tot_height),
        ]
        return corners

    def make_collection(self):
        """Generates a PatchCollection containing all graphics to be drawn other than text

        Parameters
        ----------
        skip_ival : int
            When replacing channels with dots, at what interval should the dots be drawn
        radius : float (default: 'auto')
            The radius of each dot. if 'auto' is specified, then radius = width/4
        """

        self.calc_overall_sizes()

        self.patches = []
        self.colors = []
        rad = self.diameter / 2

        if self.limited:
            # Reduce the number of shown features, only showing some on the ends, if any

            # Add end channels
            for i in range(self.end_features):
                self.patches.append(
                    Circle(
                        (self.X + rad, self.Y - self.yival * i + rad),
                        rad,
                    )
                )
                self.colors.append(self.fill_color)

            # Add placeholders
            ioffset = self.end_features
            for i in range(self.limited - 2 * self.end_features):
                if i % self.skip_ival == 0:
                    self.patches.append(
                        Circle(
                            (
                                self.X + rad,
                                self.Y - self.yival * (i + ioffset) + rad,
                            ),
                            self.limited_radius,
                        )
                    )
                    self.colors.append((0.1, 0.1, 0.1))

            # Add remaining end channels
            ioffset = self.end_features + max(0, self.limited - 2 * self.end_features)
            for i in range(self.end_features):
                self.patches.append(
                    Circle(
                        (self.X + rad, self.Y - self.yival * (i + ioffset) + rad),
                        rad,
                    )
                )
                self.colors.append(self.fill_color)

        else:
            # Show all features
            for i in range(self.features):
                self.patches.append(
                    Circle(
                        (self.X + rad, self.Y - self.yival * i + rad),
                        rad,
                    )
                )
                self.colors.append(self.fill_color)

        return PatchCollection(self.patches, ec="k", fc=self.colors)


class Layer1DRect(BaseLayer):
    """For adding vertically-stacked rectangle visualizations"""

    def __init__(
        self,
        features: int = 9,
        width: float = 10,
        height: float = 10,
        label: str = "Features",
        fill_color: tuple = (0.9, 0.9, 0.9),
        limited: int = 0,
        limited_radius: float = 5,
        skip_ival: int = 1,
        end_features: int = 5,
        shape_spacing: float = 0,
        loc: str = "above",
        X: float = 0,
        Y: float | str = "auto",
        text_kwargs: dict | None = None,
    ) -> None:
        """
        Parameters
        ----------
        features : int
            How many stacked rectangles will be drawn
        width : int
            Width of the base rectangle
        height : int
            Height of the base rectangle
        label : str
            Briefly describes the graphic
        fill_color : tuple(float, float, float)
            RGB color to fill each rectangle with
        limited : bool
            If limited is True, then the red_factor will be used to
            replace large numbers of features in the middle of the
            graphic with dots
        limited_radius : float
            When reducing the number of displayed channels, what size should the
            placeholder circles be
        skip_ival : int
            When reducing the number of displayed channels, at what interval should
            the placeholder circles be drawn (e.g. skip_ival=3 -> show 1 every 3 spaces)
        end_features : int
            When reducing the number of displayed features, how many
            should still be shown on the ends
        loc : str
            Where the label text should be placed: "above" or "below" the layer
        X : float
            The location of the leftmost edge of base rectangle
        Y : float (default: 'auto')
            The location of the bottom edge of the base rectangle.
            Specifying 'auto' will place the entire graphic symmetrically
            about 0
        text_kwargs : dict, or None (default)
            Keyword arguments to be passed to matplotlib Text object
        """
        super().__init__(X, Y, width, height, loc, text_kwargs)

        self.features = features
        self.fill_color = fill_color
        self.limited = limited
        self.limited_radius = limited_radius
        self.skip_ival = skip_ival
        self.end_features = end_features
        self.shape_spacing = shape_spacing
        self.yival = self.height + self.shape_spacing

        self.text = f"{label}\n{features}"

        self.tot_width = width
        self.tot_height = height * self.features

    def calc_overall_sizes(self):
        """Calculates any of <Y, tot_width, tot_height> if not already known"""
        if self.limited > 0:
            num_features = self.limited
        else:
            num_features = self.features

        self.tot_height = (
            self.height + self.shape_spacing
        ) * num_features - self.shape_spacing
        if self.Y == "auto":
            self.Y = self.tot_height / 2 - self.height

    def get_corners(self):
        """Used to find attachment points for operation visualizations

        Returns (x, y) coordinates in format: (Top Left, Top Right, Bottom Left, Bottom Right)
        """
        if (
            not hasattr(self, "tot_width")
            or not hasattr(self, "tot_height")
            or isinstance(self.Y, str)
        ):
            raise AttributeError("<self.calc_overall_sizes> must be run first")

        corners = [
            (self.X, self.Y + self.height),
            (self.X + self.width, self.Y + self.height),
            (self.X, self.Y + self.height - self.tot_height),
            (self.X + self.width, self.Y + self.height - self.tot_height),
        ]
        return corners

    def make_collection(self):
        """Generates a PatchCollection containing all graphics to be drawn other than text"""

        self.calc_overall_sizes()

        self.patches = []
        self.colors = []

        if self.limited > 0:
            # Reduce the number of shown features, only showing some on the ends, if any

            # Add end features
            for i in range(self.end_features):
                self.patches.append(
                    Rectangle(
                        (self.X, self.Y - self.yival * i),
                        self.width,
                        self.height,
                    )
                )
                self.colors.append(self.fill_color)

            # Add placeholders
            ioffset = self.end_features
            for i in range(self.limited - 2 * self.end_features):
                if i % self.skip_ival == 0:
                    self.patches.append(
                        Circle(
                            (
                                self.X + self.width / 2,
                                self.Y
                                - self.yival * (i + ioffset)
                                + self.limited_radius / 2
                                + self.height / 2,
                            ),
                            self.limited_radius,
                        )
                    )
                    self.colors.append((0.1, 0.1, 0.1))

            # Add remaining end features
            ioffset = self.end_features + max(0, self.limited - 2 * self.end_features)
            for i in range(self.end_features):
                self.patches.append(
                    Rectangle(
                        (self.X, self.Y - self.yival * (i + ioffset)),
                        self.width,
                        self.height,
                    )
                )
                self.colors.append(self.fill_color)

        else:
            # Show all features
            for i in range(self.features):
                self.patches.append(
                    Rectangle(
                        (self.X, self.Y - self.yival * i),
                        self.width,
                        self.height,
                    )
                )
                self.colors.append(self.fill_color)
        return PatchCollection(self.patches, ec="k", fc=self.colors)


class Layer1DDiagonal(BaseLayer):
    """For adding single diagonal rectangle visualizations"""

    def __init__(
        self,
        width: float = 10,
        height: float = 100,
        label: str = "Features",
        fill_color: tuple = (0.9, 0.9, 0.9),
        loc: str = "above",
        X: float = 0,
        Y: float | str = "auto",
        text_kwargs: dict | None = None,
    ) -> None:
        """
        Parameters
        ----------
        width : int
            Width of the base rectangle
        height : int
            Height of the base rectangle
        label : str
            Briefly describes the graphic
        fill_color : tuple(float, float, float)
            RGB color to fill each rectangle with
        loc : str
            Where the label text should be placed: "above" or "below" the layer
        X : float
            The location of the leftmost edge of base rectangle
        Y : float (default: 'auto')
            The location of the bottom edge of the base rectangle.
            Specifying 'auto' will place the entire graphic symmetrically
            about 0
        text_kwargs : dict, or None (default)
            Keyword arguments to be passed to matplotlib Text object
        """
        super().__init__(X, Y, width, height, loc, text_kwargs)

        self.text = label
        self.fill_color = fill_color

        hx = height / (2**0.5)  # 45-degree angle
        self.tot_width = width + hx
        self.tot_height = hx

        if Y == "auto":
            self.Y = self.tot_height / 2

    def calc_overall_sizes(self):
        """Unused"""

    def get_corners(self):
        """Used to find attachment points for operation visualizations

        Returns (x, y) coordinates in format: (Top Left, Top Right, Bottom Left, Bottom Right)
        """
        corners = [
            (self.X, self.Y),
            (self.X + self.width, self.Y),
            (self.X + self.tot_width - self.width, self.Y - self.tot_height),
            (self.X + self.tot_width, self.Y - self.tot_height),
        ]
        return corners

    def make_collection(self):
        """Generates a PatchCollection containing all graphics to be drawn other than text"""

        points = [
            (self.X, self.Y),
            (self.X + self.width, self.Y),
            (self.X + self.tot_width, self.Y - self.tot_height),
            (self.X + self.tot_width - self.width, self.Y - self.tot_height),
        ]
        self.patches = [Polygon(points)]
        self.colors = [self.fill_color]
        return PatchCollection(
            self.patches,
            ec="k",
            fc=self.colors,
        )


class BlockLayer(BaseLayer):
    """For adding single colored rectangle visualizations"""

    def __init__(
        self,
        width: float = 100,
        height: float = 100,
        label: str = "Block",
        fill_color: tuple = (0.9, 0.9, 0.9),
        loc: str = "above",
        X: float = 0,
        Y: float | str = "auto",
        text_kwargs: dict | None = None,
    ) -> None:
        """
        Parameters
        ----------
        width : int
            Width of the base rectangle
        height : int
            Height of the base rectangle
        label : str
            Briefly describes the graphic
        fill_color : tuple(float, float, float)
            RGB color to fill each rectangle with
        X : float
            The location of the leftmost edge of base rectangle
        Y : float (default: 'auto')
            The location of the bottom edge of the base rectangle.
            Specifying 'auto' will place the entire graphic symmetrically
            about 0
        text_kwargs : dict, or None (default)
            Keyword arguments to be passed to matplotlib Text object
        """
        super().__init__(X, Y, width, height, loc, text_kwargs)

        self.text = label
        self.fill_color = fill_color

        self.tot_width = width
        self.tot_height = height

        if Y == "auto":
            self.Y = -self.height / 2

    def calc_overall_sizes(self):
        """Unused"""

    def get_corners(self):
        """Used to find attachment points for operation visualizations

        Returns (x, y) coordinates in format: (Top Left, Top Right, Bottom Left, Bottom Right)
        """
        corners = [
            (self.X, self.Y + self.height),
            (self.X + self.width, self.Y + self.height),
            (self.X, self.Y),
            (self.X + self.width, self.Y),
        ]
        return corners

    def make_collection(self):
        """Generates a PatchCollection containing all graphics to be drawn other than text"""
        self.patches = [Rectangle((self.X, self.Y), self.width, self.height)]
        self.colors = [self.fill_color]
        return PatchCollection(
            self.patches,
            ec="k",
            fc=self.colors,
        )


class PolyLayer(BaseLayer):
    """For adding arbitrary polygon visualizations"""

    def __init__(
        self,
        coords,
        label: str = "Poly",
        fill_color: tuple = (0.9, 0.9, 0.9),
        loc: str = "above",
        X: float = 0,
        Y: float = 0,
        text_kwargs: dict | None = None,
    ) -> None:
        """
        Parameters
        ----------
        coords : iterable of (x, y) pairs
            The coordinates of the polygon points to be drawn
        label : str
            Briefly describes the graphic
        fill_color : tuple(float, float, float)
            RGB color to fill the polygon with
        loc : str
            Where the label text should be placed: "above" or "below" the layer
        X : float
            The location of the horizontal center of the polygon
        Y : float
            The location of the vertical center of the polygon
        text_kwargs : dict, or None (default)
            Keyword arguments to be passed to matplotlib Text object
        """

        width, height = self._width_height_from_coords(coords)

        super().__init__(X, Y, width, height, loc, text_kwargs)

        self.coords = coords
        self.text = label
        self.fill_color = fill_color

        self.tot_width = width
        self.tot_height = height

    def _width_height_from_coords(self, coords):
        minX = None
        maxX = None
        minY = None
        maxY = None

        for x, y in coords:
            if minX is None:
                minX = x
                maxX = x
                minY = y
                maxY = y
            else:
                minX = min(minX, x)
                maxX = max(maxX, x)
                minY = min(minY, y)
                maxY = max(maxY, y)

        width = maxX - minX
        height = maxY - minY

        return width, height

    def calc_overall_sizes(self):
        """Unused"""

    def get_corners(self):
        """Used to find attachment points for operation visualizations

        Returns (x, y) coordinates in format: (Top Left, Top Right, Bottom Left, Bottom Right)
        """
        corners = [
            (self.X - self.width / 2, self.Y + self.height / 2),
            (self.X + self.width / 2, self.Y + self.height / 2),
            (self.X - self.width / 2, self.Y - self.height / 2),
            (self.X + self.width / 2, self.Y - self.height / 2),
        ]
        return corners

    def make_collection(self):
        """Generates a PatchCollection containing all graphics to be drawn other than text"""

        patches = [Polygon([(x + self.X, y + self.Y) for x, y in self.coords])]
        colors = [self.fill_color]
        return PatchCollection(patches, ec="k", fc=colors)


class ImageLayer(BaseLayer):
    """For adding single image visualizations"""

    def __init__(
        self,
        imgpath,
        width: float = 100,
        height: float = 100,
        label: str = "Image",
        loc: str = "above",
        X: float = 0,
        Y: float | str = "auto",
        text_kwargs: dict | None = None,
    ) -> None:
        """
        Parameters
        ----------
        width : int
            Width of the base rectangle
        height : int
            Height of the base rectangle
        label : str
            Briefly describes the graphic
        X : float
            The location of the leftmost edge of base rectangle
        Y : float (default: 'auto')
            The location of the bottom edge of the base rectangle.
            Specifying 'auto' will place the entire graphic symmetrically
            about 0
        text_kwargs : dict, or None (default)
            Keyword arguments to be passed to matplotlib Text object
        """
        super().__init__(X, Y, width, height, loc, text_kwargs)

        self.text = label

        self.tot_width = width
        self.tot_height = height

        if Y == "auto":
            self.Y = -self.height / 2

    def calc_overall_sizes(self):
        """Unused"""

    def get_corners(self):
        """Used to find attachment points for operation visualizations

        Returns (x, y) coordinates in format: (Top Left, Top Right, Bottom Left, Bottom Right)
        """
        corners = [
            (self.X, self.Y + self.height),
            (self.X + self.width, self.Y + self.height),
            (self.X, self.Y),
            (self.X + self.width, self.Y),
        ]
        return corners

    def make_collection(self):
        """Generates a PatchCollection containing all graphics to be drawn other than text"""
        self.patches = [Rectangle((self.X, self.Y), self.width, self.height)]
        self.colors = [self.fill_color]
        return PatchCollection(
            self.patches,
            ec="k",
            fc=self.colors,
        )
