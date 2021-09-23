import json, sys
from re import S
import os,subprocess
from os.path import join
from os import strerror, system
from typing import Match


class Controle:
    data ={}
    global target_folders 
    global file_types
  

    target_folders = [ "materials", "models", "particles", "scenes","sound","resource" ]
    ext = ["vmt", "vtf", "mdl", "phy", "vtx", "vvd", "pcf", "vcd","wav","mp3","res"]
    file_types = ["vmt", "vtf", "mdl", "phy", "vtx", "vvd", "pcf", "vcd","wav","mp3","res"]
    def submenu_title(self):
        txt ="""CURRENT SEARCH PARAMETERS.
        
        Choose an option to either ADD or REMOVE files that 
        the program will scan to include in your .vpk file.
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
        11) RETURN
        12) RESET

        SELECT OPTION: 
        """
        print(file_types)
        print(len(file_types))
        opcao = int(input(txt))
        return opcao

    def submenu_choices(self):
        while True:
            try:
                opcao = self.submenu_title()
            except ValueError:
                print("INPUT INVALID \n")
                opcao = controle.submenu_choices()
                
            if opcao > 12:
                print("invalid option \n")
                self.submenu_choices()
            else:
                typec = self.switch(opcao)   
                if typec in self.ext:
                    if typec in file_types:
                        file_types.remove(typec)
                        print (typec +" was REMOVED from the search")
                    else:
                        file_types.append(typec)
                        print (typec +" was ADDED to the search")
                if opcao == 12 and len(file_types) == 0:
                    for x in range(0,10):
                        file_types.append(self.switch(x))
                    print ("RESET completed")
                    self.submenu_choices()
                if opcao == 11:
                    break


    def switch(self,op):
        switcher ={
            0:"vmt", 1:"vtf", 2:"mdl", 
            3:"phy", 4:"vtx", 5:"vvd", 
            6:"pcf", 7:"vcd", 8:"wav",
            9:"mp3", 10:"res",
        }
        return switcher.get(op)
        
controle = Controle()
controle.submenu_choices()
