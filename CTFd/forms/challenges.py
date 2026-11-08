from wtforms import MultipleFileField, SelectField, StringField
from wtforms.validators import InputRequired

from CTFd.forms import BaseForm
from CTFd.forms.fields import SubmitField


class ChallengeSearchForm(BaseForm):
    field = SelectField(
        "Search Field",
        choices=[
            ("name", "用户名"),
            ("id", "用户ID"),
            ("category", "题目类别"),
            ("type", "题目类型"),
        ],
        default="name",
        validators=[InputRequired()],
    )
    q = StringField("Parameter", validators=[InputRequired()])
    submit = SubmitField("Search")


class ChallengeFilesUploadForm(BaseForm):
    file = MultipleFileField(
        "上传文件",
        description="使用 Control+Click 或 Cmd+Click 附加多个文件。",
        validators=[InputRequired()],
    )
    submit = SubmitField("上传")
