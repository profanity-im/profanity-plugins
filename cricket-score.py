import prof
import urllib2
import json

#_score_url = "http://api.scorescard.com/?type=score&teamone=Australia&teamtwo=England"
_score_url = None
_summary = None

def _cmd_cricket():
    global _score_url
    global _summary
    new_summary = None

    result_json = _retrieve_scores_json()

    if 'ms' in result_json.keys():
        new_summary = result_json['ms']

    prof.cons_show("")
    prof.cons_show("Cricket score:")
    if 't1FI' in result_json.keys():
        prof.cons_show("  " + result_json['t1FI'])

    if 't2FI' in result_json.keys():
        prof.cons_show("  " + result_json['t2FI'])

    if 't1SI' in result_json.keys():
        prof.cons_show("  " + result_json['t1SI'])

    if 't2SI' in result_json.keys():
        prof.cons_show("  " + result_json['t2SI'])

    _summary = new_summary
    prof.cons_show("")
    prof.cons_show("  " + _summary)
    prof.cons_alert()

def _get_scores():
    global _score_url
    global _summary
    notify = None
    new_summary = None
    change = False

    result_json = _retrieve_scores_json()

    if 'ms' in result_json.keys():
        new_summary = result_json['ms']
        if new_summary != _summary:
            change = True

    if change:
        prof.cons_show("")
        prof.cons_show("Cricket score:")
        if 't1FI' in result_json.keys():
            notify = result_json['t1FI']
            prof.cons_show("  " + result_json['t1FI'])

        if 't2FI' in result_json.keys():
            notify += "\n" + result_json['t2FI']
            prof.cons_show("  " + result_json['t2FI'])

        if 't1SI' in result_json.keys():
            notify += "\n" + result_json['t1SI']
            prof.cons_show("  " + result_json['t1SI'])

        if 't2SI' in result_json.keys():
            notify += "\n" + result_json['t2SI']
            prof.cons_show("  " + result_json['t2SI'])

        _summary = new_summary
        notify += "\n\n" + _summary
        prof.cons_show("")
        prof.cons_show("  " + _summary)
        prof.cons_alert()
        prof.notify(notify, 5000, "Cricket score")

def _retrieve_scores_json():
    req = urllib2.Request(_score_url, None, {'Content-Type': 'application/json'})
    f = urllib2.urlopen(req)
    response = f.read()
    f.close()
    return json.loads(response)
def prof_init(version, status):
    if _score_url:
        prof.register_timed(_get_scores, 60)
        prof.register_command("/cricket", 0, 0,
            "/cricket",
            "Get latest cricket score.",
            "Get latest cricket score.",
            _cmd_cricket)

def prof_on_start():
    if _score_url:
        _get_scores()
