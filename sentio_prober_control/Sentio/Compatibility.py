from enum import IntEnum


class CompatibilityLevel(IntEnum):
    """ Compatibility level of the prober. 
    
        The compatibility level is determined at time of instantiating the prober class. 
        It is used to determine which features are available in the prober. This enum
        only contains SENTIO versions which introduces API changes.
    """
    Auto = 0
    Sentio_24 = 1
    Sentio_25_2 = 2
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
            raise RuntimeError(f"Compatibility level {Compatibility.level} is lower than required {level}.")