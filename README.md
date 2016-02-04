# querystring_tools

Tools to debug & compare query strings. 

Consists of a flask server with a simple interface for pasting query strings. 

## Usage

`http://localhost:5000/query/parse`

Paste a query string, get a list of all parameters and their values.

`http://localhost:5000/query/compare`

Paste two query strings and see the difference between them; added, removed and changed values.