from abc import ABC, abstractmethod
import json


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
        return (f"{self._name} - Būsena: {'ON' if self._status else 'OFF'}, "
                f"kanalas: {self._channel}, garsas: {self._volume}")


class Light(Device):
    def __init__(self, name, brightness):
        super().__init__(name)
        self._brightness = brightness

    def get_brightness(self):
        return self._brightness

    def set_brightness(self, brightness):
        self._brightness = brightness
        print(f"{self._name} nustatytas ryškumas: {self._brightness}%.")

    def device_info(self):
        return (f"{self._name} - Būsena: {'ON' if self._status else 'OFF'}, "
                f"Ryškumas: {self._brightness}%")


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
            print(f"{self._name} nustatyta temperatūra: {self._temperature}°C.")

    def device_info(self):
        return (f"{self._name} - Būsena: {'ON' if self._status else 'OFF'}, "
                f"Temperatura: {self._temperature}°C")


class Door(Device):
    def __init__(self, name, locked=False):
        super().__init__(name)
        self._locked = locked

    def get_status(self):
        return "Užrakinta" if self._locked else "Atrakinta"

    def set_status(self, status):
        self._locked = status
        print(f"{self._name} durys dabar yra "
              f"{'užrakintos' if self._locked else 'atrakintos'}.")

    def device_info(self):
        return f"{self._name} - Būsena: {self.get_status()}"


class Camera(Device):
    def __init__(self, name, resolution):
        super().__init__(name)
        self._resolution = resolution

    def get_resolution(self):
        return self._resolution

    def set_resolution(self, resolution):
        self._resolution = resolution
        print(f"{self._name} pakeista rezoliucija į {self._resolution}.")

    def device_info(self):
        return (f"{self._name} - Būsena: {'ON' if self._status else 'OFF'}, "
                f"Rezoliucija: {self._resolution}")


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
        raise ValueError(f"Nerastas įrenginys: {device_type}")


class Valdymas:
    def __init__(self, device_factory):
        self._device_factory = device_factory
        self.devices = []

    def create_device(self, device_type, name, *args, **kwargs):
        device = self._device_factory.create_device(
            device_type, name, *args, **kwargs)
        self.devices.append(device)
        print(f"{device.get_name()} įrenginys pridėtas.")
        return device

    def delete_device(self, device):
        if device in self.devices:
            self.devices.remove(device)
            print(f"{device.get_name()} įrenginys ištrintas.")

    def turn_on_all(self):
        for device in self.devices:
            device.turn_on()

    def turn_off_all(self):
        for device in self.devices:
            device.turn_off()

    def print_device_info(self):
        for device in self.devices:
            print(device.device_info())

    def leavehome(self):
        for device in self.devices:
            if isinstance(device, (Light, TV, AirConditioner)):
                device.turn_off()
            elif isinstance(device, Door):
                device.set_status(True)
            elif isinstance(device, Camera):
                device.turn_on()
        print("Režimas 'Išėjau iš namų' aktyvuotas.")

    def save_devices_to_file(self, filename="devices.json"):
        data = []
        for device in self.devices:
            device_data = {
                "type": type(device).__name__,
                "name": device.get_name(),
                "status": device.is_on()
            }
            if isinstance(device, TV):
                device_data.update({
                    "channel": device.get_channel(),
                    "volume": device.get_volume()
                })
            elif isinstance(device, Light):
                device_data["brightness"] = device.get_brightness()
            elif isinstance(device, AirConditioner):
                device_data["temperature"] = device.get_temperature()
            elif isinstance(device, Door):
                device_data["locked"] = device._locked
            elif isinstance(device, Camera):
                device_data["resolution"] = device.get_resolution()
            data.append(device_data)

        with open(filename, "w") as f:
            json.dump(data, f, indent=4)

    def load_devices_from_file(self, filename="devices.json"):
        try:
            with open(filename, "r") as f:
                data = json.load(f)

            for item in data:
                params = {k: v for k, v in item.items()
                         if k not in ("type", "name", "status")}
                device = self._device_factory.create_device(
                    item["type"], item["name"], **params)

                if item["status"]:
                    device.turn_on()
                else:
                    device.turn_off()

                self.devices.append(device)


        except FileNotFoundError:
            print("Nėra išsaugoto įrenginių failo.")


# Registruojame įrenginius
DeviceFactory.register_device("TV", TV)
DeviceFactory.register_device("Light", Light)
DeviceFactory.register_device("AirConditioner", AirConditioner)
DeviceFactory.register_device("Door", Door)
DeviceFactory.register_device("Camera", Camera)

valdymas = Valdymas(DeviceFactory)
valdymas.load_devices_from_file()



def show_menu():
    print("\nMeniu:")
    print("1. Įjungti visus įrenginius")
    print("2. Išjungti visus įrenginius")
    print("3. Rodyti įrenginių informaciją")
    print("4. Pridėti naują įrenginį")
    print("5. Ištrinti įrenginį")
    print("6. Aktyvuoti 'Išvykimo' režimą")
    print("7. Keisti parametrus")
    print("8. Įjungti/išjungti įrenginį")
    print("9. Išeiti")

    return input("Pasirinkite veiksmą: ")


def handle_tv_parameters(tv):
    param = input("Keisti (kanalas/garso lygis): ").lower()
    if param == "kanalas":
        tv.set_channel(int(input("Naujas kanalas: ")))
    elif param == "garso lygis":
        tv.set_volume(int(input("Naujas garsumas: ")))
    else:
        print("Neteisinga komanda.")


def handle_ac_parameters(ac):
    param = input("Keisti (temperatūra): ").lower()
    if param == "temperatūra":
        ac.set_temperature(int(input("Nauja temperatūra: ")))
    else:
        print("Neteisinga komanda.")


