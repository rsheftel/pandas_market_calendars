{
  inputs = {

    nixpkgs.url = "github:NixOS/nixpkgs/nixos-25.05";

  };
  outputs =
    {
      self,
      nixpkgs,
    }:
    let
      lib = nixpkgs.lib;
      systems = [
        "x86_64-linux"
        "aarch64-darwin"
      ];
    in
    {
      config = import ./nix/config;

      devShells = lib.genAttrs systems (
        system:
        let
          pkgs = import nixpkgs { inherit system; };
        in
        {
          default = pkgs.mkShell {
            packages = [
              (pkgs.python312.withPackages (ps: [
                ps.pandas
                ps.exchange-calendars
              ]))

            ];
            shellHook = ''
                echo "Running shellHook for prod"
                export PYTHONPATH=$PWD
                export PYTHONBREAKPOINT=ipdb.set_trace

                source ~/.profile 2>/dev/null || echo "No profile"
              '';
          };
        }
      );

    };
}
