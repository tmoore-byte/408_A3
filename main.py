#thomas moore
#a3


import application as a

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
############################################################
#thomas moore
#a3

#importing application file so I can use the functions I made


def run_application():
    #put all our functions created in application file

    a.options() #giving the user options + checking their input

    #close the connection
    a.conn.close()

if __name__ == '__main__':
    run_application()