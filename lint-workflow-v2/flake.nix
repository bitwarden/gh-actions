{
  description = "GitHub Action Linter";
  inputs = { nixpkgs.url = "github:nixos/nixpkgs/nixpkgs-unstable"; };

  outputs = { self, nixpkgs, flake-utils}:
    flake-utils.lib.eachDefaultSystem (system:
      let
        #pkgs = nixpkgs.legacyPackages.x86_64-linux.pkgs;
        pkgs = nixpkgs.legacyPackages.${system};
        packageName = "workflow-linter";
      in {
        devShells.default = pkgs.mkShell {
          name = "${packageName}";
          buildInputs = [
            pkgs.pipenv
            pkgs.python311
          ];
          shellHook = ''
            echo "Welcome in $name"
            export PS1="\[\e[1;33m\][nix(workflow-linter)]\$\[\e[0m\] "
          '';
        };
      }
    );
}
