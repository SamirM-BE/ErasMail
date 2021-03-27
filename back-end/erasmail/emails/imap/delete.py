from imapclient import IMAPClient, imapclient


def move_to_trash(host, username, password, folder_uids):
    server = IMAPClient(host)
    server.login(username, password)

    trash_folder = server.find_special_folder(imapclient.TRASH)

    for folder_name, uids in folder_uids.items():
        server.select_folder(folder_name)
        server.move(uids, trash_folder)
        server.unselect_folder()

    server.logout()

