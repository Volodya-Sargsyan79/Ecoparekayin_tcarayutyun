from gps_server.services.device_service import DeviceService


class IMEIHandler:

    @staticmethod
    def authenticate(imei):

        device = DeviceService.get_device(imei)

        if device:
            return True

        return False