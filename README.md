# Stockholm

Stockholm is a simple command-line program designed to encrypt or decrypt files within a specified directory. It primarily targets certain file extensions for encryption, appending the .ft extension to encrypted files to indicate they have been affected. The goal is to reproduce the behavior of Ransomware-type malware.

----
## Encryption Methodology

#### Key Generation
For encryption, the utility generates a random 32-byte key using the os.urandom function. This key is necessary for both the encryption and decryption processes. It's displayed to the user upon generation (unless -s option is used), and they should make sure to keep a safe record of it.

#### Encryption Algorithm
Stockholm uses the AES (Advanced Encryption Standard) cipher in CBC (Cipher Block Chaining) mode for file encryption. The initialization vector (IV) for the CBC mode is derived from the first 16 bytes of the file data, ensuring that each file has a unique IV, which is a recommended practice for encryption.

#### Data Padding
The utility employs PKCS7 padding to ensure data blocks are of the required length for the AES encryption process.

#### File Naming
After encryption, affected files will have their extension changed to include .ft. For example, a file named document.txt will become document.txt.ft post encryption.

----
### How to Use

#### (Optionnal) Launch process into a Docker
Simply run ``make``, it will launch a Docker, open a bash, and just follow the rest of instructions.

#### Encrypting Files
Simply run the Stockholm utility. By default, it will generate a random encryption key, display it to the user, and start encrypting target files within the specified directory. Only the same type of files that Wanacry infectes are targeted (https://gist.github.com/xpn/facb5692980c14df272b16a4ee6a29d5#file-wannacry_file_extensions-txt)
``python3 stockholm.py``

This will display the generated encryption key and the targeted files (unless -s option is used). **Ensure you keep this key safe, as it is required to decrypt the files later**.

#### Decrypting Files
To decrypt the files, run the Stockholm utility with the -r flag followed by the previously generated encryption key in hexadecimal format.
``python3 stockholm.py -r YOUR_ENCRYPTION_KEY_IN_HEX``

Replace **YOUR_ENCRYPTION_KEY_IN_HEX** with the key that was displayed during the encryption process.

#### Silent Mode
If you want to run the utility without any console output, use the -s or --silent flag:
``python3 stockholm.py --silent``

#### Checking Version
To display the version of the utility, use the -v or --version flag:
``python3 stockholm.py --version``

----
### Warning
This utility has the potential to irreversibly encrypt files. Always backup your data and thoroughly test the program in a safe environment before using it on essential data. Remember to securely store the generated encryption key, as losing it means you won't be able to decrypt the files. **This utility is provided for educational purposes only. Ensure you have proper permissions before running it on any system or dataset. Misuse can lead to loss of data.**
