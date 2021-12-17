import os
import json
import plistlib
import lxml.etree as ET


def get_file_type(file):
    file_type = os.path.splitext(file)[1]
    return file_type


def update_json(version, file):
    with open(file) as json_file:
        data = json.load(json_file)
        data["version"] = version
        try:
            data["packages"][""]["version"] = version
        except KeyError:
            pass
        json.dump(data, open(file, "w"), indent=2)


def update_plist(version, file):
    with open(file, "rb") as plist:

        pl = plistlib.load(plist)
        pl["CFBundleShortVersionString"] = version

        data = pl
    with open(file, "wb") as update_plist:
        plistlib.dump(data, update_plist, sort_keys=False)


def update_xml(version, file):
    mytree = ET.parse(file)
    myroot = mytree.getroot()

    # Android Manifests
    if myroot.tag == "manifest":
        myroot.attrib[
            "{http://schemas.android.com/apk/res/android}versionName"
        ] = version
        ET.register_namespace("android", "http://schemas.android.com/apk/res/android")
        ET.register_namespace("tools", "http://schemas.android.com/tools")
        mytree.write(file, encoding="utf-8", xml_declaration=True, pretty_print=True)
    # Microsoft .NET project files
    elif "Microsoft.NET.Sdk.Web" in myroot.attrib["Sdk"]:
        version_property = [x for x in myroot[0] if x.tag == "Version"][-1]
        version_property.text = version
        mytree.write(file)
    # MSBuild Props
    else:
        myroot[0][1].text = version
        mytree.write(file, encoding="utf-8")


if __name__ == "__main__":
    version = os.getenv("INPUT_VERSION")
    file_path = os.getenv("INPUT_FILE_PATH")

    # Throw an exception if there is no file path defined.
    try:
        os.path.isfile(file_path)
    except TypeError:
        raise Exception(f"File path for {file_path} not found.")

    file_type = get_file_type(file_path)

    # Handle the file based on the extension.
    if file_type in {".xml", ".props", ".csproj"}:
        update_xml(version, file_path)
    elif file_type == ".json":
        update_json(version, file_path)
    elif file_type == ".plist":
        update_plist(version, file_path)
    else:
        raise Exception("No file was recognized as a supported format.")

    print(f"::set-output name=status::Updated {file_path}")
