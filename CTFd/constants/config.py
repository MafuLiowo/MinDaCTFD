import json

from flask import url_for

from CTFd.constants import JinjaEnum, RawEnum
from CTFd.utils import get_config


class ConfigTypes(str, RawEnum):
    CHALLENGE_VISIBILITY = "题目可见性"
    SCORE_VISIBILITY = "分数可见性"
    ACCOUNT_VISIBILITY = "账户可见性"
    REGISTRATION_VISIBILITY = "是否可注册"


@JinjaEnum
class UserModeTypes(str, RawEnum):
    USERS = "个人"
    TEAMS = "团队"


@JinjaEnum
class ChallengeVisibilityTypes(str, RawEnum):
    PUBLIC = "公开"
    PRIVATE = "不公开"
    ADMINS = "仅管理员"


@JinjaEnum
class ScoreVisibilityTypes(str, RawEnum):
    PUBLIC = "公开"
    PRIVATE = "不公开"
    HIDDEN = "隐藏"
    ADMINS = "仅管理员"


@JinjaEnum
class AccountVisibilityTypes(str, RawEnum):
    PUBLIC = "公开"
    PRIVATE = "不公开"
    ADMINS = "仅管理员"


@JinjaEnum
class RegistrationVisibilityTypes(str, RawEnum):
    PUBLIC = "公开"
    PRIVATE = "不公开"
    MLC = "仅MLC成员"


class _ConfigsWrapper:
    def __getattr__(self, attr):
        return get_config(attr)

    @property
    def ctf_name(self):
        return get_config("ctf_name", default="CTFd")

    @property
    def ctf_small_icon(self):
        icon = get_config("ctf_small_icon")
        if icon:
            return url_for("views.files", path=icon)
        return url_for("views.themes", path="img/favicon.ico")

    @property
    def theme_header(self):
        from CTFd.utils.helpers import markup

        return markup(get_config("theme_header", default=""))

    @property
    def theme_footer(self):
        from CTFd.utils.helpers import markup

        return markup(get_config("theme_footer", default=""))

    @property
    def theme_settings(self):
        try:
            return json.loads(get_config("theme_settings", default="null"))
        except json.JSONDecodeError:
            return {"error": "invalid theme_settings"}

    @property
    def tos_or_privacy(self):
        tos = bool(get_config("tos_url") or get_config("tos_text"))
        privacy = bool(get_config("privacy_url") or get_config("privacy_text"))
        return tos or privacy

    @property
    def tos_link(self):
        return get_config("tos_url", default=url_for("views.tos"))

    @property
    def privacy_link(self):
        return get_config("privacy_url", default=url_for("views.privacy"))


Configs = _ConfigsWrapper()
