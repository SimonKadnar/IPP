import sys
import xml.etree.ElementTree as ET

class node:
    def __init__(self, opcode):
        self.prev = None
        self.next = None

        self.opcode = opcode
        self.order = None

        self.arg1_type = None
        self.arg1_value = None
        
        self.arg2_type = None
        self.arg2_value = None
       
        self.arg3_type = None
        self.arg3_value = None

class List:
    def __init__(self):
        self.head = None
		
    def insert(self, opcode, order):    #vlozi novy prvok na zaciatok linkedlistu
        new_node = node(opcode)
        new_node.order = order
        new_node.next = self.head
        if self.head is not None:
            self.head.prev = new_node
        self.head = new_node

    def arg1(self, arg1_type, arg1_value):  #vlozi typ a hodnotu do argumentu
            self.head.arg1_type = arg1_type
            self.head.arg1_value = arg1_value

    def arg2(self, arg2_type, arg2_value):
            self.head.arg2_type = arg2_type
            self.head.arg2_value = arg2_value
    
    def arg3(self, arg3_type, arg3_value):
            self.head.arg3_type = arg3_type
            self.head.arg3_value = arg3_value

    def list_sort(self, dllist):    #utriedi list od najmensieho ordru po najvedsi
        arr = []        #pole pre cisla ordov na zoradenie
        i = dllist.head
        while (i is not None):
            arr.append( (int(i.order)) )
            i = i.next

        i = 0       
        while (i != len(arr) ): 
            j = 0
            while (j != len(arr) ):
                if(arr[i] == arr[j] and i != j):    #kontrola zda nebolo pouzitych viac rovnakych ordrov
                    err32()
                j = j + 1
            i = i + 1

        arr = sorted(arr)
        j = len(arr)-1

        new_dllist = List()     #novy list pre zoradene ordre
        i = dllist.head

        while i is not None:    #vkladanie zoradenych hodnot do noveho pola
            if( j < 0):
                break
            if (arr[j] == (int(i.order)) ):
                new_dllist.insert(i.opcode,i.order)
                new_dllist.arg1(i.arg1_type,i.arg1_value)
                new_dllist.arg2(i.arg2_type,i.arg2_value)
                new_dllist.arg3(i.arg3_type,i.arg3_value)
                j = j-1
                i = dllist.head 
            else:
                i = i.next
        return new_dllist

    def list_print(self, node):     #ladiaca funckia na vypis instrukcii a jej argumentov
        print("--------------------list_print--------------------")
        while (node is not None):
            print("\n OPCODE : "+node.opcode)
            print(" ORDER : "+node.order)
            if (node.arg1_type):
                print("   TYPE :"+node.arg1_type)
                print("   VALUE :"+node.arg1_value)
            if (node.arg2_type):
                print("   TYPE :"+node.arg2_type)
                print("   VALUE :"+node.arg2_value)
            if (node.arg3_type):
                print("   TYPE :"+node.arg3_type)
                print("   VALUE :"+node.arg3_value)
            last = node
            node = node.next
        print("--------------------list_print--------------------")

    def list_find(self,order):   #najdenie instrukcie v poly instrukcii podla cisla ordru
        i = self.head
        while (i is not None):
            if( (int(i.order)) == (int(order)) ):
                return i
            i = i.next
        return None       

    def find_label(self,label): #najdenie navestia v liste instrukcii podla nazvu
        i = self.head
        while(i != None):
            if( i.arg1_value == label and i.opcode == "LABEL"):
                return i        
            i = i.next
        err52()

class variable:
    def __init__(self, var_name):
        self.prev = None
        self.next = None

        self.var_name = var_name
        self.var_type = None 
        self.var_value = None
        self.var_frame = "LF"  

