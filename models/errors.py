wrongPlanetMessage = "Planet change has been detected. Please refresh the page to make sure you are performing the operation on the right planet."
notEnoughResourcesMessage = "Not enough resources."
maximumLimitMessage = "The maximum limit has been reached for this unit."
shipsNotFoundMessage = "Ships not found."
notEnoughDeuterium = "Not enough deuterium for fuel"
notEnoughShipsMessage = "Not enough ships."


class WrongPlanetException(Exception):
    pass

class NotEnoughResourcesException(Exception):
    pass

class MaximumLimitException(Exception):
    pass

class ShipsNotFoundException(Exception):
    pass

class NotEnoughDeuterium(Exception):
    pass

class NotEnoughShipsException(Exception):
    pass

class ZeroShipsException(Exception):
    pass


class NoShipsCustomException(Exception):
    pass