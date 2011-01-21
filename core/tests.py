# encoding: utf-8

import unittest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.models import extend_markdown


class TestExtendedMarkdown(unittest.TestCase):
    def test_working_messsage(self):
        string = u"""Årets høydepunkt i korps-Trøndelag kommer allerede søndag 23. januar: ![][4927]

Søndag 23. januar avsluttes Hellsymposiene med konsert i **Nidarosdomen klokken 20:00**.

Katedralen vår vil danne en storslagen ramme rundt David Maslankas mektige musikk og billetter fås kjøpt i Nidarosdomens besøkssenter eller av medlemene. Billettene koster **200 (voksen) / 100 (stud/mil/honnør) / 50 (barn u 16)**.


Repertoar
------------

- **Traveler** dirigeres av David Maslanka selv
- **Concerto** for marimba and band med solist Anders Kristiansen
- **Symphony no. 4**

Maslankas mektige Symphony no.4 og Concerto dirigeres av Espen Andersen. 

Konserten arrangeres av Norge Musikkorps Forbund og Musikkforeningen Nidarholm i samarbeid.

Les mer på [prosjektsiden](/projects/odysse/) for Odyssé"""

        markdown = u"""<p>\xc5rets h\xf8ydepunkt i korps-Tr\xf8ndelag kommer allerede s\xf8ndag 23. januar: <div class="preview"><a href="4927"><img src="/files/get/4927/4" alt=""/></a><p class="caption"></p></div></p>\n<p>S\xf8ndag 23. januar avsluttes Hellsymposiene med konsert i <strong>Nidarosdomen klokken 20:00</strong>.</p>\n<p>Katedralen v\xe5r vil danne en storslagen ramme rundt David Maslankas mektige musikk og billetter f\xe5s kj\xf8pt i Nidarosdomens bes\xf8kssenter eller av medlemene. Billettene koster <strong>200 (voksen) / 100 (stud/mil/honn\xf8r) / 50 (barn u 16)</strong>.</p>\n<h2>Repertoar</h2>\n<ul>\n<li><strong>Traveler</strong> dirigeres av David Maslanka selv</li>\n<li><strong>Concerto</strong> for marimba and band med solist Anders Kristiansen</li>\n<li><strong>Symphony no. 4</strong></li>\n</ul>\n<p>Maslankas mektige Symphony no.4 og Concerto dirigeres av Espen Andersen. </p>\n<p>Konserten arrangeres av Norge Musikkorps Forbund og Musikkforeningen Nidarholm i samarbeid.</p>\n<p>Les mer p\xe5 <a href="/projects/odysse/">prosjektsiden</a> for Odyss\xe9</p>"""
        self.assertEqual(extend_markdown(string), markdown)
        #self.assertEqual(my_func(a, 1), 'curly')

    def test_working_message_with_image_first(self):
        string = u"""![][4927]Årets høydepunkt i korps-Trøndelag kommer allerede søndag 23. januar:
Søndag 23. januar avsluttes Hellsymposiene med konsert i **Nidarosdomen klokken 20:00**.

Katedralen vår vil danne en storslagen ramme rundt David Maslankas mektige musikk og billetter fås kjøpt i Nidarosdomens besøkssenter eller av medlemene. Billettene koster **200 (voksen) / 100 (stud/mil/honnør) / 50 (barn u 16)**.


Repertoar
------------

- **Traveler** dirigeres av David Maslanka selv
- **Concerto** for marimba and band med solist Anders Kristiansen
- **Symphony no. 4**

Maslankas mektige Symphony no.4 og Concerto dirigeres av Espen Andersen. 

Konserten arrangeres av Norge Musikkorps Forbund og Musikkforeningen Nidarholm i samarbeid.

Les mer på [prosjektsiden](/projects/odysse/) for Odyssé"""
        markdown = u"""<div class="preview"><a href="4927"><img src="/files/get/4927/4" alt=""/></a><p class="caption"></p></div>\n\n<p>\xc5rets h\xf8ydepunkt i korps-Tr\xf8ndelag kommer allerede s\xf8ndag 23. januar:\nS\xf8ndag 23. januar avsluttes Hellsymposiene med konsert i <strong>Nidarosdomen klokken 20:00</strong>.</p>\n<p>Katedralen v\xe5r vil danne en storslagen ramme rundt David Maslankas mektige musikk og billetter f\xe5s kj\xf8pt i Nidarosdomens bes\xf8kssenter eller av medlemene. Billettene koster <strong>200 (voksen) / 100 (stud/mil/honn\xf8r) / 50 (barn u 16)</strong>.</p>\n<h2>Repertoar</h2>\n<ul>\n<li><strong>Traveler</strong> dirigeres av David Maslanka selv</li>\n<li><strong>Concerto</strong> for marimba and band med solist Anders Kristiansen</li>\n<li><strong>Symphony no. 4</strong></li>\n</ul>\n<p>Maslankas mektige Symphony no.4 og Concerto dirigeres av Espen Andersen. </p>\n<p>Konserten arrangeres av Norge Musikkorps Forbund og Musikkforeningen Nidarholm i samarbeid.</p>\n<p>Les mer p\xe5 <a href="/projects/odysse/">prosjektsiden</a> for Odyss\xe9</p>"""
        self.assertEqual(extend_markdown(string), markdown)

    def test_working_message_with_image_first_then_newline(self):
        string = u"""![][4927]

Årets høydepunkt i korps-Trøndelag kommer allerede søndag 23. januar:

Søndag 23. januar avsluttes Hellsymposiene med konsert i **Nidarosdomen klokken 20:00**.

Katedralen vår vil danne en storslagen ramme rundt David Maslankas mektige musikk og billetter fås kjøpt i Nidarosdomens besøkssenter eller av medlemene. Billettene koster **200 (voksen) / 100 (stud/mil/honnør) / 50 (barn u 16)**.


Repertoar
------------

- **Traveler** dirigeres av David Maslanka selv
- **Concerto** for marimba and band med solist Anders Kristiansen
- **Symphony no. 4**

Maslankas mektige Symphony no.4 og Concerto dirigeres av Espen Andersen. 

Konserten arrangeres av Norge Musikkorps Forbund og Musikkforeningen Nidarholm i samarbeid.

Les mer på [prosjektsiden](/projects/odysse/) for Odyssé"""
        markdown = u"""<div class="preview"><a href="4927"><img src="/files/get/4927/4" alt=""/></a><p class="caption"></p></div>\n\n<p>\xc5rets h\xf8ydepunkt i korps-Tr\xf8ndelag kommer allerede s\xf8ndag 23. januar:</p>\n<p>S\xf8ndag 23. januar avsluttes Hellsymposiene med konsert i <strong>Nidarosdomen klokken 20:00</strong>.</p>\n<p>Katedralen v\xe5r vil danne en storslagen ramme rundt David Maslankas mektige musikk og billetter f\xe5s kj\xf8pt i Nidarosdomens bes\xf8kssenter eller av medlemene. Billettene koster <strong>200 (voksen) / 100 (stud/mil/honn\xf8r) / 50 (barn u 16)</strong>.</p>\n<h2>Repertoar</h2>\n<ul>\n<li><strong>Traveler</strong> dirigeres av David Maslanka selv</li>\n<li><strong>Concerto</strong> for marimba and band med solist Anders Kristiansen</li>\n<li><strong>Symphony no. 4</strong></li>\n</ul>\n<p>Maslankas mektige Symphony no.4 og Concerto dirigeres av Espen Andersen. </p>\n<p>Konserten arrangeres av Norge Musikkorps Forbund og Musikkforeningen Nidarholm i samarbeid.</p>\n<p>Les mer p\xe5 <a href="/projects/odysse/">prosjektsiden</a> for Odyss\xe9</p>"""
        self.assertEqual(extend_markdown(string), markdown)
if __name__ == '__main__':
    unittest.main()
