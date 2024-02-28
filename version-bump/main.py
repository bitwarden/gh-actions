from datetime import date
import json
import lxml.etree as ET
import os
import plistlib
import re
import yaml


def get_next_version(version):
    version_split = version.split('.')
    year = int(version_split[0])
    month = int(version_split[1])
    patch = int(version_split[2])
    current_date = date(date.today().year, date.today().month, 1)
    patch = 0 if year != current_date.year or month != current_date.month else patch + 1
    return f"{current_date.year}.{current_date.month}.{patch}"


def get_file_type(file_path):
    file_type = os.path.splitext(file_path)[1]
    return file_type


def get_file_name(file_path):
    file_name = os.path.basename(file_path)
    return file_name


def update_json(file_path, version=None):
    with open(file_path) as json_file:
        data = json.load(json_file)
        data["version"] = version if version is not None else get_next_version(data["version"])
        try:
            data["packages"][""]["version"] = version if version is not None else get_next_version(data["packages"][""]["version"])
        except KeyError:
            pass
        json.dump(data, open(file_path, "w"), indent=2)
    with open(file_path, "a") as f:
        f.write("\n")  # Make sure we add the new line back in at EOF.

    return data["version"]


def update_plist(file_path, version=None):
    with open(file_path, "rb") as plist:

        pl = plistlib.load(plist)
        pl["CFBundleShortVersionString"] = version if version is not None else get_next_version(pl["CFBundleShortVersionString"])

        data = pl
    with open(file_path, "wb") as update_plist:
        plistlib.dump(data, update_plist, sort_keys=False)

    return pl["CFBundleShortVersionString"]


def update_xml(file_path, version=None):
    mytree = ET.parse(file_path)
    myroot = mytree.getroot()

    # Android Manifests
    if myroot.tag == "manifest":
        new_version = version if version is not None else get_next_version(myroot.attrib.get('{http://schemas.android.com/apk/res/android}versionName'))
        with open(file_path, "r") as f:
            data = f.read()
            data_new = re.sub(
                'android:versionName="[0-9]+\.[0-9]+\.[0-9]+"',
                f'android:versionName="{new_version}"',
                data,
                flags=re.M,
            )
        with open(file_path, "w") as f:
            f.write(data_new)

        return new_version

    # Microsoft .NET project files
    elif myroot.attrib.has_key("Sdk") and "Microsoft.NET.Sdk" in myroot.attrib["Sdk"]:
        version_property = [x for x in myroot[0] if x.tag == "Version"][-1]
        version_property.text = version if version is not None else get_next_version(version_property.text)
        mytree.write(file_path)

        return version_property.text
    # MSBuild Props
    else:
        version_property = [x for x in myroot[0] if x.tag == "Version"][-1]
        version_property.text = version if version is not None else get_next_version(version_property.text)
        mytree.write(file_path, encoding="utf-8")

        return version_property.text


# For updating Helm Charts - Chart.yaml version
def update_yaml(file_path, version=None):
    with open(file_path, "r") as f:
        doc = yaml.load(f, Loader=yaml.FullLoader)

    doc["version"] = version if version is not None else get_next_version(doc["version"])

    with open(file_path, "w") as f:
        yaml.dump(doc, f)

    return doc["version"]


if __name__ == "__main__":
    version = os.getenv("INPUT_VERSION")
    file_path = os.getenv("INPUT_FILE_PATH")

    # Throw an exception if there is no file path defined.
    try:
        os.path.isfile(file_path)
    except TypeError:
        raise Exception(f"File path for {file_path} not found.")

    file_name = get_file_name(file_path)
    file_type = get_file_type(file_path)

    # Handle the file based on the extension.
    if file_type in {".xml", ".props", ".csproj"}:
        new_version = update_xml(file_path, version)
    elif file_type == ".json":
        new_version = update_json(file_path, version)
    elif file_type == ".plist":
        new_version = update_plist(file_path, version)
    elif file_name == "Chart.yaml" or file_name == "Chart.yml":
        new_version = update_yaml(file_path, version)
    else:
        raise Exception("No file was recognized as a supported format.")

    if "GITHUB_OUTPUT" in os.environ:
        with open(os.environ["GITHUB_OUTPUT"], "a") as f:
            print("{0}={1}".format("status", f"Updated {file_path}"), file=f)
            print("{0}={1}".format("version", f"New Version: {new_version}"), file=f)

