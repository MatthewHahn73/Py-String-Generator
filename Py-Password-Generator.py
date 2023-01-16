"""
Password Generator

Future Features
    TODO

Required Software
    -Python 
        -Version >= 3.6
        -Installation: https://www.python.org/downloads/
    -Python Modules
        -pyperclip
            -Purpose: Clipboard Interactivity
            -Installation: https://pypi.org/project/pyperclip/
        -Cryptodomex 
            -Purpose: 256-Bit AES
            -Installation: https://pypi.org/project/pycryptodomex/

Functionality
    -Generates N character passwords
    -Parameters
        -char       <Required> password character length
        -lc         <Optional> include lowercase alphabet characters (Default is digits only)
        -uc         <Optional> include uppercase alphabet characters (Default is digits only)
        -punc       <Optional> include puncuation characters (Default is digits only)
        -unique     <Optional> each character of the string will be unique (No duplicates)
        -clip       <Optional> outputs the generated password to the clipboard
        -txt        <Optional> outputs the generated password to a .txt file
        -etxt       <Optional> outputs the generated password to an encrypted .txt file     
"""

import string
import argparse
import logging
import random
import pathlib
import pyperclip
from Cryptodome.Cipher import AES
from getpass import getpass

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
ERROR_TEMPLATE = "A {0} exception occurred. Arguments:\n{1!r}"

