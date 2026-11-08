from wtforms import BooleanField, FileField, SelectField, StringField, TextAreaField
from wtforms.fields.html5 import IntegerField, URLField
from wtforms.widgets.html5 import NumberInput

from CTFd.constants.config import (
    AccountVisibilityTypes,
    ChallengeVisibilityTypes,
    RegistrationVisibilityTypes,
    ScoreVisibilityTypes,
)
from CTFd.constants.languages import SELECT_LANGUAGE_LIST
from CTFd.forms import BaseForm
from CTFd.forms.fields import SubmitField
from CTFd.utils.csv import get_dumpable_tables


class ResetInstanceForm(BaseForm):
    accounts = BooleanField(
        "账户",
        description="删除所有用户和团队账户及其相关数据",
    )
    submissions = BooleanField(
        "提交记录",
        description="删除所有账户获得积分或采取行动的记录",
    )
    challenges = BooleanField(
        "题目",
        description="删除所有题目及其相关数据"
    )
    pages = BooleanField(
        "页面",
        description="删除所有页面及其相关文件"
    )
    notifications = BooleanField(
        "通知", description="删除所有通知"
    )
    submit = SubmitField("重置CTF")


class AccountSettingsForm(BaseForm):
    domain_whitelist = StringField(
        "邮箱白名单",
        description="用户可以在允许的域名下注册 (比如 example.com *.example.com)",
    )
    team_creation = SelectField(
        "团队创建",
        description="控制用户是否可以创建自己的团队 (仅团队模式)",
        choices=[("true", "开启"), ("false", "关闭")],
        default="true",
    )
    team_size = IntegerField(
        "团队规模",
        widget=NumberInput(min=0),
        description="每个团队的最大用户数 (仅团队模式)",
    )
    num_teams = IntegerField(
        "最大团队数",
        widget=NumberInput(min=0),
        description="最大允许注册队伍数 (仅团队模式)",
    )
    num_users = IntegerField(
        "最大用户数",
        widget=NumberInput(min=0),
        description="最大允许注册的用户数",
    )
    verify_emails = SelectField(
        "验证邮箱",
        description="控制用户是否需要在开始前确认他们的邮箱",
        choices=[("true", "开启"), ("false", "关闭")],
        default="false",
    )
    team_disbanding = SelectField(
        "团队解散",
        description="控制团队队长是否被允许解散自己的团队",
        choices=[
            ("inactive_only", "为未激活的队伍开启"),
            ("disabled", "关闭"),
        ],
        default="inactive_only",
    )
    name_changes = SelectField(
        "名字更改",
        description="控制用户是否可以更改他们的用户名或团队名",
        choices=[("true", "开启"), ("false", "关闭")],
        default="true",
    )
    incorrect_submissions_per_min = IntegerField(
        "每分钟可以提交的错误答案数",
        widget=NumberInput(min=1),
        description="每分钟允许提交flag的次数，防止flag爆破 (默认: 10)",
    )

    submit = SubmitField("更新")


class ExportCSVForm(BaseForm):
    table = SelectField("数据表", choices=get_dumpable_tables())
    submit = SubmitField("下载CSV格式的表")


class ImportCSVForm(BaseForm):
    csv_type = SelectField(
        "CSV类型",
        choices=[("users", "个人"), ("teams", "团队"), ("challenges", "题目")],
        description="CSV表的类型",
    )
    csv_file = FileField("CSV文件", description="CSV文件")


class SocialSettingsForm(BaseForm):
    social_shares = SelectField(
        "社交分享",
        description="开启或关闭社交分享按钮",
        choices=[("true", "开启"), ("false", "关闭")],
        default="true",
    )
    submit = SubmitField("更新")


class LegalSettingsForm(BaseForm):
    tos_url = URLField(
        "条例连接",
        description="通往条例文件的外部链接",
    )
    tos_text = TextAreaField(
        "服务条例",
        description="展示在服务条例页面的文本",
    )
    privacy_url = URLField(
        "隐私政策链接",
        description="通往隐私政策文件的外部链接",
    )
    privacy_text = TextAreaField(
        "隐私政策",
        description="展示在隐私政策页面的文本",
    )
    submit = SubmitField("更新")


class VisibilitySettingsForm(BaseForm):
    challenge_visibility = SelectField(
        "题目可见性",
        description="控制用户是否需要登录才能查看题目",
        choices=[
            (ChallengeVisibilityTypes.PUBLIC, "开放"),
            (ChallengeVisibilityTypes.PRIVATE, "不开放"),
            (ChallengeVisibilityTypes.ADMINS, "仅管理员"),
        ],
        default=ChallengeVisibilityTypes.PRIVATE,
    )
    account_visibility = SelectField(
        "账户可见性",
        description="控制用户或队伍是显示给所有人、仅显示给经过身份验证的用户还是仅显示给管理员",
        choices=[
            (AccountVisibilityTypes.PUBLIC, "开放"),
            (AccountVisibilityTypes.PRIVATE, "不开放"),
            (AccountVisibilityTypes.ADMINS, "仅管理员"),
        ],
        default=AccountVisibilityTypes.PUBLIC,
    )
    score_visibility = SelectField(
        "分数可见性",
        description="控制解题/分数是否向公众、登录用户、所有非管理员隐藏或仅向管理员显示",
        choices=[
            (ScoreVisibilityTypes.PUBLIC, "开放"),
            (ScoreVisibilityTypes.PRIVATE, "不开放"),
            (ScoreVisibilityTypes.HIDDEN, "隐藏"),
            (ScoreVisibilityTypes.ADMINS, "仅管理员"),
        ],
        default=ScoreVisibilityTypes.PUBLIC,
    )
    registration_visibility = SelectField(
        "是否可注册",
        description="控制用户是否可注册",
        choices=[
            (RegistrationVisibilityTypes.PUBLIC, "开放"),
            (RegistrationVisibilityTypes.PRIVATE, "不开放"),
            (RegistrationVisibilityTypes.MLC, "仅MLC成员"),
        ],
        default=RegistrationVisibilityTypes.PUBLIC,
    )


class LocalizationForm(BaseForm):
    default_locale = SelectField(
        "默认语言",
        description="当用户未在账户设置设置语言时的默认语言 CTFd会自动检查用户的语言偏好",
        choices=SELECT_LANGUAGE_LIST,
    )
