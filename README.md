# formed2formbar
Helpers to convert a XML form definition from `formed` to `formbar`

The tool is able to extract information on field in a form written in `formed`
format and output these fields as `formabar` entities.  Only enties are
converted. No layout is converted. You will need to rebuild the forms.

The following features are supported for enties:

- ID
- Label
- Name
- Type (string, integer, date)
- Options (from choices)
- Desired-Flag

**TODO:**

- Help
- Rules
- Layout
