from tkinter import *

root = Tk()

#size of window
root.geometry('1920x1080')
#window title
root.title('Human Pose estimate')
root.maxsize(1920,1080)
root.minsize(400,270)


# create a canvas
canvas = Canvas(root, width=500, height=300, bg=None)
image_file = PhotoImage(file="2.gif")
image = canvas.create_image(250, 0, anchor='n', image=image_file)
canvas.pack()

# create a Label Widget
myLabel = Label(root, text='Human pose estimate',
    bg='green',     # background color
    font=('Arial', 14),     
    width=30, height=3) 
# shoving it onto the screen

myLabel.pack()

myButton = Button(root,text='hit me',     
    width=15, height=2, 
    #command=hit_me
    )
   
   
myButton.pack()

root.mainloop()