from enum import IntEnum


class CompatibilityLevel(IntEnum):
    """ Compatibility level of the prober. 
    
        The compatibility level is determined at time of instantiating the prober class. 
        It is used to determine which features are available in the prober. This enum
        only contains SENTIO versions which introduces API changes.
    """
    # Undefined compatibility level, used for prober instances that are not yet initialized.
    # Do NOT use this value in your code production code. It is signalling an uninitialized 
    # state.
    Auto = 0
    Sentio_24_0 = 1
    Sentio_25_1 = 2
    Sentio_25_2 = 3
    Experimental = 99


class Compatibility:
    """Compatibility class to determine the compatibility level of the prober.
    
    The compatibility level is determined at time of instantiating the prober class.
    It is used to determine which features are available in the prober. This class
    only contains SENTIO versions which introduces API changes.
    """
    
    # Default compatibility level is Undefined 
    level : CompatibilityLevel = CompatibilityLevel.Auto

    @staticmethod
    def assert_min(level : CompatibilityLevel) -> None:
        """Asserts that the compatibility level is at least the given level.
        
        Args:
            level (CompatibilityLevel): The minimum compatibility level required.
        
        Raises:
            RuntimeError: If the current compatibility level is lower than the required level.
        """
        if Compatibility.level < level:
            raise RuntimeError(f"This command is not supported by your machine! The machine reports a compatibility level of {Compatibility.level.name} but {level.name} is required to execute the command.")