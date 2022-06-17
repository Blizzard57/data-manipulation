'''
The code contains the class Convert which enables conversion of
file formats wherever possible.
'''

from array import array
from os.path import exists
from pyHepMC3.rootIO import HepMC3 as hmrootIO
from pyHepMC3 import HepMC3 as hm

class Convert():
    '''
    The module converts data between the compatible
    file formats.
    The file format conversions supported are :
        - HEPMC2 -> ROOT
        - ROOT -> HEPMC2 (The compatible file)
        - LHE -> ROOT
        - ROOT -> LHE (The compatible file)

    Support is coming for :
        - HEPMC2 -> HDF5
        - LHE -> HDF5
    
    Conversions that does not work :
        - HEPMC2 -> LHE

    Converisons whose implementation is unknown :
        - ROOT -> HDF5

    Attributes :
    ------------
    input_file : str
        The input file with the extension

    output_file : str
        The output file with the extension

    convert_dict : dict
        The dictionary where functions for conversions
        are stored

    Methods :
    ---------
    add_input_file()
        The internal method that allows
        setting input file name

    add_output_file()
        The internal method that allows
        setting output file name

    convert_hepmc2_root()
        Convert HEPMC2 file to ROOT file

    convert_root_hepmc2()
        Convert previously converted HEPMC2 file
        back to HEPMC2 from ROOT

    convert_lhe_root()
        Convert LHE file to ROOT file

    convert_root_lhe()
        Convert previously converted LHE file
        back to LHE from ROOT

    sanitize_format()
        Helper function that allows any uppercase
        lowercase file format input for universality

    convert_menu()
        The external function that can be utilized outside
        the scope of the class for interaction from outside    
    '''

    def __init__(self):
        '''
        The initializer that gets all the attribute
        without assigning any of them

        Parameters :
        ------------
        None

        Exceptions :
        ------------
        None

        Returns :
        ---------
        None
        '''
        self.input_file = None
        self.output_file = None
        self.convert_dict = None

    def __add_input_file(self,input_file):
        '''
        The internal function to enter the input file

        Parameters :
        ------------
        input_file : str
            The input file which exists

        Exceptions :
        ------------
        ValueError
            The error is thrown if the file
            does not exist

        Returns :
        ---------
        None
        '''

        if not exists(input_file):
            raise ValueError('ERROR : The file does not exists')

        self.input_file = input_file

    def __add_output_file(self,output_file):
        '''
        The internal function to enter the output file

        Parameters :
        ------------
        output_file : str
            The output file which exists

        Exceptions :
        ------------
        ValueError
            The error is thrown if the file exist

        Returns :
        ---------
        None
        '''

        if exists(output_file):
            raise ValueError('ERROR : The file already exists')

        self.output_file = output_file

    def __convert_hepmc2_root(self):
        '''
        Convert the HEPMC2 file to ROOT file

        Parameters :
        ------------
        None

        Exceptions :
        ------------
        ValueError
            The error is thrown if the HEPMC file 
            cannot be read

            The error is thrown if the ROOT file
            cannot be opened

        Returns :
        ---------
        None
        '''

        input_hep = hm.ReaderAsciiHepMC2(self.input_file)

        if input_hep.failed():
            raise ValueError('ERROR : Could not read HepMC2 file successfully.')

        output_root = hmrootIO.WriterRootTree(self.output_file)
        if output_root.failed():
            raise ValueError('ERROR : Could not open ROOT file successfully.')

        pb = tqdm()

        while not input_hep.failed():
            evt = hm.GenEvent()
            input_hep.read_event(evt)
            pb.update(1)
            if input_hep.failed():
                print("INFO : File successfully converted")
                break

            output_root.write_event(evt)
            evt.clear()

        input_hep.close()
        output_root.close()

    def __convert_root_hepmc2(self):
        '''
        Convert the ROOT file to HepMC2 file

        Parameters :
        ------------
        None

        Exceptions :
        ------------
        ValueError
            The error is thrown if the ROOT file 
            cannot be read

            The error is thrown if the HEPMC file
            cannot be opened

        Returns :
        ---------
        None
        '''
        input_root = hmrootIO.ReaderRootTree(self.input_file)
        if input_root.failed():
            raise ValueError('ERROR : Could not read ROOT file successfully.')

        output_hep = hm.WriterAsciiHepMC2(self.output_file)
        if output_hep.failed():
            raise ValueError('ERROR : Could not open HepMC2 file successfully.')

        pb = tqdm()

        while not input_root.failed():
            evt = hm.GenEvent()
            input_root.read_event(evt)
            pb.update(1)
            if input_root.failed():
                print("INFO : File successfully converted")
                break
            output_hep.write_event(evt)
            evt.clear()

        input_root.close()
        output_hep.close()

    def __convert_lhe_root(self):
        '''
        Convert the LHE file to ROOT file

        Parameters :
        ------------
        None

        Exceptions :
        ------------
        ValueError
            The error is thrown if the LHE file 
            cannot be read

            The error is thrown if the ROOT file
            cannot be opened

        Returns :
        ---------
        None
        '''
        events = []
        event = ""
        in_event = False
        try:
            with open(self.input_file, "r") as fhin:
                for line in tqdm(fhin):

                    if in_event and line.startswith("<"):
                        in_event = False
                        events.append(event)
                        event = ""

                    if in_event:
                        event += line

                    if line.startswith("<event>"):
                        in_event = True

                if event:
                    events.append(event)

        except:
            raise ValueError('ERROR : Could not read the LHE file successfully')

        try:
            f1 = r.TFile(self.output_file, "recreate")

        except:
            raise ValueError('ERROR : Could not create the ROOT file successfully')

        t1 = r.TTree("t","t")

        pdgid = array( 'i', [ 0 ] )
        bevent = array( 'i', [ 0 ] )
        status = array( 'i', [ 0 ] )
        parent1 = array( 'i', [ 0 ] )
        parent2 = array( 'i', [ 0 ] )
        color1 = array( 'i', [ 0 ] )
        color2 = array( 'i', [ 0 ] )
        mass = array( 'd', [ 0 ] )
        spin = array( 'd', [ 0 ] )
        p4 = r.TLorentzVector(1,1,0,5)

        t1.Branch("id",pdgid, "id/I")
        t1.Branch("event",bevent, "event/I")
        t1.Branch("status",status, "status/I")
        t1.Branch("parent1",parent1, "parent1/I")
        t1.Branch("parent2",parent2, "parent2/I")
        t1.Branch("color1",color1, "color1/I")
        t1.Branch("color2",color2, "color2/I")
        t1.Branch("mass",mass, "mass/F")
        t1.Branch("spin",spin, "spin/F")
        t1.Branch("p4.","TLorentzVector",p4)

        for ievt,evt in tqdm(enumerate(events)):
            particle_lines = evt.splitlines()[1:]
            for particle_line in particle_lines:
                parts = particle_line.split()
                evt_pdgid = int(parts[0])
                evt_status = int(parts[1])
                evt_parent1 = int(parts[2])
                evt_parent2 = int(parts[3])
                evt_color1 = int(parts[4])
                evt_color2 = int(parts[5])
                evt_px, evt_py, evt_pz, evt_e = map(float,parts[6:10])
                evt_mass = float(parts[10])
                evt_spin = float(parts[11])

                p4.SetPxPyPzE(evt_px, evt_py, evt_pz, evt_e)

                bevent[0] = ievt
                pdgid[0] = evt_pdgid
                status[0] = evt_status
                parent1[0] = evt_parent1
                parent2[0] = evt_parent2
                color1[0] = evt_color1
                color2[0] = evt_color2
                mass[0] = evt_mass
                spin[0] = evt_spin

                t1.Fill()

        t1.Print()
        t1.Write()
        f1.Close()

    def __sanitize_format(self,file_format):
        '''
        Convert the string to lowercase to remove case specific issues

        Parameters :
        ------------
        file_format : str
            The string which is converted to lowercase

        Exceptions :
        ------------
        None

        Returns :
        ---------
        None
        '''
        return file_format.lower()

    def __get_convert_table(self):
        '''
        Convert the string to lowercase to remove case specific issues

        Parameters :
        ------------
        file_format : str
            The string which is converted to lowercase

        Exceptions :
        ------------
        None

        Returns :
        ---------
        None
        '''
        self.convert_dict = {
            'root' : {
                'hepmc2' : self.__convert_root_hepmc2
                },
            'hepmc2' : {
                'root' : self.__convert_hepmc2_root
                },
            'lhe' : {
                'root' : self.__convert_lhe_root
            }
        }

    def convert_menu(self,input_file,output_file,input_format,output_format):
        '''
        The main function that converts the file formats by
        combining all the functions.It is the only function
        accessible from outside the function scope

        Parameters :
        ------------
        input_file : str
            The input file

        output_file : str
            The output file

        input_format : str
            The input format, the extension
            of input_file

        output_file : str
            The output format, the extension
            of output_file

        Exceptions :
        ------------
        None

        Returns :
        ---------
        None
        '''

        self.__add_input_file(input_file)
        self.__add_output_file(output_file)
        self.__get_convert_table()

        input_format = self.__sanitize_format(input_format)
        output_format = self.__sanitize_format(output_format)

        self.convert_dict[input_format][output_format]()
