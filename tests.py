import unittest
from unittest.mock import patch
from io import StringIO
from main import TV, Light, AirConditioner, Door, Camera, DeviceFactory, Valdymas


class TestDeviceMethods(unittest.TestCase):
    def setUp(self):
        # Sukuriame valdymo objektą su pradiniu įrenginių fabriku
        self.device_factory = DeviceFactory()
        self.valdymas = Valdymas(self.device_factory)
        
    # Testas TV įrenginiui
    def test_tv_device(self):
        tv = TV("Samsung TV", 1, 20)  # Sukuriame TV įrenginį
        self.assertEqual(tv.get_name(), "Samsung TV")
        self.assertEqual(tv.get_channel(), 1)
        self.assertEqual(tv.get_volume(), 20)
        tv.turn_on()
        self.assertTrue(tv.is_on())
        tv.set_channel(5)
        self.assertEqual(tv.get_channel(), 5)
        tv.set_volume(30)
        self.assertEqual(tv.get_volume(), 30)

    # Testas Light įrenginiui
    def test_light_device(self):
        light = Light("Living Room Light", 50)  # Sukuriame šviesos įrenginį
        self.assertEqual(light.get_name(), "Living Room Light")
        self.assertEqual(light.get_brightness(), 50)
        light.turn_on()
        self.assertTrue(light.is_on())
        light.set_brightness(75)
        self.assertEqual(light.get_brightness(), 75)

    # Testas AirConditioner įrenginiui
    def test_air_conditioner_device(self):
        ac = AirConditioner("Bedroom AC", 22)  # Sukuriame kondicionierių
        self.assertEqual(ac.get_name(), "Bedroom AC")
        self.assertEqual(ac.get_temperature(), 22)
        ac.turn_on()
        self.assertTrue(ac.is_on())
        ac.set_temperature(18)
        self.assertEqual(ac.get_temperature(), 18)

    # Testas Door įrenginiui
    def test_door_device(self):
        door = Door("Front Door", False)  # Sukuriame durų įrenginį
        self.assertEqual(door.get_name(), "Front Door")
        self.assertEqual(door.get_status(), "Atrakinta")
        door.turn_on()
        self.assertTrue(door.is_on())
        door.set_status(True)
        self.assertEqual(door.get_status(), "Užrakinta")

    # Testas Camera įrenginiui
    def test_camera_device(self):
        camera = Camera("Security Camera", "1080p")  # Sukuriame kamerą
        self.assertEqual(camera.get_name(), "Security Camera")
        self.assertEqual(camera.get_resolution(), "1080p")
        camera.turn_on()
        self.assertTrue(camera.is_on())
        camera.set_resolution("4K")
        self.assertEqual(camera.get_resolution(), "4K")


class TestValdymasMethods(unittest.TestCase):
    def setUp(self):
        # Sukuriame Valdymas objektą su įrenginių fabriku
        self.device_factory = DeviceFactory()
        self.valdymas = Valdymas(self.device_factory)

    # Testas, ar įrenginiai sėkmingai pridedami
    def test_create_device(self):
        tv = self.valdymas.create_device("TV", "Samsung TV", channel=1, volume=10)
        self.assertIn(tv, self.valdymas.devices)
        self.assertEqual(tv.get_name(), "Samsung TV")
    
    # Testas, ar įrenginiai sėkmingai ištrinami
    def test_delete_device(self):
        tv = self.valdymas.create_device("TV", "Samsung TV", channel=1, volume=10)
        self.valdymas.delete_device(tv)
        self.assertNotIn(tv, self.valdymas.devices)

    # Testas, ar visi įrenginiai sėkmingai įjungiami
    def test_turn_on_all_devices(self):
        tv = self.valdymas.create_device("TV", "Samsung TV", channel=1, volume=10)
        light = self.valdymas.create_device("Light", "Living Room Light", brightness=50)
        self.valdymas.turn_on_all()
        self.assertTrue(tv.is_on())
        self.assertTrue(light.is_on())

    # Testas, ar visi įrenginiai sėkmingai išjungiami
    def test_turn_off_all_devices(self):
        tv = self.valdymas.create_device("TV", "Samsung TV", channel=1, volume=10)
        light = self.valdymas.create_device("Light", "Living Room Light", brightness=50)
        self.valdymas.turn_off_all()
        self.assertFalse(tv.is_on())
        self.assertFalse(light.is_on())

    # Testas, ar informaciją apie įrenginius spausdinama teisingai
    def test_print_device_info(self):
        tv = self.valdymas.create_device("TV", "Samsung TV", channel=1, volume=10)
        light = self.valdymas.create_device("Light", "Living Room Light", brightness=50)
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            self.valdymas.print_device_info()
            output = mock_stdout.getvalue()
            self.assertIn("Samsung TV", output)
            self.assertIn("Living Room Light", output)

    # Testas režimo 'Išėjau iš namų' aktyvavimas
    def test_leave_home_mode(self):
        tv = self.valdymas.create_device("TV", "Samsung TV", channel=1, volume=10)
        light = self.valdymas.create_device("Light", "Living Room Light", brightness=50)
        door = self.valdymas.create_device("Door", "Front Door", locked=False)
        self.valdymas.leavehome()
        self.assertFalse(tv.is_on())
        self.assertFalse(light.is_on())
        self.assertTrue(door.get_status() == "Užrakinta")


if __name__ == "__main__":
    unittest.main()
