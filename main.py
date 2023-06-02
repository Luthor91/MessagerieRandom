import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from tkinter import *
from datetime import datetime

def send_message():
    # recuperer le pseudo de l'utilisateur
    pseudo = pseudo_box_value.get()
    # recuperer le message de la box
    msg = new_message_box_value.get()
    
    # condition message vide
    if msg  == '' or pseudo == '':
        return
    
    # insertion message dans base de données
    reference.add({
        'author': pseudo,
        'content': msg,
        'date': firestore.SERVER_TIMESTAMP
    })
    
    # reactivation de l'écriture dans la chat box
    chat_box.config(state=NORMAL)
    
    # ajouter dans la zone de texte
    chat_box.insert(END, f"{pseudo} dit : \n\t {msg} \n")
    
    # déactivation de l'écriture dans la chat box
    chat_box.config(state=DISABLED)
    
    # vider le champs texte
    new_message_box.delete(0, END)

def print_messages():
    # reactivation de l'écriture dans la chat box
    chat_box.config(state=NORMAL)
    chat_box.delete("1.0", "end")    
    query = reference.order_by("date")
    results = query.get()
    for msg in results:
        if msg.to_dict()['author'] == '' or msg.to_dict()['content'] == '':
            continue
        date = datetime.fromtimestamp(msg.to_dict()['date'].timestamp())
        # ajouter dans la zone de texte
        chat_box.insert(END, f"Le {date} > {msg.to_dict()['author']} dit : \n\t {msg.to_dict()['content']} \n")
        
    # déactivation de l'écriture dans la chat box
    chat_box.config(state=DISABLED)

# connection à firebase firestore
cred = credentials.Certificate("wishscord.json")
app = firebase_admin.initialize_app(cred)
db = firestore.client()
reference = db.collection('Messages')

# création de la fenêtre 
root = Tk()

# modification de la fenetre
root.title("Discord Gold Edition")
root.minsize(1080, 720)

# ajouter la scrollbar
scrollbar = Scrollbar(root, orient="vertical")
scrollbar.grid(rowspan=2, column=3,  sticky=N+S+W)

# ajouter la zone de chat
chat_box = Text(root, state=DISABLED, yscrollcommand=scrollbar.set)
scrollbar.config(command=chat_box.yview)
chat_box.grid(row=0, columnspan=2)

# ajouter le label du pseudo
label_pseudo = Label(root, text="Pseudo : ")
label_pseudo.grid(row=1)

# ajouter la zone de texte du pseudo
pseudo_box_value = StringVar()
pseudo_box = Entry(root, textvariable=pseudo_box_value)
pseudo_box.grid(row=1, column=1)

# ajouter le label de l'input
label_input = Label(root, text="Input : ")
label_input.grid(row=2)

# ajouter la zone d'input text
new_message_box_value = StringVar()
new_message_box = Entry(root, textvariable=new_message_box_value)
new_message_box.grid(row=2, column=1)

# ajouter le bouton d'envoie de message
submit_button = Button(root, text="Envoyer", command=send_message)
submit_button.grid(row=3, column=0)

# ajouter le bouton de refresh
refresh_button = Button(root, text="Refresh", command=print_messages)
refresh_button.grid(row=3, column=1)

# bind 
root.bind('<Return>', send_message)

print_messages()

# afficher la fenêtre
root.mainloop()

