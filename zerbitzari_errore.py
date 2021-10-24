from typing import Final

class ErroreaEskaeran(Exception):
    def __init__(self, errorekodea=0, erroredeskrib=''):
        self.errore_kodea = errorekodea
        self.errore_mezua = erroredeskrib

    def get_errore_kode(self):
        return self.errore_kodea

    def __repr__(self):
        mezua = "Err " + str(self.get_errore_kode())
        if self.errore_mezua:
            mezua += ": " + self.errore_mezua
        return mezua

class ErrKomandoEzezaguna(ErroreaEskaeran):
    OINARRIZKO_ERR_KODE: Final[int] = 1

    def __init__(self, erroredeskrib=''):
        super().__init__(self.OINARRIZKO_ERR_KODE, erroredeskrib)


class ErrEzEsperoParam(ErroreaEskaeran):
    OINARRIZKO_ERR_KODE: Final[int] = 2

    def __init__(self, erroredeskrib=''):
        super().__init__(self.OINARRIZKO_ERR_KODE, erroredeskrib)


class ErrHautaParamFalta(ErroreaEskaeran):
    OINARRIZKO_ERR_KODE: Final[int] = 3

    def __init__(self, erroredeskrib=''):
        super().__init__(self.OINARRIZKO_ERR_KODE, erroredeskrib)


class ErrParamFormatuEzEgoki(ErroreaEskaeran):
    OINARRIZKO_ERR_KODE: Final[int] = 4

    def __init__(self, erroredeskrib=''):
        super().__init__(self.OINARRIZKO_ERR_KODE, erroredeskrib)

