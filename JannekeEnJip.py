from zipfile import ZipFile
import copy

class Book():
    
    def __init__(self):
        self.filename_jipenjanneke = None
        self.filename_jannekeenjip = None
        self.data_jipenjanneke = {}
        self.data_jannekeenjip = {}
        self.filenames = []
    
    def open_epub(self, filename):
        self.filename_jipenjanneke = filename
        
        with ZipFile(self.filename_jipenjanneke) as zipfile_jipenjanneke:
            self.filenames = zipfile_jipenjanneke.namelist()
            self.data_jipenjanneke = {
                fn: zipfile_jipenjanneke.read(fn)
                for fn in self.filenames
            }
            self.data_jannekeenjip = copy.copy(self.data_jipenjanneke)
    
    def hergender(self):
        filenames_html = [fn for fn in self.filenames if fn[-5:] == '.html']
        for filename in filenames_html:
            data = self.data_jannekeenjip[filename]
            data = data.replace("Janneke", "XXREPLACEMEXX")
            data = data.replace("Jip", "Janneke")
            data = data.replace("XXREPLACEMEXX", "Jip")
            self.data_jannekeenjip[filename] = data
            

    
    def schrijf_epub(self, filename):
        self.filename_jannekeenjip = filename
        
        with ZipFile(self.filename_jannekeenjip, 'w') as zipfile_jannekeenjip:
            for filename in self.filenames:
                zipfile_jannekeenjip.writestr(
                    filename,
                    self.data_jannekeenjip[filename],
                )


if __name__ == '__main__':
    book = Book()
    book.open_epub('jip_en_janneke_2_annie_m_g_schmidt.epub')
    book.hergender()
    book.schrijf_epub('janneke_en_jip_2.epub')

    
