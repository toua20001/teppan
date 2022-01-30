class ReadHtmlException(Exception):
    """HTMLの読み込みで発生したエラー"""
    pass

class SaveTypeException(Exception):
    """SaveTypeが規定のもの以外が設定されている時のエラー"""
    pass

class NotFoundArgsException(Exception):
    """引数に該当のものが見つからない時のエラー"""
    pass
