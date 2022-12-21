#!/usr/bin/env python3

import sys
import textwrap
import socketserver
import string
import readline
import threading
from time import *
from colorama import *
import subprocess

prompt = f"{Fore.GREEN}{Style.BRIGHT}user@challenge{Fore.RESET}{Style.NORMAL}:{Fore.CYAN}{Style.BRIGHT}~{Fore.RESET}{Style.NORMAL}$ "

class Service(socketserver.BaseRequestHandler):

    def handle(self):

        
        while ( 1 ):    
            command = self.receive(prompt)
            no_spaces = command.replace(" ","")
            no_spaces = no_spaces.replace("\t","")
            no_spaces = no_spaces.replace("\n","")
            if no_spaces == "exit":
                return
            print(no_spaces)
            p = subprocess.Popen(no_spaces, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            stdout, stderr = p.communicate()
            self.send(stderr + stdout)
            

    def send(self, string, newline=True):
        if type(string) is str:
            string = string.encode("utf-8")

        if newline:
            string = string + b"\n"
        self.request.sendall(string)

    def receive(self, prompt="> "):
        self.send(prompt, newline=False)
        return self.request.recv(4096).strip().decode("utf-8")


class ThreadedService(socketserver.ThreadingMixIn, socketserver.TCPServer, socketserver.DatagramRequestHandler):
    pass


def main():

    port = 1337

    host = '0.0.0.0'

    service =  Service
    server = ThreadedService((host, port), service)
    server.allow_reuse_address = True
    
    server_thread = threading.Thread(target=server.serve_forever)

    server_thread.daemon = True
    server_thread.start()

    print( "Server started on " + str(server.server_address) + "!")
    
    # Now let the main thread just wait...
    while ( True ): sleep(10)

if __name__ == "__main__":
    main()