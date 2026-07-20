from apps.gps.models import Device


class DeviceService:

    @staticmethod
    def get_device(imei):

        return Device.objects.filter(
            imei=imei,
            is_active=True
        ).first()