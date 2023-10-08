import logging

import tkinter as tk
import backoff

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver

from selenium_stealth import stealth

from webdriver_manager.chrome import ChromeDriverManager, ChromeType

logger = logging.getLogger(__name__)


class Browser:
    def __init__(self, driver: WebDriver):
        self._driver = driver
        self._wait = WebDriverWait(self.driver, 20, 1)
        self._wait_slow = WebDriverWait(self.driver, 60, 1)
        self._metamask_handle = None

    @property
    def driver(self):
        return self._driver

    @property
    def wait(self):
        return self._wait

    @property
    def wait_slow(self):
        return self._wait_slow

    @property
    def metamask_handle(self):
        return self._metamask_handle

    def __enter__(self):
        return self

    def close(self):
        self.driver.quit()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


class ChromeBrowser(Browser):
    def __init__(self):
        options = Options()
        options.add_argument('--window-size=1920,1080')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
        options.add_extension('meta.crx')
        srv = Service(ChromeDriverManager(chrome_type=ChromeType.GOOGLE).install())
        driver = webdriver.Chrome(service=srv, options=options)
        super().__init__(driver)
        stealth(self.driver,
                languages=['en-US', 'en'],
                vendor='Google Inc.',
                platform='Win32',
                webgl_vendor='Intel Inc.',
                renderer='Intel Iris OpenGL Engine',
                fix_hairline=True, )

        self.wait.until(EC.number_of_windows_to_be(2))
        self._metamask_handle = self.driver.window_handles[1]


class Metamask(ChromeBrowser):
    def __init__(self, metamask_password: str):
        super().__init__()
        self._password = metamask_password

    @property
    def password(self):
        return self._password

    @backoff.on_exception(backoff.constant, Exception, interval=1, max_tries=3)
    def _do_create_account(self):
        self.driver.switch_to.window(self.metamask_handle)
        self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="onboarding__terms-checkbox"]'))).click()
        self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//button[text()="Create a new wallet"]'))).click()
        self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//button[text()="I agree"]'))).click()
        self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="app-content"]/div/div[2]/div/div/div/div[2]/form/div[1]/label/input'))).send_keys(
            self.password)
        self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="app-content"]/div/div[2]/div/div/div/div[2]/form/div[2]/label/input'))).send_keys(
            self.password)
        self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="app-content"]/div/div[2]/div/div/div/div[2]/form/div[3]/label/input'))).click()
        self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="app-content"]/div/div[2]/div/div/div/div[2]/form/button'))).click()
        self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="app-content"]/div/div[2]/div/div/div/div[5]/button[2]'))).click()
        self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="app-content"]/div/div[2]/div/div/div/div[6]/button'))).click()
        word1 = self.wait.until(EC.presence_of_element_located(
            (By.XPATH,
             '//*[@id="app-content"]/div/div[2]/div/div/div/div[5]/div/div[1]/div[2]')
        )).text
        word2 = self.wait.until(EC.presence_of_element_located(
            (By.XPATH,
             '//*[@id="app-content"]/div/div[2]/div/div/div/div[5]/div/div[2]/div[2]')
        )).text
        word3 = self.wait.until(EC.presence_of_element_located(
            (By.XPATH,
             '//*[@id="app-content"]/div/div[2]/div/div/div/div[5]/div/div[3]/div[2]')
        )).text
        word4 = self.wait.until(EC.presence_of_element_located(
            (By.XPATH,
             '//*[@id="app-content"]/div/div[2]/div/div/div/div[5]/div/div[4]/div[2]')
        )).text
        word5 = self.wait.until(EC.presence_of_element_located(
            (By.XPATH,
             '//*[@id="app-content"]/div/div[2]/div/div/div/div[5]/div/div[5]/div[2]')
        )).text
        word6 = self.wait.until(EC.presence_of_element_located(
            (By.XPATH,
             '//*[@id="app-content"]/div/div[2]/div/div/div/div[5]/div/div[6]/div[2]')
        )).text
        word7 = self.wait.until(EC.presence_of_element_located(
            (By.XPATH,
             '//*[@id="app-content"]/div/div[2]/div/div/div/div[5]/div/div[7]/div[2]')
        )).text
        word8 = self.wait.until(EC.presence_of_element_located(
            (By.XPATH,
             '//*[@id="app-content"]/div/div[2]/div/div/div/div[5]/div/div[8]/div[2]')
        )).text
        word9 = self.wait.until(EC.presence_of_element_located(
            (By.XPATH,
             '//*[@id="app-content"]/div/div[2]/div/div/div/div[5]/div/div[9]/div[2]')
        )).text
        word10 = self.wait.until(EC.presence_of_element_located(
            (By.XPATH,
             '//*[@id="app-content"]/div/div[2]/div/div/div/div[5]/div/div[10]/div[2]')
        )).text
        word11 = self.wait.until(EC.presence_of_element_located(
            (By.XPATH,
             '//*[@id="app-content"]/div/div[2]/div/div/div/div[5]/div/div[11]/div[2]')
        )).text
        word12 = self.wait.until(EC.presence_of_element_located(
            (By.XPATH,
             '//*[@id="app-content"]/div/div[2]/div/div/div/div[5]/div/div[12]/div[2]')
        )).text

        secret = word1, word2, word3, word4, word5, word6, word7, word8, word9, word10, word11, word12

        logger.info(secret)

        self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="app-content"]/div/div[2]/div/div/div/div[6]/div/button'))).click()

        # input secret words

        self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="app-content"]/div/div[2]/div/div/div/div[4]/div/div[3]/div[2]/input'))).send_keys(
            word3)
        self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="app-content"]/div/div[2]/div/div/div/div[4]/div/div[4]/div[2]/input'))).send_keys(
            word4)
        self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="app-content"]/div/div[2]/div/div/div/div[4]/div/div[8]/div[2]/input'))).send_keys(
            word8)
        self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="app-content"]/div/div[2]/div/div/div/div[5]/button'))).click()

        self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="app-content"]/div/div[2]/div/div/div/div[2]/button'))).click()
        self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="app-content"]/div/div[2]/div/div/div/div[2]/button'))).click()
        self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="app-content"]/div/div[2]/div/div/div/div[2]/button'))).click()

        try:
            self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="popover-content"]/div/div/section/div[1]/div/button'))).click()
        except Exception:
            pass

        popover = (
            By.XPATH,
            '//*[@class="popover-bg"]'
        )
        self.wait_slow.until(EC.invisibility_of_element_located(popover))

        # get public key
        self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="app-content"]/div/div[3]/div/div/div/div[1]/div/div/div/button'))).click()
        root = tk.Tk()
        public_key = root.clipboard_get()

        logger.info(public_key)

        # get private key
        try:
            self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="popover-content"]/div/div/section/div[1]/div/button'))).click()
        except Exception:
            pass
        self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="app-content"]/div/div[3]/div/div/div/div[1]/span/button'))).click()
        self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="popover-content"]/div[2]/button[2]'))).click()
        self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="app-content"]/div/span/div[1]/div/div/div/button[3]'))).click()
        self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="app-content"]/div/span/div[1]/div/div/div/div[5]/input'))).send_keys(self.password)
        self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="app-content"]/div/span/div[1]/div/div/div/div[7]/button[2]'))).click()
        private_key = self.wait.until(EC.presence_of_element_located(
            (By.XPATH,
             '//*[@id="app-content"]/div/span/div[1]/div/div/div/div[5]/div')
        )).text

        logger.info(private_key)

        return secret, public_key, private_key

    def _put_in_file(self, secret, public_key, private_key):
        with open('new_accounts.txt', mode="a") as file:
            file.write(f'secret: {str(secret)}\n')
            file.write(f'public: {public_key}\n')
            file.write(f'private: {private_key}\n\n')

    def create_account(self):
        secret, public_key, private_key = self._do_create_account()
        self._put_in_file(secret, public_key, private_key)


