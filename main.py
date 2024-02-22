from http.server import BaseHTTPRequestHandler, HTTPServer
from xml.etree import ElementTree as ET


class SOAPRequestHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        # print (post_data)
        soap_request = ET.fromstring(post_data)
        body = soap_request.find('.//{http://schemas.xmlsoap.org/soap/envelope/}Body')
        method_element = list(body)[0]
        method_name = method_element.tag
        # print(method_name)
        if method_name.endswith('getFinlandCities'):
            response = self.get_finland_cities()
        else:
            response = '''
                <soap:Fault>
                    <faultcode>Server</faultcode>
                    <faultstring>Method not found</faultstring>
                </soap:Fault>
            '''

        self.send_response(200)
        self.send_header('Content-type', 'text/xml')
        self.end_headers()
        self.wfile.write(response.encode())

    def get_finland_cities(self):
        # Dummy implementation, replace with actual data
        cities = ['Helsinki', 'Tampere', 'Turku', 'Oulu']
        expenses = [1500, 1200, 1300, 1100]

        city_elements = ''
        for city, expense in zip(cities, expenses):
            city_elements += f'<city><name>{city}</name><expense>{expense}</expense></city>'

        soap_response = f"""
        <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
            <soap:Body>
                <getFinlandCities xmlns="http://www.example.com/your-namespace">
                    <cities>{city_elements}</cities>
                </getFinlandCities>
            </soap:Body>
        </soap:Envelope>
        """
        return soap_response


def run(server_class=HTTPServer, handler_class=SOAPRequestHandler, port=8081):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting SOAP server on port {port}...')
    httpd.serve_forever()


if __name__ == '__main__':
    run()
