#####lấy thông tin từ các file txt, chỉnh sửa file ovpn và chạy script tới openvpn.
def main():
 print("Write by Kietpg with love <3 \n")
 print("đọc hướng dẫn trước khi sử dụng :> hoặc liên hệ kietpg@vng.com.vn")
 import pyotp
 import subprocess
 import glob
 with open("pin.txt", "r") as file, open("user.txt", "r") as file2, open("secret.txt", "r") as file3 :
    user = file2.readline().strip()
    pin = file.readline().strip()
    secret = file3.readline().strip()
 if user and pin and secret is not None:
    print("Đã tìm thấy thông tin")
 else:
     print("hãy đọc readme và làm theo hướng dẫn")        
# Create a TOTP object
 totp = pyotp.TOTP(secret)
# Generate a Google Authenticator code
 authenticator_code = totp.now()   
    
# Define the content to write to the file
 file_content = [user, f"{pin}{authenticator_code}"]

# Write the content to the file
 with open("pwd.conf", "w") as file5:
    file5.write("\n".join(file_content))
# Open .ovpn file 
# Use glob to find the first .ovpn file in the current directory
 ovpn_files = glob.glob("*.ovpn")
 script_path = ovpn_files[0]
 # Check if the line already exists in the file
 with open(script_path, "r") as file4:
    lines = file4.readlines()
 if "auth-user-pass pwd.conf" in lines[-1]:
    print('file opvn đã được cài đặt')
 elif "auth-user-pass pwd.conf" not in lines:
    # Line does not exist, add it to the end of the file
    lines.append("auth-user-pass pwd.conf" + "\n")  # Add a newline character
    print("Đã edit file ovpn")
    # Write the modified content back to the file
    with open(script_path, "w") as file4:
        file4.writelines(lines)
#run openvpn
 openvpn_executable = r'C:\Program Files\OpenVPN\bin\openvpn-gui.exe'
 subprocess.run(f'"{openvpn_executable}" --command connect "{script_path}"', shell=True, check=True)

#ping liên tục tới 10.115.76.1 để kiểm tra đã kết nối hay chưa
def connnect():
 import time
 import ping3
 import glob
 ovpn_files = glob.glob("*.ovpn")
 script_path = ovpn_files[0]
 openvpn_executable = r'C:\Program Files\OpenVPN\bin\openvpn-gui.exe'
 attempts = 0
 while attempts < 3:
        response_time = ping3.ping("10.115.76.1")
        if response_time is not None:
            print("đã kết nối thành công")
            time.sleep(3)
            break
        else:
            print(f"Đang kết nối...")
            time.sleep(1)
            attempts += 1
 else:
        print(f"Kết nối không thành công. Hãy thử lại.")
        subprocess.run(f'"{openvpn_executable}" --command disconnect "{script_path}"', shell=True, check=True)
if __name__ == "__main__":
   main()
   connnect()

####python -m PyInstaller --onefile --disable-windowed-traceback --hidden-import=pyotp --hidden-import=subprocess --hidden-import=glob --hidden-import=time --hidden-import=ping3 --ico=icon.ico auto.py