def create_account(metamask_password: str):
    with Metamask(metamask_password) as metamask:
        try:
            metamask.create_account()
            metamask.close()
        except Exception:
            metamask.close()


def sorting(src_file: str):
    """
    Func sorts data from like this:
        secret: ('word', 'word', 'word', 'word', 'word', 'word', 'word', 'word', 'word', 'word', 'word', 'word')
        public: 0xaaaaaaaaaaaaAaaaaaaaaaaaaaaa
        private: asdsadaaaaaaaaaaaaaaaaaaaasfafadf
    in files
    :param src_file: source file path (str)
    :return:
    """
    with open(src_file, "r") as file:
        accounts = [row.strip() for row in file]
    for row in accounts:
        if 'public:' in row:
            with open('public_keys.txt', mode="a") as public_keys:
                public_keys.write(f'{str(row.split(" ")[1])}\n')
        elif 'private:' in row:
            with open('private_keys.txt', mode="a") as private_keys:
                private_keys.write(f'{str(row.split(" ")[1])}\n')


def get_qtt() -> int:
    return int(input('Enter the number of wallets to generate: '))


def get_password() -> str:
    return input("Enter your password for Metamask wallets: ")


if __name__ == '__main__':
    logging.basicConfig(
        format='[%(asctime)s] [%(levelname)-7s] %(message)s',
        level=logging.DEBUG,
        filename='create_accounts.log'
    )
    logging.getLogger('selenium.webdriver.remote.remote_connection').setLevel(logging.INFO)
    logging.getLogger('urllib3').setLevel(logging.INFO)
    steps = get_qtt()
    password = get_password()
    for _ in range(steps):
        create_account(password)
    sorting('new_accounts.txt')
