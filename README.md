## Getting Started
 - [Invite this bot to your server!](https://discord.com/api/oauth2/authorize?client_id=996571275919097898&permissions=8&scope=bot)
 - [Github open source code](https://github.com/xckev/CipherBot)
 
 ## Developers
 
 [Kevin Xiao](https://github.com/xckev)
 
 Socials/Links: https://linktr.ee/xckev
 
## Commands
 
### Cryptography
 
 Cryptographic algorithms/functions and inspiration for these commands were taken from the [2022 Stanford Pre-Collegiate Summer Institute Cryptography and Cryptocurrency course](https://summerinstitutes.spcs.stanford.edu/courses/2022/cryptography-and-cryptocurrency). Here is the course content website: https://crypto.stanford.edu/spcs/
 
#### $keygen
  
 Generates new Diffie-Hellman private and public keys for encryption and decryption. Execute often for better security. /encrypt calls this automatically if keys were not previously generated.
 
 In the Diffie-Hellman key-exchange protocol, two parties who want to send encrypted messages to each other have to generate public and private keys in order to get a shared key that can be used for encryption and decryption. If we let G be a cyclic group of prime order q and generator g, each party generates a private key which is a random integer in the set {0, 1, ..., q-1}. Both parties also must agree on a prime modulus m. Each attain a public key by raising g to the private key, modulus m. The public keys are shared to the other party. Finally, by raising the other party's public key to the private key and applying modulo m, both parties get the same result that is the shared key. This means encrypting and decrypting messages between the two parties can begin.
 
 ![image](https://user-images.githubusercontent.com/54916002/183491466-51e8d778-40bf-4a50-8ec9-70ac879cef41.png)

This Khan Academy [link](https://www.khanacademy.org/computing/computer-science/cryptography/modern-crypt/v/diffie-hellman-key-exchange-part-2) is a simplified video demonstration. You may read more about Diffie-Hellman key exchange [here](https://en.wikipedia.org/wiki/Diffie%E2%80%93Hellman_key_exchange).
 
#### /encrypt
 
 Encrypt a secret message to send to a user of choice. This command does an undercover $keygen if both parties have not yet generated their encryption keys. 
 
 This command uses a shared key to encrypt plaintext into ciphertext. This is done by using a stream cipher, where a pseudo-random generator is applied on the key to generate a one-time-pad that is the same length in bytes as the plaintext. This one-time-pad is then XORed with the bytes of the plaintext to produce the ciphertext, which is displayed in hexadecimal.
 
#### /decrypt
 
 Decrypts ciphertext that was sent by someone.
 
 This command uses the shared key to decrypt ciphertext into plaintext. This is again done using a stream cipher, with the same one-time-pad XORed with the ciphertext as bytes. Converting back into ASCII characters, the command results in the original plaintext.
 
### Secure Voting
 
#### $vote \<duration> <option 1> <option 2> \<prompt>
 
 Creates a 2-option poll with a prompt that accepts submissions for a specified number of minutes. Use quotation marks to separate arguments that have spaces. No user will be able to see another's votes (exceptions exist for bot hosters).
 
 This command utilizes cryptographic techniques of both mix-networks and homomorphic encryption. Mix-networks, or mix-nets, usually consist of multiple servers that accept a batch of votes and output the batch in randomly permuted order so that one cannot link the input votes to the output votes. The goal of this is to hide the option each voter voted for, to ensure integrity. Mix-nets are often used in government-level electronic voting, and are a useful tool that can help keep society's most important elections secure.
 
 ![image](https://user-images.githubusercontent.com/54916002/183489961-84b08067-72e5-4c8b-962e-7d36d5102cf8.png)
 
The above image is a simplified demonstration of the network of servers that mix the votes. Each server is called a "mix" which outputs an arbitrary permutation of the recieved input votes, which may have already been through other mixes. Since CipherBot is only hosted on one server, we could only randomly permute the votes one or more times on the same server, which is suboptimal for true security, but the main purpose here is to emulate the process for academic purposes.

Mix-nets are usually combined with other cryptographic techniques. There are re-encryption mix-nets, which rely on using public key encryption schemes within each mix and a shared decryption key among all the mix servers. Another type of mix-net is the shuffle decryption mix-net, that accepts votes as a collection of ciphertexts and outputs the votes as a randomly ordered list of plaintexts. For CipherBot, we decided to combine the mix-net permutations with [homomorphic encryption](https://en.wikipedia.org/wiki/Homomorphic_encryption). Homomorphic encryption allows for operations to be done on ciphertexts and for the correct result to remain after decryption. From the paper ["A Comparative Study of Generic Cryptographic Models for Secure Electronic Voting"](https://www.researchgate.net/publication/236594949_A_COMPARATIVE_STUDY_OF_GENERIC_CRYPTOGRAPHIC_MODELS_FOR_SECURE_ELECTRONIC_VOTING) by several scholars from Ladoke Akintola University of Technology:

"With homomorphic encryption there is an operation ⊕ defined on the message space and an operation 
⊗ defined on the cipher space, such that the “product” of the encryptions of any two votes is the encryption 
of the “sum” of the votes, i.e.:

EM1 ⊕ EM2 = E (M1 ⊗ M2)

This property allows either to tally votes as aggregates or to combine shares of votes, without decrypting single votes"

 ![image](https://user-images.githubusercontent.com/54916002/183494829-ccb73f29-9757-4a89-9730-375f31ade5fa.png)
 
Above is a simple example of the homomorphic voting model. For CipherBot, the [Microsoft SEAL](https://www.microsoft.com/en-us/research/project/microsoft-seal/) Homomorphic Encryption library was used, and their developers have a [paper](https://www.microsoft.com/en-us/research/uploads/prod/2017/11/sealmanual-2-3-1.pdf) where you may learn more. We would like to reemphasize that CipherBot merely emulates the mix-net and homomorphic processes for academic purposes, and does not provide true security with these cryptographic techniques.

### Cryptocurrency

#### $crypto \<coin symbol>

Shows the price of the coin with the requested coin symbol.

This command and the rest of the commands in the Cryptocurrency section use the pro.coinmarketcap.com API to access the latest cryptocurrency prices. Here is the link to the documentation and more information about this API: https://coinmarketcap.com/api/documentation/v1/

#### $bitcoin

Shows the price of Bitcoin (BTC).

#### $ethereum

Shows the price of Ethereum (ETH).

#### $dogecoin

Shows the price of Dogecoin (DOGE).

### Utilities and Miscellaneous

#### $help

Shows CipherBot information and commands.

#### $hello

Exchange greetings with CipherBot!

#### $kick \<user> 

Mention a user to kick from the server.

#### $ban \<user>

Mention a user to ban from the server.

#### $shutdown

CipherBot will go offline; only the bot's host may use this.
 
## Self Hosting
 We support self hosting. You may contact Kevin Xiao via any medium for help related to self hosting. Listed below are the requirements for hosting CipherBot.
  - [Python 3.8 or later](https://www.python.org/downloads/)
  - [Discord.py API](https://discordpy.readthedocs.io/en/latest/index.html)
  - [Microsoft SEAL](https://www.microsoft.com/en-us/research/project/microsoft-seal/)
  - [Pyfhel Microsoft SEAL Python Wrapper](https://pyfhel.readthedocs.io/en/latest/)
  - Coinmarketcap Token
  - Discord Bot Token
 
## Privacy Policy
We are fully committed to protecting to your privacy. 

#### Information Stored
- User ID and Guild IDs
- Public and private keys generated for each user

#### Data Usage
We use this data to encrypt/decrypt messages and to run our secure polls.

#### Distribution
We will not disclose any personal information without your consent and we do not share it with any external sites.

#### Concerns and Contact
Public and private keys are generated only if a CipherBot encryption command is used. You may send secrets through other means if you do not wish to use CipherBot. If you have any further issues, you can contact Kevin Xiao via any medium.

#### Disclaimer:
CipherBot's features are not all completely secure from cryptographic attacks. Many of the implemented cryptographic algorithms are shallow or are emulations for academic purposes. We work within the boundaries given by the Discord.py API, and cannot ensure security from threats beyond other users in your Discord server. CipherBot is not intended for professional or truly secure settings.
 
## License
 [MIT License](https://github.com/xckev/CipherBot/blob/master/LICENSE)
