import os
import dropbox

def update_on_dropbox():
    with open("app_corona/.token") as tk:
        token = tk.read().split("\n")[0]

    dbx = dropbox.Dropbox(token)
    dbx.users_get_current_account()
    
    dropbox_folder = "/Corona_Statistics"

    def send(dbx, path, file):
        with open(file,"rb") as f:
            return dbx.files_upload(f.read(), os.path.join(path, os.path.split(file)[-1]))
        
    def ls(dbx, path):
        return [f.name for f in dbx.files_list_folder(path).entries]

    def delete(dbx, path, name):
        return dbx.files_delete(os.path.join(path,name))

    current_files = ls(dbx,dropbox_folder)
    for file in current_files:
        delete(dbx, dropbox_folder, file)

    for file in os.listdir("app_corona/plots"):
        send(dbx, dropbox_folder, "app_corona/plots/"+file)
    
    
