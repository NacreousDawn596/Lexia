{ pkgs ? import <nixpkgs> {} }:

let
  token = builtins.toString ./token.txt;
  python = pkgs.python312Full;

in pkgs.mkShell {
  buildInputs = [
    pkgs.python312Full
    pkgs.git 
    pkgs.curl
  ];

  shellHook = ''
    export TOKEN=$(cat ${token})
    if [ ! -d "bin" ]; then
      ${python}/bin/python3 -m venv ./
    fi
    source ./bin/activate
    pip install -r requirements.txt
  '';
}

