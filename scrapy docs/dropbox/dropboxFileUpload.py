import dropbox


#! Enter Access token, Local path, Backup path
TOKEN = '-8zc9vbHFSEAAAAAAAAAAWgY-pn1dBK0YVE3CorOQR46JlnCJ6Fsg9Le5KyQxmXK'
LOCALFILE = 'items.csv'
BACKUPPATH = '/Local_Machine/dropboxItems.csv'

dbx = dropbox.Dropbox(TOKEN)

with open("items.csv", "rb") as f:
    dbx.files_upload(f.read(), BACKUPPATH, mode=dropbox.files.WriteMode.overwrite)


print("File upload accordingly on Dropbox")








