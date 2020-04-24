import trafilatura
import time
from tabulate import tabulate
from lxml import html
from lxml import etree
from trafilatura.xml import validate_tei

downloaded=trafilatura.fetch_url('https://github.blog/2019-03-29-leader-spotlight-erin-spiceland/')
if not downloaded is None: 
    print ("Download successful.")
    
# Programm mit default-Werten fuer die keyword-Argumente ausfuehren und Zeit messen:
start=time.time()
result=trafilatura.extract(downloaded)
end=time.time()
duration=end-start
#print(result)

# Programm mit den Werten fuer die keyword-Argumente ausfuehren, die die vermutlich schnellste
# Ausfuehrungszeit sicherstellen und Zeit messen:
start2=time.time()
result2=trafilatura.extract(downloaded, include_comments=False, include_tables=False, no_fallback=True)
end2=time.time()
duration2=end2-start2

# verschieden Einstellungen ausprobieren:
start3=time.time()
result3=trafilatura.extract(downloaded, include_tables=False, no_fallback=True)
end3=time.time()
duration3=end3-start3

start4=time.time()
result4=trafilatura.extract(downloaded, no_fallback=True)
end4=time.time()
duration4=end4-start4

start5=time.time()
result5=trafilatura.extract(downloaded, include_comments=False, no_fallback=True)
end5=time.time()
duration5=end5-start5

start6=time.time()
result6=trafilatura.extract(downloaded, include_comments=False)
end6=time.time()
duration6=end6-start6

start7=time.time()
result7=trafilatura.extract(downloaded, include_tables=False)
end7=time.time()
duration7=end7-start7

start8=time.time()
result8=trafilatura.extract(downloaded, include_comments=False, include_tables=True)
end8=time.time()
duration8=end8-start8

# Differenz bezueglich der Laufzeit und prozentuale Verbesserung ausgeben:
print("Difference in performance between 'default' and optimized settings: {}".format(duration-duration2))
diff=duration-duration2
percentage_faster=(diff/duration)*100
print("The optimized settings made the program run {}% faster compared to the default settings.".format(percentage_faster))
# Verschiedene Zeiten ausgeben:
print(tabulate([["Default settings",duration], \
["Without comments", duration6], \
["Without tables", duration7], \
["Without fallback algorithm", duration4], \
["Without comments and tables", duration8], \
["Without tables and without fallback algorithm",duration3], \
["Without comments and without fallback algorithm", duration5], \
["Without comments and tables and without fallback algorithm",duration2], \
], headers=['Settings', 'Execution time'], tablefmt='orgtbl'))

# trafilatura kann das html-Dokument auch als string einlesen, das wird hier ausprobiert:
mytree = html.fromstring('<html><body><article><p>Here is the main text. It has to be long enough in order to bypass the safety checks. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.</p></article></body></html>')
from_tree_result=trafilatura.extract(mytree)
print("result from html-string: ",from_tree_result)

# Versuch, die Keyword-Argumente url und target_language zu aendern; 
# result9 und result11 liefern None (liegt anscheinend am Aendern der Target-language),
# das Eingeben einer url funktioniert aber: 
url1='https://github.blog/2019-03-29-leader-spotlight-erin-spiceland/'
result9 = trafilatura.extract(downloaded, target_language='de')
print(result9)
result10 = trafilatura.extract(downloaded, url=url1)
print(result10)
result11 = trafilatura.extract(downloaded, url=url1, target_language='de')
print(result11)

  
# Ausprobieren der Validierung bzgl. TEI (siehe https://trafilatura.readthedocs.io/en/latest/validation.html)
print("test TEI-Validation:")
mytree2=etree.parse("DU_sense.xml")
print("Correct file: ",validate_tei(mytree2))
mytree3=etree.parse("DU_sense_illformed.xml")
print("Illformed file: ")
print(validate_tei(mytree3))

# Ausprobieren der Funktion xmltotxt() (siehe https://trafilatura.readthedocs.io/en/latest/corefunctions.html)
#f=open("DU_sense.xml","r")
#xml_text=f.read()
#print(trafilatura.xml.xmltotxt(xml_text))
# --> fuehrt zu TypeError: Invalid input object: str

#f=open("DU_sense.xml","r")
#print(trafilatura.xml.xmltotxt(f))
# --> fuehrt zu TypeError: Invalid input object: _io.TextIOWrapper

#print(trafilatura.xml.xmltotxt("DU_sense.xml"))
# --> fuehrt zu TypeError: Invalid input object: str
