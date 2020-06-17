# _*_coding:utf-8_*_
# Created by #Suyghur, on 2020-02-26.
# Copyright (c) 2020 3KWan.
# Description :


class ParamsInfo:
    def __init__(self, info: dict):
        self.__common_params = info["common_params"]
        self.__channel_params = info["channel_params"]
        self.__plugin_params = info["plugin_params"]
        self.__game_params = info["game_params"]

    class __CommonParams:
        def __init__(self, info: dict):
            self.__game_id = info["game_id"]
            self.__package_chanle = info["package_chanle"]
            self.__total = info["total"]
            self.__channel_name = info["channel_name"]
            self.__channel_id = info["channel_id"]
            self.__deploy_id = info["deploy_id"]

        @property
        def game_id(self) -> str:
            return self.__game_id

        @property
        def package_chanle(self) -> dict:
            return self.__package_chanle

        @property
        def total(self) -> int:
            return self.__total

        @property
        def channel_name(self) -> str:
            return self.__channel_name

        @property
        def channel_id(self) -> str:
            return self.__channel_id

        @property
        def deploy_id(self) -> str:
            return self.__deploy_id

    class __GameParams:
        def __init__(self, info: dict):
            self.__game_package_name = info["game_package_name"]
            self.__game_name = info["game_name"]
            self.__game_version_code = info["game_version_code"]
            self.__game_version_name = info["game_version_name"]
            self.__game_orientation = info["game_orientation"]
            self.__game_icon_url = info["game_icon_url"]
            self.__game_logo_url = info["game_logo_url"]
            self.__game_splash_url = info["game_splash_url"]
            self.__game_background_url = info["game_background_url"]
            self.__game_loading_url = info["game_loading_url"]
            self.__game_resource_url = info["game_resource_url"]

        @property
        def game_package_name(self) -> str:
            return self.__game_package_name

        @property
        def game_name(self) -> str:
            return self.__game_name

        @property
        def game_version_code(self) -> str:
            return self.__game_version_code

        @property
        def game_version_name(self) -> str:
            return self.__game_version_name

        @property
        def game_orientation(self) -> str:
            return self.__game_orientation

        @property
        def game_icon_url(self) -> str:
            return self.__game_icon_url

        @property
        def game_logo_url(self) -> str:
            return self.__game_logo_url

        @property
        def game_splash_url(self) -> str:
            return self.__game_splash_url

        @property
        def game_background_url(self) -> str:
            return self.__game_background_url

        @property
        def game_loading_url(self) -> str:
            return self.__game_loading_url

        @property
        def game_resource_url(self) -> str:
            if self.__game_resource_url is None:
                return ""
            return self.__game_resource_url

    @property
    def common_params(self) -> __CommonParams:
        return self.__CommonParams(self.__common_params)

    @property
    def channel_params(self) -> dict:
        return self.__channel_params

    @property
    def plugin_params(self) -> dict:
        return self.__plugin_params

    @property
    def game_params(self) -> __GameParams:
        return self.__GameParams(self.__game_params)
