import json, sys
import os,subprocess
from os.path import join
from os import system

class Controle:
    global data
    global target_folders 
    global file_types
    
    target_folders = [ "materials", "models", "particles", "scenes","sound","resource" ]
    file_types = ["vmt", "vtf", "mdl", "phy", "vtx", "vvd", "pcf", "vcd","wav","mp3","res"]

    
    def menu(self):
        txt = """
        P2Multichunker: An easy tool to pack your mod assets into proper subdivided vpk's.

        ==INSTRUCTIONS==

        a)-Place the executable under your mod directory where the 'materials','models',
        'sounds' etc.. folders are located.
        b)-Set your vpk path (option 1), which is normally located by default under
            Windows 64bits C:\Program Files (x86)\Steam\steamapps\common\Portal 2\\bin
            Windows 32bits C:\Program Files\Steam\steamapps\common\Portal 2\\bin
        c)-Execute P2Multichunker (option 2) and wait untill the process is finished.

        Option 3: Just generates the responsefile, a txt file containing a list of all your
        non vpk packed assets.

        OPTIONS
            1-VPK.exe path
            2-Execute P2Multichunker
            3-Generate only Responsefile
            4-EXIT
        ENTER A NUMBER: 
        """
        opcao = int(input(txt))
        return opcao
    
    def main(self):
        opcoes = {1:self.opcao1,2:self.p2_multichunk,3:self.createResponsefile}
        while True:
            opcao = self.menu()
            if opcao in opcoes:
                opcoes[opcao]()
            else:
                if opcao == 4:
                    break
                else:
                    print("Opção inválida")

    def opcao1(self):
        print("Your current Path is: ")
        controle.data_check()
        print("\n")
        choice = input("Do you wish to update y/n?: ")
        if choice == 'y' or choice == 'Y':
            txt = """Enter VPK path:"""
            vpk_path = input(txt)
            isFile = os.path.isdir(vpk_path)
            if isFile == True:
                vpk_path = vpk_path.replace("\\","\\\\")
                vpk_path = '"'+vpk_path+'\\\\vpk.exe'+'"'
                controle.data_insert(vpk_path)
                controle.data_check()
            else:
                print("\n")
                print("VPK.exe not found on: "+vpk_path)
                print("Please check for spelling errors or insert a vaild directory")
                print("EXAMPLE: C:\Program Files (x86)\Steam\steamapps\common\Portal 2\\bin")
                print("\n")
                controle.opcao1()
        else:
            controle.main()
    
    def data_insert(self,path):
        data = {}
        data['vpk_path'] = path
        with open('data.json','w') as outfile:
            json.dump(data,outfile)
            
    def data_check(self):
        with open('data.json') as json_file:
            controle.data = json.load(json_file)
            text = controle.data['vpk_path']
            return text
        
    def startupCheck(self):
        if os.path.exists('data.json'):
            print("Startup Check: [OK]")
            print("Current VPK Path" + controle.data_check())
            controle.main()
        else:
            print("Startup Check: [FAIL]")
            print("Startup Check: [GENERATING FILE NEEDED]")
            controle.data_insert("C:\\\\Program Files (x86)\\\\Steam\\\\steamapps\\\\common\\\\Portal 2\\\\bin\\\\vpk.exe")
            print("Current VPK Path" + controle.data_check())
            print("Startup Check: [OK]")
            controle.main()
            
    def createResponsefile(self):
        system('cls')
        print("GNERATING: responsefile.txt")
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
        
    def p2_multichunk(self):
        system('cls')
        path = controle.data_check()
        vpk_path = str(path)
    
        controle.createResponsefile()
        
        #This section generates the batch file and executes (for some reason I could only execute the process like this)
        title_text = 'ECHO !#!#!#!#!===== GENERATING VPK FILES DO NOT CLOSE THIS WINDOW UNTIL ITS DONE =====!#!#!#!#! \n'
        directory = join(os.getcwd())
        with open(os.path.join(directory, 'packing.bat'), 'w') as OPATH:
            OPATH.writelines(['@ECHO OFF \n',title_text,vpk_path,' -M a pak01 @responsefile.txt \n','pause'])
               
        response_p = join(os.getcwd(),"packing.bat")
        subprocess.call([response_p])
        os.remove("packing.bat")
        os.remove("responsefile.txt")
   

controle = Controle()
controle.startupCheck()
