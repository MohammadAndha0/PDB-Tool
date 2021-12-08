#!/usr/bin/env python3

# File title: pdb.py 
# Authorship: Noushin Haque, Mohammad Andha, Andy Huang, Andrea Moreno (Class: 10761)
# Usage: pdb.py <valid_pdb_file_name>
# Purpose:The program is designed to give an organized data collection or record extracted from a PDB file with information 
# about the atoms such as the atom frequency, residue frequency, and the maximum distance of the distances. 
# Date created: Friday Dec 3, 2021
##################################################################################################################################################################################

import sys      #import the sys module to access any command-line arguments via the sys.argv
import math     #import the math module which extends the list of mathematical functions - it's used in calculating the distance between coordinates  

#lists to store the atom records
atom_serial_number = []
residue = []
chain_ID = []
res_seq_num = []
x_coordinate = []
y_coordinate = []
z_coordinate = []
element_name = []
atom_records = []

#resLength function calculations
x_values = []
y_values = []
z_values = []
coordinate_dist = []



#defined functions: atom_info, help, atomFreq, resFreq, resLength, coordinate_distances, main


count = 0
def atom_info(count):
    
    with open(sys.argv[1], "r") as file:     #opening the file entered as the second command line argument for reading and naming it 'file'
        contents = file.read()                  
        lines = contents.splitlines()
        for line in lines:                    #iterate through each line by using a for loop
            if line.startswith('ATOM'):       #recognize if the line starts with 'ATOM' to count how many atoms are present within in the file 
                count += 1                    #update counter to record how many atoms are present  
                atom_records.append(line)
                residue.append(line[17:20])
                for res in residue:            #iterate through each residue contained with the residue list 
                    if len(res.strip()) < 3:   #check if the length of the residue is less than three - should only be a three-letter uppercase reisude name 
                        residue.remove(res)    #remove the residues containing only 2 uppercase letters after removing any trailing or leading spaces 
                atom_serial_number.append(line[7:11])            
                chain_ID.append(line[21])
                res_seq_num.append(line[23:26])
                x_coordinate.append(line[31:38])
                y_coordinate.append(line[39:46])
                z_coordinate.append(line[47:54])
                element_name.append(line[77:78])
        
        #print(res_seq_num)

        return count      #returns the count of atoms present within the file to where the function was called



def help():

    HelpMenu = True          #setting the variable HelpMenu to true
    while HelpMenu:          #using a while loop to keep asking the user to enter a command correlating to the help menu
        print("""
        1.help
        2.Program Details
        3.atomFreq
        4.resFreq
        5.resLength
        6.quit
        Type Exit to exit the help menu
        """)                                                                                            
        UserInput=input("Type in a command or it's corresponding number to learn its function: ")    #use the inbuilt function input() to prompt the user to enter a command as mentioned
        
        #use an if loop to print particular statements that explain how each command entered by the user functions
    
        if UserInput=="help" or UserInput=="1": 
            print("The help function provides a menu that lists the fuctions of the program.") 
        elif UserInput=="Program Details" or UserInput=='2':
            print("The program is designed to give an organized data collection or record extracted from a PDB file with information about the atoms such as the atom frequency, residue frequency, and the maximum distance of the distances.") 
        elif UserInput=="atomFreq" or UserInput=="3":
            print("Displays each distinct atom that is stored and the number of occurrences of that atom in the file.")
            print("Output: element: <n>")
            print("element is the element name and <n> is the number of atoms of that element, sorted alphabetically.") 
        elif UserInput=="resFreq" or UserInput=="4":
            print("Displays each distinct residue that is stored and the number of occurrences of that residue in the file.")
            print("Output: residue: <n>")
            print("residue is the three-letter uppercase residue name and <n> is the number of occurrences of that residue in the file, sorted alphabetically.")
        elif UserInput=="resLength" or UserInput=="5":
            print("The reslength function allows you to calculate the distance between every pair of atoms in the specified residue and displays the maximum distance of the distances.")
            print("usage: reslength <res_name> <chain_id> <res_seq_num>")
            print("Ouput: <res_name> with sequence number <res_seq_num> in chain <chain_id> has length <distance> angstroms.")
            print("<res_name> is a three-letter residue name in uppercase, <chain_id> is a one-letter chain id in uppercase, and <res_seq_num> is an integer that uniquely identifies the position of the residue named res_name in the given chain.")

        elif UserInput=="quit" or UserInput=="6":
            print("The quit function allows you to quit the program if you type quit as a command.")
        elif UserInput=="Exit" or UserInput=="exit":  
            break
        else:
            print("Invalid Input; Please enter a valid response from the menu.")


#Function: atomFreq - displays each distinct atom that is stored and the number of occurrences of that atom in the file

