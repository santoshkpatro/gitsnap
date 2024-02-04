import os
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from playwright.sync_api import sync_playwright, expect

from gitsnap.models.user import User


class AccountsTests(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
        super().setUpClass()
        cls.playwright = sync_playwright().start()
        cls.browser = cls.playwright.chromium.launch(headless=True)

        # Create a sample user
        user = User(
            username="santoshkpatro",
            email="santoshkpatro@gitsnap.io",
            first_name="Santosh Kumar",
            last_name="Patro",
        )
        user.set_password("12345")
        user.save()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.browser.close()
        cls.playwright.stop()

    def test_login(self):
        page = self.browser.new_page()
        page.goto(f"{self.live_server_url}/accounts/login/")

        # Try with invalid username or password
        page.get_by_label("username").fill("unknow")
        page.get_by_label("password").fill("wrongpassword")
        page.get_by_label("login").click()
        expect(page.locator(".alert")).to_have_text(
            "No user exists with the given username or email address."
        )

        # Try with wrong password to test error messages
        page.get_by_label("username").fill("santoshkpatro")
        page.get_by_label("password").fill("wrongpassword")
        page.get_by_label("login").click()
        expect(page.locator(".alert")).to_have_text("Please enter valid password.")

        # Try with actual password for login
        page.get_by_label("password").fill("12345")
        page.get_by_label("login").click()
        page.close()
