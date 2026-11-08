from flask import url_for

from CTFd.utils import get_config
from CTFd.utils.config import get_mail_provider
from CTFd.utils.email.providers.mailgun import MailgunEmailProvider
from CTFd.utils.email.providers.smtp import SMTPEmailProvider
from CTFd.utils.formatters import safe_format
from CTFd.utils.security.email import (
    generate_email_confirm_token,
    generate_password_reset_token,
)

PROVIDERS = {"smtp": SMTPEmailProvider, "mailgun": MailgunEmailProvider}

DEFAULT_VERIFICATION_EMAIL_SUBJECT = "确认创建用户 {ctf_name}"
DEFAULT_VERIFICATION_EMAIL_BODY = (
    "欢迎{ctf_name}!\n\n"
    "点击下列链接确认注册:\n"
    "{url}"
    "\n\n"
    "如果链接不可点击，请复制到浏览器打开"
)
DEFAULT_SUCCESSFUL_REGISTRATION_EMAIL_SUBJECT = "成功注册用户{ctf_name}"
DEFAULT_SUCCESSFUL_REGISTRATION_EMAIL_BODY = (
    "你已经成功注册了{ctf_name}!"
)
DEFAULT_USER_CREATION_EMAIL_SUBJECT = "来自{ctf_name}的信息"
DEFAULT_USER_CREATION_EMAIL_BODY = (
    "一个新的名叫{ctf_name}的账户在{url}完成注册. \n\n"
    "用户名:{name}\n"
    "密码:{password}"
)
DEFAULT_PASSWORD_RESET_SUBJECT = "来自{ctf_name}的密码重置"
DEFAULT_PASSWORD_RESET_BODY = (
    "你确定要重置{ctf_name}的密码吗? "
    "如果你没有重置密码，请忽略这封邮件 \n\n"
    "点击链接重置密码\n{url}\n\n"
    "如果链接点不了，请复制到浏览器打开"
)
DEFAULT_PASSWORD_CHANGE_ALERT_SUBJECT = "确认为{ctf_name}重置密码"
DEFAULT_PASSWORD_CHANGE_ALERT_BODY = (
    "用户名{ctf_name}的密码已成功重置\n\n"
    "如果你没有要求更改密码或者被盗号了，可以在这里重置密码\n{url}\n\n"
    "如果链接点不了，请复制到浏览器打开"
)


def sendmail(addr, text, subject="来自{ctf_name}的信息"):
    subject = safe_format(subject, ctf_name=get_config("ctf_name"))
    provider = get_mail_provider()
    EmailProvider = PROVIDERS.get(provider)
    if EmailProvider is None:
        return False, "未配置邮箱信息"
    return EmailProvider.sendmail(addr, text, subject)


def password_change_alert(email):
    text = safe_format(
        get_config("password_change_alert_body") or DEFAULT_PASSWORD_CHANGE_ALERT_BODY,
        ctf_name=get_config("ctf_name"),
        ctf_description=get_config("ctf_description"),
        url=url_for("auth.reset_password", _external=True),
    )

    subject = safe_format(
        get_config("password_change_alert_subject")
        or DEFAULT_PASSWORD_CHANGE_ALERT_SUBJECT,
        ctf_name=get_config("ctf_name"),
    )
    return sendmail(addr=email, text=text, subject=subject)


def forgot_password(email):
    text = safe_format(
        get_config("password_reset_body") or DEFAULT_PASSWORD_RESET_BODY,
        ctf_name=get_config("ctf_name"),
        ctf_description=get_config("ctf_description"),
        url=url_for(
            "auth.reset_password",
            data=generate_password_reset_token(email),
            _external=True,
        ),
    )

    subject = safe_format(
        get_config("password_reset_subject") or DEFAULT_PASSWORD_RESET_SUBJECT,
        ctf_name=get_config("ctf_name"),
    )
    return sendmail(addr=email, text=text, subject=subject)


def verify_email_address(addr):
    text = safe_format(
        get_config("verification_email_body") or DEFAULT_VERIFICATION_EMAIL_BODY,
        ctf_name=get_config("ctf_name"),
        ctf_description=get_config("ctf_description"),
        url=url_for(
            "auth.confirm",
            data=generate_email_confirm_token(addr),
            _external=True,
            _method="GET",
        ),
    )

    subject = safe_format(
        get_config("verification_email_subject") or DEFAULT_VERIFICATION_EMAIL_SUBJECT,
        ctf_name=get_config("ctf_name"),
    )
    return sendmail(addr=addr, text=text, subject=subject)


def successful_registration_notification(addr):
    text = safe_format(
        get_config("successful_registration_email_body")
        or DEFAULT_SUCCESSFUL_REGISTRATION_EMAIL_BODY,
        ctf_name=get_config("ctf_name"),
        ctf_description=get_config("ctf_description"),
        url=url_for("views.static_html", _external=True),
    )

    subject = safe_format(
        get_config("successful_registration_email_subject")
        or DEFAULT_SUCCESSFUL_REGISTRATION_EMAIL_SUBJECT,
        ctf_name=get_config("ctf_name"),
    )
    return sendmail(addr=addr, text=text, subject=subject)


def user_created_notification(addr, name, password):
    text = safe_format(
        get_config("user_creation_email_body") or DEFAULT_USER_CREATION_EMAIL_BODY,
        ctf_name=get_config("ctf_name"),
        ctf_description=get_config("ctf_description"),
        url=url_for("views.static_html", _external=True),
        name=name,
        password=password,
    )

    subject = safe_format(
        get_config("user_creation_email_subject")
        or DEFAULT_USER_CREATION_EMAIL_SUBJECT,
        ctf_name=get_config("ctf_name"),
    )
    return sendmail(addr=addr, text=text, subject=subject)


def check_email_is_whitelisted(email_address):
    local_id, _, domain = email_address.partition("@")
    domain_whitelist = get_config("domain_whitelist")

    if domain_whitelist:
        domain_whitelist = [d.strip() for d in domain_whitelist.split(",")]

        for allowed_domain in domain_whitelist:
            if allowed_domain.startswith("*."):
                # domains should never container the "*" char
                if "*" in domain:
                    return False

                # Handle wildcard domain case
                suffix = allowed_domain[1:]  # Remove the "*" prefix
                if domain.endswith(suffix):
                    return True

            elif domain == allowed_domain:
                return True

        # whitelist is specified but the email doesn't match any domains
        return False

    # whitelist is not specified - allow all emails
    return True
