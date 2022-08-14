import json, sys
import os,subprocess
from os.path import join
from os import system
import time

class Controle:
    data ={}
    global target_folders 
    global file_types
  

    target_folders = [ "materials", "models", "particles", "scenes","sound","resource" ]
    ext = ["vmt", "vtf", "mdl", "phy", "vtx", "vvd", "pcf", "vcd","wav","mp3","res"]
    file_types = ["vmt", "vtf", "mdl", "phy", "vtx", "vvd", "pcf", "vcd","wav","mp3","res"]

    
    def menu(self):
        txt = """
        P2Multichunker: An easy tool to pack your mod assets into proper subdivided vpk's.

        ==INSTRUCTIONS==

        a)-Place the executable under your mod directory where the 'materials','models',
        'sounds' etc.. folders are located.
        b)-Set your vpk path (option 1), which is normally located by default under:
            Windows 64bits C:\Program Files (x86)\Steam\steamapps\common\<GAME>\\bin
            Windows 32bits C:\Program Files\Steam\steamapps\common\<GAME>\\bin
        c)-Execute P2Multichunker (option 2) and wait untill the process is finished.

        Option 3: Just generates the responsefile, a txt file containing a list of all your
        non vpk packed assets.
        
        Option 4: Changes the prefix your generated vpk files will have, the default is "pak01".

        Option 5: Manages the extensions that will be scanned for inclusion in your responsefile.
        (For easy problems handling this is reseted everytime you open the program)

        OPTIONS
            1-VPK.exe path
            2-Execute P2Multichunker
            3-Generate only Responsefile
            4-Change .vpk file prefix.
            5-Manage extensions
            6-EXIT
        ENTER A NUMBER: 
        """
        opcao = int(input(txt))
        return opcao
    
    def main(self):
        system('cls')
        opcoes = {1:self.opcao1,2:self.p2_multichunk,3:self.createResponsefile,4:self.changeprefix,5:self.submenu_choices}
        while True:
            try:
                opcao = self.menu()
            except ValueError:
                system('cls')
                print("INPUT INVALID \n")
                opcao = self.menu()
                
            if opcao in opcoes:
                opcoes[opcao]()
            else:
                if opcao == 6:
                    break
                else:
                    print("Opção inválida")
                    
    def submenu_title(self):
        txt ="""
        Choose an option to either ADD or REMOVE files that 
        the program will scan to include in your responsefile.
        ---------------------------------------------------------------
        MATERIALS |MODELS   |PARTICLES |SCENES  |SOUNDS  |CONFIG. FILES
        ---------------------------------------------------------------
        0).vmt    |2).mdl   |6).pcf    |7).vcd  |8).wav  |10).res
        1).vtf    |3).phy   |          |        |9).mp3  | 
                  |4).vtx   |          |        |        | 
                  |5).vvd   |          |        |        |
        ---------------------------------------------------------------
                                    CONFIGS
        ---------------------------------------------------------------
        11) RESET SEARCH PARAMETERS
        12) RETURN

        SELECT OPTION: 
        """
        print("CURRENT SEARCH PARAMETERS")
        print(file_types)
        opcao = int(input(txt))
        return opcao
        
    #Handles files include in the responsefile/vpk
    def submenu_choices(self):
        system('cls')
        while True:
            try:
                opcao = self.submenu_title()
            except ValueError:
                system('cls')
                print("INPUT INVALID \n")
                opcao = controle.submenu_choices()
                
            if opcao > 12:
                print("invalid option \n")
                self.submenu_choices()
            else:
                typec = self.switch(opcao)   
                if typec in self.ext:
                    if typec in file_types:
                        system('cls')
                        file_types.remove(typec)
                        print ("\n."+typec +" was REMOVED from the search \n")     
                    else:
                        system('cls')
                        file_types.append(typec)
                        print ("\n."+typec +" was ADDED to the search \n")
                        
                if opcao == 11 and len(file_types) < 11:
                    file_types.clear()
                    for x in range(0,10):
                        file_types.append(self.switch(x))
                    print ("RESET completed")
                    self.submenu_choices()
                if opcao == 12:
                    controle.main()
                
    def switch(self,op):
        switcher ={
            0:"vmt", 1:"vtf", 2:"mdl", 
            3:"phy", 4:"vtx", 5:"vvd", 
            6:"pcf", 7:"vcd", 8:"wav",
            9:"mp3", 10:"res",
        }
        return switcher.get(op)

    #Handles VPK path change
    def opcao1(self):
        system('cls')
        print("Your current Path is: ")
        print(self.get_path()+"\n")
        choice = input("Do you wish to update y/n?: ")
        if choice == 'y' or choice == 'Y':
            controle.data_insert("vpk_path","")
            txt = """Enter VPK path:"""
            vpk_path = input(txt)
            isFile = os.path.isdir(vpk_path)
            if isFile == True:
                vpk_path = vpk_path.replace('\\','\\')
                vpk_path = vpk_path+'\\vpk.exe'
                print (vpk_path)
                controle.data_insert("vpk_path",vpk_path)
                controle.data_check("vpk_path")
            else:
                print("\n")
                print("VPK.exe not found on: "+vpk_path)
                print("Please check for spelling errors or insert a vaild directory")
                print("EXAMPLE: C:\Program Files (x86)\Steam\steamapps\common\Portal 2\\bin")
                print("\n")
                controle.opcao1()
        else:
            controle.main()
            
    #Inserts data into VPK    
    def data_insert(self,type,path):
        controle.data[type] = path
        with open('data.json','w') as outfile:
            json.dump( controle.data,outfile)

    #Checks if the file still exits and get data from it       
    def data_check(self,type):
        with open('data.json') as json_file:
            controle.data = json.load(json_file)
            text = controle.data[type]
            return text
    
    def get_path(self):
        return str(controle.data_check("vpk_path"))

    def get_prefix(self):    
        return str(controle.data_check("vpk_prefix"))

    #Initial check for files    
    def startupCheck(self):

        if os.path.exists('data.json'):
            try:
                print("Startup Check: [INITIATING]")
                time.sleep(1)
                print("Current VPK Path: " + self.get_path())
                print("Current VPK Prefix: " + self.get_prefix())
                print("Startup Check: [OK]")
                time.sleep(2)
                controle.main()
            except (ValueError,KeyError):
                print("Startup Check: [FAIL]")
                time.sleep(1)
                print("CORRUPT SAVE FILE, RESTARTING... \n")
                os.remove('data.json')
                time.sleep(2)
                controle.startupCheck()
                
        else:
            print("Startup Check: [GENERATING FILE NEEDED]")
            time.sleep(2)
            controle.data_insert("vpk_path","C:\\Program Files (x86)\\Steam\\steamapps\\common\\Portal 2\\bin\\vpk.exe")
            controle.data_insert("vpk_prefix","pak01")
            print("Current VPK Path: " + self.get_path())
            print("Current VPK Prefix: " + self.get_prefix())
            time.sleep(2)
            print("Startup Check: [OK]")
            time.sleep(1)
            controle.main()

    #Create Responsefile, as a loose file or to be used in the creation.
    def createResponsefile(self):
        system('cls')
        print("GENERATING: responsefile.txt")
        response_path = join(os.getcwd(),"responsefile.txt")
        out = open(response_path,'w')
        len_cd = len(os.getcwd()) + 1
        for user_folder in target_folders:
            for root, dirs, files in os.walk(join(os.getcwd(),user_folder)):
                    for file in files:
                            if len(file_types) and file.rsplit(".")[-1] in file_types:
                                    out.write(os.path.join(root[len_cd:].replace("/","\\"),file) + "\n")
        out.close()
        print("DONE")

    #Handles the prefix change that will be used in the generated VPK files
    def changeprefix(self):
        system('cls')
        print("Your current prefix is: ")
        print(self.get_prefix()+"\n")
        choice = input("Do you wish to update y/n?: ")
        if choice == 'y' or choice == 'Y':
            txt = """Enter VPK prefix:"""
            vpk_prefix = input(txt)
            if vpk_prefix is not int or float:
                controle.data_insert("vpk_prefix",vpk_prefix)
                controle.data_check("vpk_prefix")
            else:
                print("\n")
                print( vpk_prefix + " is not a valid prefix")
                print("Please check for spelling errors or insert a vaild prefix")
                print("\n")
                controle.changeprefix()
         #else:
             #controle.main()

    #GENERATES VPKs
    def p2_multichunk(self):
        system('cls')
        path = controle.data_check("vpk_path")
        prefix = controle.data_check("vpk_prefix")
        vpk_path = str(path)
        vpk_prefix = str(prefix)
        
        system('cls')
        print("CURRENT SEARCH PARAMETERS")
        print(file_types)
        controle.createResponsefile()
        print("Current VPK Path: " + vpk_path)
        print("Current VPK Prefix: " + vpk_prefix)
        print("\n")

        #This section generates the batch file and executes (for some reason I could only execute the process like this)
        title_text = 'ECHO !#!#!#!#!===== GENERATING VPK FILES DO NOT CLOSE THIS WINDOW UNTIL ITS DONE =====!#!#!#!#! \n'
        
        directory = join(os.getcwd())
        with open(os.path.join(directory, 'packing.bat'), 'w') as OPATH:
            OPATH.writelines(['@ECHO OFF \n',title_text,'"'+vpk_path,'"'+' -M a '+vpk_prefix+' @responsefile.txt \n','pause'])
               
        response_p = join(os.getcwd(),"packing.bat")
        subprocess.call([response_p])
        os.remove("packing.bat")
        os.remove("responsefile.txt")
   

controle = Controle()
controle.startupCheck()
