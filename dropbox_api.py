import os
import dropbox

def update_on_dropbox():
    with open("app_corona/.token") as tk:
        token = tk.read().split("\n")[0]

    dbx = dropbox.Dropbox(token)
    dbx.users_get_current_account()

    def send(dbx, file):
        with open(file,"rb") as f:
            return dbx.files_upload(f.read(), '/{}'.format(os.path.split(file)[-1]))
    def ls(dbx):
        return [f.name for f in dbx.files_list_folder("").entries]

    def delete(dbx,name):
        return dbx.files_delete("/"+name)


    current_files = ls(dbx)
    for file in current_files:
        delete(dbx, file)

    for file in os.listdir("app_corona/plots"):
        send(dbx, "app_corona/plots/"+file)
    
    
