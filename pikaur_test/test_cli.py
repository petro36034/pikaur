""" This file is licensed under GPLv3, see https://www.gnu.org/licenses/ """

from pikaur_test.helpers import PikaurTestCase, pikaur, pacman


class CliTest(PikaurTestCase):

    def test_unknown_argument(self):
        """
        unknown argument passed to pacman
        """
        self.assertEqual(pikaur('-Zyx').returncode, 1)

    def test_search(self):
        self.assertEqual(
            sorted(
                pikaur('-Ssq oomox').stdout.splitlines()
            ),
            ['oomox', 'oomox-git']
        )

    def test_list(self):
        result_all = pikaur('-Ssq').stdout.splitlines()
        result_aur = pikaur('-Ssq --aur').stdout.splitlines()
        result_repo = pikaur('-Ssq --repo').stdout.splitlines()
        self.assertIn('oomox-git', result_all)
        self.assertIn('oomox-git', result_aur)
        self.assertNotIn('oomox-git', result_repo)
        self.assertIn('pacman', result_all)
        self.assertNotIn('pacman', result_aur)
        self.assertIn('pacman', result_repo)
        self.assertGreaterEqual(len(result_aur), 50000)
        self.assertGreaterEqual(len(result_repo), 100)
        self.assertEqual(len(result_all), len(result_aur) + len(result_repo))

    def test_aur_package_info(self):
        result = pikaur('-Si oomox')
        pkg_name_found = False
        for line in result.stdout.splitlines():
            if 'name' in line and 'oomox' in line:
                pkg_name_found = True
        self.assertTrue(pkg_name_found)

    def test_repo_package_info(self):
        result1 = pikaur('-Si mpv')
        result2 = pacman('-Si mpv')
        self.assertEqual(result1, result2)

    def test_incompatible_args(self):
        self.assertEqual(
            pikaur('-Qs pkg --repo').returncode, 1
        )
        self.assertEqual(
            pikaur('-Qs pkg --aur').returncode, 1
        )

    # just run info commands for coverage:

    def test_version(self):
        self.assertEqual(
            pikaur('-V').returncode, 0
        )

    def test_help(self):
        self.assertEqual(
            pikaur('-h').returncode, 0
        )

    def test_sync_help(self):
        self.assertEqual(
            pikaur('-Sh').returncode, 0
        )

    def test_query_help(self):
        self.assertEqual(
            pikaur('-Qh').returncode, 0
        )

    def test_pkgbuild_help(self):
        self.assertEqual(
            pikaur('-Ph').returncode, 0
        )

    def test_getpkgbuild_help(self):
        self.assertEqual(
            pikaur('-Gh').returncode, 0
        )
