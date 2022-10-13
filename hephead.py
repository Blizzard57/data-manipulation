import argparse
from pyHepMC3 import HepMC3 as hm
from seek_event import EventSeeker
from compose_event import EventComposer

def parseReq():
    parser = argparse.ArgumentParser(description='''This program facilitates splitting of data file and get 
                                    a file with top N events.''')
    
    parser.add_argument(metavar="I",dest="type",type=str,
                        help="The input file")

    parser.add_argument("-o","--output-file",metavar="O",type=str,required=True,
                        help="The output file")


    parser.add_argument("-n",metavar="N",type=int,
                        help="The number of events to be taken. Default value is 10",default=10)


    args = parser.parse_args()
    return args

def hephead(inputfile,outputfile,n_events):
    e1 = EventSeeker(inputfile)
    tot = e1.getTotalEvents()
    
    n_events = n_events if n_events < tot else tot

    o1 = hm.WriterAscii(outputfile)
    for _ in range(n_events):
        temp_compose = EventComposer(e1.findNext())
        o1.write_event(temp_compose.getEvent())

if __name__ == "__main__":
    args = parseReq()
    hephead(args.type,args.output_file,args.n)