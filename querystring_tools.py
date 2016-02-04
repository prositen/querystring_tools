import urllib.request
from flask import Flask, request
from flask import render_template

app = Flask(__name__)


def parse_string(query):
    if not query:
        return dict()
    params = dict()
    unquote_query = urllib.request.unquote(query.strip())
    for item in unquote_query.split('&'):
        nv = item.split('=', 2)
        name = nv[0]
        value = ""
        if len(nv) == 2:
            value = nv[1]
        params[name] = value
    return params


def diff(old_params, new_params):
    """
    Get the changes between old_params and new_params
    :param old_params: Parameters from first query string
    :param new_params: Parameters from second query string
    :return: added, removed, changed
    """
    old_keys = set(old_params.keys())
    new_keys = set(new_params.keys())

    added_keys = new_keys - old_keys
    added = {key: new_params[key] for key in added_keys}

    removed_keys = old_keys - new_keys
    removed = {key: old_params[key] for key in removed_keys}

    common_keys = old_keys.intersection(new_keys)
    changed = dict()
    for key in common_keys:
        old_value = old_params[key]
        new_value = new_params[key]
        if old_value != new_value:
            changed[key] = (old_value, new_value)

    keys = old_keys.union(new_keys)
    return added, removed, changed, keys


@app.route('/query/parse', methods=['GET', 'POST'])
def parse():
    params = dict()
    if request.method == 'POST':
        if 'query' in request.form:
            params = parse_string(request.form['query'])
    return render_template('query.html.j2',
                           values=params)


@app.route('/query/compare', methods=['GET', 'POST'])
def compare():
    params1 = {}
    query1 = ""
    params2 = {}
    query2 = ""
    summary = False
    added, removed, changed, keys = dict(), dict(), dict(), dict()
    if request.method == 'POST':
        if 'query1' in request.form:
            query1 = request.form['query1']
            params1 = parse_string(query1)
        if 'query2' in request.form:
            query2 = request.form['query2']
            params2 = parse_string(query2)
        if 'summary' in request.form:
            summary = True
        added, removed, changed, keys = diff(params1, params2)
    return render_template('compare.html.j2',
                           query1=query1,
                           query2=query2,
                           values1=params1,
                           values2=params2,
                           keys=keys,
                           added=added,
                           removed=removed,
                           changed=changed,
                           summary=summary)


if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)
