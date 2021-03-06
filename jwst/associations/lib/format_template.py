"""FormatTemplate

Format template string allowing partial formatiing.
"""
from collections import defaultdict
from string import Formatter

__all__ = ['FormatTemplate']


class FormatTemplate(Formatter):
    """Format a template

    Parameters
    ----------
    template: str
        A Python format string

    separator: string
        Separater to use for values which have no
        matching replacement strings

    kwargs: dict or named parameters
        The key/values pairs to fill into the Python format string

    Returns
    -------
    str
        The formatted string

    Notes
    -----
    This differences from Pythons `format` method are:
        - If a replacement field does not have a given value,
          the replacement field is left in the result
        - If a key/value pair is present but has no replacement field,
          the value is simply appended.
        - Template can only use named replacement fields.

    Examples
    --------
    The basic example:
    >>> template = 'name="{name}" value="{value}"'
    >>> fmt = FormatTemplate()
    >>> fmt(template)
    'name="{name}" value="{value}"'

    But with actual values given:
    >>> fmt(template, name='fred', value='great')
    'name="fred" value="great"'

    But wait, too many values given:
    >>> fmt(template, name='fred', value='great', extra='more')
    'name="fred" value="great"_more'

    And with too many and not enough:
    >>> fmt(template, value='great', extra='more')
    'name="{name}" value="great"_more'

    With a different separator:
    >>> fmt.separator = '---'
    >>> fmt(template, name='fred', value='great', extra='more')
    'name="fred" value="great"---more'

    Initializing with a different separator:
    >>> fmt_newsep = FormatTemplate(separator='_now-with_')
    >>> fmt_newsep(template, name='fred', value='great', extra='more')
    'name="fred" value="great"_now-with_more'

    Setup preformatting
    >>> key_formats = {'value': 'pre_{:s}_format'}
    >>> fmt_preformat = FormatTemplate(key_formats=key_formats)
    >>> fmt_preformat(template, name='fred', value='great')
    'name="fred" value="pre_great_format"'
    """
    def __init__(self, separator='_', key_formats=None):
        """Inialize class

        Parameters
        ----------
        separator: str
            For key/value pairs given that do not have a
            replacement field, the values are appened to
            the string using this separator.

        key_formats: {key: format(, ...)}
            dict of formats to pre-format the related values
            before insertion into the the template
        """
        super(FormatTemplate, self).__init__()
        self.separator = separator

        self.key_formats = defaultdict(lambda: '{}')
        if key_formats:
            self.key_formats.update(key_formats)

    def format(self, format_string, **kwargs):
        """Perform the formatting

        Parameters
        ----------
        format_string: str
            The string to be formatted

        kwargs: dict
            The key/value pairs to insert into the string

        Returns
        -------
        formatted: str
            The formatted string.
        """
        self._used_keys = []

        # Preformat the values
        formatted_kwargs = {
            key: self.key_formats[key].format(value)
            for key,value in kwargs.items()
        }
        result = super(FormatTemplate, self).format(format_string, **formatted_kwargs)

        # Get any unused arguments and simply do the appending
        unused_keys = set(formatted_kwargs).difference(self._used_keys)
        unused_values = [formatted_kwargs[unused] for unused in unused_keys]
        result_parts = [result] + unused_values
        result = self.separator.join(result_parts)

        return result
    __call__ = format

    def get_value(self, key, args, kwargs):
        """Return a given field value

        Parameters
        ----------
        key: str
            The key to retrieve.

        args: [arg(, ...)]
            Positional arguments passed.
            This is ignored.

        kwargs: {k:v(, ...)}
            The key/value pairs passed in.

        Returns
        -------
        obj
            The value from the kwargs.
            If not found, the string '{key}' is returned.
        """
        value = kwargs.get(key, '{' + key + '}')
        self._used_keys.append(key)

        return value
