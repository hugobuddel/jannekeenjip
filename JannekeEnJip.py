from zipfile import ZipFile
import copy

class Book():
    
    interpuncties = ["&#x2018;", "&#x2019;", " ", ".", ",", ":", ";", "!", "?"]
    
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
    
    def hergender_data(self, data):
        
        def verwissel_woorden(data, woord_man, woord_vrouw):
            data = data.replace(woord_man, "XX__XX")
            data = data.replace(woord_man.upper(), "XX_UPPER_XX")
            data = data.replace(woord_man.lower(), "XX_LOWER_XX")
            data = data.replace(woord_man.capitalize(), "XX_CAPIL_XX")
            data = data.replace(woord_man.lower().capitalize(), "XX_LOWERCAPIT_XX")
            data = data.replace(woord_vrouw, "XY__XY")
            data = data.replace(woord_vrouw.upper(), "XY_UPPER_XY")
            data = data.replace(woord_vrouw.lower(), "XY_LOWER_XY")
            data = data.replace(woord_vrouw.capitalize(), "XY_CAPIL_XY")
            data = data.replace(woord_vrouw.lower().capitalize(), "XY_LOWERCAPIT_XY")
            data = data.replace("XX__XX", woord_vrouw)
            data = data.replace("XX_UPPER_XX", woord_vrouw.upper())
            data = data.replace("XX_LOWER_XX", woord_vrouw.lower())
            data = data.replace("XX_CAPIL_XX", woord_vrouw.capitalize())
            data = data.replace("XX_LOWERCAPIT_XX", woord_vrouw.lower().capitalize())
            data = data.replace("XY__XY", woord_man)
            data = data.replace("XY_UPPER_XY", woord_man.upper())
            data = data.replace("XY_LOWER_XY", woord_man.lower())
            data = data.replace("XY_CAPIL_XY", woord_man.capitalize())
            data = data.replace("XY_LOWERCAPIT_XY", woord_man.lower().capitalize())
            return data

        def zewerkwoord(data, derde, meervoud):
            data = data.replace("ze " + derde, "XY_hij_XY " + derde)
            data = data.replace("zij " + derde, "XY_hij_XY " + derde)
            data = data.replace("Ze " + derde, "XY_Hij_XY " + derde)
            data = data.replace("Zij " + derde, "XY_Hij_XY " + derde)
            data = data.replace(derde + " zij", derde + " XY_hij_XY")
            data = data.replace(derde.capitalize() + " zij", derde.capitalize() + " XY_hij_XY")
            data = data.replace(derde + " ze", derde + " XY_hij_XY")
            data = data.replace(derde.capitalize() + " ze", derde.capitalize() + " XY_hij_XY")
            
            
            return data
        
        def zewerkwoorden(data):
            werkwoordparen = [
                ("is", "zijn"),
                ("heeft", "hebben"),
                ("zegt", "zeggen"),
                ("kijkt", "kijken"),
                ("zit", "zitten"),
                ("lacht", "lachen"),
                ("loopt", "lopen"),
                ("maakt", "maken"),
                ("speelt", "spelen"),
                # etc...
            ]
            for (derde, meervoud) in werkwoordparen:
                data = zewerkwoord(data, derde, meervoud)

            for interpunctie1 in self.interpuncties:
                for interpunctie2 in self.interpuncties:
                    data = data.replace(interpunctie1 + "hij" + interpunctie2, interpunctie1 + "ze" + interpunctie2)
                    data = data.replace(interpunctie1 + "Hij" + interpunctie2, interpunctie1 + "Ze" + interpunctie2)
            
            data = data.replace("XY_hij_XY", "hij")
            data = data.replace("XY_Hij_XY", "Hij")
            
            return data

        # Haal eerst de spaties eruit, want daar wordt op gematched.
        # Haalt dit ook het watermark eruit?
        data = data.replace("  ", " ")
        data = verwissel_woorden(data, 'Jip', 'Janneke')
        data = verwissel_woorden(data, 'vader', 'moeder')
        
        # Dit werkt niet, maar is opgelost met zewerkwoorden().
        #data = verwissel_woorden(data, 'hij ', 'ze ')
        
        # Dit werkt ook niet, 'rohaaren' :). Nog niet opgelost.
        #data = verwissel_woorden(data, 'haar', 'zijn')
        
        data = zewerkwoorden(data)
        return data

    def hergender(self):
        filenames_html = [fn for fn in self.filenames if fn[-5:] == '.html']

        for filename in filenames_html:
            data = self.data_jannekeenjip[filename]
            data = self.hergender_data(data)
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

    
