from core.config import postgres_settings
from db.postgres import PostgreSQL
from fastapi import Request
from providers.yookassa_provider import get_yookassa
from services.providers_workers.yookassa import get_yookassa_worker


class ProviderDefiner:
    PROVIDERS = {
        "yookassa": get_yookassa,
        # Возможность добавить другие провайдеры
    }
    PROVIDERS_WORKERS = {
        "yookassa": get_yookassa_worker,
        # Возможность добавить другие провайдеры
    }

    @staticmethod
    async def get_payment_info_from_provider(payment_id: str, psql: PostgreSQL):
        transaction = await psql.get_object_by_id(
            postgres_settings.TRANSACTIONS_LOG_TABLE, payment_id
        )
        if not transaction:
            return
        provider_name = transaction["provider"]
        provider_get_func = ProviderDefiner.PROVIDERS.get(provider_name)
        if provider_get_func is None:
            raise ValueError(f"Unknown provider name: {provider_name}")
        provider = provider_get_func()
        return provider.get_payment_info(payment_id)

    @staticmethod
    async def webhook_confirmation(request: Request, provider_name: str, psql: PostgreSQL):
        provider_worker_get_func = ProviderDefiner.PROVIDERS_WORKERS.get(provider_name)
        if provider_worker_get_func is None:
            raise ValueError(f"Unknown provider name: {provider_name}")
        provider_worker = provider_worker_get_func()
        return await provider_worker.webhook_worker(request, psql)
