from dependency_injector import containers, providers

from core.config import Settings


from services.openai_service import OpenAIClient


class Container(containers.DeclarativeContainer):

    config = providers.Singleton(Settings)

    openai_client = providers.Singleton(
        OpenAIClient,
        api_key=config.provided.openai_api_key,
        assistant_id=config.provided.assistant_id,
        proxy_url=config.provided.proxy_url,
    )
    # endregion