def atomFreq():

    atomFreq = dict()      #create an empty dictionary and set to variable atomFreq

    for element in element_name:    #for loop to iterate through each element in the list element_name
        try:
            atomFreq[element] += 1    #increment if key element occurs or appears more than once
        except:
            atomFreq[element] = 1     #set the key element value of 1 for the first time it appears 

    for element in (sorted(atomFreq)):   #for loop to iterate through each element stored in the dictionary atomFreq, sorted aplhabetically 
        print(element, ':', atomFreq[element])   #print element[key], and the number of times it appears[value] 




#Function: resFreq - displays each distinct residue that is stored and the number of occurrences of that residue in the file

def resFreq():

    resFreq = dict()      #create an empty dictionary and set to variable resFreq

    for res in residue:     #for loop to iterate through each residue in the list residue
        try:
            resFreq[res] += 1   #increment if key res occurs or appears more than once
        except:
            resFreq[res] = 1     #set the key res value of 1 for the first time it appears

    for res in (sorted(resFreq)):  #for loop to iterate through each residue stored in the dictionary resFreq, sorted aplhabetically 
        print(res, ':',resFreq[res])   #print res[key], and the number of times it appears[value]


#The reslength function allows you to calculate the distance between every pair of x,y,z values and the coordinate_distances displays the maximum distance of the distances.

def resLength(residue, chain_ID, res_seq_number):    #the indexed values from the command arguments the user entered in the main function are passed to this function (parameters)
    
    x_values.clear()
    y_values.clear()
    z_values.clear()
    coordinate_dist.clear()

    #lists that stores all the x, y, and z values of each coordinate  
    x_coord = []
    y_coord = []
    z_coord = []

    try:
        for line in atom_records:         #iterate through each line stored in the list atom_records
            if line[17:20] == residue and line[21] == chain_ID and line[23:26] == res_seq_number:    #check if the residue, chain ID, and residue sequence number aligns with each other
                x_coord.append(line[31:38])        #append the x, y, z values to the lists 
                y_coord.append(line[39:46])
                z_coord.append(line[47:54])
    
    except Exception as error:        #detect any possible errors
        print("An error occurred")
                 
    
    #set start_index and index to 0 and 1

    start_index = 0
    index = 1
    
    #assign the x1, x2, y1, y2 variables to its correlating indexed values from the lists for only the first pair of coordinates 
    #this is for comparison and confirm the first distance between the first pair is calculated correctly
    
    x1 = float(x_coord[start_index])   
    x2 = float(x_coord[index])
    y1 = float(y_coord[start_index])
    y2 = float(y_coord[index])
    z1 = float(z_coord[start_index])
    z2 = float(z_coord[index])

    x_value = ((x2) - (x1))**2   #calculates the distance between the first pair of x values in the first two coordinates
    x_values.append(x_value)

    y_value = ((y2) - (y1))**2   #calculates the distance between the first pair of y values in the first two coordinates 
    y_values.append(y_value)
        
    z_value = ((z2) - (z1))**2   #calculates the distance between the first pair of z values in the first two coordinates
    z_values.append(z_value)
        
    first_pair_dist = math.sqrt(float(x_value) + float(y_value) + float(z_value))   #calculates the overall distance between the first pair of coordinates
    coordinate_dist.append(first_pair_dist)                    #append or add the distance to the list coordinate_dist
    

    #use a while loop to go through the other coordinates and calculate the distances between every pair of x, y, z values, excluding the first pair as it's calculated earlier
    while index < (len(x_coord) - 1):
        
        start_index += 1       #incrementing to go through every pair of x,y,z values in the other coordinates
        index += 1
        x1 = float(x_coord[start_index])   
        x2 = float(x_coord[index])
                
        y1 = float(y_coord[start_index])
        y2 = float(y_coord[index])

        z1 = float(z_coord[start_index])
        z2 = float(z_coord[index])

        x_coords = (float(x2) - float(x1))**2         #calculates the distance between each pair of x values of the other coordinates
        x_values.append(x_coords)   

        y_coords = (float(y2) - float(y1))**2         #calculates the distance between each pair of y values of the other coordinates 
        y_values.append(y_coords)

        z_coords = (float(z2) - float(z1))**2         #calculates the distance between each pair of z values of the other coordinates
        z_values.append(z_coords)


#Displays the maximum distance of the distances

def coordinate_distances(x_values, y_values, z_values):    #the lists containing the distances between each pair of x, y, z, values are passed to this function and returns the max distance
                                                           #to where it's called in the main
    
    start_index = 0
    index = 1
    
    while index < (len(x_values)):         #use a while loop to go through each pair of x,y,z values stored within the lists, using indexing and incrementing 
        start_index += 1                   #use the Euclidean distance formula (math module) to calculate the distance overall between each coordinate stored in coordinate_dist
        index += 1

        pair1 = float(x_values[start_index])
        pair2 = float(y_values[start_index])
        pair3 = float(z_values[start_index])
            
        other_pairs_dist = math.sqrt(float(pair1) + float(pair2) + float(pair3))  #calculate the distance and append/add the additional distances between every other pair of coordinates
        coordinate_dist.append(other_pairs_dist)             #to the list coordinate_dist

    
    max_Distance = round(max(coordinate_dist), 2)   #set the variable max_Distance to the maximum value rounded to the hundredths place within the list of calculated coordinates (math module) 
                                                    #using the max and round functions

    return max_Distance   #returns the value max_Distance to the main function


