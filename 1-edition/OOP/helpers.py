def get_group_id(client, group_username):
    group_info = client.get_chat(group_username)
    return group_info.id

def get_origin_and_dest_chat_id(client):
    origin_group_username = input("origin_group_username please bitch: ")
    destination_group_username = input("destination_group_username please bitch: ")
    origin_group_id = get_group_id(client, origin_group_username)
    destination_group_id = get_group_id(client, destination_group_username)
    return origin_group_id,destination_group_id