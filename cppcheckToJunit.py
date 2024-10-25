#!/usr/bin/python3

"""
    :brief RATS to JUNIT Converter
    :date 24.10.2024
    :version v1.0.0
    :author Severin Sprenger
"""

import xml.etree.ElementTree as ET
import platform
import datetime
import sys
import os

# Scan files that were scanned by cppcheck
scannedFiles = []

def list_files_recursive(path='.'):
    for entry in os.listdir(path):
        full_path = os.path.join(path, entry)
        if os.path.isdir(full_path):
            list_files_recursive(full_path)
        else:
            if full_path.endswith((".c", ".cpp", ".h", ".ino")): # Add custom file types here
            	scannedFiles.append(full_path.replace("./", "", 1))

list_files_recursive(sys.argv[2])

# Build JUnit XML
cppcheck_output = ET.parse(sys.argv[1])
cppcheck_output_root = cppcheck_output.getroot()

root = ET.Element("testsuites", name="cppcheck")
testsuites = ET.SubElement(root, "testsuite",
    name="CppCheck static code analysis",
    timestamp=str(datetime.datetime.now()),
    hostname=platform.node(),
    tests=str(len(scannedFiles)),
    errors="0", failures="0", skipped="0"
)

errorCount = 0

for files in scannedFiles:
    testcase = ET.SubElement(testsuites, "testcase",
        name=str(files),
        time="3.0e-05",
        classname="Static code analysis"
    )

    for errors in cppcheck_output_root.findall("errors/error"):
        if errors.find("location") != None and str(errors.find("location").attrib["file"]) == str(files):
            print("lol")
