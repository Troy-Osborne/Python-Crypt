# Python-Crypt
Generate Keys, Encrypt Files &amp; Folders. Symettric key one-time pad cryptography
Run Crypt.py and it will prompt you for your input, once a password is entered it will be mixed with your chosen salt and sent to a SHA256 digest, the resulting hash from the digest will then be mixed with the salt yet again and used to generate a new hash, this process repeats until it reaches the desired length with all hashes appended to the resulting key file.
This resulting key file should be non-terminating/non-repeating and is used for XOR encryption.

This is just a proof of concept and if conforming to best practices than each bit of your key should be independent of all other keys. This isn't the case here!

It's still fairly strong, I'd sure have trouble cracking it but ideally it should be mixed with some form of tranposition cypher, like my rubik's cube inspired method.
https://trogramming.com/blog/2022/02/25/rubiks-crypt/

For stronger key generation I suggest using mouse movements or hashing timestamps from a global keyboard hook. 
Maybe study how the /dev/random entropy pool works under GNU/linux.
