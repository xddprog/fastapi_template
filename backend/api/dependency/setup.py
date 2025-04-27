from dishka import AsyncContainer, make_async_container
from dishka.integrations.fastapi import FastapiProvider

from backend.api.dependency.providers.app import AppProvider
from backend.api.dependency.providers.request import RequestProvider


def setup_container() -> AsyncContainer:
    return make_async_container(
        AppProvider(),
        RequestProvider(),
        FastapiProvider()
    )