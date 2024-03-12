import os
import json
import plistlib
import re
import lxml.etree as ET
import yaml


def get_file_type(file_path):
    file_type = os.path.splitext(file_path)[1]
    return file_type


def get_file_name(file_path):
    file_name = os.path.basename(file_path)
    return file_name


def update_json(version, file_path):
    with open(file_path) as json_file:
        data = json.load(json_file)
        data["version"] = version
        try:
            data["packages"][""]["version"] = version
        except KeyError:
            pass
        json.dump(data, open(file_path, "w"), indent=2)
    with open(file_path, "a") as f:
        f.write("\n")  # Make sure we add the new line back in at EOF.


def update_plist(version, file_path):
    with open(file_path, "rb") as plist:

        pl = plistlib.load(plist)
        pl["CFBundleShortVersionString"] = version

        data = pl
    with open(file_path, "wb") as update_plist:
        plistlib.dump(data, update_plist, sort_keys=False)


def update_xml(version, file_path):
    mytree = ET.parse(file_path)
    myroot = mytree.getroot()

    # Android Manifests
    if myroot.tag == "manifest":
        with open(file_path, "r") as f:
            data = f.read()
            data_new = re.sub(
                'android:versionName="[0-9]+\.[0-9]+\.[0-9]+"',
                f'android:versionName="{version}"',
                data,
                flags=re.M,
            )
        with open(file_path, "w") as f:
            f.write(data_new)

    # Microsoft .NET project files
    elif myroot.attrib.has_key("Sdk") and "Microsoft.NET.Sdk" in myroot.attrib["Sdk"]:
        version_property = [x for x in myroot[0] if x.tag == "Version"][-1]
        version_property.text = version
        mytree.write(file_path)
    # MSBuild Props
    else:
        version_property = [x for x in myroot[0] if x.tag == "Version"][-1]
        version_property.text = version
        mytree.write(file_path, encoding="utf-8")


# For updating Helm Charts - Chart.yaml version
def update_yaml(version, file_path):
    with open(file_path, "r") as f:
        doc = yaml.load(f, Loader=yaml.FullLoader)

    doc["version"] = version

    with open(file_path, "w") as f:
        yaml.dump(doc, f)


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
        update_xml(version, file_path)
    elif file_type == ".json":
        update_json(version, file_path)
    elif file_type == ".plist":
        update_plist(version, file_path)
    elif file_name == "Chart.yaml" or file_name == "Chart.yml":
        update_yaml(version, file_path)
    else:
        raise Exception("No file was recognized as a supported format.")

    if "GITHUB_OUTPUT" in os.environ:
        with open(os.environ["GITHUB_OUTPUT"], "a") as f:
            print("{0}={1}".format("status", f"Updated {file_path}"), file=f)

