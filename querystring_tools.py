import urllib.request, urllib.parse
from flask import Flask, request
from flask import render_template

app = Flask(__name__)


def parse_string(query):
    if not query:
        return dict()
    params = urllib.parse.parse_qs(query)
    return {n: ','.join(v) for n,v in params.items() }


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
    old_params = {}
    old_query = ""
    new_params = {}
    new_query = ""
    summary = False
    added, removed, changed, keys = dict(), dict(), dict(), dict()
    if request.method == 'POST':
        if 'query1' in request.form:
            old_query = request.form['query1']
            old_params = parse_string(old_query)
        if 'query2' in request.form:
            new_query = request.form['query2']
            new_params = parse_string(new_query)
        if 'summary' in request.form:
            summary = True
        added, removed, changed, keys = diff(old_params, new_params)
    return render_template('compare.html.j2',
                           old_values={'query': old_query,
                                       'params': old_params},
                           new_values={'query': new_query,
                                       'params': new_params},
                           data={'names': keys,
                                 'added': added,
                                 'removed': removed,
                                 'changed': changed},
                           summary=summary)


if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)
