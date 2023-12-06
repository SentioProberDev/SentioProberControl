""" # Communication package
    
    This package contains classes for communication with the MPI probe station with
    different protocols: TCP/IP, Gpib or VISA. Communication is handled by instances of Communicator objects.
    When initializing a probe station a communicator object must be passed to the constructor of the probe 
    station but the communicator could also be used standalone.

    # Communication Methods
    * `sentio_prober_control.Communication.CommunicatorTcpIp`<br/>for plain TCP/IP communication
    * `sentio_prober_control.Communication.CommunicatorGpib`<br/>for GPIB communication via native drivers (ADLINK and NI)
    * `sentio_prober_control.Communication.CommunicatorVisa`<br/>for using the NI-VISA interface which warps (TCP/IP, GPIB and RS232) 

    ## Communicator Example

    The following example will establish a Tcp/Ip connection to a locally running SENTIO instance. It will then send a "*IDN?" command
    in order to read the system information of the probe station back.

    >>> from sentio_prober_control.Communication.CommunicatorTcpIp import CommunicatorTcpIp
    >>> comm = CommunicatorTcpIp.create("127.0.0.1:35555")
    >>> comm.send("*IDN?")
    >>> comm.read_line()
    'MPI Corporation,Sentio - Probe System Software Suite,0,23.2.99.0'
    
"""
print(f"Initializing package {__name__}")
