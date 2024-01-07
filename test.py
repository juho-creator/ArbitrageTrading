# while(1):
#     try:
#         print("Wali")
#     except Exception as e:
#         print("fuck!")   
#     else:
#         print("No Error")
#     finally:
#         print("Code executed")


import pyttsx3
engine = pyttsx3.init() # object creation

""" RATE"""
rate = engine.getProperty('rate')   # getting details of current speaking rate
print (rate)                        #printing current voice rate
engine.setProperty('rate', 125)     # setting up new voice rate


"""VOLUME"""
volume = engine.getProperty('volume')   #getting to know current volume level (min=0 and max=1)
print (volume)                          #printing current volume level
engine.setProperty('volume',1.0)    # setting up volume level  between 0 and 1

"""VOICE"""
voices = engine.getProperty('voices')       #getting details of current voice
engine.setProperty('voice', voices[1].id)   #changing index, changes voices. 1 for female


import time

while(1):
    start_time = time.time()

    engine.say('reverse order filled')
    engine.say('kimp order filled')
    print("--- %s seconds ---" % (time.time() - start_time))