class Var_list:
    def __init__(self):
        self.head = None
    
    def var_insert(self, var_name):     # vlozenie novej premennej do listu inicializovanych premennych (priradi sa jej frame, meno)

        if(not(var_name.find('GF@'))):  #priradenie framu podla nazvu premennej
            var_frame = "GF"
        elif(not(var_name.find('LF@'))):
            var_frame = "LF"
        else:
            var_frame = "TF"

        new_variable = variable(var_name)
        new_variable.var_frame = var_frame
        new_variable.next = self.head
        if self.head is not None:
            self.head.prev = new_variable
        self.head = new_variable

    def variable_find(self, var_name):  #najdenie premmnej v liste premennych v pripade ze nema ramec povazuje sa tato premenna ako neinicializovana
        i = self.head
        while (i is not None):
            if( i.var_name == var_name):
                if(i.var_frame != "NO"):
                    return i
                else:
                    err54()
            i = i.next
        return None

    def variable_find_NO(self, var_name):   #najdenie premmnej v liste premennych
        i = self.head
        while (i is not None):
            if( i.var_name == var_name):
                return i
            i = i.next
        return None

    def variable_find_err(self, var_name,framy):  #najdenie premmnej v liste premennych v pripade ze nema ramec povazuje sa tato premenna ako neinicializovana 
                                            #+ osetrenie chyb s neexistujucim ramcom
        i = self.head
        while (i is not None):
            if( i.var_name == var_name ):
                if( i.var_frame == "NO"):
                     err54()
                else:
                    return i
            i = i.next
       
        if(not(var_name.find("GF@"))):
            err54()
        elif(not(var_name.find("TF@"))):
            find_frame_TF(framy)
        elif(not(var_name.find("LF@"))):
            find_frame_LF(framy)
        else:
            err55()

    def variable_find_err_miss(self, var_name,framy): #najdenie premmnej v liste premennych v pripade ze nema ramec povazuje sa tato premenna ako neinicializovana 
                                                #+ osetrenie chyb s neexistujucim ramcom alebo ak v sebe nema yiadnu hodnotu
        i = self.head
        while (i is not None):
            if( i.var_name == var_name ):
                if( i.var_frame == "NO"):
                    err54()
                    return
                else:
                    if( not(i.var_value != None) ):
                        err56()
                        return
                    else:
                        return i
            i = i.next
        if(not(var_name.find("GF@"))):
            err54()
        elif(not(var_name.find("TF@"))):
            find_frame_TF(framy)
        elif(not(var_name.find("LF@"))):
            find_frame_LF(framy)
        else:
            err55()

    def variable_find_insert(self, var_name1,var_name2,TypE):   #najde premennu podla mena a nahra do nej hodnotu

        value = 0
        var_type = "int"
        if( TypE == "var" ):
            if(self.variable_find(var_name2)):
                tmp = self.variable_find(var_name2)
                value = tmp.var_value
                var_type = tmp.var_type
            else:
                if(not(var_name2.find("GF@"))):
                    err54()
                else:
                    err55()
        else:
            value = var_name2
            var_type = TypE

        i = self.head
        while (i is not None):
            if( i.var_name == var_name1 ):
                i.var_value = value
                i.var_type = var_type
                return
            i = i.next
        if(not(var_name1.find("GF@"))):
            err54()
        else:
            err55()

    def add_sub(self,i,framy):    #funkcie add, sub, mul
        tmp1 = self.variable_find_err(i.arg1_value,framy) #overenie zda dana premenna vobec existuje
        tmp1.var_type = "int"                       #zmena jej tipu podla vysledku funkcie

        if( (i.arg2_type == "var") and (i.arg3_type == "var") ):                                             #2x var
            tmp2 = self.variable_find_err_miss(i.arg2_value,framy)    #overenie zda dana premenna vobec existuje a ma v sebe hodnotu
            tmp3 = self.variable_find_err_miss(i.arg3_value,framy)    #overenie zda dana premenna vobec existuje a ma v sebe hodnotu
            type_int(tmp2.var_type)     #overenie tipu premennej
            type_int(tmp3.var_type)     #overenie tipu premennej

            if( i.opcode == "ADD"):
                tmp = int(tmp2.var_value) + int(tmp3.var_value)
                tmp1.var_value = tmp
            elif( i.opcode == "SUB"):
                tmp = int(tmp2.var_value) - int(tmp3.var_value)
                tmp1.var_value = tmp
            elif( i.opcode == "MUL"):
                tmp = int(tmp2.var_value) * int(tmp3.var_value)
                tmp1.var_value = tmp
            else:
                if( int(tmp3.var_value) == 0 ):
                    err57()
                tmp = int(int(tmp2.var_value) / int(tmp3.var_value))
                tmp1.var_value = tmp

        elif( i.arg2_type == "var" ):                           #1x var
            tmp2 = self.variable_find_err_miss(i.arg2_value,framy)
            type_int(tmp2.var_type)
            type_int(i.arg3_type)

            if( i.opcode == "ADD"):
                tmp = int(tmp2.var_value) + int(i.arg3_value)
                tmp1.var_value = tmp
            elif( i.opcode == "SUB"):
                tmp = int(tmp2.var_value) - int(i.arg3_value)
                tmp1.var_value = tmp
            elif( i.opcode == "MUL"):
                tmp = int(tmp2.var_value) * int(i.arg3_value)
                tmp1.var_value = tmp
            else:
                if( int(i.arg3_value) == 0 ):
                    err57()
                tmp = int(int(tmp2.var_value) / int(i.arg3_value))
                tmp1.var_value = tmp
        
        elif( i.arg3_type == "var" ):                               #1x var
            tmp3 = self.variable_find_err_miss(i.arg3_value,framy)
            type_int(tmp3.var_type)
            type_int(i.arg2_type)

            if( i.opcode == "ADD"):
                tmp = int(i.arg2_value) + int(tmp3.var_value)
                tmp1.var_value = tmp
            elif( i.opcode == "SUB"):
                tmp = int(i.arg2_value) - int(tmp3.var_value)
                tmp1.var_value = tmp
            elif( i.opcode == "MUL"):
                tmp = int(i.arg2_value) * int(tmp3.var_value)
                tmp1.var_value = tmp
            else:
                if( int(tmp3.var_value) == 0 ):
                    err57()
                tmp = int(int(i.arg2_value) / int(tmp3.var_value))
                tmp1.var_value = tmp

        else:                                                   #0x var
            type_int(i.arg2_type)
            type_int(i.arg3_type)

            if( i.opcode == "ADD"):
                tmp = int(i.arg2_value) + int(i.arg3_value)
                tmp1.var_value = tmp
            elif( i.opcode == "SUB"):
                tmp = int(i.arg2_value) - int(i.arg3_value)
                tmp1.var_value = tmp
            elif( i.opcode == "MUL"):
                tmp = int(i.arg2_value) * int(i.arg3_value)
                tmp1.var_value = tmp
            else:
                if( int(i.arg3_value) == 0 ):
                    err57()
                tmp = int(int(i.arg2_value) / int(i.arg3_value))
                tmp1.var_value = tmp

    def jumpif(self,i,dllist,framy):
        tmp1 = dllist.find_label(i.arg1_value)      #overenie zda dane navestie vobec existuje a ak ano vrati ukazatel nan
        if( (i.arg2_type == "var") and (i.arg3_type == "var") ):
            tmp2 =self.variable_find_err_miss(i.arg2_value,framy)     #overenie zda dana premenna vobec existuje a ma v sebe hodnotu
            tmp3 =self.variable_find_err_miss(i.arg3_value,framy)     #overenie zda dana premenna vobec existuje a ma v sebe hodnotu

            if(tmp2.var_type != tmp3.var_type):
                err53()

            if(i.opcode == "JUMPIFEQ"):
                if ( int(tmp2.var_value) == int(tmp3.var_value) ):  #ak sa rovnaju skoc na navestie
                    return tmp1     
                else:                                               #ak nie tak pokracuj dalsou instruckiou
                    return i   
            else:
                if ( int(tmp2.var_value) != int(tmp3.var_value) ):
                    return tmp1      
                else:
                    return i
        elif(i.arg2_type == "var"):
            tmp2 = self.variable_find_err_miss(i.arg2_value,framy)
            tmp3 = i.arg3_value

            if(tmp2.var_type != i.arg3_type):
                err53()

            if(i.opcode == "JUMPIFEQ"):
                if( int(tmp2.var_value) == int(tmp3) ):
                    return tmp1
                else:
                    return i
            else:
                if( int(tmp2.var_value) != int(tmp3) ):
                    return tmp1
                else:
                    return i
        elif(i.arg3_type == "var"):
            tmp3 = self.variable_find_err_miss(i.arg2_value,framy)
            tmp2 = i.arg2_value

            if(tmp3.var_type != i.arg2_type):
                err53()

            if(i.opcode == "JUMPIFEQ"):
                if ( int(tmp2) == int(tmp3.var_value) ):
                    return tmp1
                else:
                    return i
            else:
                if ( int(tmp2) != int(tmp3.var_value) ):
                    return tmp1
                else:
                    return i
        else:
            if(i.arg2_type != i.arg3_type):
                err53()

            if(i.opcode == "JUMPIFEQ"):
                if ( int(i.arg2_value) == int(i.arg3_value) ):
                    return tmp1
                else:
                    return i 
            else:
                if ( int(i.arg2_value) != int(i.arg3_value) ):
                    return tmp1
                else:
                    return i          

    def INT2CHAR(self,i,framy):
        tmp1 = self.variable_find_err(i.arg1_value,framy)
        tmp1.var_type = "string"
        if(i.arg2_type == "var"):
            tmp2 = self.variable_find_err_miss(i.arg2_value,framy)
            type_int(tmp2.var_type)
            try:
                tmp1.var_value = chr(int(tmp2.var_value))
            except:
                err58()
        else:
            type_int(i.arg2_type)
            try:
                tmp1.var_value = chr(int(i.arg2_value))
            except:
                err58()

    def STRI2INT(self,i,framy):
        tmp1 = self.variable_find_err(i.arg1_value,framy)
        tmp1.var_type = "int"
        if(i.arg2_type == "var" and i.arg3_type == "var"):
            tmp2 = self.variable_find_err_miss(i.arg2_value,framy)
            tmp3 = self.variable_find_err_miss(i.arg3_value,framy)
            type_string(tmp2.var_type)
            type_int(tmp3.var_type)

            try:
                tmp2 = tmp2.var_value[int(tmp3.var_value)]
                tmp1.var_value = ord(tmp2)
            except:
                err58()
        elif(i.arg2_type == "var"):
            tmp2 = self.variable_find_err_miss(i.arg2_value,framy)
            type_string(tmp2.var_type)
            type_int(i.arg3_type)
            try:
                tmp2 = tmp2.var_value[int(i.arg3_value)]
                tmp1.var_value = ord(tmp2)
            except:
                err58()
        elif(i.arg3_type == "var"):
            tmp3 = self.variable_find_err_miss(i.arg3_value,framy)
            type_string(i.arg2_type)
            type_int(tmp3.var_type)
            try:
                tmp2 = i.arg2_value[int(tmp3.var_value)]
                tmp1.var_value = ord(tmp2)
            except:
                err58()
        else:
            type_string(i.arg2_type)
            type_int(i.arg3_type)
            try:
                tmp2 = i.arg2_value[int(i.arg3_value)]
                tmp1.var_value = ord(tmp2)
            except:
                err58()

    def variable_print(self, variable): #ladiaci vypis
        if (self.head):
            print("--------------------variable_print--------------------")
            while (variable is not None):
                print("\n NAME  : "+variable.var_name)
                print(" FRAME : "+variable.var_frame)
                if (variable.var_value):
                    print(" VALUE : "+(str(variable.var_value)))
                if (variable.var_type):
                    print(" TYPE  : "+(str(variable.var_type)))
                variable = variable.next
            print("--------------------variable_print--------------------")
        else:
            print("HEAD = NONE")

    def STRLEN(self,i,framy):
        tmp1 = self.variable_find_err(i.arg1_value,framy)
        tmp1.var_type = "int"
        if(i.arg2_type == "var"):
            tmp2 = self.variable_find_err_miss(i.arg2_value,framy)
            tmp1.var_value = len(tmp2.var_value)
        else:
            tmp1.var_value = len(i.arg2_value)

    def GETCHAR (self,i,framy):
        tmp1 = self.variable_find_err(i.arg1_value,framy)
        tmp1.var_type = "string"

        if( (i.arg2_type == "var") and (i.arg3_type == "var") ):
            tmp2 = self.variable_find_err_miss(i.arg2_value,framy)
            tmp3 = self.variable_find_err_miss(i.arg3_value,framy)

            try:
                tmp1.var_value = tmp2.var_value[int(tmp3.var_value)]
            except:
                err58()

        elif( (i.arg2_type == "var")):
            tmp2 = self.variable_find_err_miss(i.arg2_value,framy)

            try:
                tmp1.var_value = tmp2.var_value[int(i.arg3_value)]
            except:
                err58()
        
        elif( (i.arg3_type == "var")):
            tmp3 = self.variable_find_err_miss(i.arg3_value,framy)

            try:
                tmp1.var_value = i.arg2_value[int(tmp3.var_value)]
            except:
                err58()

        else:
            try:
                tmp1.var_value = i.arg2_value[int(i.arg3_value)]
            except:
                err58()

    def CONCAT (self,i,framy):
        tmp1 = self.variable_find_err(i.arg1_value,framy)     #overenie existencie premennej
        tmp1.var_type = "string"
        if( (i.arg2_type == "var") and (i.arg3_type == "var") ):
            tmp2 = self.variable_find_err_miss(i.arg2_value,framy)    #overenie existencie premennej a skontrolovanie zda obsahuje nejaku hodnotu
            tmp3 = self.variable_find_err_miss(i.arg3_value,framy)
            if(i.opcode == "CONCAT"):
                type_string(tmp2.var_type)
                type_string(tmp3.var_type)
                tmp1.var_value = tmp2.var_value + tmp3.var_value
        elif( i.arg2_type == "var" ):
            tmp2 = self.variable_find_err_miss(i.arg2_value,framy)
            if(i.opcode == "CONCAT"):
                type_string(tmp2.var_type)
                type_string(i.arg3_type)
                tmp1.var_value = tmp2.var_value + i.arg3_value
        elif( i.arg3_type == "var" ):
            tmp3 = self.variable_find_err_miss(i.arg3_value,framy)
            if(i.opcode == "CONCAT"):
                type_string(i.arg2_type)
                type_string(tmp3.var_type)
                tmp1.var_value = i.arg2_value + tmp3.var_value
        else:
            if(i.opcode == "CONCAT"):
                type_string(i.arg2_type)
                type_string(i.arg3_type)
                tmp1.var_value = i.arg2_value + i.arg3_value

    def AND_OR(self,i,framy):
        tmp1 = self.variable_find_err(i.arg1_value,framy)
        tmp1.var_type = "bool"
        if( (i.arg2_type == "var") and (i.arg3_type == "var") ):
            tmp2 = self.variable_find_err_miss(i.arg2_value,framy)
            tmp3 = self.variable_find_err_miss(i.arg3_value,framy)
            type_bool(tmp2.var_type)
            type_bool(tmp3.var_type)

            if(i.opcode == "AND"):
                if((tmp2.var_value == "true") and (tmp3.var_value == "true")):
                    tmp1.var_value = "true"
                else:
                    tmp1.var_value = "false"
            elif(i.opcode == "OR"):
                if((tmp2.var_value == "true") or (tmp3.var_value == "true")):
                    tmp1.var_value = "true"
                else:
                    tmp1.var_value = "false"
        elif(i.arg2_type == "var"):
            tmp2 = self.variable_find_err_miss(i.arg2_value,framy)
            type_bool(tmp2.var_type)
            type_bool(i.arg3_type)

            if(i.opcode == "AND"):
                if((tmp2.var_value == "true") and (i.arg3_value == "true")):
                    tmp1.var_value = "true"
                else:
                    tmp1.var_value = "false"
            elif(i.opcode == "OR"):
                if((tmp2.var_value == "true") or (i.arg3_value == "true")):
                    tmp1.var_value = "true"
                else:
                    tmp1.var_value = "false"
        elif(i.arg3_type == "var"):
            tmp3 = self.variable_find_err_miss(i.arg2_value,framy)
            type_bool(i.arg2_type)
            type_bool(tmp3.var_type)

            if(i.opcode == "AND"):
                if((i.arg2_value == "true") and (tmp3.var_value == "true")):
                    tmp1.var_value = "true"
                else:
                    tmp1.var_value = "false"
            elif(i.opcode == "OR"):
                if((i.arg2_value == "true") or (tmp3.var_value == "true")):
                    tmp1.var_value = "true"
                else:
                    tmp1.var_value = "false"
        else:
            type_bool(i.arg2_type)
            type_bool(i.arg3_type)

            if(i.opcode == "AND"):
                if((i.arg2_value == "true") and (i.arg3_type == "true")):
                    tmp1.var_value = "true"
                else:
                    tmp1.var_value = "false"
            elif(i.opcode == "OR"):
                if((i.arg2_value == "true") or (i.arg3_type == "true")):
                    tmp1.var_value = "true"
                else:
                    tmp1.var_value = "false"

    def NOT(self,i,framy):
        tmp1 = self.variable_find_err(i.arg1_value,framy)
        tmp1.var_type = "bool"

        if(i.arg2_type == "var"):
            tmp2 = self.variable_find_err_miss(i.arg2_value,framy)
            type_bool(tmp2.var_type)
            if(tmp2.var_value == "true"):
                tmp1.var_value = "false"
            else:
                tmp1.var_value = "true"
        else:
            type_bool(i.arg2_type)
            if(i.arg2_value == "true"):
                tmp1.var_value = "false"
            else:
                tmp1.var_value = "true"

    def LT_GT(self,i,framy):
        tmp1 = self.variable_find_err(i.arg1_value,framy)
        tmp1.var_type = "bool"
        if( (i.arg2_type == "var") and (i.arg3_type == "var") ):
            tmp2 = self.variable_find_err_miss(i.arg2_value,framy)
            tmp3 = self.variable_find_err_miss(i.arg3_value,framy)
            if(tmp2.var_type != tmp3.var_type):
                err53() 
            if(i.opcode == "LT"):
                if(tmp2.var_value < tmp3.var_value):
                    tmp1.var_value = "true"
                else:
                    tmp1.var_value = "false"
            else:
                if(tmp2.var_value > tmp3.var_value):
                    tmp1.var_value = "true"
                else:
                    tmp1.var_value = "false"

        elif(i.arg2_type == "var"):
            tmp2 = self.variable_find_err_miss(i.arg2_value,framy)
            if(tmp2.var_type != i.arg3_type):
                err53() 
            if(i.opcode == "LT"):
                if(tmp2.var_value < i.arg3_value):
                    tmp1.var_value = "true"
                else:
                    tmp1.var_value = "false"
            else:
                if(tmp2.var_value > i.arg3_value):
                    tmp1.var_value = "true"
                else:
                    tmp1.var_value = "false"
        
        elif(i.arg3_type == "var"):
            tmp3 = self.variable_find_err_miss(i.arg3_value,framy)
            if(i.arg2_type != tmp3.var_type):
                err53() 
            if(i.opcode == "LT"):
                if(i.arg2_type < tmp3.var_value):
                    tmp1.var_value = "true"
                else:
                    tmp1.var_value = "false"
            else:
                if(i.arg2_type > tmp3.var_value):
                    tmp1.var_value = "true"
                else:
                    tmp1.var_value = "false"
        else:
            if(i.arg2_type != i.arg3_type):
                err53() 
            if(i.opcode == "LT"):
                if(i.arg2_type < i.arg3_type):
                    tmp1.var_value = "true"
                else:
                    tmp1.var_value = "false"
            else:
                if(i.arg2_type > i.arg3_type):
                    tmp1.var_value = "true"
                else:
                    tmp1.var_value = "false"
            
    def EQ(self,i,framy):
        tmp1 = self.variable_find_err(i.arg1_value,framy)
        tmp1.var_type = "bool"
        if( (i.arg2_type == "var") and (i.arg3_type == "var") ):
            tmp2 = self.variable_find_err_miss(i.arg2_value,framy)
            tmp3 = self.variable_find_err_miss(i.arg3_value,framy)
            if(not((tmp2.var_type == tmp3.var_type) or (tmp2.var_type =="nil") or (tmp3.var_type =="nil"))):
                err53() 
            if(tmp2.var_value == tmp3.var_value):
                tmp1.var_value = "true"
            else:
                tmp1.var_value = "false"
        elif(i.arg2_type == "var"):
            tmp2 = self.variable_find_err_miss(i.arg2_value,framy)
            if(not((tmp2.var_type == i.arg3_type) or (tmp2.var_type =="nil") or (i.arg3_type =="nil"))):
                err53() 
            if(tmp2.var_value == i.arg3_value):
                tmp1.var_value = "true"
            else:
                tmp1.var_value = "false"
        elif(i.arg3_type == "var"):
            tmp3 = self.variable_find_err_miss(i.arg3_value,framy)
            if(not((i.arg2_type == tmp3.var_type) or (i.arg2_type =="nil") or (tmp3.var_type =="nil"))):
                err53() 
            if(i.arg2_value == tmp3.var_value):
                tmp1.var_value = "true"
            else:
                tmp1.var_value = "false"
        else:
            if(not((i.arg2_type == i.arg3_type) or (i.arg2_type =="nil") or (i.arg3_type =="nil"))):
                err53() 
            if(i.arg2_value == i.arg3_value):
                tmp1.var_value = "true"
            else:
                tmp1.var_value = "false"

    def CALL(self,i,dllist,pole,framy):
        label = dllist.find_label(i.arg1_value)
        pole.append(i)      #ulozi aktualnu poziciu do listu pre call a return aby sa vedel vratit po retunre
        pole.append("CALL")
        return label

    def RETURN(self,pole,framy):
        
        pole.pop()      #popne call
        call = pole.pop()   #popne poziciu callu
        return call

    def PUSHS_POPS(self,i,push_var,framy):

        if(i.arg1_type == "var"):
            if(i.opcode == "PUSHS"):    #ak sa pushuje obsah premennej
                tmp = self.variable_find_err_miss(i.arg1_value,framy) #kontrola zda premenna existuje a obsahuje hodnotu ktora sa ma pushnut
                push_var.append(tmp.var_value)  #pushe hodnotu
                push_var.append(tmp.var_type)   #pushe typ
            else:
                tmp = self.variable_find_err(i.arg1_value,framy)  #kontrola zda premenna existuje do ktorej sa ma hodnota popnut
                try:
                    tmp.var_type = push_var.pop()   
                    tmp.var_value = push_var.pop()
                except:
                    err56()
        else:
            if(i.opcode == "PUSHS"):
                push_var.append(i.arg1_value)   #pushe hodnotu
                push_var.append(i.arg1_type)    #pushe typ

    def CREATEFRAME_PUSHFRAME_POPFRAME(self,i,framy):

        if(i.opcode == "CREATEFRAME"):
            framy.append("CREATEFRAME") #pushnutie createframu aby sa vedelo ze lokalne a docasne ramce sa mozu vytvarat

        elif(i.opcode == "PUSHFRAME"):

            j = len(framy)-1
            framy.append("PUSHFRAME")
            while(j != -1 ):
                if(framy[j] == "CREATEFRAME"):  #pushovanie premennych LF a TF kde LF sa zmeni na ziaden ramec a teda tuto premennu nemozno pouzit
                    break
                tmp = self.variable_find_NO(framy[j])
                if(tmp.var_frame == "TF"):
                    tmp.var_frame = "LF"
                    framy.append(framy[j])
                elif(tmp.var_frame == "LF"):
                    tmp.var_frame = "NO"
                    framy.append(framy[j])
                j = j-1
                
            if( j == -1 or framy[j] == "PUSHFRAME"):    #v pripdane ze neexistuje crateframe tak nemozno pushovat
                err55()

        elif(i.opcode == "POPFRAME"):
            if(len(framy) == 0):
                    err55()

            j = len(framy)-1
            while(j != -1 ):
                if(framy[j] == "PUSHFRAME"): #popovanie a obnovovanie ramcov ktore boli oznaacene ako neexistujuce
                    framy.pop()
                    break
                tmp = self.variable_find_NO(framy[j])   #najdenie premennych aj tych co nemaju ramec podla mena 
                tmp.var_frame
                if(tmp.var_frame == "LF"):
                    tmp.var_frame = "TF"
                    framy.pop()
                elif(tmp.var_frame == "NO"):
                    tmp.var_frame = "LF"
                    framy.pop()
                elif(tmp.var_frame == "TF"): 
                    tmp.var_frame = "NO"
                    framy.pop()
                j = j-1
                if( j == -1 or framy[j] == "CREATEFRAME"):
                    err55()

    def READ(self,i,input_for_read,framy):
        tmp1 = self.variable_find_err(i.arg1_value,framy)
            
        try:
            if( i.arg2_value == "bool" ):
                tmp1.var_value = (input_for_read.pop(0)).lower()
                tmp1.var_type = i.arg2_value
            else:
                tmp1.var_value = input_for_read.pop(0)
                tmp1.var_type = i.arg2_value
        except:     #ak ziadna hodnota neni na vstupe tak sa nastavi na nil
            tmp1.var_value = "nil"
            tmp1.var_type = "nil"

    def SETCHAR(self,i,framy):
        tmp1 = self.variable_find_err(i.arg1_value,framy) #kontrola existencie
        if(tmp1.var_value == None):
            err58()
        tmp1.var_type = "string"

        if( (i.arg2_type == "var") and (i.arg3_type == "var") ):
            tmp2 = self.variable_find_err_miss(i.arg2_value,framy)    #kontrola existencie a hodnotz v premennej
            tmp3 = self.variable_find_err_miss(i.arg3_value,framy)
            type_int(tmp2.var_type)     #kontrola tipu premennej
            type_string(tmp3.var_type)

            if( len(tmp1.var_value)-1 < int(tmp2.var_value) ):
                err58()
            
            tmp1.var_value = tmp1.var_value[:int(tmp2.var_value)]+tmp3.var_value[0]+tmp1.var_value[int(tmp2.var_value)+1:]
        
        elif(i.arg2_type == "var"):
            tmp2 = self.variable_find_err_miss(i.arg2_value,framy)
            type_int(tmp2.var_type)
            type_string(i.arg3_type)

            if( len(tmp1.var_value)-1 < int(tmp2.var_value) ):
                err58()
            
            tmp1.var_value = tmp1.var_value[:int(tmp2.var_value)]+i.arg3_type[0]+tmp1.var_value[int(tmp2.var_value)+1:]
        
        elif(i.arg3_type == "var"):
            tmp3 = self.variable_find_err_miss(i.arg3_value,framy)
            type_int(i.arg2_type)
            type_string(tmp3.var_type)

            if( len(tmp1.var_value)-1 < int(i.arg2_value) ):
                err58()

            tmp1.var_value = tmp1.var_value[:int(i.arg2_value)]+tmp3.var_value[0]+tmp1.var_value[int(i.arg2_value)+1:]
        
        else:
            type_int(i.arg2_type)
            type_string(i.arg3_type)

            if( len(tmp1.var_value)-1 < int(i.arg2_value) ):
                err58()
                
            tmp1.var_value = tmp1.var_value[:int(i.arg2_value)]+i.arg3_value[0]+tmp1.var_value[int(i.arg2_value)+1:]

