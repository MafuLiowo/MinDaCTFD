from wtforms import RadioField

from CTFd.constants.languages import LANGUAGE_NAMES
from CTFd.forms import BaseForm


def LanguageForm(*args, **kwargs):
    from CTFd.utils.user import get_locale

    class _LanguageForm(BaseForm):
        """仅用于切换语言而不显示所有账户语言配置"""

        language = RadioField(
            "",
            choices=LANGUAGE_NAMES.items(),
            default=get_locale(),
        )

    return _LanguageForm(*args, **kwargs)
