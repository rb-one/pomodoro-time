from flask_testing import TestCase
from flask import url_for
from main import app


class AppMainTest(TestCase):
    """App Configuration"""

    def create_app(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        return app

    # 404 route
    def test_404_render_template(self):
        self.client.get('undefined_route')
        self.assertTemplateUsed('404.html')

    def test_index_redirect(self):
        '''test if app redirects from index to pomodoro_time'''
        response = self.client.get(url_for('index'))
        self.assert_redirects(response, url_for('pomodoro_time'))
