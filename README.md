## The Problem

From Athens, Greece in 508 BCE to the United States in 2022, democracies have protected liberty and nurtured prosperity among people throughout history. Although no implementation of it is perfect, it is undeniable that democracy is the best form of government we've got. Not only does democracy allow everyone to have an equal voice, but it also makes way for flexibility because policies can remain representative of the constantly changing ideologies among the governed. Democracies have reduced state conflicts in number and size, encouraged citizens to educate themselves about societal issues, and reinforced justice and ethicality within people. Due to all the great perks that democracy brings, determining national policies through fair voting and elected officials is something that must remain protected.

Unfortunately, democracies have been put into significant danger as the internet has become more ubiquitous. Specifically, many democratic nations have taken on electronic and online voting. Many countries such as Australia, Belgium, Brazil, France, Germany, India, and USA have already incorporated some form of electronic or online voting in their elections. 

In the United States at least, election security has become a major concern as of late. Both the 2016 and 2020 presidential elections have seen tension and conflict regarding integrity. Whether it was potential foreign meddling or fraudulent votes, many Americans have started to question the legitimacy of election results. The existence of inaccurate elections, or even just skepticism about election integrity, poses a huge danger to the validity of a democracy. Much of the skepticism lies in the fact that “black box” machines are used to tally votes across the US. Black box means that the algorithms used to hide, secure, and verify votes are undisclosed, where no one knows how they work. With a need for better transparency and more trust in the digital voting, we turn to technology for solutions.


## The Technology

Superior electronic voting systems are a fairly new topic of study, but quick development and building off of older technologies have paved the way for the secure voting solutions that exist today. 

Within process of developing better electronic voting systems, we must begin with defining our criteria. What should our voting systems provide?

-	Accuracy: Votes cannot be altered, duplicated, or eliminated. Each vote must be counted as cast in the final tally.
-	Privacy: Votes must never be shared with others. Secrecy of votes keep voters safe from being pressured and coerced.
-	Verifiability: Voters can verify that their votes were counted correctly and included in the final tally
-	Usability: Voting systems must be simple to use. Complexity should not be an obstacle to a fair vote.

The accuracy, privacy, and verifiability criteria are largely dependent on cryptography. The cryptographic solutions that can be implemented for secure voting are fairly complicated, and not everyone can understand how they work. The point, however, is not for the public to understand the algorithms, but it is rather for the systems to be transparent. Therefore, it is possible to verify election integrity.

Intrigued by the algorithms knowing the importance of secure elections, I started to work on CipherBot. CipherBot utilizes the Discord instant messaging social platform as a medium to implement encryption/decryption and emulate secure voting. The functionality of CipherBot is discussed in this next section.

## Cryptography

This section will only give a quick overview of the cryptographic algorithms used in CipherBot and some others. For a more detailed explanation and links to further resources, refer to the README.md file on Github. 

The first function of CipherBot is encryption/decryption of data. Specifically, users can encrypt standard ASCII text and send the hexadecimal encryptions as a message in a server. No one else will be able to decrypt the message other than the intended receiver. This is done using traditional Diffie-Hellman key exchange to generate a shared key between two parties with each party using a public and private key. Public key encryption then encrypts the message with the shared key.

Encrypt(public key, message) = ciphertext

Decrypt(secret key, ciphertext) = message

 Diffie Hellman uses mathematical principles of exponentiation and modular arithmetic for two parties to achieve the same value without leaking important information that adversaries can use for an attack.
 
Beneath the encryption and decryption algorithms lies functions that converts all data to bytes, makes the key just as long as the message with a pseudo-random generator, and XORs the key with the message (this is called a stream cipher).

The reasons that it is extremely hard for an attacker to find the shared key can be explained by group theory (specifically groups of prime orders), and the naturally difficult problem of large prime numbers. 
