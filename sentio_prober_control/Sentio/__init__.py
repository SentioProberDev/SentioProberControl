""" # The Sentio package

    The Sentio package is your gateway to control a probe station running the MPI SENTIO Software suite. 
    To start you need two things: A communication channel and a `SentioProber` instance.

    ## Creating a Prober Instance

    The following example will Connect to a probe station and switch to SENTIO's wafermap module.

    >>> from sentio_prober_control.Sentio.ProberSentio import SentioProber
    >>> from sentio_prober_control.Communication.CommunicatorTcpIp import CommunicatorTcpIp
    >>> prober = SentioProber(CommunicatorTcpIp.create("127.0.0.1:35555"))
    >>> prober.select_module(Module.Wafermap)
"""
print(f"Initializing package {__name__}")
