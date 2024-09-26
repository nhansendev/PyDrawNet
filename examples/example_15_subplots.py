from pydrawnet.renderers import SeqRenderer
from pydrawnet import layers, operations

import matplotlib.pyplot as plt

""" Demonstrating adding visualizations within plots """

fig, ax = plt.subplots()
axs = fig.axes

axs[0].plot([0, 1, 2], [0, 1, 0], ".-")
axs[0].grid()
axs[0].set_xlabel("Metric")
axs[0].set_ylabel("Metric")

subax1 = axs[0].inset_axes([0.2, 0.5, 0.2, 0.2])
subax2 = axs[0].inset_axes([0.5, 0.2, 0.5, 0.5])

# Subplot 1
SR = SeqRenderer(subax1)

SR.add_layer(layers.Layer2D())
SR.add_operation(operations.Conv2dOp())
SR.add_layer(layers.Layer2D())

SR.render(show=False)

# Subplot 2
SR = SeqRenderer(subax2)

SR.add_layer(layers.BlockLayer())
SR.add_operation(operations.ArrowOp(arrow_size=30))
SR.add_layer(layers.BlockLayer())

SR.render()
