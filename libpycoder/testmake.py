import requests
from bs4 import BeautifulSoup
import config
from .atconnector import AtConnector
from .pathmanager import PathManager
from .atscraper import extract_sample_test_cases_from_prob_page
import sys, os

class TestMaker():
    def __init__(self, contest_type, contest_id):
        self.contest_type = contest_type
        self.contest_id = contest_id
        self.pm = PathManager(contest_type, contest_id)
        self.ac = AtConnector()
        self.ac.init_session()

    def fetch_sample_cases(self):
        problems = ['a', 'b', 'c', 'd', 'e', 'f']
        prob_urls = self.ac.get_prob_urls(self.contest_type, self.contest_id)
        for p in problems:
            print('*', end='')
            url = prob_urls[p]
            if url == '': continue
            # login済みのセッションを利用して、HTMLを取得する
            res = self.ac.session.get(url)
            # レスポンスの HTML から BeautifulSoup オブジェクトを作る
            soup = BeautifulSoup(res.text, 'html5lib')
            sample_test_cases = extract_sample_test_cases_from_prob_page(res.text)
            file_dir = self.pm.get_tests_dir_path(p)
            for k, v in sample_test_cases.items():
                iname = '0' + str(k) + '_input.txt'
                oname = '0' + str(k) + '_output.txt'
                with open(file_dir + iname, 'w') as f: f.write(v[0])
                with open(file_dir + oname, 'w') as f: f.write(v[1])
        print('\nDone!')

    def add_test_case(self, problem_type):
        print('Input:')
        input_case = ''
        s = sys.stdin.readline()
        while not s == '\n':
            input_case += s
            s = sys.stdin.readline()
        print('Output:')
        output_case = ''
        s = sys.stdin.readline()
        while not s == '\n':
            output_case += s
            s = sys.stdin.readline()
        file_dir = self.pm.get_tests_dir_path(problem_type)
        tests = os.listdir(file_dir)
        additional_cases = [t for t in tests if t[0] == '1']
        prefix = str(10 + len(additional_cases)//2)
        with open(file_dir + prefix + '_input.txt', 'w') as f: f.write(input_case.rstrip())
        with open(file_dir + prefix + '_output.txt', 'w') as f: f.write(output_case)
        print('Done!')