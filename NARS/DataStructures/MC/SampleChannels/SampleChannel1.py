from pynars.NARS.DataStructures.MC.ChannelMC import ChannelMC
from pynars.Narsese import Term, parser


class SampleChannel1(ChannelMC):

    def __init__(self, ID: str, num_slot, num_event, num_anticipation, num_prediction, memory):
        super(SampleChannel1, self).__init__(ID, num_slot, num_event, num_anticipation, num_prediction, memory)
        self.operations = [Term("^write")]
        self.read_cursor = 0
        self.count = 0

    def execute(self, term: Term):
        if term.equal(self.operations[0]):
            f = open("C://Users//TORY//Downloads//PyNARS-0_0_2_pre_alpha ("
                     "1)//PyNARS-0_0_2_pre_alpha//pynars//NARS//DataStructures//MC//playground.txt", "w")
            f.write("I am writing" + str(self.count))
            self.count += 1
            f.close()

    def information_gathering(self):
        f = open("C://Users//TORY//Downloads//PyNARS-0_0_2_pre_alpha ("
                 "1)//PyNARS-0_0_2_pre_alpha//pynars//NARS//DataStructures//MC//playground.txt", "r")
        lines = f.readlines()
        f.close()
        line = lines[self.read_cursor].rstrip('\n')
        line = line.split(" ")
        self.read_cursor += 1
        tasks = []
        for each in line:
            tasks.append(parser.parse("<(*, {Channel1}, " + each + ") --> ^see>."))
        return tasks