def list_fill(source,dllist,var_list):
    
    sourcefile = source.lstrip('source=')  #ziskanie vstupneho suboru

    try:                                        #otestovanie chybnosti xml vstupu
        tree = ET.parse(sourcefile)             #nacitanie do stromu
        root = tree.getroot()                   #nacitanie do korena
    except:
        err31()
            
    try:  
        for child in root:
            if ( (int(child.attrib['order'])) <= 0):    #instrukcia ma poradove cislo mensie ako 1
                err32()
            guard1 = 0      #guard zabepecuje ze nebude pouzity rovnaky nazov atributu viac krat v jednej instrukcii
            guard2 = 0
            guard3 = 0  

            if(child.tag != "instruction"):
                err32() 

            dllist.insert(child.attrib['opcode'].upper(),child.attrib['order'])
            for leaf in child:

                if( child.attrib['opcode'].upper() == "LABEL" ):
                    if( not(var_list.variable_find(leaf.text)) ):
                        var_list.var_insert(leaf.text)
                        var_list.head.var_frame = "label"
                    else:
                        err52()
                
                if ((leaf.tag == "arg1") and guard1 == 0):
                    if( leaf.attrib['type'] == "int" ):
                        check_int(leaf.text)
                    dllist.arg1(leaf.attrib['type'],leaf.text)
                    guard1 = 1

                elif((leaf.tag == "arg2") and guard2 == 0):
                    if( leaf.attrib['type'] == "int" ):
                        check_int(leaf.text)
                    dllist.arg2(leaf.attrib['type'],leaf.text)
                    guard2 = 1

                elif((leaf.tag == "arg3") and guard3 == 0):
                    if( leaf.attrib['type'] == "int" ):
                        check_int(leaf.text)
                    dllist.arg3(leaf.attrib['type'],leaf.text)
                    guard3 = 1

                else:       #nazov argumentu alebo jeho cislo je chybne
                    err32()

            if( guard1 == 0 and (guard2 == 1 or  guard3 == 1) ):    #overenie zda nema zle cisla argumentov
                err32()
            if( guard2 == 0 and  guard3 == 1 ):
                err32()
            
            check_num_arg(child.attrib['opcode'].upper(),guard1,guard2,guard3)  #overenie poctu argumentov pre danu instrukciu
    except:
        err32()

