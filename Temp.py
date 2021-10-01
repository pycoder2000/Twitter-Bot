#    import Tkinter as tk     ## Python 2.x
#except ImportError:
import tkinter as tk     ## Python 3.x 
import os
from tkinter import ttk
from tkinter import messagebox
from tkinter import Frame
#from tkinter import Style
import json
import datetime
import time
# Tkintertable
from tkintertable.Tables import TableCanvas
from tkintertable.TableModels import TableModel

__author__ = "Parth Desai"
__copyright__ = "Copyright (C) 2020 Parth Desai"
__credits__ = ["Parth Desai"]
__license__ = "MIT"
__version__ = "1.0"
__maintainer__ = "Parth Desai"
__email__ = "desaiparth2000@gmail.com"
__status__ = "Buiding"

TwitterAuthButton = None
UpdateTwitterStreamButton = None
TwitterKeysWindow = None
E1=E2=E3=E4=None
root = None

class TwitterBot(tk.Frame):
    """
        This is the base class for the program.
    """

    # window count
    count = 0
    
    # window status flags
    twitterAuthOpenedFlag = False
    tweetSentimentOpenedFlag = False
    termFrequenciesOpenedFlag = False
    happiestStateOpenedFlag = False

    # is authenticated flag
    twitterAuthCompletedFlag = False
    
    twitterStreamUpdatedFlag = False
    
    # file paths
    TwitterKeysFile = "Twitter_API_Keys"
    ConfigFile = "config.json"
    AFINNFile = "word_scores/AFINN-111.txt"

    # dictionary for storing configuration data
    config = {}

    def __init__(self, parent):
        """
            Initialize the parent Frame
        """
        
        tk.Frame.__init__(self, parent)            
        self.parent = parent
        self.initUI()
        


    def initUI(self):
        """
            Method for initializing the root window elements. 
            All root level buttons and labels are initialized here.
        """

        self.parent.title("TwitterBot : Download Twitter Threads")
        self.pack(fill=tk.BOTH, expand=1)

        # canvas for logo
        TwitterBotCanvas = tk.Canvas(self.parent, height=130, width=600)
        TwitterBotCanvas.create_text(300, 50, font=("Purisa", 40), text = "TWITTERBOT")
        TwitterBotCanvas.create_text(300, 100, font=("Purisa", 20), text = "Twitter Thread Downloader")
        TwitterBotCanvas.place(x = 100, y = 40, width = 600, height = 130)
        
        # button for twitter credentials window
        global TwitterAuthButton
        if not os.path.isfile(self.TwitterKeysFile):
            TwitterAuthButton = tk.Button(self.parent, text = "Set Twitter Credentials", command = self.setTwitterAuth, bg="blue", fg="white")
            TwitterAuthButton.place(x = 160, y = 220, width = 200, height = 30)
        else:
            TwitterAuthButton = tk.Button(self.parent, text = "Update Twitter Credentials", command = self.updateTwitterAuth, bg="gray", fg="white")
            TwitterAuthButton.place(x = 160, y = 220, width = 200, height = 30)

        self.var = tk.StringVar()

        # logic for downloading / updating twitter stream
        if os.path.isfile(self.ConfigFile):

            with open(self.ConfigFile, 'r') as f:
                cfg = json.load(f)
            try:        
                updated = cfg['TwitterStreamLastUpdated']
            except:
                updated = None
                
            if updated:
                self.var.set("Stream last updated on: " + updated)
                
                TwitterStreamStatusLabel = tk.Label(self.parent, textvariable = self.var, justify = tk.LEFT, wraplength = 400)
                TwitterStreamStatusLabel.place(x = 180, y = 270, width = 400, height = 30)

                global UpdateTwitterStreamButton
                UpdateTwitterStreamButton = tk.Button(self.parent, text = "Update Twitter Stream", command = self.updateTwitterStream, bg="gray", fg="white")
                UpdateTwitterStreamButton.place(x = 420, y = 220, width = 200, height = 30)
            
        else:
            self.var.set("Download Required")
        
            TwitterStreamStatusLabel = tk.Label(self.parent, textvariable = self.var, justify = tk.LEFT, wraplength = 400)
            TwitterStreamStatusLabel.place(x = 180, y = 270, width = 400, height = 30)

            DownloadTwitterStreamButton = tk.Button(self.parent, text = "Download Twitter Thread", command = None, bg="blue", fg="white")
            DownloadTwitterStreamButton.place(x = 420, y = 220, width = 200, height = 30)

