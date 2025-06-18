{pkgs}: {
  deps = [
    pkgs.python310
    pkgs.python310Packages.pip
    pkgs.python310Packages.virtualenv
    pkgs.python310Packages.flask
    pkgs.python310Packages.flask-sqlalchemy
    pkgs.python310Packages.flask-login
    pkgs.python310Packages.gunicorn
  ];
}