def help():
    print("help                      : python3.8 interpret.py --help")
    print("source file               : python3.8 interpret.py source=\"sourcefile\"")
    print("source file and input file: python3.8 interpret.py source=\"sourcefile\" input=\"inputfile\"")

def check_num_arg(n,g1,g2,g3):
    #n --> name g1 --> guard1 g2 --> guard2 g3 --> guard3 
    if ( n == "CREATEFRAME" or n == "PUSHFRAME" or n == "POPFRAME" or n == "RETURN" or n == "BREAK" ):
        if(g1 == 1 or g2 == 1 or g3 == 1):
            err32()
    elif( n == "DEFVAR" or n == "CALL" or n == "PUSHS" or n == "POPS" or n == "WRITE" or n == "LABEL" or n == "JUMP" or n == "EXIT" or n == "DPRINT"):
        if(g1 == 0 or g2 == 1 or g3 == 1):
            err32()
    elif( n == "MOVE" or n == "INT2CHAR" or n == "STRLEN" or n == "TYPE" or n == "READ"):
        if(g1 == 0 or g2 == 0 or g3 == 1):
            err32()
    else:
        if(g1 == 0 or g2 == 0 or g3 == 0):
            err32()

def print_string(string):
    i = 0
    while( i != len(string) ): #printuje pokial neni na konci stringu
        if(string[i] == "\\"):  #ak pride lomitko ocakavame 3 cisla
            i = i + 3
            j = 0
            num_to_char = 0
            while( j != 3):
                num_to_char = num_to_char + int(string[i]) * 10**j
                i = i - 1
                j = j + 1
            print(chr(num_to_char),end="")
            i = i + 3
        else:
            print(string[i],end="")
        i = i + 1

