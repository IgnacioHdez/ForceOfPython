import urllib.request as url  # Package to read urls and download images
import bs4 as bs              # Package to find information in the url
import os as os               # Package to manage directories
import DeckCreate  as DC      # My function to create decks
# ----------------Set up initial variables---------------
PreDir = 'C:\\Users\\Ignacio\\Pictures\\Cartas\\'
SaveDir = 'C:\\Users\\Ignacio\\Pictures\\Cartas\\Mazos\\'
Dirbase = "http://www.fowtcg.com/card/"
carminnum = 100       # Including
carmaxnum = 8000      # Including

print ('Downloading path set as:' + PreDir)
print('Setting url path as: '+Dirbase)
print('Downloading from index '+str(carminnum)+' to '+str(carmaxnum))
#To save used directories
DirNames = set()
# ----------------Start the loop------------------------
for i in range(carminnum, carmaxnum+1):
    print('    Start iteration for index: '+str(i))
    try:
        # ----------------Get the url data-----------------------
        Dir = Dirbase + str(i)
        print('        Fetching URL: ' + Dir)

        page = url.urlopen(Dir)
        sp = bs.BeautifulSoup(page, "lxml")
        
        #----------------Get the card name information----------
        cardname  = sp.find('div',class_='prop-item col-xs-4')
        #Name
        cardname  = cardname.find('p',class_='prop-value').string
        cardname  = cardname.replace('*','')
        cardname  = cardname +  '_' + str(i) + ".jpg" 
        print('        Card name set as: ' + cardname)
        
        #Image url
        imagedir = sp.find('div',class_='ps-gallery').figure.a.get("href")
        
        #Directory to save
        namepos=cardname.find('-')
        if namepos==-1:
            name_new = 'Extras'
            directory = PreDir+'Extras'
        else:
            name_new = ''.join([h for h in cardname[0:namepos] if not h.isdigit()])
            directory = PreDir+name_new
        print('        Card Directory set as: ' + directory)
        
        DirNames.add(name_new)
        
        #----------------Check if already exists----------------
        if os.path.exists(directory + '\\' + cardname):
            print('        Card already exists'+'\033[93m')
        else:    
            #----------------Create the directory--------------------
            if os.path.isdir(directory)==False:
                os.mkdir(directory)  
        
            #----------------Download the card----------------------
            print('        Card Downloading...')
            savedir=directory + '\\' + cardname
            url.urlretrieve(imagedir,savedir)
            print('        Card Download '+'Successful'+'\033[92m')
            
    except:
        print('        No page found for index: ' + str(i) +'\033[91m')
    print('    End iteration for index: '+str(i))
    print()

print('End Of Downloading Process')
print('')
print('Starting Deck Creation Process')

for name in DirNames:
    print('    Creating Deck For: '+name)
    DC.DeckCreator(PreDir + name+'\\', SaveDir,deck_name = 'Deck_'+name)
    
print('End Of Deck Creation Process')
