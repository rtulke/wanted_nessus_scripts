#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
audit_parser.py


This script analyzes .audit files in XML format and outputs the contained information.
It supports reading multiple files through the -a or --audit parameters.

Usage:
    python3 audit_parser.py -a file1.audit file2.audit
    python3 audit_parser.py --audit file1.audit file2.audit
    python3 audit_parser.py -h
    python3 audit_parser.py --help

Robert Tulke, rt@debian.sh, 2021-09-26
"""

import argparse
import xml.etree.ElementTree as ET
import sys
import os

# Function to parse the .audit file
def parse_audit(file_path):
    if not os.path.isfile(file_path):
        print(f"File not found: {file_path}")
        return

    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
    except ET.ParseError:
        print(f"Invalid XML format: {file_path}")
        return
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
        return

    print(f"Analyzing file: {file_path}")
    print("=" * 50)

    # Iterate over each <custom_item> element
    for custom_item in root.findall('.//custom_item'):
        control_data = {
            "type": custom_item.findtext('type', default="").strip(),
            "description": custom_item.findtext('description', default="").strip(),
            "info": custom_item.findtext('info', default="").strip(),
            "solution": custom_item.findtext('solution', default="").strip(),
            "reference": custom_item.findtext('reference', default="").strip(),
            "see_also": custom_item.findtext('see_also', default="").strip(),
            "value_type": custom_item.findtext('value_type', default="").strip(),
            "value_data": custom_item.findtext('value_data', default="").strip(),
            "password_policy": custom_item.findtext('password_policy', default="").strip()
        }

        # Output the control information
        print(f"Type: {control_data['type']}")
        print(f"Description: {control_data['description']}")
        print(f"Info: {control_data['info']}")
        print(f"Solution: {control_data['solution']}")
        print(f"Reference: {control_data['reference']}")
        print(f"See Also: {control_data['see_also']}")
        print(f"Value Type: {control_data['value_type']}")
        print(f"Value Data: {control_data['value_data']}")
        print(f"Password Policy: {control_data['password_policy']}")
        print("=" * 50)

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description="Analyze .audit files in XML format and output the contained information."
    )
    parser.add_argument(
        '-a', '--audit',
        nargs='+',
        required=True,
        help='Path to one or more .audit files to be analyzed.'
    )

    args = parser.parse_args()

    audit_files = args.audit
    
    # Iterate over each audit file
    for audit_file in audit_files:
        parse_audit(audit_file)

if __name__ == "__main__":
    main()
