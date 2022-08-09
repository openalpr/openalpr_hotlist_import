
class SafeList(list):
    def get(self, index, default=None):
        try:
            return self.__getitem__(index).strip()
        except IndexError:
            if not default:
                return ''
            return default
