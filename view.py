from tkinter import *
from PIL import Image, ImageTk

class ImageViewer:
    def __init__(self, root, images):
        self.root = root
        self.images = images
        self.canvas = Canvas(root, width=3*images[0].width, height=images[0].height)
        self.canvas.pack()

        # Display images side-by-side
        self.photo_images = []
        for i, image in enumerate(images):
            photo = ImageTk.PhotoImage(image)
            self.photo_images.append(photo)
            self.canvas.create_image(i*image.width, 0, anchor=NW, image=photo)

        # Bind mouse events for panning
        self.canvas.bind("<ButtonPress-2>", self.start_pan)
        self.canvas.bind("<B2-Motion>", self.do_pan)
        self.canvas.bind("<ButtonRelease-2>", self.stop_pan)
        self.canvas.configure(cursor='fleur')

        # Variables for panning
        self.start_x = None
        self.start_y = None

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
    image_viewer = ImageViewer(root, images)
    root.mainloop()
