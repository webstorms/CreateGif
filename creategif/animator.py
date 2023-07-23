import matplotlib.pyplot as plt
from matplotlib import animation as render
from IPython.display import HTML


class Animation:

    def render(self, i):
        pass


class DefaultAnimation(Animation):

    def __init__(self, data, vmin=None, vmax=None, cmap=None):
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(1, 1, 1)

        if vmin is None and vmax is None:
            vmin, vmax = -data.abs().max(), data.abs().max()

        self.frame = self.ax.imshow(data[0], vmin=vmin, vmax=vmax, cmap=cmap)
        self.data = data

        self._nicify()

    def render(self, i):
        self.frame.set_data(self.data[i])

    def _nicify(self):
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.ax.spines["top"].set_visible(False)
        self.ax.spines["right"].set_visible(False)
        self.ax.spines["bottom"].set_visible(False)
        self.ax.spines["left"].set_visible(False)


class Animator:

    def __init__(self, animation, n_frames, fps=30, **kwargs):
        self.animation = animation
        self.n_frames = n_frames
        self.fps = fps

        # Create animation
        interval = int(1000 / self.fps)
        self._clip = render.FuncAnimation(animation.fig, self._render, frames=self.n_frames, interval=interval, **kwargs)

    def _render(self, i):
        self.animation.render(i)

    def to_html5_video(self):
        return self._clip.to_html5_video()

    def to_jshtml(self):
        return self._clip.to_jshtml()

    def to_notebook(self):
        return HTML(self.to_jshtml())

    def to_gif(self, path):
        self._clip.save(path, writer="imagemagick", fps=self.fps)

    def to_mov(self):
        return NotImplementedError


class TensorAnimator(Animator):

    def __init__(self, tensor, fps=30, vmin=None, vmax=None, cmap=None, **kwargs):
        super().__init__(DefaultAnimation(tensor, vmin, vmax, cmap), tensor.shape[0], fps, **kwargs)
