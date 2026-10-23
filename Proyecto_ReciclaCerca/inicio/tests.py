from django.test import SimpleTestCase
from django.urls import reverse


class PortadaTests(SimpleTestCase):
    def test_portada_responde_en_la_raiz(self):
        respuesta = self.client.get('/')
        self.assertEqual(respuesta.status_code, 200)
        self.assertTemplateUsed(respuesta, 'inicio/Plantilla.html')

    def test_portada_tiene_nombre_de_ruta(self):
        self.assertEqual(reverse('inicio:inicio'), '/')
