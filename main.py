
from abc import ABC, abstractmethod

class Device(ABC):
    def __init__(self, name):
        self._name = name
        self._status = False

    def get_name(self):
        return self._name

    def is_on(self):
        return self._status

    def turn_on(self):
        self._status = True
        print(f"{self._name} įjungtas.")

    def turn_off(self):
        self._status = False
        print(f"{self._name} išjungtas.")

    @abstractmethod
    def device_info(self):
        pass

class TV(Device):
    def __init__(self, name, channel, volume):
        super().__init__(name)
        self._channel = channel
        self._volume = volume

    def get_channel(self):
        return self._channel

    def get_volume(self):
        return self._volume

    def set_channel(self, channel):
        self._channel = channel
        print(f"{self._name} perjungtas į kanalą {self._channel}.")

    def set_volume(self, volume):
        self._volume = volume
        print(f"{self._name} nustatytas garsas {self._volume}.")

    def device_info(self):
        return f"{self._name} -  Būsena: {'ON' if self._status else 'OFF'}, kanalas: {self._channel}, garsas: {self._volume}"

class Light(Device):
    def __init__(self, name, brightness):
        super().__init__(name)
        self._brightness = brightness


    def get_brightness(self):
        return self._brightness

    def set_brightness(self, brightness):
        self._brightness = brightness
        print(f"{self._name} nustatytas ryškumas: {self._brightness} %.")

    def device_info(self):
        return f"{self._name} - Būsena: {'ON' if self._status else 'OFF'}, Ryškumas: {self._brightness} %"

class AirConditioner(Device):
    def __init__(self, name, temperature):
        super().__init__(name)
        self._temperature = temperature

    def get_temperature(self):
        return self._temperature

    def set_temperature(self, temperature):
        if temperature < -5 or temperature > 30:
            print("Tokia temperatūra negalima")
        else:
            self._temperature = temperature
            print(f"{self._name} nustatyta temperatura: {self._temperature} C.")

    def device_info(self):
        return f"{self._name} - Būsena: {'ON' if self._status else 'OFF'}, Temperatura: {self._temperature} C"

class Door(Device):
    def __init__(self, name, locked=False):
        super().__init__(name)
        self._locked = locked

    def get_status(self):
        return "Užrakinta" if self._locked else "Atrakinta"

    def set_status(self, status):
        self._locked = locked
        print(f"{self._name} durys dabar yra {'užrakintos' if self._locked else 'atrakintos'}.")

    def device_info(self):
        return f"{self._name} - Būsena: {'Užrakinta' if self._locked else 'Atrakinta'}"

class Camera(Device):
    def __init__(self, name, resolution):
        super().__init__(name)
        self._resolution = resolution

    def get_resolution(self):
        return self._resolution

    def set_resolution(self, resolution):
        self._resolution = resolution
        print(f"{self._name} pakeistas į {self._resolution} pikselių.")

    def device_info(self):
        return f"{self._name} - Būsena: {'ON' if self._status else 'OFF'}, Resolucija: {self._resolution} pikselių"


class DeviceFactory:
    _device_registry = {}

    @staticmethod
    def register_device(device_type, device_class):
        DeviceFactory._device_registry[device_type] = device_class

    @staticmethod
    def create_device(device_type, name, *args, **kwargs):
        device_class = DeviceFactory._device_registry.get(device_type)
        if device_class:
            return device_class(name, *args, **kwargs)
        else:
            raise ValueError(f"Nerastas įrenginys: {device_type}")

class Valdymas:
    def __init__(self, device_factory):
        self._device_factory = device_factory
        self.devices = []

    def create_device(self, device_type, name, *args, **kwargs):
        device = self._device_factory.create_device(device_type, name, *args, **kwargs)
        self.devices.append(device)
        print(f"{device.get_name()} įrenginys pridėtas į valdymą.")
        return device


    def turn_on_all(self):
        for device in self.devices:
            device.turn_on()

    def turn_off_all(self):
        for device in self.devices:
            device.turn_off()

    def print_device_info(self):
        for device in self.devices:
            print(device.device_info())
    def delete_device(self, device):
        if device in self.devices:
            self.devices.remove(device)
            print(f"{device.get_name()} įrenginys ištrintas iš valdymo.")

    def leavehome(self):
      for device in self.devices:
        if isinstance(device, Light) or isinstance(device, TV) or isinstance(device, AirConditioner):
            device.turn_off()
        elif isinstance(device, Door):
            device.set_status(True)
        elif isinstance(device, Camera):
            device.turn_on()
            print("Režimas 'Išėjau iš namų' aktyvuotas.")

DeviceFactory.register_device("TV", TV)
DeviceFactory.register_device("Light", Light)
DeviceFactory.register_device("AirConditioner", AirConditioner)
DeviceFactory.register_device("Door", Door)
DeviceFactory.register_device("Camera", Camera)

valdymas = Valdymas(DeviceFactory)

tv = valdymas.create_device("TV", "Living Room TV", channel=5, volume=10)
light = valdymas.create_device("Light", "Kitchen Light", brightness=70)
ac = valdymas.create_device("AirConditioner", "Bedroom AC", temperature=10)
door = valdymas.create_device("Door", "Front Door", locked=False)
camera = valdymas.create_device("Camera", "Security Camera", resolution="1080p")
print("\n")

def show_menu():
    print("\nMeniu:")
    print("1. Įjungti visus įrenginius")
    print("2. Išjungti visus įrenginius")
    print("3. Rodyti visų įrenginių informaciją")
    print("4. Pridėti naują įrenginį")
    print("5. Ištrinti įrenginį")
    print("6. Aktyvuoti 'Išvykimo' režimą")
    print("7. Išeiti")
    choice = input("Pasirinkite veiksmą: ")
    return choice

def main():


    while True:
        choice = show_menu()

        if choice == "1":
            valdymas.turn_on_all()
        elif choice == "2":
            valdymas.turn_off_all()
        elif choice == "3":
            valdymas.print_device_info()
        elif choice == "4":
            device_type = input("Įveskite įrenginio tipą (TV, Light, AirConditioner, Door, Camera): ")
            name = input("Įveskite įrenginio pavadinimą: ")
            if device_type == "TV":
                channel = int(input("Įveskite kanalą: "))
                volume = int(input("Įveskite garsumą: "))
                valdymas.create_device(device_type, name, channel=channel, volume=volume)
            elif device_type == "Light":
                brightness = int(input("Įveskite ryškumą: "))
                valdymas.create_device(device_type, name, brightness=brightness)
            elif device_type == "AirConditioner":
                temperature = int(input("Įveskite temperatūrą: "))
                valdymas.create_device(device_type, name, temperature=temperature)
            elif device_type == "Door":
                status = input("Ar durys užrakintos? (True/False): ").lower() == 'true'
                valdymas.create_device(device_type, name, locked=status)
            elif device_type == "Camera":
                resolution = input("Įveskite kameros rezoliuciją: ")
                valdymas.create_device(device_type, name, resolution=resolution)
        elif choice == "5":
            device_name = input("Įveskite įrenginio, kurį norite ištrinti, pavadinimą: ")
            device = next((d for d in valdymas.devices if d.get_name() == device_name), None)
            if device:
                valdymas.delete_device(device)
            else:
                print("Įrenginys nerastas.")
        elif choice == "6":
            valdymas.leavehome()
        elif choice == "7":
            print("Išeinama iš programos.")
            break
        else:
            print("Neteisingas pasirinkimas, pabandykite dar kartą.")

if __name__ == "__main__":
    main()







