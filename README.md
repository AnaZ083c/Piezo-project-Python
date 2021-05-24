# Piezo-project-Python
 
glavni projekt je v: <b>Arduino/Python/Buzzer/make_wav_on_led.py</b> <br>
Trenutno delovanje je prikazano na tej povezavi: https://drive.google.com/file/d/1ejvl6h9ShkUew9RzedjvKmLPhlpWiPF4/view?usp=sharing
<br>
## Priprava na delovanje knjižnice PyMata3
Da bo knjižnica PyMata3 zaznala Arduino, je na Arduino IDE potrebno naložiti knjižnice (<b>libraries.zip</b>). <br>
Nato pa je z Arduino IDE potrebno na Arduino naložiti program (iz prej naloženih knjižnic) <b>FirmataPlus32u4</b>. <i>Morebitni "warning"-i niso pomembni. Važno je, da se program uspešno naloži na Arduino.</i>
<br>
<br>
<b><u>POMEMBNO!</u></b> Da PyMata3 v Python projektu zazna priključen Arduino, je najprej potrebno naložiti zgoraj omenjeni program. Šele potem se lahko dela v Python-u.
<br>
## Povezave do knjižnic za zvok
### audio-to-midi
https://github.com/NFJones/audio-to-midi <br>
https://pypi.org/project/audio-to-midi/ <br>
<br>
### pretty-midi
https://craffel.github.io/pretty-midi/ <br>
https://pypi.org/project/pretty_midi/ <br>
<br>
### pymata-aio
https://htmlpreview.github.io/?https://github.com/MrYsLab/pymata-aio/blob/master/documentation/html/index.html <br>
https://pypi.org/project/pymata-aio/
