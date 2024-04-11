"""Power module."""


class PowerModule:
    """Module to control battery power."""

    MAX_VOLTAGE = 4.2
    MIN_VOLTAGE = 3.0
    LOW_VOLTAGE = 3.3

    def __init__(self):
        """Power initialization."""
        self._charging = False
        self._battery_voltage = 0

    def battery_level(self) -> int:
        """Return battery level in percents."""
        if self._battery_voltage > self.MAX_VOLTAGE:
            return 100
        if self._battery_voltage < self.MIN_VOLTAGE:
            return 0
        return int((self._battery_voltage - self.MIN_VOLTAGE) * 100 //
                   (self.MAX_VOLTAGE - self.MIN_VOLTAGE))

    def power_consumption(self) -> float:
        """Return power consumption in mA."""
        # TODO
        return 0.0

    def is_critical_low(self) -> bool:
        """Return if the battery voltage is too low."""
        # TODO: critical low signal
        return self._battery_voltage <= self.LOW_VOLTAGE

    def status(self):
        """List of strings with module status."""

        def _voltage_text() -> str:
            if self._battery_voltage > self.MAX_VOLTAGE:
                return f"overvoltage: {self._battery_voltage} V"
            if self._battery_voltage < self.MIN_VOLTAGE:
                return f"undervoltage: {self._battery_voltage} V"
            return f"voltage: {self._battery_voltage} V"

        def _critical_low_text() -> str:
            if self.is_critical_low():
                return "critical low voltage"
            return ""

        return [
            f'charging: {self._charging}',
            _voltage_text(),
            _critical_low_text(),
            f'level: {self.battery_level()}%',
            f'using: {self.power_consumption()} mA',
        ]
