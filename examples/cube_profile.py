from rendercanvas.auto import RenderCanvas, loop
from rendercanvas.utils.cube import setup_drawing_sync
import sys


if __name__ == "__main__":
    framerate = float(sys.argv[1])
    canvas = RenderCanvas(
        title="The wgpu cube example on $backend with $fps", update_mode="continuous", max_fps=framerate
    )
    draw_frame = setup_drawing_sync(canvas)

    frame_num = 0
    @canvas.request_draw
    def draw_n_frames(n=1000):
        global frame_num
        frame_num += 1
        if frame_num > n:
            canvas.close()
            return
        draw_frame()
        canvas.request_draw()

    loop.run()
