from wtforms import BooleanField, RadioField, StringField, TextAreaField
from wtforms.validators import InputRequired

from CTFd.forms import BaseForm
from CTFd.forms.fields import SubmitField


class NotificationForm(BaseForm):
    title = StringField("标题", description="通知标题")
    content = TextAreaField(
        "内容",
        description="通知内容 可以包含HTML或Markdown格式",
    )
    type = RadioField(
        "通知类型",
        choices=[("toast", "简短"), ("alert", "弹窗"), ("background", "后台")],
        default="toast",
        description="用户收到的通知类型",
        validators=[InputRequired()],
    )
    sound = BooleanField(
        "播放声音",
        default=True,
        description="在用户收到通知的时候播放声音",
    )
    submit = SubmitField("提交")
