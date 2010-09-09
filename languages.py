
import gtksourceview2
import mimetypes

lang_manager = gtksourceview2.LanguageManager()

def guess_lang( filename ):
   guess = mimetypes.guess_type(filename)
   ext = '.' + filename.split('.')[-1]
   if guess[0] in mime_to_lang: 
      return lang_manager.get_language( mime_to_lang[guess[0]] )
   elif ext in ext_to_lang:
      return lang_manager.get_language( ext_to_lang[ext] )
   else:
      return None

mime_to_lang = {
   'text/x-bibtex' : 'bibtex', 
   'text/x-boo' : 'boo', 
   'text/x-csrc' : 'c', 
   'text/x-c++src' : 'cpp', 
   'text/css' : 'css', 
   'text/x-dsrc' : 'd', 
   'text/x-diff' : 'diff', 
   'text/x-haskell' : 'haskell', 
   'text/x-literate-haskell' : 'haskell-literate', 
   'text/html' : 'html', 
   'text/x-java': 'java', 
   'text/x-tex' : 'latex', 
   'text/x-pascal' : 'pascal', 
   'text/x-perl' : 'perl', 
   'text/x-python' : 'python', 
   'text/x-sh' : 'sh', 
   'text/x-tcl' : 'tcl', 
   'text/texmacs' : 'texinfo',
}

ext_to_lang = {
   '.ada'   : 'ada',
   '.asp'   : 'asp', 
   '.awk'   : 'awk', 
   '.bib'   : 'bibtex',
   '.cs'    : 'c-sharp', 
   '.cg'    : 'cg', 
   '.cmake' : 'cmake', 
   '.cuda'  : 'cuda', 
   '.bat'   : 'dosbatch', 
   '.e'     : 'eiffel', 
   '.erl'   : 'erlang', 
   '.f'     : 'fortran',
   '.for'   : 'fortran',
   '.f90'   : 'fortran',
   '.f95'   : 'fortran', 
   '.fs'    : 'fsharp', 
   '.js'    : 'js', 
   '.lua'   : 'lua', 
   '.m4'    : 'm4', 
   '.make'  : 'makefile', 
   '.page'  : 'mallard', 
   '.msil'  : 'msil', 
   '.n'     : 'nemerle', 
   '.m'     : 'objc', 
   '.ml'    : 'objective-caml', 
   '.ocl'   : 'ocl', 
   '.m'     : 'octave', 
   '.ooc'   : 'ooc', 
   '.php'   : 'php', 
   '.r'     : 'r', 
   '.rb'    : 'ruby', 
   '.scala' : 'scala',
   '.ss'    : 'scheme', 
   '.sql'   : 'sql', 
   '.vb'    : 'vbnet', 
   '.xml'   : 'xml', 
   '.y'     : 'yacc',
}







