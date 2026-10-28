// 时间渲染约定:
//   后端 _fmt_time() 输出的是"北京时间字符串" —— 作为无 JS 时(以及 view-source)的兜底;
//   后端 _iso_utc() 额外给出带 Z 的 ISO8601 —— 供本文件用 dayjs 按【访客本地时区】重新渲染。
//   两者同时存在时,以本地时区那份为准。

function fmtLocal(iso) {
    if (!iso || typeof dayjs === 'undefined') return null;
    var d = dayjs(iso);                       // 带 Z 的 ISO -> dayjs 默认按浏览器本地时区格式化
    return d.isValid() ? d.format('YYYY-MM-DD HH:mm:ss') : null;
}

// 自带的 HTML 转义(原来依赖主题的 js/utils.js,但 xuan 主题里并没有这个文件)
function escHtml(v) {
    return String(v === undefined || v === null ? '' : v)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#39;');
}

// 首屏:服务端已经把北京时间写进单元格,这里按访客本地时区覆盖一次
function fillTimes() {
    $('[data-time]').each(function () {
        var $cell = $(this);
        var local = fmtLocal($cell.attr('data-time'));
        if (local) $cell.text(local);
    });
}

function updatescores() {
    $.get(script_root + '/scores', function (data) {
        var standings = data.standings;
        var tbody = $('#scoreboard > tbody');
        tbody.empty();
        for (var i = 0; i < standings.length; i++) {
            var s = standings[i];
            var local = fmtLocal(s.last_solve_time_iso);
            // 刷新出来的行不会再经过主题的 times(),所以这里直接给最终文本,
            // 同时保留 data-time 属性,方便其它脚本再次格式化(如切换时区插件)。
            var timeCell =
                '<td data-time="' + (s.last_solve_time_iso || '') + '" data-time-format="YYYY-MM-DD HH:mm:ss">' +
                (local || s.last_solve_time || '-') +
                '</td>';
            tbody.append(
                '<tr>' +
                '<td class="text-center">' + (i + 1) + '</td>' +
                '<td><a href="/user/' + s.id + '">' + escHtml(s.team) + '</a></td>' +
                '<td>' + s.score + '</td>' +
                '<td>' + s.solve_count + '</td>' +
                timeCell +
                '</tr>'
            );
        }
    });
}

function update() {
    updatescores();
}

$(function () {
    fillTimes();
    setInterval(update, 300000);   // 每 5 分钟刷新一次
});