class Generator():
    NUMBERS_LOWER = string.ascii_lowercase
    NUMBERS_UPPER = string.ascii_uppercase
    DIGITS = string.digits
    PUNCTUATION = string.punctuation

    def __init__(self, args):
        self.Parameters = argparse.Namespace(**{ 
			"CHARACTERS": args.char,
			"LOWERCASE_CHARACTERS": args.lc,
			"UPPERCASE_CHARACTERS": args.uc,
			"PUNCTUATION": args.punc,
			"UNIQUENESS": args.unique,
            "CLIPBOARD": args.clip,
			"FILE_OUTPUT": args.txt,
			"ENCRYPTED_FILE_OUTPUT": args.etxt,
		})

    def Output_To_File(self, Password, Path):
        try:
            with open(Path, "w") as File:
                File.write(Password + "\n")
            return True
        except IOError as E:
            logging.error(ERROR_TEMPLATE.format(type(E).__name__, E.args)) 
        return False

    def Output_To_File_Encrypted(self, Password, Key, Path):
        try:
            with open(Path, "wb") as File:
                Cipher_Object = AES.new(bytes(Key, "utf-8"), AES.MODE_EAX)
                Cipher_Text, Tag = Cipher_Object.encrypt_and_digest(Password.encode('utf-8'))
                [ File.write(x) for x in (Cipher_Object.nonce, Tag, Cipher_Text) ]
                return True
        except IOError:
            File_Split = pathlib.PurePath(Path)
            logging.error("IOError opening " + "'~\\" + str(File_Split.parent.name) + "\\" + str(File_Split.name) + "'")
        except UnicodeDecodeError as Unicode_Exception:
            logging.error(ERROR_TEMPLATE.format(type(Unicode_Exception).__name__, Unicode_Exception.args)) 
        except ValueError as Value_Error:
            logging.error(ERROR_TEMPLATE.format(type(Value_Error).__name__, Value_Error.args)) 
        except Exception as General_Exception:
            logging.error(ERROR_TEMPLATE.format(type(General_Exception).__name__, General_Exception.args)) 
        return False

    def Generate_String(self):
        try:
            Generated_String = ""
            Candidates = [*self.DIGITS \
                + (self.NUMBERS_LOWER if self.Parameters.LOWERCASE_CHARACTERS else "") \
                + (self.NUMBERS_UPPER if self.Parameters.UPPERCASE_CHARACTERS else "") \
                + (self.PUNCTUATION if self.Parameters.PUNCTUATION else "")]
            for i in range(0, self.Parameters.CHARACTERS):
                if self.Parameters.UNIQUENESS:
                    if self.Parameters.CHARACTERS < len(Candidates):
                        Generated_Character = random.choice(Candidates)
                        while Generated_Character in Generated_String:
                            Generated_Character = random.choice(Candidates)
                        Generated_String += Generated_Character
                    else:
                        raise Exception("Given character amount (" 
                            + str(self.Parameters.CHARACTERS) + ") is greater than the possible candidates for the string (" 
                                + str(len(Candidates)) + ")")
                else:
                    Generated_String += random.choice(Candidates)
            return Generated_String
        except Exception as E:
            logging.error(ERROR_TEMPLATE.format(type(E).__name__, E.args)) 

    def Execute(self):
        try:
            print("=" * 32
                , "Character(s): " + str(self.Parameters.CHARACTERS) 
                , "Character Uniqueness: " + str(self.Parameters.UNIQUENESS)
                , "Include Lowercase: " + str(self.Parameters.LOWERCASE_CHARACTERS)
                , "Include Uppercase: " + str(self.Parameters.UPPERCASE_CHARACTERS)
                , "Include Puncuation: " + str(self.Parameters.PUNCTUATION)
                , "Output to Clipboard: " + str(self.Parameters.CLIPBOARD)
                , "Output to File: " + str(self.Parameters.FILE_OUTPUT if not self.Parameters.ENCRYPTED_FILE_OUTPUT else self.Parameters.ENCRYPTED_FILE_OUTPUT)
                , "Encrypt: " + str(self.Parameters.ENCRYPTED_FILE_OUTPUT)
                , "=" * 32
                , sep="\n")
            Run = ""
            while len(Run) <= 0:
                Run = input("Generate a password with these parameters? (Y/N) ")
            if (Run[0].lower() == "y"):
                if self.Parameters.CHARACTERS > 0:
                    Password = self.Generate_String()
                    if Password:
                        if self.Parameters.FILE_OUTPUT:                     #Output to text file
                            Output_File = "Output.txt"
                            if self.Output_To_File(Password, Output_File): 
                                print("Password was written to '" + str(Output_File) + "'")
                        if self.Parameters.ENCRYPTED_FILE_OUTPUT:           #Prompt for AES key; Output encrypted text to file
                            Output_File = "Encrypted_Output.txt"
                            AES_Key = getpass("Key: ")
                            while len(AES_Key) != 16:
                                print("AES keys must be 16 characters")
                                AES_Key = getpass("Key: ")
                            if self.Output_To_File_Encrypted(Password, AES_Key, Output_File):
                                print("Password was written to '" + str(Output_File) + "'")
                        if self.Parameters.CLIPBOARD:                       #Copy the file to the windows clipboard
                            pyperclip.copy(Password)
                            print("Password was copied to the clipboard")
                        if not self.Parameters.FILE_OUTPUT \
                            and not self.Parameters.ENCRYPTED_FILE_OUTPUT \
                                and not self.Parameters.CLIPBOARD:          #Output generated string to console
                                    print("Password: " + str(Password))
                else:
                    raise Exception("Character count cannot be negative or 0")
        except Exception as E:
            logging.error(ERROR_TEMPLATE.format(type(E).__name__, E.args)) 

if __name__ == "__main__": 	#Reads in arguments
	par = argparse.ArgumentParser(description="Password Generator v0.7")

	#Required parameters
	par.add_argument("-char", type=int, help="<Required> password character length", required=True)

	#Optional parameters
	par.add_argument("-lc", help="<Optional> include lowercase alphabet characters (Default is digits only)", action="store_true")
	par.add_argument("-uc", help="<Optional> include uppercase alphabet characters (Default is digits only)", action="store_true")
	par.add_argument("-punc", help="<Optional> include puncuation characters (Default is digits only)", action="store_true")
	par.add_argument("-unique", help="<Optional> each character of the string will be unique (No duplicates)", action="store_true")

	#Export parameters
	par.add_argument("-clip", help="<Optional> outputs the generated password to the clipboard", action="store_true")
	par.add_argument("-txt", help="<Optional> outputs the generated password to a .txt file", action="store_true")
	par.add_argument("-etxt", help="<Optional> outputs the generated password to an encrypted .txt file", action="store_true")

	Script = Generator(par.parse_args())
	Script.Execute()
	input("Press enter to close ... ")
	exit()