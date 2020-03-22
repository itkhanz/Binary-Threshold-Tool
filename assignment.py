# import the necessary packages
# To access the GUI Functionality
from tkinter import *
from tkinter import filedialog
# PIL(photo imaging Library) allows displaying JPEG/JPG and PNG
from PIL import Image
from PIL import ImageTk
# To use OpenCV
import cv2


def adjust_size(image):
    """Downscaling the image while preserving the Aspect Ratio"""
    global width, height
    scale_percent = 90  # percent of original size
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)


def display_image(image):
    """Performs the necessary pre-processing to display the image with Tkinter"""
    global image_panel

    image = Image.fromarray(image)        # convert the images to PIL format
    image = ImageTk.PhotoImage(image)     # and then to ImageTk format

    if image_panel is None:               # if the panels are None, initialize them
        image_panel = Label(image=image)
        image_panel.image = image         # prevent Python’s garbage collection routines from deleting the image
        image_panel.pack()
    else:  # otherwise, update the image panels
        image_panel.configure(image=image)  # update the image label
        image_panel.image = image
        image_panel.pack()


def select_image():
    """Load and display the RGB image to be fitted on the screen"""
    # grab a reference to the image path, width and height
    global path, width, height
    # open a file chooser dialog and allow the user to select an input image
    path = filedialog.askopenfilename()

    if len(path) > 0:                    # ensure a file path was selected
        image = cv2.imread(path)         # load the image from path
        height, width = image.shape[:2]  # image height and width
        while height > 550 or width > 1024:
            adjust_size(image)           # adjust the resolution to fit the screen
            image = cv2.resize(image, (width, height))
        # PIL/Pillow represents images in RGB order
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        display_image(image)


def threshold_slider(*args):
    """Updates the binary threshold image dynamically based on the slider value"""
    if len(path) > 0:
        image = cv2.imread(path)
        image = cv2.resize(image, (width, height))
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

        # Reads the current threshold value from slider
        th_val = slider.get()
        # applying binary threshold on the grayscale image
        # all pixel values above threshold will be set to 255(white)
        retval, th_image = cv2.threshold(gray, th_val, 255, cv2.THRESH_BINARY)
        display_image(th_image)


def show_grayscale():
    """Displays the grayscale image on screen when user presses the corresponding button"""
    if len(path) > 0:
        image = cv2.imread(path)
        image = cv2.resize(image, (width, height))
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

        display_image(gray)


# Global Variables
image_panel, path, width, height = None, '', 0, 0

# initialize the main window
root = Tk()
root.title("Adaptive Binary Thresholding")

# Image Selection button widget
select_btn = Button(root, text="Select an image", command=select_image)
select_btn.pack(side="bottom")

# Display Grayscale image button widget
gray_button = Button(root, text="Show Grayscale", command=show_grayscale)
gray_button.pack()

# Description text of binary threshold label widget
label = Label(root, text="Move the scale to adjust the binary threshold")
label.pack()

# Adaptive Threshold scale widget
slider = Scale(root, from_=0, to=255, length=400, resolution=1, orient=HORIZONTAL, command=threshold_slider)
slider.set(127)
slider.pack()

# kick off the GUI
root.mainloop()
