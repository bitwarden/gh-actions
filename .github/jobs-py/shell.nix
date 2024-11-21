with import <nixpkgs> {};
let
  pythonEnv = python311.withPackages(ps: [
  ]);
in mkShell {
  packages = [
    pythonEnv

    pipenv
  ];
}
