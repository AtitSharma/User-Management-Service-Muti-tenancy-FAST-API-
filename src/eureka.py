from py_eureka_client.eureka_client import EurekaClient

from src.config import settings


class EurekaAuth:

    try:
        eureka_client = EurekaClient(
            eureka_server=settings.EUREKA_SERVER_URL,
            app_name=settings.EUREKA_SERVER_UMS_NAME,
            instance_port=int(settings.UMS_SERVER_PORT),
        )
    except Exception as e:
        print("Failed to register with Eureka:", e)

    @classmethod
    async def register_with_eureka(cls):
        await cls.eureka_client.start()

    @classmethod
    async def unregister_from_eureka(cls):
        await cls.eureka_client.stop()