def find_frame_TF(framy):
        j = len(framy)-1
        while(j > -1 ):
            if(framy[j] == "CREATEFRAME"):
                err54()
            if(framy[j] == "PUSHFRAME"):
                err55()
            j = j-1
        err55()

def find_frame_LF(framy):
    j = len(framy)-1
    while(j > -1 ):
        if(framy[j] == "CREATEFRAME"):
            err55()
        if(framy[j] == "PUSHFRAME"):
            err54()
        j = j-1
    err55()


def check_int(value):   #overovacia funkcia zda hodnota tipu int je skutocne tipu int
    if(value == None):
        err56()
    i = 0
    while( i != len(value)-1):
        if( not((value[i] >= '0' and value[i] <= '9') or value[i] == '-') ):
            err32()
        i = i + 1

def type_int(var_type): #overenie tipu int
    if(var_type != "int"):
        err53()

def type_string(var_type):  #overenie tipu string
    if(var_type != "string"):
        err53()

def type_bool(var_type):    #overenie tipu bool
    if(var_type != "bool"):
        err53()

def err31():
    exit(31) 

def err32():
    exit(32) 

def err52():
    exit(52) 

def err53():
    exit(53) 

def err54():
    exit(54) 

def err55():
    exit(55)  

def err56():
    exit(56) 

