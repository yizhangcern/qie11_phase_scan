#!/usr/bin/env python

# Original author: J. Mariano #
# Refactored Oct. 2017 #

import time
import fec_jm, qie11_phases, umnio


def setPhase(phase, test_mode=None, igloo=None, logfile=None):
        cmds1 = qie11_phases.commands(phase, put=True, igloo=igloo)
        cmds2 = qie11_phases.commands(phase, put=False, igloo=igloo)

        if test_mode:
                logfile.write("Test mode enabled. The following commands would be sent to the ngccm server otherwise:\n")        
                for cmd in cmds1 + cmds2:
                        logfile.write(cmd)
        else:
                fec_jm.sendAndLog(cmds1, logfile)
                fec_jm.sendAndLog(cmds2, logfile)
        logfile.write("############################################\n")


def main():
    transition_code = 999  # wrtitten to uMNIO during phase changes
    seconds_per_phase = 300
    loop = 100  # number of loops. loop = -1 for permanent looping
    test_mode = False  # if test_mode == True, then there are no actual writes to hardware

    while (loop != 0):
        for phase in qie11_phases.settings():
                logfile = open("phasescan_log.txt", "a")
                print "Writing phase %d to uMNIO." % transition_code
                if not test_mode:
                        umnio.write_setting(transition_code)
                
                print "Setting phase: %d" % phase
                setPhase(phase, test_mode=test_mode, igloo=False, logfile=logfile)
                
                print "Writing phase %d to uMNIO." % phase
                if not test_mode:
                        umnio.write_setting(phase)
                
                print "...sleeping"
                time.sleep(seconds_per_phase)
                
                print "####################################################################################"

                loop =  loop - 1
                logfile.close()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass

    print
    print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
    print "Phases are still in the final scan value."
    print "Configure a run to restore to default values."
    print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
