import bz2
import gzip
import io
import lzma
import os
import tarfile
import tempfile
import shutil
import zipfile
import py7zr
import rarfile as rarfile


def create_zip_file(file_list, temp_dir) -> zipfile:

    in_memory_buffer = io.BytesIO()
    with zipfile.ZipFile(in_memory_buffer, 'w') as new_zip:
        for file_name in file_list:
            file_path = os.path.join(temp_dir, file_name)
            new_zip.write(file_path, file_name)

    shutil.rmtree(temp_dir)

    in_memory_buffer.seek(0)
    archive = zipfile.ZipFile(in_memory_buffer, "r")
    files = archive.namelist()

    return files, archive


def archive_reader(buffer, archive_format) -> zipfile:
    temp_dir = tempfile.mkdtemp()

    if archive_format == "zip":
        archive = zipfile.ZipFile(buffer, 'r')
        file_list = archive.namelist()
        return file_list, archive

    if archive_format == "7z":
        with py7zr.SevenZipFile(buffer, mode='r') as source_archive:
            file_list = source_archive.getnames()
            source_archive.extractall(temp_dir)
            return create_zip_file(file_list, temp_dir)

    if archive_format == "tar":
        with tarfile.open(fileobj=buffer, mode='r') as source_archive:
            file_list = source_archive.getnames()
            source_archive.extractall(temp_dir)
            return create_zip_file(file_list, temp_dir)

    if archive_format == "xz":
        with lzma.open(buffer, mode='rb') as lzma_file, tarfile.open(fileobj=lzma_file, mode='r') as source_archive:
            file_list = source_archive.getnames()
            source_archive.extractall(temp_dir)
            return create_zip_file(file_list, temp_dir)

    if archive_format == "gz":
        with gzip.open(buffer, mode='rb') as gz_file, tarfile.open(fileobj=gz_file, mode='r') as source_archive:
            file_list = source_archive.getnames()
            source_archive.extractall(temp_dir)
            return create_zip_file(file_list, temp_dir)

    if archive_format == "bz2":
        with bz2.open(buffer, mode='rb') as bz2_file, tarfile.open(fileobj=bz2_file, mode='r') as source_archive:
            file_list = source_archive.getnames()
            source_archive.extractall(temp_dir)
            return create_zip_file(file_list, temp_dir)

    if archive_format == "rar":
        with rarfile.RarFile(buffer, 'r') as source_archive:
            file_list = source_archive.namelist()
            source_archive.extractall(temp_dir)
            return create_zip_file(file_list, temp_dir)
