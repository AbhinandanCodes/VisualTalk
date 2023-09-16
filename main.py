#libraries
import customtkinter as ctk
from PIL import Image
import pyttsx3
import easyocr
import threading


#global
root = ctk.CTk()
root.title("VisualTalk")
first_import=False
font = ("consolas",20)
small_font=("consolas",17)
filename=[]
current_index=0
filetypes = (("Image Files", "*.png;*.jpg;*.jpeg"),)
text=""

#speaker
speaker=pyttsx3.init('sapi5')
voices=speaker.getProperty('voices')
speaker.setProperty('voice',voices[1].id)
speaker.setProperty('rate',125)



#functions
def import_images():
    global first_import,import_button,root,filename,current_index,filetypes,bottom_frame
    bottom_frame.place_forget()
    new_filename = list(ctk.filedialog.askopenfilenames(initialdir="/",
                                                    title="Select Image File",
                                                    filetypes=filetypes))
    current_index = 0 
    if new_filename:
        filename.clear()
        filename.extend(new_filename)
        loadimage()
    if not first_import and filename:
        import_button.place_forget()
        first_import = True
        import_button.place(relx=0.19,rely=0.55,anchor=ctk.CENTER)
        add_button.place(relx=0.5,rely=0.55,anchor=ctk.CENTER)
        convert_button.place(relx=0.81,rely=0.55,anchor=ctk.CENTER)
    
def loadimage():
    global filename,current_index,convert_button,frame,remove_button,image_label
    if filename:
        if not remove_button.winfo_ismapped():
            remove_button.place(relx=0.8, rely=0.1, anchor=ctk.CENTER)

        image_path = filename[current_index]
        image = ctk.CTkImage(dark_image=Image.open(image_path),size=(205,205))
        image_label.configure(image=image)
        update_arrow()
        return
    if not filename:
        image_label.configure(image=None)
        remove_button.place_forget()
        update_buttons_placement()

def update_arrow():
    global current_index,right_button,left_button
    if current_index==0:
        left_button.place_forget()
    else:
        left_button.place(relx=0.1,rely=0.5,anchor=ctk.CENTER)
    if current_index == len(filename)-1:
        right_button.place_forget()
    else:
        right_button.place(relx=0.9,rely=0.5,anchor=ctk.CENTER)
    
def right():
    global current_index
    if current_index<len(filename)-1:
        current_index += 1
        loadimage()

def left():
    global current_index
    if current_index > 0:
        current_index -= 1
        loadimage()
        
def add_file():
    global filename,filetypes,bottom_frame
    bottom_frame.place_forget()
    new_file = ctk.filedialog.askopenfilename(initialdir="/", title="Select Image File", filetypes=filetypes)
    if new_file:
        filename.append(new_file)
        loadimage()

def remove_file():
    global filename,current_index
    filename.pop(current_index)
    if(current_index>len(filename)-1 and current_index!=0):
        current_index = len(filename)-1
    loadimage()

def update_buttons_placement():
    global import_button,add_button,convert_button,first_import,bottom_frame
    first_import=False
    import_button.place_forget()
    add_button.place_forget()
    convert_button.place_forget()
    bottom_frame.place_forget()
    import_button.place(relx=0.5,rely=0.3,anchor=ctk.CENTER)
    

def convert_ui():
    global convert_button,add_button,import_button,remove_button,filename,buttom_frame,progressbar,percent_text,save_button,saved_text
    saved_text.place_forget()
    save_button.place_forget()
    if not bottom_frame.winfo_ismapped():
        bottom_frame.place(relx=0.5,rely=0.6,anchor=ctk.N)
    progressbar.configure(progress_color="#BB86FC")
    if not progressbar.winfo_ismapped():
        progressbar.place(relx=0.05,rely=0.15,anchor=ctk.W)
        percent_text.place(relx=0.55,rely=0.15,anchor=ctk.W)
    progressbar.set(0)
    percent_text.configure(text="Reading Files...")
    percent_text.place()
    convert_button.configure(state="disabled",fg_color="#3700B3")
    add_button.configure(state="disabled",fg_color="#3700B3")
    import_button.configure(state="disabled",fg_color="#3700B3")
    remove_button.place_forget()
    threading.Thread(target=convert,daemon=True).start()
    

def convert():
    #variables
    global progressbar,filename,text,percent_text
    text=""
    language ="en"
    reader = easyocr.Reader([language])
    total=len(filename)
    current=0
    percent=0
    #reading
    for image in filename:
        current+=1
        percent_text.configure(text=f"Reading Image {current}...")
        results = reader.readtext(image)
        image_text=""
        for result in results:
            image_text+=result[1]+" "
        text+=image_text
        percent=(current/total)
        progressbar.set(percent)
    percent_text.configure(text="Reading Complete.")


    progressbar.configure(progress_color="#3700B3")
    root.after(500, update_ui_after_conversion)
    
    