##        global TweetSentimentTermEntry
##        TweetSentimentTermEntry = tk.Entry(self.parent, bd =5)
##        TweetSentimentTermEntry.place(x = 400, y = 150, width = 200, height = 30)
##        TweetSentimentTermEntry.focus()
        
        # button for running tweet sentiment
        RunTweetSentimentButton = tk.Button(self.parent, text = "Enter URL", command = None, bg="blue", fg="white")
        RunTweetSentimentButton.place(x = 50, y = 320, width = 200, height = 30)

        # button for showing term frequencies
        TermFrequencyButton = tk.Button(self.parent, text = "Generate HTML/Epub/Mobi", command = None, bg="blue", fg="white")
        TermFrequencyButton.place(x = 300, y = 320, width = 200, height = 30)

        # button for showing happiest state in the US
        HappiestStateButton = tk.Button(self.parent, text = "About", command = None, bg="blue", fg="white")
        HappiestStateButton.place(x = 550, y = 320, width = 200, height = 30)
        

        
    def setTwitterAuth(self):
        """
            Method for initializing and displaying the Twitter credentials window.
        """

        self.count += 1

        if self.twitterAuthOpenedFlag == False:
            # set window opened
            self.twitterAuthOpenedFlag = True
        
            # initialize window
            global TwitterKeysWindow
            TwitterKeysWindow = tk.Toplevel(self)
            TwitterKeysWindow.minsize(600, 500)
            TwitterKeysWindow.geometry("600x500+100+100")
            TwitterKeysWindow.title("Twitter API Authentication Details")
            TwitterKeysWindow.config(bd=5)
            L0 = tk.Label(TwitterKeysWindow, justify = tk.LEFT, wraplength = 500, text="""Help:\n\n1. Create a twitter account if you do not already have one.\n2. Go to https://dev.twitter.com/apps and log in with your twitter credentials.\n3. Click "Create New App"\n4. Fill out the form and agree to the terms. Put in a dummy website if you don't have one you want to use.\n5. On the next page, click the "API Keys" tab along the top, then scroll all the way down until you see the section "Your Access Token". Click the button "Create My Access Token" \n6. Copy the four values into the provided space. These values are your "API Key", your "API secret", your "Access token" and your "Access token secret". """)

            # initialize labels 
            L1 = tk.Label(TwitterKeysWindow, text="api_key")
            L2 = tk.Label(TwitterKeysWindow, text="api_secret")
            L3 = tk.Label(TwitterKeysWindow, text="access_token_key")
            L4 = tk.Label(TwitterKeysWindow, text="access_token_secret")
            L0.place(x=10, y=10, width=550, height=200)
            L1.place(x=50, y=250, width=150, height=30)
            L2.place(x=50, y=300, width=150, height=30)
            L3.place(x=50, y=350, width=150, height=30)
            L4.place(x=50, y=400, width=150, height=30)

            # initialize entry fields
            global E1, E2, E3, E4
            E1 = tk.Entry(TwitterKeysWindow, bd =5)
            E2 = tk.Entry(TwitterKeysWindow, bd =5)
            E3 = tk.Entry(TwitterKeysWindow, bd =5)
            E4 = tk.Entry(TwitterKeysWindow, bd =5)
            E1.place(x=250, y=250, width=300, height=30)
            E2.place(x=250, y=300, width=300, height=30)
            E3.place(x=250, y=350, width=300, height=30)
            E4.place(x=250, y=400, width=300, height=30)

            # focus on the first entry field
            E1.focus()

            TwitterKeysWindow.update()
            self.parent.update()
            self.parent.update_idletasks() 

            # button for saving entered data and closing credentials window
            TwitterVerifyButton = tk.Button(TwitterKeysWindow, text ="Save and Close", command = self.validateTwitterAuth, bg="blue", fg="white")
            TwitterVerifyButton.place(x=250, y=450, width=200, height=30)

            # button for closing credentials window
            TwitterKeysCloseButton = tk.Button(TwitterKeysWindow, text ="Cancel", command = lambda: TwitterKeysWindow.withdraw(), bg="blue", fg="white")
            TwitterKeysCloseButton.place(x=480, y=450, width=70, height=30)

        else:
            # if window already opened then bring it to front
            TwitterKeysWindow.deiconify()



    def updateTwitterAuth(self):
        """
            Method for displaying the Twitter credentials window for the case when Twitter 
            credentials have already been entered previously, and need to be updated now.
        """

        self.count += 1

        if self.twitterAuthOpenedFlag == False:
            # set window opened
            self.twitterAuthOpenedFlag = True
            
            # initialize window
            global TwitterKeysWindow
            TwitterKeysWindow = tk.Toplevel(self)
            TwitterKeysWindow.minsize(600, 500)
            #TwitterKeysWindow.overrideredirect(True)
            TwitterKeysWindow.geometry("600x500+100+100")
            TwitterKeysWindow.title("Twitter API Authentication Details")
            TwitterKeysWindow.config(bd=5)
            L0 = tk.Label(TwitterKeysWindow, justify = tk.LEFT, wraplength = 500, text="""Help:\n\n1. Create a twitter account if you do not already have one.\n2. Go to https://dev.twitter.com/apps and log in with your twitter credentials.\n3. Click "Create New App"\n4. Fill out the form and agree to the terms. Put in a dummy website if you don't have one you want to use.\n5. On the next page, click the "API Keys" tab along the top, then scroll all the way down until you see the section "Your Access Token". Click the button "Create My Access Token" \n6. Copy the four values into the provided space. These values are your "API Key", your "API secret", your "Access token" and your "Access token secret". """)

            # initialize labels
            L1 = tk.Label(TwitterKeysWindow, text="api_key")
            L2 = tk.Label(TwitterKeysWindow, text="api_secret")
            L3 = tk.Label(TwitterKeysWindow, text="access_token_key")
            L4 = tk.Label(TwitterKeysWindow, text="access_token_secret")
            L0.place(x=10, y=10, width=550, height=200)
            L1.place(x=50, y=250, width=150, height=30)
            L2.place(x=50, y=300, width=150, height=30)
            L3.place(x=50, y=350, width=150, height=30)
            L4.place(x=50, y=400, width=150, height=30)

            # initialize entry fields
            global E1, E2, E3, E4
            E1 = tk.Entry(TwitterKeysWindow, bd =5)
            E2 = tk.Entry(TwitterKeysWindow, bd =5)
            E3 = tk.Entry(TwitterKeysWindow, bd =5)
            E4 = tk.Entry(TwitterKeysWindow, bd =5)
            E1.place(x=250, y=250, width=300, height=30)
            E2.place(x=250, y=300, width=300, height=30)
            E3.place(x=250, y=350, width=300, height=30)
            E4.place(x=250, y=400, width=300, height=30)

            # pre-populate entry fields with stored Twitter credentials
            with open("Twitter_API_Keys", "r") as twitter_keys_file:
                twitter_keys = twitter_keys_file.read().split("|")
                print(twitter_keys)
                E1.insert(0, twitter_keys[0])
                E2.insert(0, twitter_keys[1])
                E3.insert(0, twitter_keys[2])
                E4.insert(0, twitter_keys[3])

            # focus on the first entry field
            E1.focus()
            
            TwitterKeysWindow.update()
            self.parent.update()
            self.parent.update_idletasks() 
            
            # button for updating data 
            TwitterVerifyButton = tk.Button(TwitterKeysWindow, text ="Update and Close", command = self.validateTwitterAuth, bg="blue", fg="white")
            TwitterVerifyButton.place(x=250, y=450, width=200, height=30)

            # button for closing window# if window already opened then bring it to front
            TwitterKeysCloseButton = tk.Button(TwitterKeysWindow, text ="Cancel", command = lambda: TwitterKeysWindow.withdraw(), bg="blue", fg="white")
            TwitterKeysCloseButton.place(x=480, y=450, width=70, height=30)

        else:
            # if window already opened then bring it to front
            TwitterKeysWindow.deiconify()        



    def validateTwitterAuth(self):
        """
            Method for validating the entered Twitter credentials.
        """

        # get data from the entry fields
        E1_text = E1.get()
        E2_text = E2.get()
        E3_text = E3.get()
        E4_text = E4.get()
        
        # validate not null
        if (E1_text == "" or E2_text == "" or E3_text == "" or E4_text == ""):
            messagebox.showerror("ERROR", "Please fill all the fields", parent = TwitterKeysWindow)

        else:
            E1_text = E1.get()
            E2_text = E2.get()
            E3_text = E3.get()
            E4_text = E4.get()
            # store credentials in local file
            with open( self.TwitterKeysFile, "w" ) as twitter_keys_file:
                twitter_keys_file.write(E1_text + "|" + E2_text + "|" + E3_text + "|" + E4_text)
                
            self.twitterAuthOpenedFlag = False
            self.twitterAuthCompletedFlag = True

            # write meta-data to config file
            if os.path.isfile(self.ConfigFile):
                cfg = {}
                with open('config.json', 'r') as f:
                    cfg = json.load(f)
                cfg['twitterAuthCompletedFlag'] = True
                st = datetime.datetime.fromtimestamp(time.time()).strftime('%d-%m-%Y %H:%M:%S')
                cfg['twitterAuthLastUpdated'] = st
                with open('config.json', 'w') as f:
                    json.dump(cfg, f)

            else:    
                cfg = {}
                cfg['twitterAuthCompletedFlag'] = True
                st = datetime.datetime.fromtimestamp(time.time()).strftime('%d-%m-%Y %H:%M:%S')
                cfg['twitterAuthLastUpdated'] = st
                with open('config.json', 'w') as f:
                    json.dump(cfg, f)

            self.initUI()
            TwitterKeysWindow.destroy()



    

def main():
    """
        The main function. 
        This function sets up the root Tkinter window.
    """

    # initialize root frame and run the app
    global root
    root = tk.Tk()
    root.geometry("800x400+100+100")
    app = TwitterBot(root)
    root.mainloop()  


if __name__ == '__main__':
    main() 