def handle_door_parameters(door):
    param = input("Keisti (užrakinti/atrakinti): ").lower()
    if param == "užrakinti":
        door.set_status(True)
    elif param == "atrakinti":
        door.set_status(False)
    else:
        print("Neteisinga komanda.")


def handle_light_parameters(light):
    param = input("Keisti (ryškumas): ").lower()
    if param == "ryškumas":
        light.set_brightness(int(input("Naujas ryškumas (0-100): ")))
    else:
        print("Neteisinga komanda.")

def handle_camera_parameters(camera):
    camera.set_resolution(input("Nauja rezoliucija: "))



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
            device_type = input("Įveskite įrenginio tipą (TV, Light, "
                              "AirConditioner, Door, Camera): ")
            name = input("Įveskite įrenginio pavadinimą: ")

            if device_type == "TV":
                channel = int(input("Įveskite kanalą: "))
                volume = int(input("Įveskite garsumą: "))
                valdymas.create_device(device_type, name, channel=channel, volume=volume)
            elif device_type == "Light":
                brightness = int(input("Įveskite ryškumą: "))
                valdymas.create_device(device_type, name,
                                      brightness=brightness)
            elif device_type == "AirConditioner":
                temperature = int(input("Įveskite temperatūrą: "))
                valdymas.create_device(device_type, name,
                                      temperature=temperature)
            elif device_type == "Door":
                status = input("Ar durys užrakintos? (True/False): ").lower() == 'true'
                valdymas.create_device(device_type, name, locked=status)

            elif device_type == "Camera":
                resolution = input("Įveskite rezoliuciją: ")
                valdymas.create_device(device_type, name, resolution=resolution)
        elif choice == "5":
            device_name = input("Įveskite įrenginio pavadinimą: ")
            device = next((d for d in valdymas.devices
                          if d.get_name() == device_name), None)
            if device:
                valdymas.delete_device(device)
            else:
                print("Įrenginys nerastas.")
        elif choice == "6":
            valdymas.leavehome()
        elif choice == "7":
            print("Pasirinkite įrenginio tipą:")
            print("1. TV\n2. Kondicionierius\n3. Durys\n4. Šviesa\n5. Kamera")
            device_choice = input("Įveskite numerį: ")

            if device_choice == "1":
                tvs = [d for d in valdymas.devices if isinstance(d, TV)]
                if tvs:
                    for i, tv in enumerate(tvs, 1):
                        print(f"{i}. {tv.get_name()}")
                    try:
                        selected = int(input("Pasirinkite TV: ")) - 1
                        handle_tv_parameters(tvs[selected])
                    except (ValueError, IndexError):
                        print("Netinkamas pasirinkimas.")
                else:
                    print("Nėra TV įrenginių.")
            if device_choice == "2":
                acs = [d for d in valdymas.devices if isinstance(d, AirConditioner)]
                if acs:
                    for i, ac in enumerate(acs, 1):
                        print(f"{i}. {ac.get_name()}")
                    try:
                        selected = int(input("Pasirinkite kondicionierių: ")) - 1
                        handle_ac_parameters(acs[selected])
                    except (ValueError, IndexError):
                        print("Netinkamas pasirinkimas.")
                else:
                    print("Nėra kondicionieriaus įrenginių.")
            if device_choice == "3":
                doors = [d for d in valdymas.devices if isinstance(d, Door)]
                if doors:
                    for i, door in enumerate(doors, 1):
                        print(f"{i}. {door.get_name()}")
                    try:
                        selected = int(input("Pasirinkite durį: ")) - 1
                        handle_door_parameters(doors[selected])
                    except (ValueError, IndexError):
                        print("Netinkamas pasirinkimas.")
                else:
                    print("Nėra tokių durų.")
            if device_choice == "4":
                lights = [d for d in valdymas.devices if isinstance(d, Light)]
                if lights:
                    for i, light in enumerate(lights, 1):
                        print(f"{i}. {light.get_name()}")
                    try:
                        selected = int(input("Pasirinkite šviesą: ")) - 1
                        handle_light_parameters(lights[selected])
                    except (ValueError, IndexError):
                        print("Netinkamas pasirinkimas.")
                else:
                    print("Nėra šviesos įrenginių.")

            if device_choice == "5":
                cameras = [d for d in valdymas.devices if isinstance(d, Camera)]
                if cameras:
                    for i, camera in enumerate(cameras, 1):
                        print(f"{i}. {camera.get_name()}")
                    try:
                        selected = int(input("Pasirinkite kamerą: ")) - 1
                        handle_camera_parameters(cameras[selected])
                    except (ValueError, IndexError):
                        print("Netinkamas pasirinkimas.")
                else:
                    print("Nėra kamerų.")

        elif choice == "8":
            for i, d in enumerate(valdymas.devices, 1):
                print(f"{i}. {d.get_name()}  ({'ON' if d.is_on() else 'OFF'})")
            try:
                pasirinktas = int(input("Pasirinkite įrenginį: ")) - 1
                if 0 <= pasirinktas < len(valdymas.devices):
                    veiksmas = input("Įjungti ar išjungti? ").lower()
                    if veiksmas == "įjungti":
                        valdymas.devices[pasirinktas].turn_on()
                    elif veiksmas == "išjungti":
                        valdymas.devices[pasirinktas].turn_off()
                    else:
                        print("Neteisingas veiksmas.")
                else:
                    print("Netinkamas pasirinkimas.")
            except:
                print("Klaida pasirenkant įrenginį.")

        elif choice == "9":
            valdymas.save_devices_to_file()
            print("Programa baigta. Įrenginiai išsaugoti.")
            break
        else:
            print("Neteisingas pasirinkimas.")



if __name__ == "__main__":
    main()