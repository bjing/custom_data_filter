
import io

class StringIteratorIO(io.TextIOBase):

    def __init__(self, iter_):
        self.__iter = iter_
        self.__left = ''

    def readable(self):
        return True

    def _read1(self, n=None):
        while not self._left:
            try:
                self.__left = next(self.__iter)
            except StopIteration:
                break
        ret = self.__left[:n]
        self.__left = self.__left[len(ret):]
        return ret
    
    def read(self, n=None):
        l = []
        if n is None or n < 0:
            while True:
                m = self._read1()
                if not m:
                    break
                l.append(m)
        else:
            while n > 0:
                m = self._read1(n)
                if not m:
                    break
                n -= len(m)
                l.append(m)
        return ''.join(l)

    def readline(self):
        l = []
        while True:
            i = self.__left.find('\n')
            if i == -1:
                l.append(self.__left)
                try:
                    self.__left = next(self.__iter)
                except StopIteration:
                    self.__left = ''
                    break
            else:
                l.append(self.__left[:i+1])
                self.__left = self.__left[i+1:]
                break
        return ''.join(l)
    
if __name__ == "__main__":
    s = ["[ www.TorrentDay.com ] - The.Newsroom.2012.S01E10.480p.HDTV.x264-mSD]", "[ www.google.com ] - The.Newsroom.2012.S01E10.480p.HDTV.x264-mSD", "[ www.ebay.com ] - The.Newsroom.2012.S01E10.480p.HDTV.x264-mSD", "[ www.shit.com ] - The.Newsroom.2012.S01E10.480p.HDTV.x264-mSD"]
    s_fd = StringIteratorIO(iter(s))
    
    for line in s_fd:
        print line + "\n"