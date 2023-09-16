from api.v1.utils.zipping import zip_file, write_to_zip, append_to_zip, zipfile
from parameterized import parameterized
import os
import unittest
from unittest.mock import Mock, patch


class TestAppendToFile(unittest.TestCase):
    """ Test if append_file calls necessary functions"""

    def test_append_to_a_file_creates_a_deflated_zipfile_instance(self):
        """test if append to file creates a ZipFile instance"""
        with patch('zipfile.ZipFile') as mkdzip:
            append_to_zip('abc.zip', ['simple'])
            mkdzip.assert_called_once()
            mkdzip.assert_called_with('abc.zip', 'a', zipfile.ZIP_DEFLATED)

    def test_append_file_calls_write(self):
        """Test if the append_file calls ZipFile.write"""
        with patch('zipfile.ZipFile.write') as mkwrite:
            append_to_zip('xyz.zip', ['folks', 'dicom'])
            self.assertEqual(mkwrite.call_count, 2)
            mkwrite.assert_called_with('xyz.zip', 'dicom')


class TestWriteToFile(unittest.TestCase):
    """ Test if write_to_file calls the approprite functions"""

    def test_write_to_zip_instantiates_deflated_zip(self):
        """Test if write to zip creates a ZipFile instance in write mode"""
        with patch('zipfile.ZipFile') as mkdzip:
            write_to_zip('abc.zip', ['simple'])
            mkdzip.assert_called_once()
            mkdzip.assert_called_with('abc.zip', 'w', zipfile.ZIP_DEFLATED)

    def test_write_to_zip_calls_write_n_times(self):
        """Test if write is called 2 times"""
        with patch('zipfile.ZipFile.write') as mkwrite:
            write_to_zip('xyz.zip', ['folks', 'dicom'])
            self.assertEqual(mkwrite.call_count, 2)
            mkwrite.assert_called_with('xyz.zip', 'dicom')


class TestZipFile(unittest.TestCase):
    """Test if function zip_file works as expected"""

    @patch('zipfile.is_zipfile')
    def test_if_zipfile_checks_for_zip_exist(self, mk_iszip):
        """ Test if zip_file calls zipfile.is_zipfile"""
        zip_file('xyz.zip', [])
        mk_iszip.assert_called_once_with('xyz.zip')

    @patch('zipfile.is_zipfile')
    def test_zip_file_calls_append_to_zip(self, mk_iszip):
        """Test if append is callrd if the file already exists"""
        mk_iszip.return_value = True
        with patch('api.v1.utils.zipping.append_to_zip') as mkd_append:
            zip_file('abc.zip', [])
            mkd_append.assert_called_with('abc.zip', [])

    @patch('zipfile.is_zipfile')
    def test_if_zipfile_calls_write_to_zip(self, mk_iszip):
        """Test if zip_file calls write if object not exist"""
        mk_iszip.return_value = False
        with patch('api.v1.utils.zipping.write_to_zip') as mkd_write:
            zip_file('xyz.zip', ['files', 'dicom'])
            mkd_write.assert_called_with('xyz.zip', ['files', 'dicom'])
