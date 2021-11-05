from Module.SENTIO import SENTIO
#from Module.CTP10 import CTP10
from Module.Enumeration import *
import os.path
import time

def main():
    # Prepare communication
    __SENTIO = SENTIO.create_SENTIO()
    ##__CTP10 = CTP10.create_CTP10()

    #0. Load subsite table
    subsiteListEastX = {
        1: 0,
        2: 0,
        3: 0,
        4: 0}
    subsiteListEastY = {
        1: 0,
        2: -260,
        3: -520,
        4: -780}

    subsiteListWestX = {
        1: 0,
        2: 0,
        3: 0,
        4: 0}
    subsiteListWestY = {
        1: 0,
        2: -260,
        3: -520,
        4: -780}
    for k in range(20):

        '''
        #1. Load project and enable laser source
        __CTP10.enable_laser1()
        __CTP10.Clear_Error_queue()
        
        path = os.path.abspath('..')
        project_path = {
            1: '\\SiPH_Demo_OFC\\SiPH_Demo_OFC.trex'}    
        __SENTIO.open_project(path + project_path[1])
        print('>>Load Project: {}'.format(project_path[1]))
        '''
        #2. Separation SiPH Probe
        __SENTIO.move_siph_separation('East')
        __SENTIO.move_siph_separation('West')

        #3. Separation chuck
        __SENTIO.move_separation()
        '''
        #4. Auto Focus
        ##__SENTIO.auto_focus()
        print('>>Auto Focus finish.')
        
        #5. Auto Align
        __SENTIO.align_wafer(180000)
        print('>>Auto Align Wafer Finish.')
        '''
        #6. Search Home
        __SENTIO.find_home()

        #7. Search Home positioner
        __SENTIO.move_probe_xy('east', 'Home', 1, 1)
        __SENTIO.move_probe_xy('west', 'Home', 1, 1)
        print('>>Home Search Finish.')

        #8. Move chuck contact
        __SENTIO.move_contact()

        #9. Move positioner hover
        __SENTIO.move_siph_hover('East')
        __SENTIO.move_siph_hover('West')

        '''
        #10. Fixed laser wavelength
        __CTP10.laser1_fixed_wavelength()
        '''

        #11. Fast alignment at home die
        __SENTIO.siph_fast_alignment()

        #12. Move First Die

        #12-1. Separation SiPH Probe
        __SENTIO.move_siph_separation('East')
        __SENTIO.move_siph_separation('West')
        print('>>Move separation SiPH Probe.')

        #12-2. Step first die
        __SENTIO.move_first_die()
        print('>>Move first die.')

        #12-3. ProbeSubsite_firstdie
        for j in range(1, len(subsiteListEastX)+1):

            __SENTIO.move_probe_xy('east', 'Home', subsiteListEastX[j],  subsiteListEastY[j])
            __SENTIO.move_probe_xy('west', 'Home', subsiteListWestX[j],  subsiteListWestY[j])

            # Hover SiPH Probe
            __SENTIO.move_siph_hover('East')
            __SENTIO.move_siph_hover('West')

            # Gradient Search SiPH Probe
            __SENTIO.gradient_search()


            '''
            # -----Measurement-CT10----
            __CTP10.Start_Laser_Scan()

            
            # -----Save data-CT10----
            Wav, Trace, err = __CTP10.Retrieve_Trace(2, 1, 1)
            file_name = 'Die{}_Device{}_Iteration{}.csv'.format(1, j, k+1)
            __CTP10.save_to_csv(file_name, Wav, Trace)

            # -----Fixed Wavelength-CT10----
            __CTP10.laser1_fixed_wavelength()
            '''




        #13. Move next die
        die_num = __SENTIO.get_num_dies(DieNumber.Selected)  # Get total dies
        for i in range(1, int(die_num)):

            #13-1. Separation SiPH Probe
            __SENTIO.move_siph_separation('East')
            __SENTIO.move_siph_separation('West')
            print('>>Move separation SiPH Probe.')

            #13-2. Step next die
            __SENTIO.move_next_die()
            print('>>Move next die with bin.')

            #13-3. ProbeSubsite_nextdie
            for j in range(1, len(subsiteListEastX)+1):
                Time_1 = time.time()
                __SENTIO.move_probe_xy('east', 'Home', subsiteListEastX[j],  subsiteListEastY[j])
                __SENTIO.move_probe_xy('west', 'Home', subsiteListWestX[j],  subsiteListWestY[j])
                Time_2 = time.time()
                print('Subsite stepping time:', Time_2 - Time_1)

                # Hover SiPH Probe
                __SENTIO.move_siph_hover('East')
                __SENTIO.move_siph_hover('West')

                # Gradient Search SiPH Probe
                Time_3 = time.time()
                __SENTIO.gradient_search()
                Time_4 = time.time()
                print('Gradient search time:', Time_4 - Time_3)

                '''
                # -----Measurement-CT10----
                Time_5 = time.time()
                __CTP10.Start_Laser_Scan()
                Time_6 = time.time()
                print('Measurement time:', Time_6 - Time_5)

                
                # -----Save data-CT10----
                Wav, Trace, err = __CTP10.Retrieve_Trace(2, 1, 1)
                file_name = 'Die{}_Device{}_Iteration{}.csv'.format(i+1, j, k+1)
                __CTP10.save_to_csv(file_name, Wav, Trace)
                

                # -----Fixed Wavelength-CT10----
                Time_7 = time.time()
                __CTP10.laser1_fixed_wavelength()
                Time_8 = time.time()
                print('Wavelength fixed time:', Time_8 - Time_7)
                '''

        #14. Move separation
        __SENTIO.move_siph_separation('East')
        __SENTIO.move_siph_separation('West')

        #15. Move separation
        __SENTIO.move_separation()

    # Close connection
    __SENTIO.close_SENTIO()
    ##__CTP10.close_CTP10()
    print('>>Finish.')

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(str(e))