#main function goes through every possible error depending on what the user enters, to use the pdb tool properly

def main():
    
    try:
        with open(sys.argv[1], "r") as file:      #opening the file entered as the second command line argument for reading and naming it 'file'
            contents = file.read()                #uses the .read() function to read a file's contents, returning it as a string and stores it in the variable contents
            
            frequency = atom_info(count)         #calls the function atom_info to calculate and return the count value, and storing that in the variable frequency 
            print("Welcome to the pdb program. \nTo begin, try typing 'help' for the list of valid commands or typing quit to exit the program")
            print(frequency, "atoms recorded.")      #print the welcome statement and the frequency of atoms recorded from the file

            while contents:                      #use a while loop to execute the block of code below while the file is being read
                x = input("Enter a command: ")   #ask the user to ask for a command and will call the specified function entered 

                if x == "help":
                    help()
                elif x == "atomFreq":
                    atomFreq()
                elif x == "resFreq":
                    resFreq()
                elif len(x.split()) == 4:      #if the user enters a total of 4 arguments
                    y = x.split()              #use split method to divide the string of 4 arguments into a list of the 4 arguments to easily index a value, and set it to the variable y 
                    u = ['resLength']
                    if y[0] in u and y[2] in chain_ID:    #check if the indexed values are present within the specific lists
                        if y[1].isupper() and y[2].isupper() is True:  #.isupper() method returns true if all indexed values are in uppercase
                            if y[1] in residue:                         #check if the residue entered is present with the list residue
                                if y[3] in res_seq_num and int(y[3]):      #check if residue sequence number is in the list of residue sequence numbers and is an integer (no decimals)
                                    
                                    try: 

                                        for line in atom_records:       #iterate through each line stored within atom_records
                                            if line[17:20] == y[1] and line[21] == y[2] and line[23:26] == y[3]:  #check if the residue, chain ID, and residue sequence number aligns with each other                                                       
                                                resLength(y[1], y[2], y[3])   #calls the function resLength and passes the indexed values as residue, chain_ID, res_seq_num (actual arguments)
                                                    
                                                max_Distance = coordinate_distances(x_values, y_values, z_values)  
                                                #the max_Distance value is returned after the function is called and stores
                                                #the value in the variable max_Distance
                                           
                                                print(y[1], "with sequence number", y[3], "in chain", y[2], "has length", max_Distance, "angstroms.")
                                                break                        #break out of loop

                                        #for loop and if loop to check if the residue,chain ID, residue sequence number don't align
                                        
                                        for line in atom_records:
                                            if not line[17:20] == y[1] and line[21] == y[2] and line[23:26] == y[3]:
                                                print("No residue present")
                                                coordinate_dist.clear()
                                                break
                                                #break out of loop
                                         
        
    #the following detects if any errors occur in the block of code above and returns an error message with the proper usage 
                                    except Exception as error:
                                        print(error)
                
                                else:
                                    print("Usage: reslength <res_name> <chain_id> <res_seq_num>")
                                    print("For details about the reslength command, use the 'help' command.")
                
                            else:
                                print("No residue present")
                                print("Usage: reslength <res_name> <chain_id> <res_seq_num>")
                                print("For details about the reslength command, use the 'help' command.")
                        else: 
                            print("Usage: reslength <res_name> <chain_id> <res_seq_num>")
                            print("For details about the reslength command, use the 'help' command.")
                    else:
                        print("Usage: reslength <res_name> <chain_id> <res_seq_num>")
                        print("For details about the reslength command, use the 'help' command.")
                
                elif x == "quit":
                    print("Leaving the program. Thank you for using the pdb tool.")
                    file.close()
                    exit()
        
                else:
                    print("Invalid Command or missing arguments/wrong number of arguments entered to the command.")
                    print("Type 'help' for more details about valid commands.")
            
            
    except FileNotFoundError:
        print("File does not exist")
        sys.exit()

    except PermissionError:
        print("No access to file. Enable read permissions")
        sys.exit()

    except IndexError:
        print("A valid file isn't entered")
        print("Usage: <pdbTool.py> <valid pdb file name>")
        sys.exit()

    except Exception as error:
        print(error)
        print("Usage: <pdbTool.py> <valid pdb file name>")
        print("For any other error, follow the proper usage format")
        sys.exit()


#calls the main function to use the commands of the pdb tool      
main()






