import asyncio
import websockets
import json
import os

async def handle_connection(websocket, path):
    try:
        data = await websocket.recv()
        user_data = json.loads(data)

        # user data saver
        result = create_user_folder(user_data)
        await websocket.send(result)  # Send data from server
    except Exception as e:
        await websocket.send(f"Bir hata oluştu: {e}")

def create_user_folder(data):
    user_type = data["type"]
    first_name = data["firstName"]
    last_name = data["lastName"]
    email = data["email"]
    password = data["password"]

    # 
    folder_name = f"{first_name}_{last_name}"

    # equal name and gmail chacker system  #Not  websockete çalış
    if os.path.exists(f"data/{folder_name}") or check_email_exists(email):
        return "Bu ad veya Gmail kullanılıyor."

    if user_type == "Module User":
        # Module User için klasör oluştur ve verileri kayıt eder
        user_path = f"data/{folder_name}"
        os.makedirs(user_path)
        with open(f"{user_path}/User Data.ini", "w") as f:
            f.write(f"Ad={first_name}\n")
            f.write(f"Soyad={last_name}\n")
            f.write(f"Gmail={email}\n")
            f.write(f"Şifre={password}\n")

    elif user_type == "Module Developer":
        # Module Developer içine klasör ve alt klasör oluşturur
        developer_path = f"data/Module User Data/{folder_name}"
        os.makedirs(developer_path)
        os.makedirs(f"{developer_path}/User Module")
        with open(f"{developer_path}/User Data.ini", "w") as f:
            f.write(f"Ad={first_name}\n")
            f.write(f"Soyad={last_name}\n")
            f.write(f"Gmail={email}\n")
            f.write(f"Şirket={data.get('company', 'Bilinmiyor')}\n")
            f.write(f"Şifre={password}\n")
    else:
        return "Geçersiz kayıt türü."

    return "Kayıt başarılı."

def check_email_exists(email):
    """equal data checker."""
    for root, dirs, files in os.walk("data"):
        for file in files:
            if file == "User Data.ini":
                with open(os.path.join(root, file), "r") as f:
                    content = f.read()
                    if f"Gmail={email}" in content:
                        return True
    return False

#websocket starter
start_server = websockets.serve(handle_connection, "127.0.0.1", 12345)

if __name__ == "__main__":
    # Ana veri klasörünü oluşturur
    if not os.path.exists("data"):
        os.makedirs("data")
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
