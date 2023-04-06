from tkinter import *
from PIL import Image, ImageTk


class ImageViewer:
    def __init__(self, root, images, show_seams=True):
        self.root = root
        self.images = images
        self.canvas = Canvas(root, width=3 * images[0].width, height=images[0].height)
        self.canvas.pack()

        # Display images side-by-side
        self.photo_images = []
        for i, image in enumerate(images):
            photo = ImageTk.PhotoImage(image)
            self.photo_images.append(photo)
            self.canvas.create_image(i * image.width, 0, anchor=NW, image=photo)

        # Bind mouse events for panning
        self.canvas.bind("<ButtonPress-2>", self.start_pan)
        self.canvas.bind("<B2-Motion>", self.do_pan)
        self.canvas.bind("<ButtonRelease-2>", self.stop_pan)
        self.canvas.configure(cursor='fleur')

        # Variables for panning
        self.start_x = None
        self.start_y = None

        # Show seams checkbox
        self.show_seams = BooleanVar(value=show_seams)
        self.show_seams_checkbox = Checkbutton(root, text="Show Seams", variable=self.show_seams,
                                               command=self.update_seams)
        self.show_seams_checkbox.pack()

        # Seam lines
        self.seam_lines = []
        self.update_seams()

    def update_seams(self):
        if self.show_seams.get():
            # Calculate the x-coordinates of the seam lines
            seam_xs = []
            for i in range(len(self.images) - 1):
                seam_xs.append((i + 1) * self.images[i].width)

            # Create red lines on the canvas at the seam positions
            for x in seam_xs:
                line_id = self.canvas.create_line(x, 0, x, self.images[0].height, fill="red", width=2)
                self.seam_lines.append(line_id)
        else:
            # Remove the seam lines from the canvas
            for line_id in self.seam_lines:
                self.canvas.delete(line_id)
            self.seam_lines = []

    def start_pan(self, event):
        self.start_x = event.x
        self.start_y = event.y

    def do_pan(self, event):
        if self.start_x is not None and self.start_y is not None:
            dx = event.x - self.start_x
            dy = event.y - self.start_y
            self.canvas.move("all", dx, dy)
            self.start_x = event.x
            self.start_y = event.y

    def stop_pan(self, event):
        self.start_x = None
        self.start_y = None

if __name__ == '__main__':
    # Load images
    image_paths = ['image1.png', 'image2.png', 'image3.png']
    images = [Image.open(path) for path in image_paths]

    # Create window and display images
    root = Tk()
    root.title("Carousel Image Viewer")
    root.state('zoomed')  # Maximize the window on startup

    # Create seam checkbox
    show_seams = BooleanVar()
    show_seams.set(False)
    seam_checkbox = Checkbutton(root, text="Show Seams", variable=show_seams, command=lambda: image_viewer.draw_seams(show_seams.get()))
    seam_checkbox.pack(side=TOP, padx=5, pady=5)

    image_viewer = ImageViewer(root, images, show_seams=False)
    root.mainloop()
