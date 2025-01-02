{
  description = "advent of code 2023 devshell";

  inputs = {
    flake-utils.url = "github:numtide/flake-utils";
    haskellNix.url = "github:input-output-hk/haskell.nix";
    nixpkgs = {
      # url = "github:NixOS/nixpkgs";
      follows = "haskellNix/nixpkgs-unstable";
    };
  };
  outputs = { self, nixpkgs, flake-utils, haskellNix }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        overlays = [ haskellNix.overlay (final: prev: {
          project = final.haskell-nix.project' {
            src = ./.;
            compiler-nix-name = "ghc983";
            shell.tools = {
              cabal = {};
              haskell-language-server = {};
            };
            shell.buildInputs = with pkgs; [
              pyright
            ];
          };
        })];
        pkgs = import nixpkgs { inherit system overlays; inherit (haskellNix) config; };
        flake = pkgs.project.flake {};
      in flake
    );
}
