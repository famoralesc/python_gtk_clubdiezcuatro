from django.utils.encoding import smart_unicode
from django.utils.translation import ugettext_lazy as _

class SValidarRutChileno:
    """
    Chilean "Rol Unico Tributario" (RUT) field. This is the Chilean national
    identification number.

    Samples for testing are available from
    https://palena.sii.cl/cvc/dte/ee_empresas_emisoras.html
    """
    default_error_messages = {
        'invalid': _('Enter a valid Chilean RUT.'),
        'strict': _('Enter a valid Chilean RUT. The format is XX.XXX.XXX-X.'),
        'checksum': _('The Chilean RUT is not valid.'),
    }

    def __init__(self, rut = None,  **kwargs):
        self.rut = rut
        
    def clean(self, value = None):
        """
        Check and clean the Chilean RUT.
        """
        if self.rut:
            value = self.rut
        rut, verificador = self._canonify(value)
        if self._algorithm(rut) == verificador:
            return self._format(rut, verificador)
        else:
            return False

    def _algorithm(self, rut):
        """
        Takes RUT in pure canonical form, calculates the verifier digit.
        """
        suma  = 0
        multi = 2
        for r in rut[::-1]:
            suma  += int(r) * multi
            multi += 1
            if multi == 8:
                multi = 2
        return u'0123456789K0'[11 - suma % 11]

    def _canonify(self, rut):
        """
        Turns the RUT into one normalized format. Returns a (rut, verifier)
        tuple.
        """
        rut = smart_unicode(rut).replace(' ', '').replace('.', '').replace('-', '')
        return rut[:-1], rut[-1]

    def _format(self, code, verifier=None):
        """
        Formats the RUT from canonical form to the common string representation.
        If verifier=None, then the last digit in 'code' is the verifier.
        """
        if verifier is None:
            verifier = code[-1]
            code = code[:-1]
        while len(code) > 3 and '.' not in code[:3]:
            pos = code.find('.')
            if pos == -1:
                new_dot = -3
            else:
                new_dot = pos - 3
            code = code[:new_dot] + '.' + code[new_dot:]
        return u'%s-%s' % (code, verifier)