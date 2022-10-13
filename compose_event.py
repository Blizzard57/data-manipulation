from pyHepMC3 import HepMC3 as hm

class EventComposer():
    def __init__(self,signalEvent):
        self.evt = hm.GenEvent()
        self.addEvent(signalEvent,True)

        runInfo = {"signal_process_id"     : hm.IntAttribute,
                   "signal_process_vertex" : hm.IntAttribute,
                   "event_scale"           : hm.DoubleAttribute,
                   "alphaQCD"              : hm.DoubleAttribute,
                   "alphaQED"              : hm.DoubleAttribute,
                   "mpi"                   : hm.IntAttribute}

        for run in runInfo.keys():
            attr = float(signalEvent.attribute(run))
            if attr.is_integer():
                attr = int(attr)
            self.evt.add_attribute(run,runInfo[run](attr))

        newCrossSection = hm.GenCrossSection()
        csValues = [int(x) if x.is_integer() else x 
                  for x in [float(x) for x in 
                  signalEvent.attribute("GenCrossSection").split(' ')]]

        newCrossSection.set_cross_section(*csValues)
        self.evt.add_attribute("GenCrossSection",newCrossSection)

        newPdfInfo = hm.GenPdfInfo()
        csValues = [int(x) if x.is_integer() else x 
                  for x in [float(x) for x in 
                  signalEvent.attribute("GenPdfInfo").split(' ')]]

        newPdfInfo.set(*csValues)
        self.evt.add_attribute("GenPdfInfo",newPdfInfo)

        self.evt.set_event_number(signalEvent.event_number())

    def addEvent(self,curEvent,issignal = False):
        
        # TODO : Find out how to implement offset
        offset = 0 if issignal else 1000000
        
        vertex_map = {}
        
        for vertex in curEvent.vertices():
            
            temp_vertex = hm.GenVertex(vertex.position())
            temp_vertex.set_id(vertex.id())
            temp_vertex.set_status(vertex.status())
            
            vertex_map[vertex] = temp_vertex
            self.evt.add_vertex(temp_vertex)

        for particle in curEvent.particles():
            temp_particle = hm.GenParticle(particle.momentum(),particle.pid(),particle.status())
            
            if particle.end_vertex() is not None:
                vertex_map[particle.end_vertex()].add_particle_in(temp_particle)

            if particle.production_vertex() is not None:
                if particle.production_vertex() in vertex_map:
                    vertex_map[particle.production_vertex()].add_particle_out(temp_particle)
                
                # TODO : Find out why GenEvent does not contain all the vertices

        # TODO : Add the beam particles

        # TODO : Find out how to add weights
        self.evt.weights().extend([i for i in curEvent.weights()])

    def getEvent(self):
        return self.evt

if __name__ == "__main__":
    
    f1 = hm.ReaderAscii('/home/blizzard/pilemc/pypilup/data/example.hepmc3')
    f2 = hm.WriterAscii('trial.hepmc3')
    
    evt = hm.GenEvent()
    f1.read_event(evt)
    e1 = EventComposer(evt)
    
    for _ in range(10):
        evt = hm.GenEvent()
        f1.read_event(evt)
        e1.addEvent(evt,False)
        print(evt.event_number())
        f2.write_event(e1.evt)