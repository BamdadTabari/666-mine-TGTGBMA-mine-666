import os
import pyrogram 

c = pyrogram.Client()
c.get_chat_members()
a = os.getcwd() + '\\1-edition\\clients'
print(a)
files = os.listdir(a)
print(os.getcwd())

#--------------- signal handler part start---------------------
# this will use in case of app crash or user closed app
    
# import signal
# import sys
# import traceback

# async def signal_handler(sig, frame):
#     """
#     This function will be called when the application receives a SIGINT or SIGTERM signal.
#     """
#     print("Caught signal:", sig)
#     print("Performing cleanup...")
#     try:
#         stop_helper_client(HELPER_CLIENT)
#     except:
#         pass
#     # Print a stack trace to help with debugging
#     traceback.print_stack(frame)
#     print("Cleanup complete. Exiting.")
#     sys.exit(0)

# # Register the signal handler for SIGINT, SIGTERM, CTRL_BREAK_EVENT, CTRL_C_EVENT
# signal.signal(signal.SIGINT, signal_handler)
# signal.signal(signal.SIGTERM, signal_handler)

#--------------- signal handler part end---------------------