def err57():
    exit(57)  

def err58():
    exit(58)  

def main():

    if(sys.argv[1]):

        input_for_read = []
        string1 = sys.argv[1]
        string2 = None
        sou = "NO"
        inp = "NO"
        if(len(sys.argv) == 3):
            string2 = sys.argv[2]
            if(not(string1.find('--source='))):
                sou = string1
            elif(not(string2.find('--source='))):
                sou = string2

            if(not(string1.find('--input='))):
                inp = string1
            elif(not(string2.find('--input='))):
                inp = string2
        else:
            sou = string1

        if(sys.argv[1] == "--help"):
            help()    
            return    

        if(not(inp.find('--input='))):

            file = inp.replace("--input=","")
            f = open(file, "r")

            tmp = "aa"
            while(tmp):
                tmp = f.readline()
                if(not(tmp)):
                    break
                input_for_read.append(tmp.replace("\n",""))
            
        if(not(sou.find('--source='))):

            sou = sou.replace("--source=","")

            pole = []
            pole.append("START")
            push_var = []                   #stack pre pushovanie premnnych
            framy = []                      #stack pre framy

            dllist = List()                 #list instruckcii
            var_list = Var_list()           #list premennych
            list_fill(sou,dllist,var_list)          #naplni list instruckciami
            dllist = dllist.list_sort(dllist)       #usporiada instrukcie v liste

            i = dllist.head
            while(i is not None):

                if (i.opcode == "MOVE"):
                    var_list.variable_find_insert(i.arg1_value,i.arg2_value,i.arg2_type)

                elif (i.opcode == "DEFVAR"):  
                    if( not(var_list.variable_find(i.arg1_value)) ):

                        try:
                            if(not(i.arg1_value.find('TF@'))):
                                j = len(framy)
                                while(j != -1 ):
                                    if(framy[j] == "CREATEFRAME"):
                                        break
                                    if(framy[j] == "PUSHFRAME"):
                                        err55()
                                    j = j-1
                        except:
                            err55()

                        var_list.var_insert(i.arg1_value)
                        tmp = var_list.variable_find_err(i.arg1_value,framy)
                        if(tmp.var_frame != "GF"):
                            framy.append(tmp.var_name)
                    else:
                        err52()
                elif (i.opcode == "WRITE"):
                    if(i.arg1_type != "var"):

                        if(i.arg1_value == None):   #kontrola ci dana premenna obsahuje aj nejaku hodnotu
                            err56()
                        if(i.arg1_type == "nil"):
                            print("",end="")
                        if(i.arg1_type == "int"):
                            print(i.arg1_value,end="")
                        elif(i.arg1_type == "bool"):
                            print(i.arg1_value,end="")
                        else:
                            print_string(i.arg1_value)
                    else:
                        tmp = var_list.variable_find_err_miss(i.arg1_value,framy)
                        if(tmp.var_type == "sitrng"):
                            print_string(tmp.var_value)
                        else:
                            print(tmp.var_value,end="")


                elif (i.opcode == "ADD" or i.opcode == "SUB" or i.opcode == "MUL" or i.opcode == "IDIV"):
                    var_list.add_sub(i,framy)

                elif(i.opcode == "TYPE"):
                    tmp = var_list.variable_find_err(i.arg1_value,framy)
                    if(i.arg2_type == "var"):
                        tmp1 = var_list.variable_find_err(i.arg2_value,framy)
                        tmp.var_value = tmp1.var_type
                    else:
                        tmp.var_value = i.arg2_type
                    tmp.var_type = "string"

                elif(i.opcode == "JUMP"):
                    i = dllist.find_label(i.arg1_value,framy)   

                elif(i.opcode == "JUMPIFEQ" or i.opcode == "JUMPIFNEQ"): 
                    i = var_list.jumpif(i,dllist,framy)

                elif(i.opcode == "EXIT"):
                    if(i.arg1_type == "var"):
                        tmp = var_list.variable_find_err(i.arg1_value,framy)
                        if(tmp.var_value > 0 and tmp.var_value < 50):
                            exit(tmp.var_value)
                        else:
                            err57()
                    else:
                        if(int(i.arg1_value) >= 0 and int(i.arg1_value) <= 49):
                            exit(int(i.arg1_value))
                        else:
                            err57()

                elif(i.opcode == "INT2CHAR"):
                    var_list.INT2CHAR(i,framy)
                elif(i.opcode == "SETCHAR"):
                    var_list.SETCHAR(i,framy)
                elif(i.opcode == "STRI2INT"):
                    var_list.STRI2INT(i,framy)
                elif(i.opcode == "STRLEN"):
                    var_list.STRLEN(i,framy)
                elif(i.opcode == "GETCHAR"):
                    var_list.GETCHAR(i,framy)
                elif(i.opcode == "CONCAT"):
                    var_list.CONCAT(i,framy)
                elif(i.opcode =="AND" or i.opcode =="OR"):
                    var_list.AND_OR(i,framy)
                elif(i.opcode =="NOT"):
                    var_list.NOT(i,framy)
                elif(i.opcode =="LT" or i.opcode =="GT"):
                    var_list.LT_GT(i,framy)
                elif(i.opcode =="EQ"):
                    var_list.EQ(i,framy)

                elif(i.opcode =="CALL"):
                    i = var_list.CALL(i,dllist,pole,framy)

                elif(i.opcode =="RETURN"):
                    i = var_list.RETURN(pole,framy)

                elif(i.opcode =="PUSHS" or i.opcode =="POPS"):
                    var_list.PUSHS_POPS(i,push_var,framy)

                elif(i.opcode == "CREATEFRAME" or i.opcode == "PUSHFRAME" or i.opcode == "POPFRAME"):
                    var_list.CREATEFRAME_PUSHFRAME_POPFRAME(i,framy)

                elif(i.opcode =="READ"):
                    var_list.READ(i,input_for_read,framy)
                    
                elif(i.opcode =="DPRINT"):
                    if(i.arg1_type == "var"):
                        tmp = var_list.variable_find_err_miss(i.arg1_value,framy)
                        sys.stderr.write("DPRINT: ")
                        sys.stderr.write(tmp.var_value)
                    else:
                        if(i.arg1_value == None):   #kontrola ci dana premenna obsahuje aj nejaku hodnotu
                            err56()
                        sys.stderr.write("DPRINT: ")
                        sys.stderr.write(i.arg1_value)

                elif(i.opcode =="BREAK"):
                    sys.stderr.write("BREAK: ")
                    sys.stderr.write(i.opcode,i.order)

                i = i.next      
         
main()             