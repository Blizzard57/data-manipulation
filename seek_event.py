import os
import re
import mmap
from pyHepMC3 import HepMC3 as hm

class EventSeeker():
    def __init__(self,filename,filetype = 'hepmc3') -> None:
        
        self.filename = filename
        self.filetype = filetype

        self.current_event = 0
        self.number_of_events = None

        self.findTotalEvents()

    def findTotalEvents(self):

        with open(self.filename, 'rb') as read_obj:
            read_obj.seek(0, os.SEEK_END)
            pointer_location = read_obj.tell()
            buffer = bytearray()

            event_number = 0
            foundLastEvent = False
            while pointer_location >= 0 and not foundLastEvent:
                read_obj.seek(pointer_location)
                pointer_location = pointer_location -1
                new_byte = read_obj.read(1)
                if new_byte == b'\n':
                    line = buffer.decode()[::-1]
                    if len(line) > 0:
                        if line[0] == 'E':
                            event_number = line.split(" ")[1]
                            foundLastEvent = True
                    buffer = bytearray()
                else:
                    buffer.extend(new_byte)
            
            if not foundLastEvent and len(buffer) > 0:
                line = buffer.decode()[::-1]
                if line[0] == 'E':
                    event_number = line.split(" ")[1]
                    foundLastEvent = True
        
        self.number_of_events = int(event_number) + 1

    def findParticularEvent(self,event_number):
        if event_number >= self.number_of_events:
            event_number%= self.number_of_events 
        
        evt = hm.GenEvent()
        f = hm.ReaderAscii(self.filename)
        f.skip(event_number - 1)
        f.read_event(evt)

        return evt

    def findNext(self):
        if self.current_event >= self.number_of_events:
            self.current_event%=self.number_of_events
        
        evt = self.findParticularEvent(self.current_event)
        self.current_event += 1
        
        return evt

    def getTotalEvents(self):
        return self.number_of_events

if __name__ == "__main__":
    e1 = EventSeeker('example.hepmc3','hepmc3')
    evt = e1.findNext()
    print(evt.event_number())
    evt = e1.findNext()
    print(evt.event_number())
    evt = e1.findNext()
    print(evt.event_number())
    evt = e1.findNext()
    print(evt.event_number())

    evt = e1.findParticularEvent(304)
    print(evt.event_number())