def update_ui_after_conversion():
    global convert_button, add_button, import_button, remove_button,progressbar,save_button
    convert_button.configure(state="normal", fg_color="#BB86FC")
    add_button.configure(state="normal", fg_color="#BB86FC")
    import_button.configure(state="normal", fg_color="#BB86FC")
    if not save_button.winfo_ismapped():

        save_button.place(relx=0.5,rely=0.5,anchor=ctk.CENTER)
    if not remove_button.winfo_ismapped():
        remove_button.place(relx=0.8, rely=0.1, anchor=ctk.CENTER)


def save_audio():
    global text,speaker,saved_text
    saved_text.place_forget()
    export_file_type = [('MP3', '*.mp3')]
    export_file = ctk.filedialog.asksaveasfile(filetypes=export_file_type,defaultextension=export_file_type).name
    if export_file:
        speaker.save_to_file(text,export_file)
        speaker.runAndWait()
        if not saved_text.winfo_ismapped():
            saved_text.place(relx=0.5,rely=0.8,anchor=ctk.CENTER)

#Ui paths
import_icon = ctk.CTkImage(Image.open("ui\\import.png"))
add_icon = ctk.CTkImage(Image.open("ui\\add.png"))
convert_icon = ctk.CTkImage(Image.open("ui\\convert.png"))
save_icon = ctk.CTkImage(Image.open("ui\\save.png"))
remove_icon = ctk.CTkImage(Image.open("ui\\remove.png"),size=(10,10))
right_arrow = ctk.CTkImage(Image.open("ui\\Right_arrow.png"),size=(40,40))
left_arrow = ctk.CTkImage(Image.open("ui\\Left_arrow.png"),size=(40,40))

#gui configures 
root.configure(fg_color="#121212")
root.geometry("500x500")
root.resizable(0,0)

#widgets

#frames
frame = ctk.CTkFrame(root,
                     width=450,
                     height=225,
                     corner_radius=15,
                     fg_color="#1F1B24")
bottom_frame = ctk.CTkFrame(root,
                            width=450,height=175,
                            corner_radius=15,
                            fg_color="#1F1B24")

#labels
image_label = ctk.CTkLabel(frame,
                           text="")
percent_text= ctk.CTkLabel(bottom_frame,
                           text="",
                           font=small_font)
saved_text= ctk.CTkLabel(bottom_frame,
                         text="Saved Audio Succesfully!!",
                         font=small_font)

#progress bar
progressbar=ctk.CTkProgressBar(bottom_frame,
                               orientation="horizontal",
                               mode="determinate",
                               height=20,width=221)

#buttons
import_button = ctk.CTkButton(root,
                              text="Import",
                              width=140,height=35,
                              fg_color="#BB86FC",
                              font=font,
                              hover_color="#3700B3",
                              image=import_icon,
                              command=import_images)

add_button = ctk.CTkButton(root,
                              text="Add",
                              width=140,height=35,
                              fg_color="#BB86FC",
                              font=font,
                              hover_color="#3700B3",
                              image=add_icon,
                              command=add_file)

convert_button = ctk.CTkButton(root,
                              text="Convert",
                              width=140,height=35,
                              fg_color="#BB86FC",
                              font=font,
                              hover_color="#3700B3",
                              image=convert_icon,
                              command=convert_ui)

save_button = ctk.CTkButton(bottom_frame,
                              text="Save",
                              width=140,height=35,
                              fg_color="#018786",
                              font=font,
                              hover_color="#005958",
                              image=save_icon,
                              command=save_audio)


right_button = ctk.CTkButton(frame,
                             image=right_arrow,
                             command=right,
                             fg_color="transparent",
                             text="",
                             hover_color="#715197",
                             width=40,height=40)

left_button = ctk.CTkButton(frame,
                            image=left_arrow,
                             command=left,
                             fg_color="transparent",
                             text="",
                             hover_color="#715197",
                             width=40,height=40)

remove_button = ctk.CTkButton(frame,
                              fg_color="#BB86FC",
                              text="",
                              image=remove_icon,
                              width=20,height=20,
                              corner_radius=30,
                              hover_color="#3700B3",
                              command=remove_file)



#place
frame.place(relx=0.5,rely=0.5,anchor=ctk.S)
import_button.place(relx=0.5,rely=0.3,anchor=ctk.CENTER)
image_label.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

#mainloop
root.mainloop()
speaker.stop()
